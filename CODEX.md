# Stock Trading LLM Wiki Schema

## Purpose

Maintain a persistent Markdown wiki for evidence-based stock-trading analysis across two distinct forecast horizons:

- `5dd`: 5–10 trading sessions
- `10dd`: 10–20 trading sessions

The wiki compiles the generated detailed analyses, entry strategies, and hold strategies into an interlinked knowledge base. It must preserve source lineage, dates, uncertainty, and the separation between the two horizons. It supports research and decision review; it must never turn a conditional setup into a claim that a trade was executed.

## Three-layer architecture

### 1. Raw and governing sources — read only

Never edit, rename, move, or delete these files while maintaining the wiki.

| Source | Path | Role |
|---|---|---|
| Detailed analyses | `detailedAnalysisResults/{5dd,10dd}/{TICKER}.md` | Primary analytical source: supplied technical data, cited news, scenarios, catalysts, risks, levels, and final judgment |
| Entry strategies | `entryStrategyResults/{5dd,10dd}/{TICKER}.md` | Derived plan for a possible new position |
| Hold strategies | `holdStrategyResults/{5dd,10dd}/{TICKER}.md` | Derived plan for an existing position |
| Analysis instructions | `instructions/stock-upside-analysis-{5-10,10-20}-instructions.md` | Rules under which detailed analyses were generated |
| Entry instructions | `instructions/stock-entry-strategy-{5-10,10-20}-instructions.md` | Rules under which entry strategies were generated |
| Hold instructions | `instructions/stock-hold-strategy-{5-10,10-20}-instructions.md` | Rules under which hold strategies were generated |
| Wiki design reference | `llm-wiki/llm-wiki.md` | Architectural reference for this persistent wiki |

The application may replace result files during its normal generation workflows. “Read only” means the wiki maintainer never changes them; they remain the authoritative snapshots from which wiki pages are derived.

### 2. Generated wiki — Codex maintained

Store all generated wiki content under `wiki/`. Codex may create and update files there according to this schema. The user normally reads these pages; Codex maintains them.

```text
wiki/
├── index.md
├── log.md
├── dashboard.md
├── stocks/
│   └── {TICKER}.md
├── windows/
│   ├── 5-10/
│   │   └── {TICKER}.md
│   └── 10-20/
│       └── {TICKER}.md
├── themes/
│   └── {theme-slug}.md
├── comparisons/
│   └── {comparison-slug}.md
├── methodology/
│   ├── source-model.md
│   ├── 5-10-trading-sessions.md
│   └── 10-20-trading-sessions.md
└── sources/
    └── {source-id}.md
```

Create directories only when they have content. Do not create empty placeholder pages.

### 3. Schema — this file

This file controls how Codex ingests, queries, and maintains the wiki. Update it when the domain, source layout, or desired workflows change. Record material schema changes in `wiki/log.md`.

## Source model and authority

### Lineage

For one ticker and one horizon, use this dependency chain:

```text
detailed analysis ──> entry strategy
                  └─> hold strategy
```

Entry and hold strategies are derived from the detailed analysis. They are not independent confirmation of its evidence. Never increase confidence because the analysis and its derived strategy repeat the same thesis, news, indicator, target, or risk.

### Authority order

When claims conflict, apply this order within the same ticker, horizon, and analytical snapshot:

1. The detailed analysis controls facts, supplied technical observations, news citations, scenarios, and analytical levels.
2. The entry strategy controls only its derived entry-plan fields and setup state.
3. The hold strategy controls only its derived existing-position decision and management fields.
4. A wiki synthesis is interpretation and never overrides a source.

The governing instruction files explain how a source was produced. They do not prove that the generated report followed every instruction; inspect the actual report and record material deviations.

### Time and horizon boundaries

- Treat every result as an `as_of` snapshot, not as a timeless fact.
- Keep `5dd` and `10dd` separate even when they cover the same ticker.
- Never copy a level, scenario probability, trigger, stop, or conclusion from one horizon into the other unless a source explicitly supports it there.
- Do not describe a setup as currently actionable after its source window ends or its data becomes stale. Retain it as historical knowledge and label it `expired` or `superseded`.
- When newer source files replace older ones, preserve the prior wiki claim in Git history and update the page to the newest snapshot. Note material thesis changes in the page and log.
- Distinguish analysis time, news cut-off, technical-data cut-off, forecast start, and forecast end. Do not collapse them into one date.

### Evidence classes

Label material claims as one of:

- **Provided technical data** — price, OHLCV, indicators, flow fields, and levels derived from the dataset embedded in the detailed analysis.
- **Reported news** — a claim supported by a link in the detailed analysis.
- **Source calculation** — a calculation already made in a source report.
- **Wiki calculation** — a reproducible calculation made during synthesis; show the inputs and formula.
- **Source judgment** — a conclusion or recommendation stated in a source.
- **Wiki synthesis** — a cross-source interpretation made by the wiki maintainer.
- **Unknown / not estimable** — evidence is missing, ambiguous, stale, or contradictory.

Never upgrade an estimate, scenario, rumor, or inference into a fact.

## File conventions

### Naming

- Ticker filenames use uppercase, for example `stocks/DEWA.md`.
- Horizon pages use `windows/5-10/{TICKER}.md` and `windows/10-20/{TICKER}.md`.
- Other filenames use lowercase kebab-case.
- Use relative Markdown links so the wiki works locally and in Obsidian.
- Prefer descriptive links: `[DEWA 5–10 session view](../windows/5-10/DEWA.md)`.

### Source identifiers

Use stable identifiers in this form:

```text
analysis:{window}:{ticker}
entry:{window}:{ticker}
hold:{window}:{ticker}
instruction:{artifact}:{window}
```

Examples:

```text
analysis:5dd:DEWA
entry:10dd:BSDE
hold:5dd:RMKE
instruction:entry:10dd
```

### Common frontmatter

Every generated page except `index.md` and `log.md` begins with YAML frontmatter. Omit unknown optional values rather than inventing them.

```yaml
---
title: "..."
page_type: stock | horizon-view | theme | comparison | methodology | source
status: current | stale | expired | superseded | incomplete
tickers: [DEWA]
window: 5dd | 10dd | cross-window | none
analysis_timestamp: "YYYY-MM-DDTHH:MM:SS+07:00"
technical_cutoff: "YYYY-MM-DD"
news_cutoff: "YYYY-MM-DDTHH:MM:SS+07:00"
forecast_end: "YYYY-MM-DD"
source_ids:
  - analysis:5dd:DEWA
source_paths:
  - detailedAnalysisResults/5dd/DEWA.md
updated: "YYYY-MM-DD"
tags: [stock, indonesia, 5dd]
---
```

Use ISO dates in metadata. Preserve the source timezone; for these reports it will commonly be `Asia/Jakarta` / WIB (`+07:00`).

### Inline provenance

Every material number, factual claim, recommendation, or state must be traceable. Cite local sources with a relative link and a concise locator, for example:

```markdown
The supplied reference close was IDR 370 on 2026-09-16
([analysis:5dd:DEWA](../../detailedAnalysisResults/5dd/DEWA.md), §1–3).
```

For reported news, link to the detailed analysis and preserve its original external citation when the claim matters to the synthesis. Do not imply that the wiki independently reverified the link unless it actually did.

## Page schemas

### `wiki/index.md`

This is the content catalog and first navigation point. Keep it concise and update it on every ingest.

Required sections:

1. `# Stock Trading Analysis Wiki`
2. `## Current dashboard` — link to `dashboard.md` and state its as-of date.
3. `## Stocks` — ticker, available windows, latest technical cut-off, current/stale status, one-line summary.
4. `## 5–10 trading sessions` — all horizon pages with one-line judgments.
5. `## 10–20 trading sessions` — all horizon pages with one-line judgments.
6. `## Themes and catalysts` — theme pages.
7. `## Comparisons` — saved query/synthesis pages.
8. `## Methodology` — methodology pages.
9. `## Source register` — source-summary pages or grouped source links.

Do not rank stocks in the index unless the ranking has its own dated comparison page and stated method.

### `wiki/dashboard.md`

Provide a dated overview, not a timeless recommendation list.

Required sections:

1. `# Current Dashboard`
2. `## Coverage and freshness` — counts by window and status, latest/oldest cut-offs, missing source types.
3. `## 5–10 session views` — compact table of ticker, source judgment, entry state, hold decision when available, principal trigger, invalidation, forecast end, status.
4. `## 10–20 session views` — the same fields for the wider window.
5. `## Near-term catalysts` — date, ticker/theme, event, expected relevance, source.
6. `## Conflicts and data gaps` — stale data, missing reports, incompatible levels, absent position context, or unresolved evidence.

Use `Not available` for a missing entry or hold strategy. Absence is not a neutral recommendation.

### `wiki/stocks/{TICKER}.md`

This is the cross-window entity page. It compares but does not merge the horizons.

Required sections:

1. `# {TICKER}`
2. `## Current source coverage`
3. `## 5–10 session view`
4. `## 10–20 session view`
5. `## Cross-window agreement and divergence`
6. `## Catalysts and risks`
7. `## What would change the view`
8. `## Data gaps and contradictions`
9. `## Sources`

When only one horizon exists, say so. Cross-window divergence is useful information; do not force consensus.

### `wiki/windows/{5-10,10-20}/{TICKER}.md`

This is the canonical decision-oriented page for one ticker and one horizon.

Required sections:

1. `# {TICKER} — {5–10 | 10–20} Trading Sessions`
2. `## Snapshot` — analysis timestamp, technical/news cut-offs, reference price, forecast window, risk tolerance, status.
3. `## Detailed-analysis view` — final judgment, confidence, bull/base/bear cases, probability-weighted return when defensible.
4. `## Technical and participation evidence` — bullish, bearish, and conflicting evidence.
5. `## News and catalyst evidence` — company, Indonesia, and global factors with dates.
6. `## Levels and risk controls` — confirmation, entry zone, tactical invalidation, structural invalidation, targets, time stop. Use `Not estimable from supplied analysis` where necessary.
7. `## Entry strategy` — current setup state and the two strategy-card outcomes, or `Not available`.
8. `## Hold strategy` — current hold decision and decisive conditions, or `Not available`. Make clear that it applies to an existing position.
9. `## Integrated synthesis` — agreement, conflicts, and the controlling evidence. Do not double-count derived strategy content.
10. `## Data quality and limitations`
11. `## Sources`

Preserve these distinctions:

- An entry order is a plan until execution data proves a fill.
- `Waiting`, `Armed`, `Triggered`, `Active—healthy`, `Active—warning`, `Invalidated`, and `Completed` are state-machine terms. Use a state only when its observable conditions are present in the source snapshot.
- A hold decision concerns an existing position and must not be presented as a new-entry recommendation.
- Tactical and structural invalidation are different. Never silently substitute one for the other.
- Report scenario expected return is not automatically the expected value of a conditional entry setup.

### `wiki/sources/{source-id}.md`

Create one source page for every ingested raw result. Replace colons in filenames with hyphens, for example `analysis-5dd-DEWA.md`.

Required sections:

1. `# {source-id}`
2. `## Source metadata` — path, artifact type, ticker, window, timestamps/cut-offs.
3. `## Key claims` — concise extraction with evidence classes.
4. `## Levels, scenarios, and decisions` — only what the source states.
5. `## Limitations and internal inconsistencies`
6. `## Used by` — backlinks to all wiki pages that rely on it.

Source pages summarize; they never silently repair the raw report.

### Theme and comparison pages

Create a theme page when a catalyst, sector factor, macro event, technical condition, or risk affects at least two ticker/horizon pages or is likely to recur. Examples include Bank Indonesia decisions, coal-market conditions, weak participation, or high-volume distribution.

Every comparison page must state:

- question and purpose;
- as-of date;
- included tickers and horizons;
- freshness and eligibility rules;
- comparison fields and calculation method;
- results;
- uncertainties and non-comparable data;
- source links.

Never compare a current snapshot with an expired one without showing the mismatch. Never rank `Not estimable` values as if they were numeric.

## Ingest workflow

When asked to ingest or refresh sources:

1. Read this file and `wiki/index.md` if it exists.
2. Inventory all relevant result files and identify new, changed, missing, or removed paths. Use content and metadata, not filename alone, to detect a changed analytical snapshot.
3. For each ticker/window, read the detailed analysis first, then its matching entry and hold strategies if present.
4. Verify lineage, ticker, window, timestamps, technical cut-off, reference price, forecast end, and source judgment. Flag mismatches rather than guessing.
5. Extract claims by evidence class. Preserve missing values and stated limitations.
6. Create or update the source page for each ingested artifact.
7. Create or update the matching horizon page.
8. Update the ticker page, showing cross-window agreement or divergence.
9. Update affected theme, comparison, dashboard, and methodology pages.
10. Update `wiki/index.md`.
11. Append one entry to `wiki/log.md`.
12. Run the lint checks below and fix issues that can be resolved from existing sources.

Do not browse the web during ordinary ingestion. The detailed analysis already contains its news research and citations. Browse only when the user explicitly requests a current update or verification; keep newly researched material clearly separate from the raw generated reports and cite it directly.

## Query workflow

When answering a question from this wiki:

1. Read `wiki/index.md`, then open the relevant ticker, horizon, source, theme, or comparison pages.
2. Check the technical cut-off, analysis timestamp, forecast end, and status before using a claim.
3. Prefer current pages whose horizon matches the question.
4. Trace decisive claims back to raw sources when precision matters.
5. Separate source facts, source judgments, and wiki synthesis.
6. State missing or non-comparable evidence explicitly.
7. Cite wiki pages and raw sources with relative links.
8. If the answer adds reusable synthesis, create or update a comparison/theme page and log it when the user asks to file it or when the query is part of wiki maintenance.

For questions asking what to buy, sell, enter, or hold “now,” do not rely on an expired or stale snapshot. State the last supported view and request or generate a refreshed analysis through the project’s normal workflow before giving a current actionable view.

## Maintenance and lint workflow

Periodically check for:

- result files with no source page;
- source pages pointing to missing raw files;
- ticker/window pages not listed in `index.md`;
- pages whose `status` disagrees with their forecast end or freshness;
- claims lacking a source ID or path;
- entry/hold claims incorrectly treated as independent evidence;
- levels copied across horizons;
- tactical and structural stops conflated;
- entry plans described as filled trades;
- hold decisions described as new-entry advice;
- probabilities that do not total 100% where the source provides a complete scenario set;
- stale claims silently presented as current;
- contradictions between detailed analysis and derived strategies;
- orphan pages and missing backlinks;
- duplicate theme pages;
- important recurring concepts that deserve their own page;
- source changes not recorded in `log.md`.

Do not resolve a contradiction by choosing the more bullish or newer-looking statement without evidence. Record the conflict, identify the controlling source under the authority rules, and state what refresh would settle it.

## Log format

`wiki/log.md` is append only. Never rewrite or reorder prior entries except to fix an obvious formatting error. Use one of these prefixes:

```markdown
## [YYYY-MM-DD] ingest | {scope}
## [YYYY-MM-DD] refresh | {scope}
## [YYYY-MM-DD] query | {title}
## [YYYY-MM-DD] lint | {scope}
## [YYYY-MM-DD] schema | {change}
```

Each entry states:

- source paths read or changed;
- wiki pages created or updated;
- key thesis changes;
- contradictions or gaps found;
- unresolved follow-up work.

## Editing and safety rules

- Modify only `wiki/` and this schema during wiki maintenance unless the user explicitly asks for application or source changes.
- Preserve user-written content inside `wiki/`; integrate around it or ask when authorship is unclear.
- Do not fabricate prices, indicator values, targets, probabilities, position size, acquisition price, transaction costs, dates, fills, or citations.
- Do not calculate portfolio-level profit/loss without the required position inputs.
- Show formulas and inputs for new numerical synthesis.
- Keep bullish and bearish evidence visible. A concise page may summarize, but it may not hide material contrary evidence.
- Use `Not available` for a missing artifact and `Not estimable from supplied analysis` for an unsupported value.
- Prefer updating an existing canonical page over creating a near-duplicate.
- Keep the wiki useful in plain Markdown; Obsidian-specific features may be additive but never required for navigation.

## Definition of done

An ingest or refresh is complete only when:

- every in-scope raw result has a source page;
- every in-scope ticker/window has a canonical horizon page;
- each ticker has an updated cross-window page;
- `dashboard.md` and `index.md` reflect the same coverage and status;
- material claims have traceable provenance;
- missing reports and contradictions are visible;
- all affected pages link to each other where relevant;
- a log entry records the operation;
- the lint checks pass or unresolved findings are recorded.
