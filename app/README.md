# Stock analysis API

This package uses a layered request flow:

`router -> controller -> service -> repository -> model`

Run the API from the project root:

```bash
uvicorn app.main:app --reload
```

Available GET endpoints:

- `GET /analysis` lists all tickers represented by Markdown files in
  `analysisResults/`.
- `GET /analysis/report?ticker={ticker}` returns the ticker and full Markdown
  report.

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

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Run with Docker Compose

Build and start only the API service:

```bash
docker compose up --build -d initialize-fastapi
```

The API is available at `http://localhost:8000`. Set `API_PORT` to publish a
different host port, for example:

```bash
API_PORT=8080 docker compose up --build -d initialize-fastapi
```
