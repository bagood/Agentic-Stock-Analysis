"""Model-free sandbox checks shared by batch and individual detailed analysis."""
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from app.errors import CodexExecutionError
from llm_runner.process import capture, check_project_configuration, diagnostic, positive_timeout

REFERENCES = ("instructions/README.md", "instructions/features/README.md", "instructions/features/INDEX.md")


@dataclass(frozen=True)
class PreflightResult:
    project: Path
    instructions: Path
    generation_timeout: float


def preflight(project: Path, instructions: Path, *, executable="codex") -> PreflightResult:
    project, instructions = project.resolve(), instructions.resolve()
    check_project_configuration(project)
    generation_timeout = positive_timeout(os.environ.get("CODEX_GENERATION_TIMEOUT_SECONDS", "900"))
    timeout = positive_timeout(os.environ.get("CODEX_PREFLIGHT_TIMEOUT_SECONDS", "20"))
    if shutil.which(executable) is None:
        raise CodexExecutionError("Preflight executable check failed: Codex is not on PATH")
    paths = [instructions, *(project / reference for reference in REFERENCES)]
    try:
        for path in paths:
            if not path.read_text(encoding="utf-8").strip():
                raise ValueError("empty reference")
    except (OSError, UnicodeError, ValueError) as exc:
        raise CodexExecutionError("Preflight reference check failed: selected instructions/feature guides must be readable and nonempty") from exc
    # Diagnostic command has no ignore-user-config flag in 0.146.0. A fresh
    # unauthenticated home excludes personal settings and needs no model call.
    with tempfile.TemporaryDirectory(prefix="analysis-sandbox-") as home:
        env = dict(os.environ, CODEX_HOME=home)
        command = [executable, "sandbox", "-c", 'sandbox_mode="read-only"',
                   "--disable", "plugins", "--", "/bin/sh", "-c",
                   'for file do test -s "$file" && cat "$file" >/dev/null || exit 1; done',
                   "reference-smoke", *(str(path) for path in paths)]
        try:
            code, _, stderr = capture(command, cwd=project, timeout=timeout, env=env)
        except CodexExecutionError as exc:
            raise CodexExecutionError(f"Preflight sandbox check failed: {exc}") from exc
    if code:
        raise CodexExecutionError(f"Preflight sandbox check failed (exit {code}): {diagnostic(stderr)}. Run python -m detailedAnalysis.sandbox_diagnostics inside the analysis service to inspect runtime policy and model-free sandbox errors. Reports were not cleared.")
    return PreflightResult(project, instructions, generation_timeout)


def check_feature_cards(project: Path, indicators: dict) -> None:
    try:
        catalog = json.loads((project / "instructions/technical_feature_catalog_v1.json").read_text())["features"]
        index = (project / REFERENCES[2]).read_text()
        cards = dict(re.findall(r"^- \[([^\]]+)\]\(([^)]+\.md)\)$", index, re.MULTILINE))
        root = (project / "instructions/features").resolve()
        for name in indicators.keys() & catalog.keys():
            if name not in cards:
                raise ValueError("matching index entry missing")
            card = (root / cards[name]).resolve()
            if card.parent != root or f"# {name}\n" not in card.read_text(encoding="utf-8"):
                raise ValueError("matching feature card missing or invalid")
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        raise CodexExecutionError("Feature-reference check failed: a supplied catalogued feature has no readable matching card") from exc


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forecast-window", choices=("5", "10"), default="10")
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    try:
        preflight(project, project / f"instructions/stock-upside-analysis-{args.forecast_window}-instructions.md")
    except (CodexExecutionError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("Codex read-only sandbox reference check passed")
