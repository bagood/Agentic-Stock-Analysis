from pathlib import Path

from detailedAnalysis.helper import normalize_ticker


def list_analysis_reports(analysis_dir: Path) -> list[Path]:
    """Return valid ticker report paths in deterministic ticker order."""
    if not analysis_dir.is_dir():
        raise ValueError(f"Analysis directory does not exist: {analysis_dir}")

    reports: list[Path] = []
    for report_path in analysis_dir.glob("*.md"):
        normalize_ticker(report_path.stem)
        reports.append(report_path)
    return sorted(reports, key=lambda path: path.stem.upper())


def build_entry_strategy_prompt(
    instructions: str,
    analysis_report: str,
    ticker: str,
    trading_window: str,
) -> str:
    """Assemble the entry-strategy instruction and source report for Codex."""
    normalized_ticker = normalize_ticker(ticker)
    request = (
        f"Generate entry strategies for IDX-listed {normalized_ticker} "
        f"for the next {trading_window}. Use IDR and the risk tolerance stated "
        "in the analysis (or Moderate when absent). Follow every instruction "
        "above and use only the supplied analysis report."
    )
    return (
        f"{instructions.rstrip()}\n\n"
        f"{request}\n\n"
        "<ANALYSIS_REPORT>\n"
        f"{analysis_report.rstrip()}\n"
        "</ANALYSIS_REPORT>\n"
    )

