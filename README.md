# Agentic Stock Analysis

agentic-stock-analysis generates short-term stock-analysis reports and exposes
the generated reports through a small FastAPI service.

The analysis workflow:

1. Fetches daily ticker recommendations from a configured HTTP endpoint.
2. Selects exactly the top K unique recommendations for the requested forecast
   window, then adds portfolio tickers from the Organizer stocks API and removes
   duplicates. K is set by `TARGET_COUNT = 4` in `run_detailed_analysis.py`.
3. Fetches technical data for each selected ticker.
4. Uses the Codex CLI and the instructions in `instructions/` to generate a
   Markdown report.
5. Saves each report under its rolling window as
   `detailedAnalysisResults/{ROLLING_WINDOW}/{TICKER}.md`.
6. A separate entry-strategy workflow can consume those reports and save
   strategies as `entryStrategyResults/{ROLLING_WINDOW}/{TICKER}.md`.

The web service reads those Markdown files and provides both REST endpoints and
an MCP server for listing available tickers and retrieving an individual
report.

The API package uses this layered request flow:

`router -> controller -> service -> repository -> model`

## Requirements

- Docker Desktop, or Docker Engine with the Compose plugin
- A recommendation API and technical-data API
- Codex authentication through either:
  - an existing Codex login in `~/.codex`, or
  - an `OPENAI_API_KEY`

## Configure the project

Create the local environment file:

```bash
cp .env.example .env
```

Edit `.env` and provide the base URL used by the analysis workflow:

```dotenv
ML_BASE_URL=http://your-ml-api:8000
ORGANIZER_BASE_URL=http://localhost:8000

DETAILED_ANALYSIS_RESULT=detailedAnalysisResults
ENTRY_STRATEGY_RESULT=entryStrategyResults
HOLD_STRATEGY_RESULT=holdStrategyResults
OPENAI_API_KEY=
API_PORT=8003
MCP_PORT=8004
CHAT_API_PORT=8005
```

`OPENAI_API_KEY` can remain empty when the host already has an authenticated
Codex configuration in `~/.codex`. Docker Compose mounts that configuration
read-only and copies the required authentication into persistent Codex volumes
when needed.

When the data API runs on the host machine, containers on Docker Desktop can
usually reach it through `host.docker.internal`, for example:

```dotenv
ML_BASE_URL=http://host.docker.internal:8000
```

## Run stock analysis with Docker

Build the analysis image:

```bash
docker compose build agentic-stock-analysis
```

Run the complete recommendation-based analysis once:

```bash
docker compose run --rm agentic-stock-analysis
```

The default mode is `10`, forecasting exactly **10 trading sessions**.
The `5` mode forecasts exactly **5 trading sessions**. Choose either supported
window explicitly with:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 5

docker compose run --rm agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 10
```

The `5` mode uses
`instructions/stock-upside-analysis-5-instructions.md` and requests the
recommendation API's `5dd` rolling window. The `10` mode uses
`instructions/stock-upside-analysis-10-instructions.md` and requests `10dd`.
The only accepted forecast-window values are `5` and `10`.
Recommendation and technical endpoint URLs are derived from `ML_BASE_URL`.
Technical requests include the matching `forecast_type=5dd` or `10dd` at
`GET /technical/`. Both windows receive three historical observations, following
the technical API v2 contract validated by
[`detailedAnalysis/technical_contract.py`](detailedAnalysis/technical_contract.py).

The client validates the response's request identity, dates, aligned numeric/null
series, quality counts, and feature-filter metadata before starting Codex. It
supplies the full envelope as compact JSON alongside the selected strategy
instructions. The agent reads the feature guide, index, and matching cards under
`instructions/features/` for definitions and interpretation. Nulls, zeros, numeric precision, and
metadata are preserved. HTTP failures retain their structured reason codes;
invalid or legacy payloads fail the ticker rather than producing an analysis.
Readiness does not establish exchange-calendar freshness. See the
[technical API client](detailedAnalysis/technical_api.py) and
[contract regression tests](tests/test_technical_contract.py)
for implementation details and validation examples.

Feature definitions and interpretation rules are maintained in
[the feature documentation](instructions/features/README.md). The prompt builder
does not generate an additional definitions or consumer-assessment context block.

Optional `TECHNICAL_API_TIMEOUT_SECONDS` overrides the runner's 30-second HTTP
timeout. Optional `TECHNICAL_MAX_DATA_AGE_CALENDAR_DAYS` rejects technical data
older than the configured positive integer calendar-age budget. Unset accepts
explicitly dated analysis with freshness unverified; passing the budget still
does not prove exchange-calendar freshness. Both settings work through exported
environment variables, local `.env`, and the Compose analysis service's `env_file`.

Run consumer regression checks with `python -m unittest discover -s tests` in an
environment installed from `requirements.txt` (Python 3.10+).

Each run fetches only the requested rolling window's recommendations and selects
exactly `TARGET_COUNT` unique ML tickers. Change the single `TARGET_COUNT = 4`
setting in `run_detailed_analysis.py` to adjust that quota; it must be a positive
integer. Selection normalizes ticker case and whitespace, keeps the highest score
for duplicates, and orders by descending score then ascending ticker for ties.
Zero and negative scores are eligible.

Detailed analysis adds portfolio tickers from
`GET /stocks?trading_window=5dd|10dd` on `ORGANIZER_BASE_URL`. The endpoint
accepts a ticker-string array, an array of ticker objects, or an object containing
a `stocks` list of either shape. The window identifier (`trading_window`, with `rolling_window` as a fallback)
must match the requested window when supplied. ML tickers are processed first in score order;
new portfolio tickers follow in service order. Duplicate tickers are processed
once within a batch. With K=4 and two new portfolio tickers, six analyses are
attempted. Portfolio overlaps do not require replacement ML recommendations.

If the upstream list supplies fewer than K valid unique recommendations, the run
fails with the requested and available counts. Portfolio holdings cannot fill
missing ML slots. Configuration, preflight, service, and payload failures preserve
existing reports; output cleanup starts only after successful selection and
portfolio validation. Each selected ticker is attempted even if an earlier
analysis fails, and any failed analysis makes the batch return a nonzero status.
The quota guarantees attempts, not successful reports.

Results are written to `detailedAnalysisResults/5dd/` or
`detailedAnalysisResults/10dd/`. Selection is independent for each window, so the
same ticker may appear in both directories. A successful selection clears and
replaces reports only in its requested rolling-window directory; reports for the
other window are preserved.

## Generate entry strategies with Docker

Generate strategies from the analysis reports in the matching rolling window.
Mode `5` uses exactly **5 trading sessions**; `10` uses exactly
**10 trading sessions** (the default). Entry plans preserve the source report’s
original dated expiry; generating a strategy does not restart the window.
Refresh stale, expired, or old range-based analysis reports before using them:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_entry_strategy.py --forecast-window 5

docker compose run --rm agentic-stock-analysis \
  python run_entry_strategy.py --forecast-window 10
```

The runner reads every Markdown file from `detailedAnalysisResults/5dd/` or
`detailedAnalysisResults/10dd/`, applies the matching instruction in `instructions/`,
and writes the result to `entryStrategyResults/5dd/` or
`entryStrategyResults/10dd/`. It clears and replaces files only in the selected
entry-strategy window. Run detailed analysis first when no source reports exist.

## Generate hold strategies with Docker

Hold mode `5` uses exactly **5 trading sessions**; `10` uses
exactly **10 trading sessions** (the default). Plans retain the source report’s
original dated expiry. Refresh stale, expired, or old range-based reports; a
newer quote alone does not refresh the analysis.

Hold-strategy tickers are retrieved from `GET /stocks` on
`ORGANIZER_BASE_URL`, using
`trading_window=5dd` or `trading_window=10dd`. When the response supplies a
stock price, it is passed as the position's average acquisition price. The
matching detailed-analysis report provides the market thesis and risk levels.

Use the existing analysis service and override its command:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_hold_strategy.py --forecast-window 5

docker compose run --rm agentic-stock-analysis \
  python run_hold_strategy.py --forecast-window 10
```

Results are written to `holdStrategyResults/5dd/` or
`holdStrategyResults/10dd/`. Only the selected output window is replaced.

## Run the FastAPI service locally

Install the Python dependencies and start Uvicorn from the project root:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The local development server is available at `http://127.0.0.1:8000`, with
interactive API documentation at `http://127.0.0.1:8000/docs`.

## Host the FastAPI service with Docker

Build and start the API in the background:

```bash
docker compose up --build -d initialize-fastapi
```

The API is then available at `http://localhost:8003`.

Available endpoints:

```text
GET /analysis?rolling_window=5dd
GET /analysis/report?ticker=SMRA&rolling_window=5dd
GET /entry_strategy?rolling_window=5dd
GET /entry_strategy/report?ticker=SMRA&rolling_window=5dd
GET /hold_strategy?rolling_window=10dd
GET /hold_strategy/report?ticker=INDY&rolling_window=10dd
GET /docs
```

Example requests:

```bash
curl "http://localhost:8003/analysis?rolling_window=5dd"
curl "http://localhost:8003/analysis/report?ticker=SMRA&rolling_window=5dd"
curl "http://localhost:8003/entry_strategy?rolling_window=5dd"
curl "http://localhost:8003/entry_strategy/report?ticker=SMRA&rolling_window=5dd"
curl "http://localhost:8003/hold_strategy?rolling_window=10dd"
curl "http://localhost:8003/hold_strategy/report?ticker=INDY&rolling_window=10dd"
```

The first request lists Markdown reports in the selected rolling-window
directory. The second returns the full report for the requested ticker and
rolling window.

Example responses:

```json
{
  "tickers": ["SMRA", "SOCI"]
}
```

```json
{
  "ticker": "SMRA",
  "report": "**1. Analysis timestamp...**"
}
```

### Run and connect an MCP client

The MCP server runs in its own container, separately from the REST API. Start it
with:

```bash
docker compose up --build -d initialize-fastapi-mcp
```

Its stateless Streamable HTTP endpoint is:

```text
http://localhost:8004/mcp
```

It provides these tools:

- `list_analysis_tickers` accepts a required `rolling_window` and lists the
  tickers with generated reports in that directory.
- `get_analysis_report` accepts required `ticker` and `rolling_window` arguments
  and returns the complete Markdown report from the matching directory. Use
  `5dd` for 5 trading sessions and `10dd` for 10 trading sessions.

For example, add it to Codex CLI:

```bash
codex mcp add agentic-stock-analysis \
  --url http://localhost:8004/mcp
```

The MCP endpoint does not currently require authentication. It is bound to
localhost by default; keep it on a trusted private network or add authentication
at a reverse proxy before exposing it publicly. Override its host port with
`MCP_PORT`.

To publish the API on another host port:

```bash
API_PORT=8080 docker compose up --build -d initialize-fastapi
```

The API will then be available at `http://localhost:8080`.

Check its status and logs:

```bash
docker compose ps initialize-fastapi
docker compose logs -f initialize-fastapi
```

Stop the API:

```bash
docker compose stop initialize-fastapi
```

The reports remain on the host because `detailedAnalysisResults/` is bind-mounted into
both containers. The analysis container has write access, while the API
container mounts the directory read-only.

## Run the quota-controlled chat API

The chat API runs Codex CLI with access to the analysis-only MCP server. It
buffers each response until the Organizer atomically consumes one quota unit
and stores the completed user/assistant turn in the current Jakarta-day
conversation.
Start the MCP and chat services with:

```bash
docker compose up --build -d \
  initialize-fastapi-mcp initialize-fastapi-assistant
```

The API is available at `http://localhost:8005` by default. Set reusable shell
variables with the API URL and a valid Organizer access token:

```bash
export CHAT_API_URL="http://localhost:8005"
export CHAT_ACCESS_TOKEN="<access-token>"
```

### Chat request examples

Ask Codex to list the analysis reports available for the 5-day rolling window:

```bash
curl --location "$CHAT_API_URL/chat" \
  --header "Authorization: Bearer $CHAT_ACCESS_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"message":"Which 5dd analysis reports are available?"}'
```

Ask Codex to retrieve and summarize a specific analysis report:

```bash
curl --location "$CHAT_API_URL/chat" \
  --header "Authorization: Bearer $CHAT_ACCESS_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"message":"Summarize the 10dd analysis report for BBCA, including its thesis and key risks."}'
```

Ask Codex to compare reports in the same rolling window:

```bash
curl --location "$CHAT_API_URL/chat" \
  --header "Authorization: Bearer $CHAT_ACCESS_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"message":"Compare the 5dd reports for BBCA and TLKM. Highlight their catalysts and downside risks."}'
```

Codex receives each request independently, so include all required tickers and
rolling-window context in each message. The Organizer stores completed turns so
the UI can restore the current day's conversation. A successful response
resembles:

```json
{
  "reply": "The available 5dd analysis reports are BBCA and TLKM.",
  "conversation_id": "87033aec-f74c-49ea-8812-37c15c9251e0",
  "messages": [
    {
      "id": "d54894fb-dce8-435a-9334-bc2a55571a91",
      "client_message_id": "3fc82b96-3bd6-4b2e-b57d-30cc723ac784",
      "role": "user",
      "content": "Which 5dd analysis reports are available?",
      "created_at": "2026-09-10T09:14:22+07:00"
    },
    {
      "id": "48cc11b6-7792-4220-bb29-1b41fd67e781",
      "client_message_id": null,
      "role": "assistant",
      "content": "The available 5dd analysis reports are BBCA and TLKM.",
      "created_at": "2026-09-10T09:14:29+07:00"
    }
  ],
  "quota": {
    "allowed": true,
    "remaining": 4,
    "daily_limit": 5,
    "resets_at": "2026-09-11T00:00:00+07:00"
  }
}
```

When the user has no remaining quota, the API returns HTTP 429 and does not
start Codex:

```json
{
  "detail": {
    "code": "quota_exhausted",
    "allowed": false,
    "remaining": 0,
    "daily_limit": 20,
    "resets_at": "2026-09-11T00:00:00+07:00"
  }
}
```

The HTTP 429 response also includes a `Retry-After` header when the reset time
is in the future. A missing or malformed bearer token returns HTTP 401:

```json
{
  "detail": "Bearer authorization is required"
}
```

Check service health without consuming quota:

```bash
curl "$CHAT_API_URL/health/live"
curl "$CHAT_API_URL/health/ready"
```

Both endpoints return `{"status":"ok"}` when healthy. To publish the chat API
on a different host port, set `CHAT_API_PORT` when starting it:

```bash
CHAT_API_PORT=8085 docker compose up --build -d \
  initialize-fastapi-mcp initialize-fastapi-assistant
curl http://localhost:8085/health/ready
```

For every request, the service first checks `GET /chat-quota` on
`ORGANIZER_BASE_URL`. This avoids starting Codex when quota is already
exhausted, but it is not a reservation: a concurrent request can still consume
the final unit. The service generates an idempotency UUID once for the request,
then calls `POST /chat-quota/consume` with that UUID, the query, and the
completed Codex answer. That
operation atomically consumes quota and stores both messages. Transient consume
failures are retried with the same UUID and payload. The answer is released only
after Organizer returns the authoritative stored messages and nested quota.
Codex failures do not consume quota, and the service fails closed when either
quota operation cannot be completed. Reset timestamps come from Organizer and
use the `Asia/Jakarta` day boundary.

Codex is run in an ephemeral read-only workspace and is configured with only
the MCP endpoint specified by `CHAT_MCP_URL`. The MCP server exposes only
`list_analysis_tickers` and `get_analysis_report`.

Useful settings:

```dotenv
CHAT_API_PORT=8005
CHAT_MCP_URL=http://agentic-mcp:8000/mcp
CHAT_CODEX_TIMEOUT_SECONDS=120
CHAT_ORGANIZER_TIMEOUT_SECONDS=5
CHAT_ORGANIZER_RETRY_ATTEMPTS=3
CHAT_ORGANIZER_RETRY_BACKOFF_SECONDS=0.1
CHAT_MAX_CONCURRENCY=2
CHAT_MAX_MESSAGE_CHARS=10000
CHAT_MAX_RESPONSE_BYTES=1000000
```

Health endpoints are available at `/health/live` and `/health/ready`.

## Project structure

```text
app/                    FastAPI router, controller, service, repository, models
detailedAnalysisResults/        Generated Markdown reports
entryStrategy/          Individual-ticker entry-strategy workflow
entryStrategyResults/   Generated entry-strategy Markdown reports
holdStrategy/           Individual-position hold-strategy workflow
holdStrategyResults/    Generated hold-strategy Markdown reports
detailedAnalysis/       Individual-ticker analysis workflow
instructions/           Prompt and analysis instructions
run_detailed_analysis.py Recommendation filtering and batch runner
run_entry_strategy.py   Analysis-report entry-strategy batch runner
run_hold_strategy.py    Organizer-stock hold-strategy batch runner
Dockerfile              Analysis/Codex image
Dockerfile.api          Lightweight FastAPI image
Dockerfile.chat         Optional standalone Codex chat API image
docker-compose.yml      Analysis and API services
```

## Detailed-analysis sandbox preflight and rollout status

Detailed analysis checks Codex, the selected horizon instructions, and local
feature guides through the actual read-only sandbox **before** fetching data or
clearing reports. Each supplied catalogued feature must also have a readable
matching card; uncatalogued features retain the prompt's interpretation limits.
Direct individual calls preflight too; batch calls pass the successful check to
each ticker. Diagnose either horizon without model tokens:

```bash
docker compose run --rm --no-deps agentic-stock-analysis \
  python -m detailedAnalysis.preflight --forecast-window 5
docker compose run --rm --no-deps agentic-stock-analysis \
  python -m detailedAnalysis.preflight --forecast-window 10
```

The image installs distribution `bubblewrap` and `ripgrep`, following
[official sandbox prerequisites](https://learn.chatgpt.com/docs/sandboxing#prerequisites).
The pinned Codex 0.146.0 Linux diagnostic syntax is `codex sandbox -- <command>`;
there is no `linux` subcommand. The diagnostic uses a temporary unauthenticated
Codex home because this command does not support `--ignore-user-config`.
Report generation preserves the existing authentication home, skips personal
configuration/rules, disables plugins, and explicitly sets read-only sandboxing,
never approvals, search, medium reasoning, and `gpt-5.6-sol`. Project
`.codex/config.toml` files are rejected rather than allowed to introduce MCP
servers or hooks. The asynchronous chat runner keeps its independent MCP setup.

Runtime investigation on 2026-10-10 used Docker Desktop 4.47.0, Engine 28.4.0,
Linux arm64, Codex 0.146.0, Debian trixie bubblewrap 0.12.0 and ripgrep 14.1.1.
Default Docker seccomp denied namespace creation despite enabled user namespaces
(`/proc/sys/user/max_user_namespaces=31325`). The analysis service alone now uses
`docker/analysis-seccomp.json`, derived from Docker's
[default profile](https://github.com/moby/profiles/blob/main/seccomp/default.json)
(original SHA-256 `6416b47770785a41ac59073cdc77d9fe98517df2799dc83ef207e622de3053f6`).
The added allow rules cover `clone` only with `CLONE_NEWUSER`, plus `unshare`,
`setns`, `mount`, `umount2`, and `pivot_root`. Removing each exception from the initially working bundled-helper profile was
tested; each removal prevented the smoke command from succeeding. Docker capabilities are
unchanged and seccomp continues filtering other syscalls.

The distribution bubblewrap also needs Docker system-path masks removed: a
syscall trace showed `mount("proc", ...) = EPERM` even in seccomp-unconfined
diagnostic containers. A disposable test passed with those masks removed. The
operator explicitly approved the analysis-only `systempaths=unconfined` setting,
which is now enabled in default Compose together with the scoped seccomp profile.
It removes Docker's default system-path masking and read-only restrictions,
increasing exposure of kernel interfaces inside the container. It adds no
capabilities, host namespaces, or privileged mode; Codex remains read-only.
API and assistant services retain their existing security settings. The optional
`docker-compose.sandbox-runtime.yml` also declares the approved settings, but it
is no longer needed for the standard analysis command.

Both actual Compose sandbox preflights passed after approval. To run a batch:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 5
docker compose run --rm agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 10
```

On an unsupported runtime, preflight still returns nonzero before clearing
reports or requesting data. Do not switch to danger-full-access or change macOS
sysctls to work around Linux namespace failure. Other hosts may need a host
AppArmor profile; investigate the Linux host's policy separately.

For a Linux server reporting `bwrap: Failed to make / slave: Permission denied`,
AppArmor may be blocking bubblewrap's mount setup even with the seccomp and
system-path settings above. Test the checked-in, analysis-only override:

```bash
sudo docker compose \
  -f docker-compose.yml \
  -f docker-compose.apparmor-diagnostic.yml \
  run --rm --no-deps agentic-stock-analysis \
  python -m detailedAnalysis.preflight --forecast-window 10
```

`docker compose run` does not accept `--security-opt`; runtime security settings
must be declared in the Compose configuration. This override disables AppArmor
confinement for the analysis container, increasing its access beyond the default
AppArmor policy. The custom seccomp profile and Codex read-only sandbox remain
enabled. API and assistant services are unaffected. For a stricter permanent
deployment, use a host-loaded custom AppArmor profile allowing the required
sandbox operations; see [Docker's AppArmor documentation](https://docs.docker.com/engine/security/apparmor/).

If preflight passes, run the batch using the same override:

```bash
sudo docker compose \
  -f docker-compose.yml \
  -f docker-compose.apparmor-diagnostic.yml \
  run --rm --no-deps agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 10
```

Use `--forecast-window 5` to check or run the other horizon. New containers pick
up the override without an image rebuild or Docker daemon restart. Omitting the
override file restores the base Compose AppArmor behavior for subsequent runs.
If preflight still fails, inspect policy denials on the Docker host:

```bash
sudo journalctl -k --since "10 minutes ago" --no-pager |
  grep -Ei 'apparmor|denied|bwrap|userns|seccomp'
```

Also collect the model-free container diagnostics, rebuilding first to include
the diagnostic module:

```bash
sudo docker compose -f docker-compose.yml build agentic-stock-analysis
sudo docker compose \
  -f docker-compose.yml \
  -f docker-compose.apparmor-diagnostic.yml \
  run --rm --no-deps agentic-stock-analysis \
  python -m detailedAnalysis.sandbox_diagnostics
```

The JSON output includes the process AppArmor profile, seccomp filter count,
effective capabilities, namespace sysctls, and bounded stdout/stderr from static
version, user-namespace, bubblewrap, and Codex sandbox probes. It prints no
environment variables, invokes no model, and does not clear reports. Exit status
is nonzero when the Codex sandbox smoke command fails. This is a runtime
diagnostic; a passing smoke command does not replace the reference preflight.

If the process profile is still confined, verify that the deployed override is
being applied. If it is `unconfined` but mounting still fails, inspect host logs
and the Docker daemon's security options rather than assuming AppArmor was the
only blocker:

```bash
sudo docker info --format '{{json .SecurityOptions}}'
systemd-detect-virt
```

The override cannot bypass an outer container runtime or provider's restrictions.
An orphan-container warning is unrelated to sandbox initialization.

On Ubuntu, `apparmor=unconfined` does not necessarily exempt a process from
`kernel.apparmor_restrict_unprivileged_userns=1`. Enabled user namespaces plus
`unshare: write failed /proc/self/uid_map: Operation not permitted`,
`bwrap: setting up uid map: Permission denied`, or a loopback `RTM_NEWADDR`
denial point to restrictions on capabilities inside the new namespace.
Confirm AppArmor denials using the host kernel logs above. Ubuntu supports a
named profile with explicit `userns` permission; see
[Ubuntu's user-namespace policy explanation](https://discourse.ubuntu.com/t/understanding-apparmor-user-namespace-restriction/58007).

The checked-in compatibility profile uses AppArmor 4 syntax and broad
`default_allow` permissions with explicit `userns` permission. It scopes the
exception to containers assigned this profile; it is not a restrictive AppArmor
filesystem or network policy. It does not add Docker capabilities or turn off
seccomp or Codex sandboxing, and does not change the host-wide sysctl.
Install and load it on the **Docker daemon host**, from the project directory:

```bash
sudo install -m 0644 docker/analysis-apparmor-userns \
  /etc/apparmor.d/agentic-stock-analysis-userns
sudo apparmor_parser -r /etc/apparmor.d/agentic-stock-analysis-userns
sudo docker compose \
  -f docker-compose.yml \
  -f docker-compose.apparmor-userns.yml \
  run --rm --no-deps agentic-stock-analysis \
  python -m detailedAnalysis.preflight --forecast-window 10
```

Use this override **instead of** `docker-compose.apparmor-diagnostic.yml`;
do not combine conflicting AppArmor options. If preflight passes, run:

```bash
sudo docker compose \
  -f docker-compose.yml \
  -f docker-compose.apparmor-userns.yml \
  run --rm --no-deps agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 10
```

No rebuild is required for this host-profile/Compose change. If loading the
profile or preflight fails, retain the error and inspect the host logs; the
profile must be validated on the target host. To remove it, first stop containers
using it, then unload and remove the profile:

```bash
sudo apparmor_parser -R /etc/apparmor.d/agentic-stock-analysis-userns
sudo rm /etc/apparmor.d/agentic-stock-analysis-userns
```

Controlled AALI real-report verification passed for both horizons with the
existing authenticated volume and its stale `localhost:8003/mcp` configuration:

| Horizon | Published report | Bytes | Web searches | MCP tool calls |
| --- | --- | ---: | ---: | ---: |
| 5 sessions | `detailedAnalysisResults/verification/5dd/AALI.md` | 34,226 | 11 | 0 |
| 10 sessions | `detailedAnalysisResults/verification/10dd/AALI.md` | 36,869 | 8 | 0 |

Both runs emitted completed turns, exited zero, and published nonempty reports.
Recorded successful command events include guide/index reads for both horizons
and feature-card reads for ten sessions; the five-session run also read batches
resolved through the feature index. Neither stderr nor the published reports
contained the tested infrastructure-failure signatures. Sanitized event summaries
are saved beside the reports as `verification.json`. Existing rolling-window
reports were not cleared. These are execution checks, not proof that the model
interpreted every card or produced financially correct conclusions.

`CODEX_PREFLIGHT_TIMEOUT_SECONDS` defaults to 20.
`CODEX_GENERATION_TIMEOUT_SECONDS` defaults to 900 and applies to the shared
synchronous runner (detailed, entry, hold); it is separate from API HTTP timeouts.
Timeouts kill and reap the process group. Structured events and stderr have a
4 MiB capture limit each; reports have a 4 MiB limit. A completed turn, zero exit,
and nonempty final output are required before atomic per-report replacement.
Unrecoverable error/turn-failed events and narrow bubblewrap/sandbox diagnostic
matches reject fallback responses. A failed infrastructure command is considered
recovered only after a successful retry of the same command. Ordinary nonzero
shell exits are permitted. Event fields were checked against the official
`@openai/codex-sdk@0.146.0` types and
[documented JSONL events](https://learn.chatgpt.com/docs/non-interactive-mode#make-output-machine-readable).
Diagnostic matching is deliberately limited; it cannot prove every card was read
or validate financial conclusions. User-facing diagnostics disclose only bounded
allowlisted failure categories, never raw prompts, payloads or stderr.
Per-report atomic publication does not preserve an entire prior rolling window
if a later generation fails after successful preflight and batch cleanup.

## Container Codex authentication and port migration

Fresh volumes import only `/host-codex/auth.json`, with mode 0600, when no volume
credentials exist. No personal config, plugins, history, or other state is copied.
Existing `auth.json` and unrelated files remain untouched. This supports Codex's
file credential store; a host keychain-only login is not portable into Linux.
Use a file-backed login or `OPENAI_API_KEY` (mapped to `CODEX_API_KEY` without
printing it). Explicit `CODEX_API_KEY` takes precedence. Authentication should be
kept in the persistent volume so refreshed tokens survive container runs.

There is no need to delete an existing volume or log in again solely because it
contains old settings: synchronous generation ignores its `config.toml` and the
chat runner supplies its own MCP endpoint. Optional targeted migration: back up
and rename only `/root/.codex/config.toml` to `config.toml.personal-backup` inside
the named volume. Leave `auth.json` and all unrelated state intact.

REST uses host `http://localhost:8003`; MCP uses host
`http://localhost:8004/mcp`. Inside Compose, chat uses
`http://agentic-mcp:8000/mcp`. `localhost:8003/mcp` is neither the published MCP
port nor the correct address inside a container. Report generation needs no
report MCP service.
