# agentic-stock-analysis

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
   `analysisResults/{ROLLING_WINDOW}/{TICKER}.md`.

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
BASE_URL=http://your-data-api:8000

OUTPUT_DIR=analysisResults
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
BASE_URL=http://host.docker.internal:8000
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
recommendation endpoint URLs are derived from `BASE_URL`.

This command retrieves the recommendation list, analyzes every ticker with a
score above `MINIMUM_SCORE` (or the top four scores when fewer qualify), and
writes the resulting Markdown files to either the local `analysisResults/5dd/`
or `analysisResults/10dd/` directory. A run clears and replaces reports only
inside its selected rolling-window directory; reports for the other window are
preserved.

Existing files with the same ticker name are replaced by newly generated
reports.

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
GET /docs
MCP /mcp
```

Example requests:

```bash
curl "http://localhost:8003/analysis?rolling_window=5dd"
curl "http://localhost:8003/analysis/report?ticker=SMRA&rolling_window=5dd"
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

### Connect an MCP client

The same container exposes a stateless Streamable HTTP MCP server:

```text
http://localhost:8003/mcp
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
  --url http://localhost:8003/mcp
```

The MCP endpoint does not currently require authentication. Keep it on a
trusted private network or add authentication at a reverse proxy before
exposing it publicly.

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

The reports remain on the host because `analysisResults/` is bind-mounted into
both containers. The analysis container has write access, while the API
container mounts the directory read-only.

## Project structure

```text
app/                    FastAPI router, controller, service, repository, models
analysisResults/        Generated Markdown reports
data/                   CSV-backed ticker portfolio
detailedAnalysis/       Individual-ticker analysis workflow
instructions/           Prompt and analysis instructions
run_detailed_analysis.py Recommendation filtering and batch runner
Dockerfile              Analysis/Codex image
Dockerfile.api          Lightweight FastAPI image
docker-compose.yml      Analysis and API services
```
