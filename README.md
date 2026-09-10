# Agentic Stock Analysis

agentic-stock-analysis generates short-term stock-analysis reports and exposes
the generated reports through a small FastAPI service.

The analysis workflow:

1. Fetches daily ticker recommendations from a configured HTTP endpoint.
2. Selects recommendations whose score is above `MINIMUM_SCORE`; when fewer
   than four qualify, selects the four highest-scoring recommendations instead.
   It then includes tickers returned by the Organizer stocks API and removes
   duplicates.
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
MINIMUM_SCORE=0.5
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

The default forecast window is `10-20` trading days. Choose either supported
window explicitly with:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 5-10

docker compose run --rm agentic-stock-analysis \
  python run_detailed_analysis.py --forecast-window 10-20
```

The `5-10` mode uses
`instructions/stock-upside-analysis-5-10-instructions.md` and requests the
recommendation API's `5dd` rolling window. The `10-20` mode uses
`instructions/stock-upside-analysis-10-20-instructions.md` and requests `10dd`.
These are the only accepted forecast-window values. Technical and
recommendation and technical endpoint URLs are derived from `ML_BASE_URL`.

This command retrieves the recommendation lists for both rolling windows and
selects up to four ML recommendations for each. When fewer than four scores are
above `MINIMUM_SCORE`, lower-scoring recommendations backfill the remaining
slots. A ticker recommended in both windows is assigned only to the window with
the higher score; equal scores are assigned to `10dd`. The other window then
continues down its ranked list so it can still select four unique tickers when
enough candidates are available.

Only the requested window is analyzed. Results are written to either the local
`detailedAnalysisResults/5dd/` or `detailedAnalysisResults/10dd/` directory. A
run clears and replaces reports only inside its selected rolling-window
directory; reports for the other window are preserved.

Existing files with the same ticker name are replaced by newly generated
reports.

Detailed analysis merges the selected ML tickers from the recommendation endpoint on
`ML_BASE_URL` and `GET /stocks?trading_window=5dd|10dd` on
`ORGANIZER_BASE_URL`.
Organizer stocks are additional to the four-ML-recommendation quota. Duplicate
tickers within the requested window are analyzed only once.
The stocks endpoint may return a ticker-only JSON array such as `["BNBR"]`.

## Generate entry strategies with Docker

Generate strategies from the analysis reports in the matching rolling window:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_entry_strategy.py --forecast-window 5-10

docker compose run --rm agentic-stock-analysis \
  python run_entry_strategy.py --forecast-window 10-20
```

The runner reads every Markdown file from `detailedAnalysisResults/5dd/` or
`detailedAnalysisResults/10dd/`, applies the matching instruction in `instructions/`,
and writes the result to `entryStrategyResults/5dd/` or
`entryStrategyResults/10dd/`. It clears and replaces files only in the selected
entry-strategy window. Run detailed analysis first when no source reports exist.

## Generate hold strategies with Docker

Hold-strategy tickers are retrieved from `GET /stocks` on
`ORGANIZER_BASE_URL`, using
`trading_window=5dd` or `trading_window=10dd`. When the response supplies a
stock price, it is passed as the position's average acquisition price. The
matching detailed-analysis report provides the market thesis and risk levels.

Use the existing analysis service and override its command:

```bash
docker compose run --rm agentic-stock-analysis \
  python run_hold_strategy.py --forecast-window 5-10

docker compose run --rm agentic-stock-analysis \
  python run_hold_strategy.py --forecast-window 10-20
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
  `5dd` for 5-10 trading days and `10dd` for 10-20 trading days.

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
