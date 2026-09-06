# Agentic Stock Analysis

agentic-stock-analysis generates short-term stock-analysis reports and exposes
the generated reports through a small FastAPI service.

The analysis workflow:

1. Fetches daily ticker recommendations from a configured HTTP endpoint.
2. Selects recommendations whose score is above `MINIMUM_SCORE`; when fewer
   than four qualify, selects the four highest-scoring recommendations instead.
   It then includes tickers from `data/portfolio.csv` and removes duplicates.
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
```

`OPENAI_API_KEY` can remain empty when the host already has an authenticated
Codex configuration in `~/.codex`. Docker Compose mounts that configuration
read-only and copies it into the persistent `codex-home` volume when needed.

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

This command retrieves the recommendation list, analyzes every ticker with a
score above `MINIMUM_SCORE` (or the top four scores when fewer qualify), and
writes the resulting Markdown files to either the local `detailedAnalysisResults/5dd/`
or `detailedAnalysisResults/10dd/` directory. A run clears and replaces reports only
inside its selected rolling-window directory; reports for the other window are
preserved.

Existing files with the same ticker name are replaced by newly generated
reports.

Detailed analysis merges tickers from the recommendation endpoint on
`ML_BASE_URL` and `GET /stocks?trading_window=5dd|10dd` on
`ORGANIZER_BASE_URL`.
Duplicate tickers are analyzed only once.
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
docker compose up --build -d mcp-server
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
- `list_portfolio` lists all ticker/price pairs in the portfolio.
- `add_portfolio_ticker` adds a `ticker`, positive `price`, and `rolling_window`.
- `modify_portfolio_ticker` changes the price for a ticker in a specified
  rolling window.
- `delete_portfolio_ticker` removes a ticker from a specified rolling window.

Portfolio data is stored in `data/portfolio.csv` with exactly the columns
`ticker,price,rolling_window`. The rolling window must be `5dd` or `10dd`, and
the same ticker may be stored once in each window. Tickers are normalized to
uppercase. Batch analysis includes only portfolio rows matching the selected
forecast window. In Docker, the `data/` directory is bind-mounted so changes
survive container recreation. Set `PORTFOLIO_CSV_PATH` to use a different path
when running locally.

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

## Project structure

```text
app/                    FastAPI router, controller, service, repository, models
detailedAnalysisResults/        Generated Markdown reports
entryStrategy/          Individual-ticker entry-strategy workflow
entryStrategyResults/   Generated entry-strategy Markdown reports
holdStrategy/           Individual-position hold-strategy workflow
holdStrategyResults/    Generated hold-strategy Markdown reports
data/                   CSV-backed ticker portfolio
detailedAnalysis/       Individual-ticker analysis workflow
instructions/           Prompt and analysis instructions
run_detailed_analysis.py Recommendation filtering and batch runner
run_entry_strategy.py   Analysis-report entry-strategy batch runner
run_hold_strategy.py    Portfolio hold-strategy batch runner
Dockerfile              Analysis/Codex image
Dockerfile.api          Lightweight FastAPI image
docker-compose.yml      Analysis and API services
```
