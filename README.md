# agentic-stock-analysis

agentic-stock-analysis generates short-term stock-analysis reports and exposes
the generated reports through a small FastAPI service.

The analysis workflow:

1. Fetches daily ticker recommendations from a configured HTTP endpoint.
2. Selects recommendations whose score is above `MINIMUM_SCORE`.
3. Fetches technical data for each selected ticker.
4. Uses the Codex CLI and the instructions in `instructions/` to generate a
   Markdown report.
5. Saves each report as `analysisResults/{TICKER}.md`.

The FastAPI service reads those Markdown files and provides endpoints for
listing available tickers and retrieving an individual report.

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

Edit `.env` and provide the URLs used by the analysis workflow:

```dotenv
BASE_URL=http://your-data-api:8000
TECHNICAL_URL=${BASE_URL}/technical
RECOMMENDATION_URL=${BASE_URL}/analytics/daily_recommendations?rolling_window=10dd

INSTRUCTIONS_PATH=instructions/stock-upside-analysis-instructions.md
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

This command retrieves the recommendation list, analyzes every ticker with a
score above `MINIMUM_SCORE`, and writes the resulting Markdown files to the
local `analysisResults/` directory.

To analyze one ticker directly:

```bash
docker compose run --rm agentic-stock-analysis python -m detailedAnalysis.main SMRA
```

Replace `SMRA` with the required ticker. Existing files with the same ticker
name are replaced by the newly generated report.

## Host the FastAPI service with Docker

Build and start the API in the background:

```bash
docker compose up --build -d initialize-fastapi
```

The API is then available at `http://localhost:8003`.

Available endpoints:

```text
GET /analysis
GET /analysis/report?ticker=SMRA
GET /docs
```

Example requests:

```bash
curl http://localhost:8003/analysis
curl "http://localhost:8003/analysis/report?ticker=SMRA"
```

The first request lists all Markdown reports currently present in
`analysisResults/`. The second returns the full report for the requested
ticker.

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
detailedAnalysis/       Individual-ticker analysis workflow
instructions/           Prompt and analysis instructions
run_detailed_analysis.py Recommendation filtering and batch runner
Dockerfile              Analysis/Codex image
Dockerfile.api          Lightweight FastAPI image
docker-compose.yml      Analysis and API services
```
