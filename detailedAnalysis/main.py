import os
import sys
import json
import subprocess
from pathlib import Path

from detailedAnalysis.helper import (
    build_prompt,
    build_technical_url,
    fetch_json,
    load_env,
    normalize_ticker,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_DIR / ".env"


def main(ticker: str, timeout: float = 30.0) -> int:
    try:
        load_env(ENV_PATH)
        instructions_value = os.environ["INSTRUCTIONS_PATH"]
        output_dir_value = os.environ["OUTPUT_DIR"]

        ticker = normalize_ticker(ticker)
        instructions_path = Path(instructions_value)
        if not instructions_path.is_absolute():
            instructions_path = PROJECT_DIR / instructions_path

        output_dir = Path(output_dir_value)
        if not output_dir.is_absolute():
            output_dir = PROJECT_DIR / output_dir

        output_path = output_dir / f"{ticker}.md"

        technical_url = build_technical_url(ticker)
        technical_data = fetch_json(technical_url, timeout)
        technical_data_text = json.dumps(
            technical_data,
            ensure_ascii=False,
            indent=2,
        )

        instructions = instructions_path.read_text(encoding="utf-8")
        prompt = build_prompt(instructions, technical_data_text, ticker)

        subprocess.run(
            [
                "codex",
                "--search",
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
    except (
        KeyError,
        OSError,
        RuntimeError,
        ValueError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Analysis saved to {output_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {Path(__file__).name} TICKER", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
