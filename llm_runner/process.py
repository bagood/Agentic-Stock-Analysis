"""Bounded process capture; diagnostics never expose arbitrary model/tool text."""
import math
import os
import re
import signal
import subprocess
import threading
from pathlib import Path

from app.errors import CodexExecutionError, CodexTimeoutError

LIMIT = 4 * 1024 * 1024
INFRASTRUCTURE = re.compile(
    r"bwrap:|No permissions to create a new namespace|"
    r"(?:creating|create|creating new) (?:a |new )?namespace[^\n]*(?:failed|denied|not permitted)|"
    r"sandbox-exec:|failed to (?:start|initialize|create) (?:the )?sandbox|"
    r"Sandbox\([^\n]*\)", re.IGNORECASE,
)


def positive_timeout(value: str | float) -> float:
    try:
        timeout = float(value)
    except (ValueError, TypeError) as exc:
        raise CodexExecutionError("Codex timeout must be a positive finite number") from exc
    if not math.isfinite(timeout) or timeout <= 0:
        raise CodexExecutionError("Codex timeout must be a positive finite number")
    return timeout


def diagnostic(text: str) -> str:
    # Allowlisted classifications only: stderr can contain credentials or payloads.
    if INFRASTRUCTURE.search(text):
        return "sandbox namespace/setup denied (bubblewrap/host runtime policy)"
    if "permission denied" in text.lower():
        return "permission denied"
    if "unauthorized" in text.lower() or "401" in text:
        return "authentication rejected"
    return "no safe diagnostic classification; inspect runtime configuration"


def capture(command, *, cwd, timeout, prompt=None, env=None):
    """Drain both pipes with bounded memory and kill/reap the process group on timeout."""
    buffers = [bytearray(), bytearray()]
    overflow = threading.Event()
    def drain(pipe, buffer):
        while True:
            chunk = pipe.read(8192)
            if not chunk:
                break
            available = LIMIT - len(buffer)
            buffer.extend(chunk[:available])
            if len(chunk) > available:
                overflow.set()
        pipe.close()
    try:
        process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
    except OSError as exc:
        raise CodexExecutionError("Unable to start Codex executable") from exc
    threads = [threading.Thread(target=drain, args=(pipe, buffer), daemon=True)
               for pipe, buffer in zip((process.stdout, process.stderr), buffers)]
    for thread in threads:
        thread.start()
    def feed():
        try:
            process.stdin.write((prompt or "").encode())
            process.stdin.close()
        except (BrokenPipeError, OSError):
            pass
    writer = threading.Thread(target=feed, daemon=True)
    writer.start()
    try:
        process.wait(timeout=positive_timeout(timeout))
    except BaseException as exc:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        for thread in threads:
            thread.join(timeout=2)
        if isinstance(exc, subprocess.TimeoutExpired):
            raise CodexTimeoutError("Codex execution exceeded its timeout") from exc
        raise
    for thread in threads:
        thread.join(timeout=2)
    if any(thread.is_alive() for thread in threads):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        raise CodexExecutionError("Codex left subprocess pipes open")
    if overflow.is_set():
        raise CodexExecutionError("Codex diagnostic output exceeded the capture limit")
    return process.returncode, *(bytes(buffer).decode("utf-8", errors="replace") for buffer in buffers)


def check_project_configuration(directory):
    # --ignore-user-config does not promise to ignore project config. Fail closed
    # rather than allow project MCP servers/hooks to initialize in batch generation.
    for root in (directory.resolve(), *directory.resolve().parents):
        # The personal home config is precisely what --ignore-user-config skips.
        if root == Path.home():
            break
        if (root / ".codex" / "config.toml").exists():
            raise CodexExecutionError("Project .codex/config.toml is unsupported for isolated report generation; move its settings out of the analysis project")
        if (root / ".git").exists():
            break
