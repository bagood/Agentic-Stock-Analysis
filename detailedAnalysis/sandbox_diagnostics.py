"""Model-free Linux sandbox diagnostics; no API requests or report cleanup."""
import json
import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

def read_runtime_file(path):
    try:
        return Path(path).read_text().strip()
    except OSError as exc:
        return f"unavailable ({exc.strerror})"


def probe(command, env):
    if shutil.which(command[0]) is None:
        return {"command": command, "error": "executable not found"}
    try:
        result = subprocess.run(command, cwd=Path.cwd(), timeout=10, env=env,
                                stdin=subprocess.DEVNULL, capture_output=True)
        return {"command": command, "exit_code": result.returncode,
                "stdout": result.stdout[:8192].decode("utf-8", errors="replace"),
                "stderr": result.stderr[:8192].decode("utf-8", errors="replace")}
    except subprocess.TimeoutExpired:
        return {"command": command, "error": "probe timed out after 10 seconds"}
    except OSError as exc:
        return {"command": command, "error": exc.strerror}


def collect_diagnostics():
    status = read_runtime_file("/proc/self/status")
    report = {
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "apparmor_profile": read_runtime_file("/proc/self/attr/current"),
        "process_policy": [line for line in status.splitlines()
                           if line.startswith(("CapEff:", "NoNewPrivs:", "Seccomp:", "Seccomp_filters:"))],
        "sysctls": {name: read_runtime_file("/proc/sys/" + name.replace(".", "/"))
                    for name in ("user.max_user_namespaces", "kernel.unprivileged_userns_clone",
                                 "kernel.apparmor_restrict_unprivileged_userns")},
    }
    # No model is invoked. Exclude authentication variables and personal Codex
    # configuration from these static smoke commands; never print environment.
    env = {key: value for key, value in os.environ.items()
           if key not in ("OPENAI_API_KEY", "CODEX_API_KEY", "OPENAI_AUTH_TOKEN")}
    with tempfile.TemporaryDirectory(prefix="analysis-diagnostic-") as home:
        env["CODEX_HOME"] = home
        report["probes"] = [probe(command, env) for command in (
            ["codex", "--version"],
            ["bwrap", "--version"],
            ["unshare", "--user", "--map-root-user", "/bin/true"],
            ["bwrap", "--unshare-user", "--unshare-pid", "--ro-bind", "/", "/",
             "--proc", "/proc", "--dev", "/dev", "/bin/true"],
            ["codex", "sandbox", "-c", 'sandbox_mode="read-only"',
             "--disable", "plugins", "--", "/bin/true"],
        )]
    return report


def main():
    report = collect_diagnostics()
    print(json.dumps(report, indent=2))
    return 0 if report["probes"][-1].get("exit_code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
