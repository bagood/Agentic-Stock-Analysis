# Development plan: detailed analysis with technical API v2

Prepared on 2026-10-10 (Asia/Jakarta). Implements the consumer work described in
[the integration plan](../technical_api_v2_integration_plan.md) for
[run_detailed_analysis.py](../run_detailed_analysis.py) and its analysis pipeline.
The original plan is retained below. Consumer implementation and local validation
are complete; production release checks remain as recorded in the status section.

User-requested revision on 2026-10-10: remove generated trusted context and use
`instructions/features/` directly. This supersedes the original plan's runtime
catalog loading, definition injection, and consumer-assessment prompt blocks.
`feature_catalog.py`, `build_feature_catalog.py`, and `evaluate_technical_agent.py`
were removed together with their supporting serializers and catalog tests.
The root catalog remains a documentation reference artifact.

## Implementation status (2026-10-10)

| Milestone | Status and evidence |
| --- | --- |
| Contract and HTTP adapter | Implemented strict required-field/numeric/alignment/provenance validation, identity checks, structured errors, finite timeouts, no retries/cache, and diagnostics. |
| Runner migration | Both CLI windows pass an explicit technical horizon. Configuration is loaded once, failed tickers do not stop subsequent analyses, and failures return a nonzero batch status. |
| Definitions | The agent reads the feature guide, exact-name index, and matching cards in `instructions/features/`. Runtime catalog loading and generated definition context have been removed at the user's request. Unsupported catalog versions are rejected by the response contract; unknown feature definitions follow the instruction file's interpretation-limitations policy. |
| Regression snapshots | Appendix A was extracted unchanged into the 5dd fixture. The local backend exactly reproduced it; the matching 10dd fixture has 193 indicators and includes all 180 5dd names. Artifact hashes are recorded in `tests/fixtures/technical_snapshot_provenance.json`. |
| Prompts and instructions | Prompt contains selected strategy instructions, stock request, and compact validated envelope once. No generated trusted-context or consumer-assessment blocks are added. Both instruction files retain their freshness, units, nulls, lag, and trajectory rules and require reading the feature documentation. |
| Consumer verification | All 121 current tests pass locally under Python 3.10 after context removal. The earlier 124-test local/container run covered the previous implementation. Container entrypoint preservation of both new environment settings was checked during that earlier run. |
| Local backend integration | Actual FastAPI technical routes feed both horizons through the consumer adapter using TestClient transport. Backend suite: 111 pass; one fails because the original backend catalog is absent. |
| Artifact coverage audit | Fixed Jakarta cutoff 2026-10-10: 105 local production CSV tickers, 210 horizon requests, 181 ready and 29 unavailable due to missing model metadata. This is a local snapshot audit, not deployment readiness. |
| Real-agent evaluation | The earlier context-injection implementation passed 13 synthetic interpretation checks per horizon through Codex CLI defaults. That script has now been removed; these results are historical and do not verify the current documentation-reading prompt. Host settings were not changed. |
| Release | Not deployed. Restore required backend metadata/catalog, resolve the host CLI model setting, and perform deployment-specific freshness-policy acceptance, live staging checks, and full report/news review before production rollout. |

See [validation evidence and release limits](technical-api-v2-validation.md) and
the implemented [consumer contract](../technical_api.md). The inventory and
milestones below describe the pre-implementation starting point and intended work.

## Outcome and scope

Running either forecast window must request the matching technical horizon,
validate the complete v2 envelope before starting Codex, resolve the supplied
feature definitions, and preserve dates, values, missingness, and provenance in
the generated analysis. Retrieval success must not imply exchange-calendar
freshness. A failed retrieval or invalid contract must never produce a successful
technical forecast.

Keep the current CLI (`--forecast-window 5|10`, default `10`), recommendation
allocation, organizer stocks, ticker ordering, and per-window report directories.
The technical history is three observations for both forecast horizons.
Availability checks, response caching, backend selection logic, raw OHLCV
retrieval, feature ranking, and model inference are outside the initial release.

## Supplied service response format

The user supplied the complete AALI/5dd service response in `Pasted text.txt`.
[Appendix A](#appendix-a-complete-supplied-aali5dd-service-response) preserves that
JSON verbatim as the concrete response example and source for the planned
regression fixture. It corresponds to:

```text
GET /technical/?ticker=AALI&forecast_type=5dd
```

| Response block | Supplied values and consumer interpretation |
| --- | --- |
| Contract and identity | `schema_version="2.0"`, `ticker="AALI"`, `forecast_type="5dd"`, `market_timezone="Asia/Jakarta"`. |
| Selection and history | `selection_policy="latest_available_before_request_date"`, `requested_sessions=3`, `returned_sessions=3`, `order="oldest_to_newest"`. |
| Dates and cutoff | `dates=["2026-10-07","2026-10-08","2026-10-09"]`; `data_as_of="2026-10-09"`. Every indicator's three positions map to these dates in the same order. |
| Quality | Request date `2026-10-10`, calendar age 1, null counts `[55,55,55]`, freshness `unverified_without_exchange_calendar`. A successful response does not establish current exchange-session coverage. |
| Feature provenance | Model-metadata `selected_features` union, model version 1, ordered `medianLoss/5dd` and `medianGain/5dd` sources. |
| Feature counts | 195 selected, 180 included, 15 selected but unavailable, 30 excluded as not selected. These counts describe this snapshot, not fixed production requirements. |
| Catalog and observations | Catalog version `1.0`; 180 exact-name indicator arrays containing numbers or nulls. Raw OHLCV is absent in this response. |

For example, `RSI Value` is
`[63.089648287735,58.00471606659483,62.630461501448025]`: it falls and then rises.
`ATR Bearish` is `[0,0,0]`, while `Foreign Net Intensity 1D` is
`[null,null,null]`. Preserve these different states and their date alignment.
Do not replace the unavailable series with zeros or call the RSI movement
steadily increasing.

The pasted JSON was checked for parseability, three-value series, finite numeric
observations, date ordering, as-of/age consistency, included/selected count
consistency, and actual per-session null counts. Full typed-contract validation,
catalog-name resolution, and live-service parity remain implementation checks.
No matched 10dd response was supplied.

## Pre-implementation inventory and gaps

| Location | Observed behavior | Required development |
| --- | --- | --- |
| `run_detailed_analysis.py::FORECAST_CONFIGS` | Already maps `5`/`10` to `5dd`/`10dd`, instructions, and prompt horizon. | Use the existing `rolling_window` as the technical `forecast_type`; avoid a second independently maintained mapping. |
| `run_detailed_analysis.py::main` | Passes the human-readable horizon but not the API horizon to the per-ticker analysis. Continues after failed tickers and returns 1 if any fail. | Pass `forecast_type` explicitly; retain batch failure aggregation. |
| `detailedAnalysis/main.py::main` | Fetches JSON and pretty-prints it directly into the prompt before calling `run_codex`. | Use one typed adapter; require validation, catalog resolution, and freshness assessment first. |
| `detailedAnalysis/helper.py::build_technical_url` | Builds `/technical?ticker=...`, omitting required `forecast_type`. | Build the canonical `/technical/` route with both parameters. |
| `detailedAnalysis/helper.py::normalize_ticker` | Accepts arbitrary alphanumeric tickers and `.`/`-`; also used by entry and hold strategy code. | Add technical-specific four-ASCII-letter validation without tightening shared normalization for unrelated callers. |
| `detailedAnalysis/helper.py::fetch_json` | Collapses HTTP/network errors into `RuntimeError`; returns unchecked JSON. Also used for recommendation and stocks calls. | Keep those callers stable; use a dedicated technical client with structured failures. |
| Upside analysis instructions | Already cover envelopes, nulls, units, publication lag, and mixed trajectories. Their trusted contract also assumes H3 is the immediately preceding completed IDX session. | Remove that assumption for API v2 unless an independent calendar check establishes it. |
| `tests/test_run_detailed_analysis.py` | Tests orchestration with the per-ticker function mocked. | Extend horizon propagation and batch-failure coverage; add real per-ticker pipeline tests with HTTP and Codex mocked. |
| `tests/test_detailed_analysis_helper.py` | Expects a technical URL without a horizon. | Replace that expectation with both required parameters and the trailing slash. |
| `README.md` | Describes v2 validation as implemented and links this development document, `technical_api.md`, and a root catalog. | Reconcile documentation with actual implementation and package the missing reference files. |

At plan preparation, the consumer had no technical schema, root
`technical_feature_catalog_v1.json`, root `technical_api.md`, or complete AALI v2
JSON fixture file. The complete AALI response was embedded in Appendix A before
implementation. Markdown feature cards already existed under `instructions/features/`.
The sibling repository supplied these read-only development references:

- [Backend schema](../../ML-Stock-Analysis/app/schemas/technical.py).
- [Backend router](../../ML-Stock-Analysis/app/routers/technical.py).
- Catalog 1.0: `../ML-Stock-Analysis/documentations/technical_feature_catalog_v1.json`.
- Migration guide: `../ML-Stock-Analysis/documentations/technical_api.md`.

The catalog and migration guide were readable during inspection but were absent
at the final path check. Reacquire those reviewed artifacts before packaging;
their content must not be reconstructed from the illustrative payload or plan.

Those sibling files are development references, not deployment dependencies.
The consumer's own `app` package does not contain `app.schemas.technical`.

## Proposed design and file ownership

```text
selected FORECAST_CONFIGS entry
  -> per-ticker main(..., forecast_type=rolling_window)
  -> technical client: request -> HTTP handling -> v2 validation -> identity check
  -> catalog resolution -> separate consumer freshness assessment
  -> trusted guidance/definitions + one compact market-data envelope
  -> run_codex -> existing <window>/<TICKER>.md report
```

| File | Responsibility |
| --- | --- |
| `run_detailed_analysis.py` | Propagate the selected horizon; load client policy/configuration once; report batch outcomes. |
| `detailedAnalysis/main.py` | Coordinate validated retrieval and prompt construction; block Codex on failures. |
| `detailedAnalysis/technical_contract.py` (new) | Consumer-owned Pydantic v2 response/error types and cross-field validation. |
| `detailedAnalysis/technical_api.py` (new) | Synchronous HTTP adapter, request validation, identity checks, and typed errors. |
| `detailedAnalysis/feature_catalog.py` (new) | Load packaged catalog 1.0 and resolve exact emitted names. |
| `detailedAnalysis/helper.py` | Technical URL and prompt assembly; retain shared nontechnical helpers. |
| `technical_feature_catalog_v1.json` (new) | Versioned catalog copied from the reviewed backend source. |
| `technical_api.md` (new) | Consumer-facing contract reference, adapted from the backend migration guide. |
| Both `instructions/stock-upside-analysis-*-instructions.md` | Align API-path validation and freshness wording. |
| `.env.example`, `README.md`, `requirements.txt` | Configuration, accurate usage, and explicit contract dependency. |
| New contract/client/pipeline tests and `tests/fixtures/` | Regression evidence independent of live services and Codex execution. |

Use `httpx`, already declared in `requirements.txt`, for the dedicated technical
adapter with an injectable synchronous client. Declare Pydantic v2 explicitly
because this consumer will use it directly; choose a version compatible with the
existing dependency set and Python 3.10 Docker runtime. Keep the contract in
`detailedAnalysis` to avoid importing the unrelated server models.

Initially maintain equivalent consumer models, with the reviewed backend revision
recorded alongside the port. Require parity fixtures when the backend contract
changes. Do not add sibling paths to `sys.path` or copy backend service/repository
implementation into this client. Preserve supplied fields during serialization;
require advertised contract fields rather than silently synthesizing a missing
`schema_version` or other provenance through model defaults. Match the backend's
unknown-field rejection and strict numeric validation.

## Implementation milestones

### 1. Package the contract, catalog, and fixtures

1. Port the reviewed response and error contract into `technical_contract.py`.
   Require `schema_version="2.0"`, the requested identity, `Asia/Jakarta`,
   `latest_available_before_request_date`, and `oldest_to_newest`.
2. Validate exactly three requested/returned sessions and three valid ISO dates,
   strictly increasing and unique. Require `data_as_of == dates[-1]`; all dates
   must precede `quality.request_date`, and its difference from `data_as_of` must
   equal the positive integer `data_age_calendar_days`. Use the server date for
   this consistency check, not the test machine's current date.
3. Validate a nonempty exact-name indicator dictionary. Each series must contain
   three finite JSON numbers or nulls; reject booleans, numeric strings, NaN,
   infinities, invalid names, and inconsistent lengths. Retain integer values,
   zeros, all-null series, null positions, and numeric precision without rounding.
4. Validate `quality.null_counts_by_session` against the actual emitted series.
   Require the documented freshness status without upgrading its meaning.
5. Validate feature provenance: `model_metadata`, `selected_features`, `union`,
   model version 1, and ordered `{label_type, window}` sources. `5dd` uses
   `medianLoss/5dd`, then `medianGain/5dd`; `10dd` adds `medianLoss/10dd`, then
   `medianGain/10dd`. Require nonnegative integer counts,
   `included_count == len(indicators)`, and
   `selected_union_count == included_count + selected_unavailable_count`.
   CSV membership, excluded-count accuracy, and omitted names remain backend
   audit responsibilities because they cannot be reconstructed from the envelope.
6. Package catalog 1.0 at the project root. Validate its version/timezone and
   resolve every emitted name exactly. Include meaning, unit/scale, lookback, and
   publication lag in the trusted context; fail before interpretation if a
   definition or supported version is missing. Load definitions once per batch
   and reuse them; this is not a market-response cache.
7. Extract the complete supplied AALI/5dd response from Appendix A into
   `tests/fixtures/technical_aali_5dd_v2.json`, preserving its values, fixed server
   request date, and user-supplied provenance. The integration plan's prose and
   backend schema example are not substitutes for this response. Add a frozen
   10dd fixture from the same artifact snapshot and smaller synthetic fixtures
   for edge cases.

Exit: valid fixtures parse without mutation, malformed payloads fail, and all
emitted fixture names resolve in the packaged catalog. Do not hardcode the AALI
feature count into production validation.

### 2. Implement one technical HTTP adapter

1. Require `forecast_type` as `5dd|10dd`; validate the stripped input ticker as
   exactly four ASCII letters before uppercasing. Validation before normalization
   avoids accepting a Unicode character whose uppercase expansion looks ASCII.
2. Update `build_technical_url(base_url, ticker, forecast_type)` to retain the
   configured base path and produce `/technical/` with encoded parameters.
   Prevent pre-existing base-query values from creating duplicate/conflicting
   `ticker` or `forecast_type` inputs. Keep unrelated base-query parameters and
   the generic URL builder's existing behavior.
3. Use `ML_BASE_URL` and a positive finite HTTP timeout. Add an optional
   `TECHNICAL_API_TIMEOUT_SECONDS` setting, falling back to the runner's supplied
   timeout (currently 30 seconds); validate configuration before the batch.
4. Inspect status before success parsing. Distinguish input, transport, API,
   contract, catalog, and freshness failures. Keep HTTP status, structured reason
   code, ticker, and horizon available to the caller; avoid logging entire bodies
   or credentials embedded in configured URLs.
5. Validate the body and independently match its ticker/horizon to the request.
   Return the validated envelope plus a separate consumer assessment, without
   rewriting server quality or feature metadata.
6. Start with no automatic retries and no response cache. A later bounded retry
   policy may cover transport/service failures and concurrent metadata refresh;
   `feature_filter_unavailable` alone does not prove a transient cause.

Exit: mocked requests send both inputs, use the canonical route, preserve error
categories, and never return malformed/legacy/identity-mismatched data as success.

### 3. Wire the selected horizon through the runner

Add a required keyword-only `forecast_type` parameter to
`detailedAnalysis.main.main`, keeping its existing positional arguments intact.
At the existing call in `run_detailed_analysis.py::main`, pass
`forecast_type=forecast_config["rolling_window"]`. Do not infer the API input
from prompt text, instruction filenames, or a default within the client.

Replace the per-ticker `build_technical_url`/`fetch_json` sequence with the typed
adapter. Complete contract, catalog, and policy checks before calling `run_codex`.
Handle typed integration failures in the existing per-ticker error boundary:
return 1, continue remaining tickers, and include the failed ticker in the final
batch failure summary. An empty ticker list still returns 0. Neither error bodies
nor availability responses may be treated as market observations.

Exit: both CLI modes propagate the same horizon to recommendation selection,
technical requests, instructions, and report directory; failure of one ticker
does not stop later tickers or report batch success.

### 4. Align prompt construction and freshness policy

Serialize the validated envelope once with compact JSON
(`separators=(",", ":"), ensure_ascii=False, allow_nan=False`). Do not transpose
or duplicate it unless a downstream reader actually needs a derived row view.
Latest-value access uses `dates[-1]` and `values[-1]`; dictionary order must not
become a positional feature contract.

Extend `build_prompt` to receive a separate trusted definitions block and
consumer assessment. Supply only definitions for emitted names, deduplicated
across the three dates. Retain the local feature guide/cards as supplemental
references, but avoid requiring a second load of definitions already supplied.
Returned market data must not override trusted analysis instructions.

Update both upside instructions so the API path:

- Requires the validated v2 envelope and exactly three observations. Existing
  guidance for directly supplied one/two-row datasets must not become an API
  fallback for `insufficient_sessions` or an invalid v2 body.
- Calls H3 the latest available supplied observation; does not assume it is the
  immediately preceding completed exchange session. Observed date gaps are
  allowed and are not proof of missing exchange sessions.
- Displays `data_as_of`, forecast horizon, server request date/age, relevant null
  counts, omitted-feature coverage, and freshness limitations. Keeps generation
  time, news cutoff, and technical cutoff separate.
- Preserves null versus zero, all-null/all-zero features, unavailable selected
  features, exact units, already applied flow publication lags, and reversals.
  Three observations permit two transitions, not a sustained trend claim.
- Continues supported qualitative analysis when OHLCV is omitted; unsupported
  price calculations remain unavailable. The payload is not a complete model
  inference vector.

Proposed consumer policy: without a product-approved age cutoff, accept a valid
envelope for explicitly dated analysis with freshness marked unverified. Add
optional `TECHNICAL_MAX_DATA_AGE_CALENDAR_DAYS`, a positive integer, to reject
payloads exceeding an explicitly configured calendar-age budget before Codex.
Leaving it unset must disclose that no age budget was applied; passing it still
does not verify exchange-calendar freshness. Final release requires the consuming
product owner to accept this policy or specify a different one. Do not invent a
one-calendar-day rule that would incorrectly classify weekends or holidays.

Exit: prompt tests prove separation of trusted definitions, consumer policy, and
the unchanged envelope. Held-out report review confirms the freshness wording
and interpretation rules actually survive generation.

### 5. Make failures explicit

| Failure | Consumer behavior |
| --- | --- |
| Invalid local request/configuration | Fail before HTTP; explain the input or configuration error. |
| HTTP 422 with a validation-list `detail` | Input failure; preserve validation diagnostics and do not retry unchanged inputs. |
| 404 `technical_data_missing`, `no_eligible_sessions` | Unavailable ticker/horizon; no report generation. |
| 409 `insufficient_sessions` | Insufficient history; no fabricated/degraded API forecast. |
| 409 `feature_filter_unavailable` | Unavailable metadata/artifacts; no fallback to all columns. |
| 409 `no_eligible_indicators` | No selected indicators; no feature-selection bypass. |
| 500 `invalid_technical_data`, `invalid_model_metadata` | Data-integrity failure for operator investigation. |
| 500 `internal_error` | Service failure. |
| Unexpected status/code pairing or unknown error shape | Explicit service/protocol failure, retaining status and safe diagnostics. |
| Timeout/network failure | Transport failure; no partial analysis. |
| Malformed JSON, unsupported schema, invalid alignment/identity | Contract failure; no Codex invocation. |
| Unsupported/missing catalog definitions | Catalog integration failure; no guessed units. |
| Configured age budget exceeded | Consumer policy rejection; preserve server metadata and do not label it a backend availability failure. |

Optional readiness support belongs in a later increment unless a readiness UI is
required. It must inspect `available`, `reason_code`, and `failure_status_code`
even for HTTP 200, validate ready `data_as_of`/quality, and make no promise that a
subsequent retrieval succeeds. Normal analysis retrieves directly.

## Validation and release sequence

Use the repository's existing `unittest` style and mocked HTTP/Codex calls.
Add `test_technical_contract.py`, `test_technical_api_client.py`,
`test_feature_catalog.py`, and `test_detailed_analysis_main.py`; extend the two
existing runner/helper modules.

| Test group | Required evidence |
| --- | --- |
| Supplied regression fixture | AALI/5dd has dates 2026-10-07 through 2026-10-09, 180 indicators, 195 selected, 15 unavailable, 30 excluded, 55 nulls per date, and age 1 at server request date 2026-10-10. These expectations apply only to that fixture. |
| Requests/orchestration | Both horizons reach HTTP; lowercase inputs normalize; invalid ASCII/Unicode/length inputs fail; timeout is finite; request inputs cannot be duplicated through a base URL. Existing allocation/deduplication and output-window behavior remain covered. |
| Contract/identity | Missing required fields, unsupported versions, wrong ticker/horizon, duplicate/out-of-order/impossible dates, wrong series lengths, as-of/age/count mismatches, malformed sources, and invalid names fail. |
| Values and coverage | Preserve a mixed `50,55,53` trajectory, null positions, integer flags, full numeric values, all-zero/all-null series, omitted names, and varying feature counts. Reject booleans, strings, and nonfinite observations. |
| Horizon provenance | Validate two versus four source descriptors. Test 5dd feature inclusion in 10dd only using a common frozen artifact snapshot, not unrelated live responses. |
| Catalog/prompt | Every emitted name resolves; wrong version/missing definition fails; definitions match catalog units/lookbacks/lags; market JSON occurs once and retains provenance. |
| Failure gating | Exercise every documented status/code and malformed error body, transport failure, policy rejection, and Codex error. Assert no Codex invocation for pre-generation failures and correct batch exit/continuation. |
| Agent evaluation | Review both horizons with reversals, missing OHLCV, all-null/all-zero series, omitted features, MACD ratios/RSI points/PVO percentage points, lagged flows, old dates, and unverified freshness. No invented prices, features, or continuity claims. |

After implementation, in the consumer's configured Python 3.10+ environment:

```bash
python -m unittest tests.test_run_detailed_analysis tests.test_detailed_analysis_helper tests.test_technical_contract tests.test_technical_api_client tests.test_feature_catalog tests.test_detailed_analysis_main
python -m unittest discover -s tests
```

Then verify a staging backend against the matching artifact snapshot and run the
backend tests/audit in that backend's own environment, following the integration
plan. The fixed `2026-10-10` audit date reproduces fixture selection; release
readiness uses the actual Jakarta date and the full intended ticker/horizon scope.
Backend availability does not replace the consumer age-policy check.

Complete packaging/documentation checks before rollout: catalog and contract are
present in the consumer Docker image without sibling mounts, feature-card content
matches catalog 1.0, Markdown links resolve, optional environment settings work in
the container, and README claims match implemented behavior. The current
`docker-entrypoint.sh` preserves exported environment variables but writes only a
subset to `.env`; document how new settings reach local and container runs.

Roll out contract/catalog first, adapter second, then runner/prompt migration and
documentation together. Enable production generation only after mocked tests,
staging calls, backend served-scope audit, and agent evaluation pass. Monitor
HTTP/reason codes, client validation/catalog failures, dates/age, coverage/null
counts, latency, and response size per ticker/horizon. Measure tokens and report
quality separately before claiming savings.

Keep compatible backend and consumer releases available for joint rollback. If
all callers cannot migrate together, coordinate a separately staged backend
versioned route; `/technical/v2/` is not an existing route. Follow the backend's
quiesced-refresh or immutable-snapshot procedure for multi-file artifact updates.
Do not deploy an old parser against the v2 endpoint.

## Dependencies, evidence, and completion

The AALI/5dd and matching 10dd regression snapshots are now packaged. Remaining
release inputs are repaired backend artifact coverage, restoration of the original
backend catalog for its generating-function validation, a supported host Codex
configuration, accepted product freshness policy, and access to the deployment
environment for staging verification. Local evidence and synthetic evaluation do
not establish live deployment readiness.

During preparation, the relevant consumer code, tests, instructions, Docker
runtime, and sibling backend schema/router/catalog/migration guide were inspected.
The baseline command
`python3 -m unittest tests.test_run_detailed_analysis tests.test_detailed_analysis_helper`
passed five helper tests but failed to import the runner test module because the
host Python 3.9 environment lacks `pydantic`. This is not a passing runner suite or
evidence of completed v2 migration. No live backend requests, artifact audit,
Codex generation, or dependency installation were performed for this plan.

Completion requires both CLI modes to send their explicit horizon, validation and
definitions to precede every Codex call, documented failure/freshness behavior to
be verified, fixtures and release checks to pass in the intended environment, and
all shipped documentation to describe the implemented contract accurately.

## Appendix A: complete supplied AALI/5dd service response

Complete user-supplied service JSON, preserved without shortening or changing its
values. The dates and counts belong to the supplied snapshot.

```json
{
    "schema_version": "2.0",
    "ticker": "AALI",
    "forecast_type": "5dd",
    "market_timezone": "Asia/Jakarta",
    "selection_policy": "latest_available_before_request_date",
    "requested_sessions": 3,
    "returned_sessions": 3,
    "dates": [
        "2026-10-07",
        "2026-10-08",
        "2026-10-09"
    ],
    "order": "oldest_to_newest",
    "data_as_of": "2026-10-09",
    "quality": {
        "request_date": "2026-10-10",
        "data_age_calendar_days": 1,
        "freshness_status": "unverified_without_exchange_calendar",
        "null_counts_by_session": [
            55,
            55,
            55
        ]
    },
    "feature_filter": {
        "source": "model_metadata",
        "key": "selected_features",
        "strategy": "union",
        "model_version": 1,
        "sources": [
            {
                "label_type": "medianLoss",
                "window": "5dd"
            },
            {
                "label_type": "medianGain",
                "window": "5dd"
            }
        ],
        "selected_union_count": 195,
        "included_count": 180,
        "selected_unavailable_count": 15,
        "excluded_not_selected_count": 30
    },
    "feature_catalog_version": "1.0",
    "indicators": {
        "ATR Bullish": [
            1,
            1,
            1
        ],
        "ATR Bearish": [
            0,
            0,
            0
        ],
        "ATR Stop Distance Percent": [
            0.08402763408618187,
            0.0677195285227844,
            0.08550984003234882
        ],
        "Aroon Up": [
            48.0,
            44.0,
            40.0
        ],
        "Aroon Down": [
            76.0,
            72.0,
            68.0
        ],
        "Aroon Oscillator": [
            -28.0,
            -28.0,
            -28.0
        ],
        "Aroon Change Position": [
            0.0,
            0.0,
            0.0
        ],
        "Aroon Up Trend": [
            0,
            0,
            0
        ],
        "Aroon Down Trend": [
            1,
            1,
            0
        ],
        "Plus Directional Index": [
            26.369295710995868,
            24.280646951772123,
            25.2213217715581
        ],
        "ADX Value": [
            32.27328870626728,
            31.026296840749264,
            30.340214727083588
        ],
        "ADXR Value": [
            44.65486295110276,
            42.88012351490783,
            40.97822530644599
        ],
        "Directional Index Spread": [
            11.49727549832078,
            6.266189929236223,
            8.899102993714013
        ],
        "ADX Strong Trend": [
            1,
            1,
            1
        ],
        "ADX Change 5D": [
            -6.265483089960881,
            -4.866310912591448,
            -3.980300192605167
        ],
        "Bull Power Up Trend": [
            1.0,
            1.0,
            1.0
        ],
        "Bull Power 80% Positives": [
            0.0,
            0.0,
            0.0
        ],
        "Bear Power Trend": [
            0.0,
            0.0,
            0.0
        ],
        "Bear Power 80% Negatives": [
            1.0,
            0.0,
            0.0
        ],
        "Bull Power Percent": [
            0.04023800910623144,
            0.034679880973306765,
            0.040787880091200435
        ],
        "Bear Power Percent": [
            0.02566074963101286,
            0.005006290468855812,
            0.002097403900724246
        ],
        "MACD Near 0": [
            1,
            1,
            1
        ],
        "MACD Non-Near 0 Negative": [
            0,
            0,
            0
        ],
        "MACD Non-Near 0 Positive": [
            0,
            0,
            0
        ],
        "MACD Percent": [
            0.01222392771202134,
            0.013131995378064028,
            0.015741808100789182
        ],
        "MACD Signal Percent": [
            0.009743619712316902,
            0.010400914365754972,
            0.01143294602027429
        ],
        "MACD Histogram Percent": [
            0.002480307999704438,
            0.0027310810123090568,
            0.004308862080514892
        ],
        "MACD Histogram Change 5D": [
            0.01640935780491091,
            0.01514046808539649,
            0.012416311139643846
        ],
        "SuperTrend Change": [
            0,
            0,
            0
        ],
        "Vortex Positive": [
            0.9677418323361293,
            0.9668873388548885,
            1.0081362844146855
        ],
        "Vortex Negative": [
            1.032257928115872,
            1.0529799996562481,
            0.9893880988938525
        ],
        "Vortex Spread": [
            -0.0645160957797426,
            -0.08609266080135958,
            0.018748185520833016
        ],
        "Keltner Percent B": [
            0.888117634804485,
            0.712727858552941,
            0.8725014151673911
        ],
        "Keltner Overbought": [
            0,
            0,
            0
        ],
        "Keltner Oversold": [
            0,
            0,
            0
        ],
        "Keltner Width": [
            0.12167829046441478,
            0.12260671595629467,
            0.12600344794797574
        ],
        "Donchian Percent B": [
            0.81818176801859,
            0.6818181497701402,
            0.8762873217797137
        ],
        "Donchian Overbought": [
            0,
            0,
            0
        ],
        "Donchian Oversold": [
            0,
            0,
            0
        ],
        "Width Donchian Increasing": [
            0.0,
            0.0,
            0.0
        ],
        "Width Donchian Decreasing": [
            0.0,
            0.0,
            0.0
        ],
        "Donchian Width": [
            0.13373855412675645,
            0.13373855412675645,
            0.13373855412675645
        ],
        "Bollinger Percent B": [
            0.754079681454438,
            0.6403126684345868,
            0.79906057524256
        ],
        "Bollinger Overbought": [
            0,
            0,
            0
        ],
        "Bollinger Oversold": [
            0,
            0,
            0
        ],
        "Bollinger Width": [
            0.1600101311639953,
            0.1600101311639953,
            0.16105303989244593
        ],
        "RSI Value": [
            63.089648287735,
            58.00471606659483,
            62.630461501448025
        ],
        "RSI Rate of Change 5": [
            13.881366198070047,
            11.683803242407535,
            6.587729372547955
        ],
        "RSI Rate of Change 10": [
            19.92446097670294,
            16.531143903127564,
            18.786869717910164
        ],
        "Stochastic J": [
            100.75756822525483,
            90.13207973537843,
            96.77493390318253
        ],
        "Stochastic K Value": [
            74.9999958894365,
            78.6713222405071,
            85.3810625670621
        ],
        "Stochastic D Value": [
            62.12120972152735,
            72.94094349307143,
            79.6841268990019
        ],
        "Stochastic K Minus D": [
            12.878786167909155,
            5.730378747435665,
            5.696935668060206
        ],
        "Stochastic Oscillator Overbought": [
            0.0,
            0.0,
            1.0
        ],
        "RSI 7": [
            71.67388830926149,
            60.308906982113356,
            68.59433265520924
        ],
        "RSI 21": [
            61.78755438525359,
            58.36969274143878,
            61.5542113752983
        ],
        "On Balance Volume Increasing": [
            1.0,
            1.0,
            1.0
        ],
        "OBV to MA20 Ratio": [
            0.9865180151222025,
            0.9661964524250991,
            0.9861837862640948
        ],
        "OBV Change 5D Normalized": [
            0.04187836040760389,
            0.04430387475934328,
            0.039367009239270015
        ],
        "MFI Value": [
            29.72582317264937,
            29.85923644278202,
            35.340545097266755
        ],
        "MFI Overbought": [
            0,
            0,
            0
        ],
        "MFI Increasing": [
            1.0,
            1.0,
            1.0
        ],
        "MFI Decreasing": [
            0.0,
            0.0,
            0.0
        ],
        "CMF Value": [
            0.0241460975202412,
            0.06622169980082242,
            0.0711983698034777
        ],
        "CMF Change 5D": [
            0.05934243943219639,
            0.18072613503405155,
            0.15360194962887136
        ],
        "Strong Positive CMF": [
            0,
            0,
            0
        ],
        "Negative CMF": [
            0,
            0,
            0
        ],
        "Crossover CMF": [
            0.0,
            0.0,
            0.0
        ],
        "Accumulation Distribution Line Increasing": [
            1.0,
            1.0,
            1.0
        ],
        "Accumulation Distribution Line Decreasing": [
            0.0,
            0.0,
            0.0
        ],
        "ADL Change 5D Normalized": [
            0.023687422858170482,
            0.026319172331900727,
            0.026095607677466645
        ],
        "PVO Value": [
            1.5497998884273094,
            3.5757335765798115,
            1.6436237980602237
        ],
        "PVO Signal": [
            7.927928184465642,
            7.057489262888476,
            5.974716169922825
        ],
        "PVO Histogram": [
            -6.378128296038333,
            -3.4817556863086643,
            -4.331092371862601
        ],
        "PVO Histogram Change 5D": [
            -3.342986730517697,
            -2.283668226972343,
            -2.515453556126893
        ],
        "Fisher Transform": [
            0.59915243132312,
            1.0281009515864727,
            1.4506438060079492
        ],
        "Fisher Transform Trigger": [
            -0.041292881250142854,
            0.59915243132312,
            1.0281009515864727
        ],
        "Fisher Up trend": [
            0,
            0,
            0
        ],
        "Fisher Down Trend": [
            0,
            0,
            0
        ],
        "Fisher Spread": [
            0.6404453125732629,
            0.42894852026335273,
            0.42254285442147643
        ],
        "Fisher Change 5D": [
            2.7731020771964183,
            3.018777426278774,
            2.985878757832117
        ],
        "Fisher Reversal": [
            0.0,
            0.0,
            0.0
        ],
        "Foreign Net Intensity 1D": [
            null,
            null,
            null
        ],
        "Foreign Buy Share 1D": [
            null,
            null,
            null
        ],
        "Foreign Sell Share 1D": [
            null,
            null,
            null
        ],
        "Foreign Participation 1D": [
            null,
            null,
            null
        ],
        "Foreign Net Flow Signed Log": [
            null,
            null,
            null
        ],
        "Foreign Net Intensity 5D": [
            null,
            null,
            null
        ],
        "Foreign Buy Share 5D": [
            null,
            null,
            null
        ],
        "Foreign Sell Share 5D": [
            null,
            null,
            null
        ],
        "Foreign Participation 5D": [
            null,
            null,
            null
        ],
        "Foreign Net Flow ZScore 5D": [
            null,
            null,
            null
        ],
        "Foreign Accumulation Day Share 5D": [
            null,
            null,
            null
        ],
        "Foreign Net Value Intensity 5D": [
            null,
            null,
            null
        ],
        "Foreign Net Intensity 10D": [
            null,
            null,
            null
        ],
        "Foreign Buy Share 10D": [
            null,
            null,
            null
        ],
        "Foreign Sell Share 10D": [
            null,
            null,
            null
        ],
        "Foreign Participation 10D": [
            null,
            null,
            null
        ],
        "Foreign Net Flow ZScore 10D": [
            null,
            null,
            null
        ],
        "Foreign Accumulation Day Share 10D": [
            null,
            null,
            null
        ],
        "Foreign Net Value Intensity 10D": [
            null,
            null,
            null
        ],
        "Foreign Net Intensity 20D": [
            null,
            null,
            null
        ],
        "Foreign Buy Share 20D": [
            null,
            null,
            null
        ],
        "Foreign Sell Share 20D": [
            null,
            null,
            null
        ],
        "Foreign Participation 20D": [
            null,
            null,
            null
        ],
        "Foreign Net Flow ZScore 20D": [
            null,
            null,
            null
        ],
        "Foreign Accumulation Day Share 20D": [
            null,
            null,
            null
        ],
        "Foreign Net Value Intensity 20D": [
            null,
            null,
            null
        ],
        "Foreign Net Intensity 60D": [
            null,
            null,
            null
        ],
        "Foreign Buy Share 60D": [
            null,
            null,
            null
        ],
        "Foreign Sell Share 60D": [
            null,
            null,
            null
        ],
        "Foreign Participation 60D": [
            null,
            null,
            null
        ],
        "Foreign Net Flow ZScore 60D": [
            null,
            null,
            null
        ],
        "Foreign Accumulation Day Share 60D": [
            null,
            null,
            null
        ],
        "Foreign Net Value Intensity 60D": [
            null,
            null,
            null
        ],
        "Foreign Net Intensity EMA 5D Minus 20D": [
            null,
            null,
            null
        ],
        "Foreign Net Intensity Acceleration 5D": [
            null,
            null,
            null
        ],
        "Foreign Flow Return Correlation 20D": [
            null,
            null,
            null
        ],
        "Foreign Flow Price Divergence 20D": [
            null,
            null,
            null
        ],
        "Foreign Flow Return Correlation 60D": [
            null,
            null,
            null
        ],
        "Foreign Flow Price Divergence 60D": [
            null,
            null,
            null
        ],
        "Non Regular Volume Share 1D": [
            null,
            null,
            null
        ],
        "Non Regular Volume Share 5D": [
            null,
            null,
            null
        ],
        "Non Regular Value Share 5D": [
            null,
            null,
            null
        ],
        "Non Regular Volume ZScore 5D": [
            null,
            null,
            null
        ],
        "Non Regular Value ZScore 5D": [
            null,
            null,
            null
        ],
        "Non Regular Frequency ZScore 5D": [
            null,
            null,
            null
        ],
        "Non Regular Volume Share 20D": [
            null,
            null,
            null
        ],
        "Non Regular Value Share 20D": [
            null,
            null,
            null
        ],
        "Non Regular Volume ZScore 20D": [
            null,
            null,
            null
        ],
        "Non Regular Value ZScore 20D": [
            null,
            null,
            null
        ],
        "Non Regular Frequency ZScore 20D": [
            null,
            null,
            null
        ],
        "Non Regular Volume Share 60D": [
            null,
            null,
            null
        ],
        "Non Regular Value Share 60D": [
            null,
            null,
            null
        ],
        "Non Regular Volume ZScore 60D": [
            null,
            null,
            null
        ],
        "Non Regular Value ZScore 60D": [
            null,
            null,
            null
        ],
        "Non Regular Frequency ZScore 60D": [
            null,
            null,
            null
        ],
        "Price Momentum 5D": [
            0.07187496390659454,
            0.06645566240810297,
            0.047141324635723514
        ],
        "Price Momentum 10D": [
            0.09235664063319615,
            0.08360131296401807,
            0.10049881705588937
        ],
        "Price Momentum 20D": [
            -0.0029069753862381864,
            0.0,
            0.004525127842919696
        ],
        "Volume Ratio 20D": [
            0.5684000529783781,
            1.1792003517084728,
            0.7740735647001107
        ],
        "Log Return 1D": [
            0.005847967134645415,
            -0.017647508472403928,
            0.02507363755211678
        ],
        "Log Return 3D": [
            0.03863777424951209,
            0.002971768969999289,
            0.013274096214358266
        ],
        "Log Return 5D": [
            0.06940941769901876,
            0.06434068507690327,
            0.04606390332922494
        ],
        "Log Return 10D": [
            0.08833741798894934,
            0.08029004289659802,
            0.09576354706866219
        ],
        "Log Return 20D": [
            -0.002911208845551627,
            0.0,
            0.004514920234161224
        ],
        "Open Gap Percent": [
            -2.7477769252529308e-9,
            -0.005830895497549236,
            0.007080078125
        ],
        "Intraday Return Percent": [
            0.005865102639296068,
            -0.011730205278592342,
            0.01818181818181818
        ],
        "High Low Range Percent": [
            0.014577259475218582,
            0.029673590504450953,
            0.03869047619047619
        ],
        "Close Location Value": [
            1.0,
            0.0,
            0.8461538461538461
        ],
        "Close to EMA 5D": [
            0.023880701376519955,
            0.003972268295411197,
            0.01945146341748186
        ],
        "Close to EMA 10D": [
            0.03886747430414528,
            0.016868697663506,
            0.034657253903362654
        ],
        "Close to EMA 20D": [
            0.047225490302101845,
            0.026081864129591202,
            0.046936462676591614
        ],
        "Close to EMA 50D": [
            0.08887822889013877,
            0.06690911415774589,
            0.0899806950295547
        ],
        "EMA 5D to 20D Spread": [
            0.022800301728704155,
            0.022022118072761773,
            0.026960576589857916
        ],
        "EMA 10D to 50D Spread": [
            0.04813968655577721,
            0.049210302774802164,
            0.05347030711617596
        ],
        "Realized Volatility 5D": [
            0.28846278943380577,
            0.3126758428646601,
            0.2346853411034228
        ],
        "Realized Volatility 20D": [
            0.3500179618103784,
            0.3480179040149618,
            0.3517094716529795
        ],
        "Realized Volatility 60D": [
            0.31396681831880735,
            0.3172114323512942,
            0.3196862313168024
        ],
        "Volatility 5D to 20D Ratio": [
            0.8241371041126168,
            0.8984475777177766,
            0.6672704604753418
        ],
        "Volatility 20D to 60D Ratio": [
            1.1148246928914765,
            1.097116523938996,
            1.1001708462834696
        ],
        "ATR Percent 14D": [
            0.028678071643577118,
            0.029435251702216052,
            0.029419528616319735
        ],
        "Distance From 20D High": [
            -0.02279202146115643,
            -0.039886030569975556,
            -0.015508136814916345
        ],
        "Distance From 20D Low": [
            0.1172637916403825,
            0.09771982776504524,
            0.1255916202668921
        ],
        "Price ZScore 20D": [
            1.0163187258177724,
            0.5612506737383578,
            1.196242300970264
        ],
        "Distance From 60D High": [
            -0.02279202146115643,
            -0.039886030569975556,
            -0.015508136814916345
        ],
        "Distance From 60D Low": [
            0.36653385120400717,
            0.34262948016630956,
            0.37125652122962677
        ],
        "Volume Change 1D": [
            -0.3263844606857311,
            1.1093715866889973,
            -0.349109362054681
        ],
        "Volume Change 5D": [
            -0.3791029930373452,
            -0.08491281273692186,
            -0.24383396831762583
        ],
        "Volume ZScore 20D": [
            -0.6840862720846208,
            0.28851504754888907,
            -0.3595396381616861
        ],
        "Volume ZScore 60D": [
            -0.33028504022821303,
            0.9236160168663636,
            0.05142861774213454
        ],
        "Dollar Volume Ratio 20D": [
            0.5966167379548935,
            1.2154603457101933,
            0.8183477075697105
        ],
        "Up Volume Share 20D": [
            0.37994602827720936,
            0.37368211090214853,
            0.36834283391801104
        ],
        "Return Volume Correlation 20D": [
            -0.30283570190459114,
            -0.3300383256724375,
            -0.34827418841560587
        ],
        "Return Volume Correlation 60D": [
            0.05695707006772556,
            0.03723845239334465,
            0.02277804748547635
        ],
        "Price Volume Divergence 20D": [
            -0.04748202980128604,
            0.018563255814290844,
            -0.016561799135304422
        ],
        "Choppiness Index 14D": [
            47.715369679876346,
            51.29553487613316,
            50.31996949601205
        ],
        "Hurst Exponent 100D": [
            0.7298617400861246,
            0.758617499386768,
            0.7186225072190394
        ],
        "Regime Persistent": [
            1,
            1,
            1
        ],
        "Regime Mean Reverting": [
            0,
            0,
            0
        ]
    }
}
```
