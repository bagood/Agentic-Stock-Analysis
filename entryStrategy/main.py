import subprocess
import sys
from pathlib import Path

from detailedAnalysis.helper import normalize_ticker
from entryStrategy.helper import build_entry_strategy_prompt

PROJECT_DIR = Path(__file__).resolve().parent.parent


def main(
    ticker: str,
    analysis_path_value: str,
    instructions_value: str,
    trading_window: str,
    output_dir_value: str,
) -> int:
    """Generate one entry-strategy report from one stock-analysis report."""
    try:
        ticker = normalize_ticker(ticker)

        analysis_path = Path(analysis_path_value)
        if not analysis_path.is_absolute():
            analysis_path = PROJECT_DIR / analysis_path
        if not analysis_path.is_file():
            raise ValueError(f"Analysis report does not exist: {analysis_path}")

        instructions_path = Path(instructions_value)
        if not instructions_path.is_absolute():
            instructions_path = PROJECT_DIR / instructions_path
        if not instructions_path.is_file():
            raise ValueError(f"Instructions file does not exist: {instructions_path}")

        output_dir = Path(output_dir_value)
        if not output_dir.is_absolute():
            output_dir = PROJECT_DIR / output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{ticker}.md"

        prompt = build_entry_strategy_prompt(
            instructions_path.read_text(encoding="utf-8"),
            analysis_path.read_text(encoding="utf-8"),
            ticker,
            trading_window,
        )

        subprocess.run(
            [
                "codex",
                "exec",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "-o",
                str(output_path),
                "-",
            ],
            input=prompt,
            text=True,
            cwd=PROJECT_DIR,
            check=True,
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Entry strategy saved to {output_path}")
    return 0


if __name__ == "__main__":
    print(
        "Run individual entry strategies through run_entry_strategy.py so the "
        "trading window is selected consistently.",
        file=sys.stderr,
    )
    raise SystemExit(2)

