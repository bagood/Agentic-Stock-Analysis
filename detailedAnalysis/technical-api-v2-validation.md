# Technical API v2 implementation validation

Recorded 2026-10-10 (Asia/Jakarta). This is evidence for the consumer implementation,
not certification of a deployed backend or a live stock forecast.

## Current revision: feature documentation instead of generated context

At the user's request, the prompt now contains the strategy instructions, stock
request, and validated compact service JSON. Feature definitions and guidance are
read from `instructions/features/` through the strategy file's reference workflow.
The catalog loader, definition/assessment serializers, catalog-generation script,
context-evaluation script, and their obsolete catalog tests were removed.
The response contract still requires catalog version 1.0. HTTP/identity/date/value
validation and configured calendar-age rejection remain in the retrieval path.
Unknown definitions are handled through the documented interpretation-limitations
policy rather than a runtime catalog lookup. The root catalog is retained only
as a reference artifact linked by the documentation.

All 121 current repository tests pass locally under Python 3.10.20. Regression
checks confirm the prompt uses the local feature-reference workflow and adds no
generated context blocks. The result is recorded in the machine-readable report.
The container and real-agent results below describe the earlier implementation;
they were not rerun for this revision.

## Original implementation checks (before context removal)

- All 124 repository tests pass under Python 3.10.20 with dependencies installed
  from `requirements.txt` in a temporary environment.
- All 124 tests also pass under Linux Python 3.10.22 in a clean validation directory
  packaged into a temporary image based on the existing analysis image. No host
  mounts or network access were available during the container tests. This checks
  the new source and catalog packaging; it is not a production image deployment.
- The existing container entrypoint preserves `TECHNICAL_API_TIMEOUT_SECONDS=12`
  and `TECHNICAL_MAX_DATA_AGE_CALENDAR_DAYS=7` for consumer configuration.
- Catalog regeneration check passes. All 210 reference cards match the packaged
  interpretation fields; all 180/193 fixture feature names resolve.
- The full 5dd fixture preserves the JSON supplied in development-plan Appendix A.
  The local backend response exactly equals that fixture at the fixed cutoff. Its
  matching 10dd response contains 193 features and includes all 5dd feature names.
  [Snapshot provenance](../tests/fixtures/technical_snapshot_provenance.json)
  records source CSV, metadata, and contract checksums.
- Actual FastAPI backend technical routes were exercised for both horizons through
  TestClient transport into the real consumer adapter. HTTP input handling,
  typed validation, catalog resolution, and consumer assessment succeeded. This
  is in-process route integration, not a request to a deployed network service.
- `git diff --check` and relevant Markdown-link checks pass. A pre-existing README
  link to `docs/trading-session-migration.md` remains outside this migration.

## Agent interpretation

Before removal, `scripts/evaluate_technical_agent.py`
provided a synthetic evaluation. It covered reversals, zero versus
null, omitted selected features, decimal-ratio/RSI-point/PVO-percent units, already
applied lag, absent OHLCV, cutoff, horizon, and unverified freshness.

The host-configured `gpt-6.1-sol` was rejected by its current ChatGPT authentication.
A temporary executable wrapper retried with `--ignore-user-config --ephemeral`;
Codex CLI 0.146.0 selected `gpt-5.6-sol`. Host configuration was not changed.
Both horizons passed all 13 checks: 5dd took 8.99 seconds and 10dd took 6.26 seconds
in this run. No news research or actual financial forecast was requested. These
results do not measure full report quality, model-version parity, or token savings.
Normal report generation still needs a supported host CLI model configuration.

## Backend audit and release limits

The read-only backend suite ran with pytest caching and bytecode writing disabled:
111 tests passed; `test_catalog_definitions_resolve_to_generating_functions` failed
because the original backend `documentations/technical_feature_catalog_v1.json`
is absent. Consumer definitions are derived from the checked-in catalog-1.0 cards
and explicitly record that provenance. They do not replace the backend's missing
storage/generating-function catalog. No sibling backend files were modified.

The local `APP_ENV=prod` artifact audit at Jakarta cutoff 2026-10-10 scanned
105 CSV tickers and both horizons: 181 of 210 requests are ready, with calendar
age one day; 29 return `feature_filter_unavailable`. Missing coverage is:

| Ticker | Unavailable horizons |
| --- | --- |
| BAIK | 5dd, 10dd |
| CBRE | 5dd, 10dd |
| CUAN | 5dd, 10dd |
| HATM | 10dd |
| INET | 5dd, 10dd |
| MBMA | 5dd, 10dd |
| MSJA | 5dd, 10dd |
| NCKL | 5dd, 10dd |
| NSSS | 5dd, 10dd |
| OMED | 5dd, 10dd |
| PACK | 5dd, 10dd |
| PGEO | 5dd, 10dd |
| RSCH | 5dd, 10dd |
| SMIL | 5dd, 10dd |
| VKTR | 5dd, 10dd |

Repair the required metadata using the normal artifact publisher; do not invent
selected-feature lists in the consumer. Restore the original backend catalog,
resolve host CLI configuration, accept the product's freshness policy, audit the
actual served deployment scope at its current Jakarta date, verify live staging
requests, and review complete generated reports/news handling before rollout.
No production deployment, backend training, or global Codex configuration change
was performed. Retain compatible backend/consumer releases for joint rollback.

[Machine-readable results](technical-api-v2-validation.json) contain the counts,
metadata failures, and synthetic evaluation timings.
