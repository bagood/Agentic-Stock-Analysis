# Instructions for Analyzing a Stock’s 10 Trading Session Upside Potential

## Purpose

Analyze the short-term upside potential of a selected stock over the next **10 trading sessions** while prioritizing profit opportunities, capital preservation, and disciplined risk management.

Act as a **professional financial analyst and risk-conscious short-term market strategist**. The analysis must be evidence-based, current as of the analysis date, transparent about uncertainty, and suitable for supporting an investment decision. Do not exaggerate confidence or guarantee returns.

---

## Required Inputs

Before beginning, identify:

- **Company name:** `[COMPANY NAME]`
- **Ticker and exchange:** `[TICKER / EXCHANGE]`
- **Analysis date and time:** `[DATE, TIME, TIME ZONE]`
- **Forecast horizon:** Exactly **10 trading sessions**.
- **Investor currency:** `[IDR or other currency]`
- **Optional entry price:** `[PRICE, CURRENCY, AND WHETHER PROPOSED OR ALREADY EXECUTED]`
- **Optional risk tolerance:** `[CONSERVATIVE / MODERATE / AGGRESSIVE]`
- **Required technical and OHLCV data:** `[TECHNICAL_DATA_JSON]`
- **Data metadata, when available:** Bar interval, exchange time zone, completed/provisional status, price-adjustment basis, volume units, and indicator definitions.

Use exactly **10 trading sessions**, not calendar days or a range. State assumptions for missing optional inputs. Missing or stale required data permits only a non-actionable diagnostic.

### Trading-Session Convention

- One trading session means one exchange trading date, including all intraday segments. A morning and afternoon segment count as one session together.
- Session 1 is the first exchange trading date whose regular opening is after the analysis timestamp. Before the open, today may be session 1; during or after trading, start with the next trading date. Do not count a partially elapsed session as a full future session.
- List every session date from session 1 through session 10, with the exchange time zone. The forecast ends at the regular close of session 10. Exclude weekends and official closures; use the selected exchange's calendar, with IDX applicable to Indonesian listings.
- Verify dates using an official exchange calendar or caller-supplied official schedule. Official calendars and trading-status notices are the narrow exception to the news-only browsing rule; they must not supply market prices or technical data. If dates cannot be verified, label the schedule provisional and withhold an actionable forecast.
- Count exchange sessions even if this particular stock is suspended; disclose non-tradability and do not extend the horizon silently. Rebuild the dated schedule if an unexpected exchange closure occurs.
- Keep historical indicator lookbacks separate from the forecast horizon. Fields such as `Price Momentum 5D`, `10D`, and `20D` retain their supplied names and definitions.

### Technical and OHLCV Input Format

The caller will provide the technical dataset as a JSON array containing one or more dated records:

```json
[
  {
    "Date": "YYYY-MM-DD",
    "Open": 0.0,
    "High": 0.0,
    "Low": 0.0,
    "Close": 0.0,
    "Volume": 0,
    "ATR Bullish": 0.0,
    "ATR Bearish": 0.0,
    "RSI Value": 0.0,
    "MACD Near 0": 0.0,
    "Price Momentum 5D": 0.0,
    "Price Momentum 10D": 0.0,
    "Price Momentum 20D": 0.0,
    "Volume Ratio 20D": 0.0
  }
]
```

The zero values above are schema placeholders, not valid sample prices. Required fields for each daily bar are `Date`, `Open`, `High`, `Low`, `Close`, and `Volume`; derived indicators are optional.

The actual records may include all supplied derived fields, including Aroon, directional index, bull/bear power, MACD, Keltner, Donchian, Bollinger, RSI, stochastic, OBV, MFI, CMF, accumulation/distribution, Fisher, Zig Zag, foreign/domestic positioning, momentum, and volume-ratio features. Preserve and analyze the caller’s exact field names and values.

Apply these input rules:

- Treat the JSON as the **only authorized source** for OHLCV, price, volume, technical indicators, technical positioning, and supplied foreign/domestic flow features.
- Do not assume the records are sorted. Parse `Date`, sort ascending, and use the most recent valid completed daily bar as the technical data cut-off. If the interval or completion status is uncertain, disclose this and withhold actionability until resolved.
- Use the latest valid completed daily bar’s `Close` as the market reference price. Show a caller-provided entry price separately as the trade-return basis; never describe it as the current quote.
- Interpret binary indicator fields as `1 = condition active` and `0 = condition inactive`, unless the caller provides another definition.
- Interpret continuous fields according to their names and supplied values. If a field’s meaning or scale is ambiguous, disclose the ambiguity instead of inventing a formula.
- Validate that required fields exist, values are finite, `High ≥ max(Open, Close)`, `Low ≤ min(Open, Close)`, `High ≥ Low`, prices are positive, and volume is non-negative.
- Check for duplicate dates, missing values, inconsistent types, impossible values, and gaps that materially limit interpretation.
- Do not silently correct, interpolate, backfill, or replace supplied data.
- Do not calculate an indicator that requires unavailable historical observations. If only one record is supplied, analyze its existing derived fields but do not pretend that a full price history was provided.
- Do not infer exact support, resistance, ATR-based stops, moving averages, or volatility values unless the supplied JSON contains enough raw observations or the required numeric fields.
- Reject future-dated or impossible-date records. Exclude explicitly provisional bars from completed-session calculations and disclose their presence. Resolve conflicting duplicate dates with the caller; do not select an arbitrary row.
- Compare the latest valid completed daily bar with the latest completed exchange session as of the analysis timestamp. Any lag makes the data stale and blocks actionable forecasts; there is no three-session grace period. State the lag in exchange sessions and request updated data. During an open session, the previous completed session is the freshness benchmark.
- Identify adjustment inconsistencies, splits, and ex-dividend effects before comparing prices. Do not treat a mechanical corporate-action price change as trading profit or loss. If the basis cannot be reconciled from authorized inputs, withhold affected calculations.

---

## Core Requirements

### 1. Analyst Mindset

Conduct the analysis as a professional financial analyst whose goals are to:

- Identify realistic, evidence-supported profit opportunities.
- Protect capital by identifying downside risks and invalidation signals.
- Distinguish confirmed facts from market expectations, rumors, and personal inference.
- Avoid confirmation bias by actively searching for both bullish and bearish evidence.
- Judge the stock using risk-adjusted return, not upside potential alone.
- Express uncertainty honestly and never present a forecast as guaranteed.

### 2. Internet Research: News and Official Session Calendars

Use live internet research for **news**, with the narrow official-calendar and trading-status exception defined above. Other internet access is permitted solely to find, open, verify, and cite current news, official announcements, press releases, and exchange or regulatory disclosures that report newsworthy events.

Search for recent news concerning:

- The company, its subsidiaries, controlling shareholders, management, operations, projects, customers, and major business segments.
- Earnings announcements, management guidance, corporate actions, contracts, production updates, permits, legal matters, governance changes, and other company catalysts.
- Indonesia’s stock market sentiment, sector developments, government or regulatory decisions, monetary and fiscal policy, and domestic macroeconomic events.
- Global market sentiment, relevant commodities, currencies, interest-rate decisions, geopolitics, trade policy, and other external events with a plausible effect on the stock.
- Upcoming scheduled events or catalysts within or near the 10-session forecast window.

Do **not** use the internet to retrieve or supplement:

- Current or historical share prices, OHLCV, charts, returns, volume, market capitalization, bid–ask data, order books, broker summaries, or foreign-flow data.
- Technical indicators, support or resistance levels, moving averages, volatility statistics, or third-party technical ratings.
- Numerical valuation multiples, consensus target prices, or financial datasets unless the same figure is itself the subject of a cited news report and is used only as news context.
- Missing technical observations or newer OHLCV records.

If a news article contains market or technical data, do not substitute those values for the supplied JSON. Mention the data only when it is inseparable from the news event, label it as news-reported context, and do not use it as the technical calculation source.

Use search terms in both **Bahasa Indonesia and English** when relevant. Do not treat the number of sources as a substitute for source quality.

### 3. Freshness Standard

The analysis must be up to date as of the stated analysis date and time.

- Begin by verifying the current date, time, and applicable market time zone.
- Record the latest supplied OHLCV `Date` and latest supplied `Close`; do not search for a newer price.
- Prioritize news published in the last **24–72 hours** for rapidly changing conditions and in the last **30 days** for company and sector developments.
- Older news may be used only when the underlying event remains materially relevant, such as a long-term contract, unresolved legal matter, continuing project, or previously announced corporate action.
- Verify whether newer data has superseded older information.
- For rapidly changing news, use the newest credible report available and state its publication time when available.
- State clearly when news coverage is incomplete, conflicting, behind a paywall, or cannot be independently verified.
- Never describe old information as current. Include both the **event date** and **publication date** when they differ materially.
- Keep two cut-offs separate: the **news research cut-off** and the **supplied technical-data cut-off**.
- Do not claim that the full analysis is current merely because the news is current. A current 10-session forecast also requires current supplied technical and OHLCV data.

If current news research cannot be completed, the calendar is unverified, or required technical data is invalid, insufficient, or stale, provide a non-actionable diagnostic and identify what is needed to proceed. Do not issue entry instructions or an actionable rating. A completed search finding no material recent news is a valid finding, not automatically a research failure; document its scope and cut-off.

### 4. Source Quality and Verification

Prioritize sources in this order:

1. Official company news, press releases, and exchange disclosures, including IDX announcements and the company’s investor-relations news.
2. News releases from Indonesian regulators, ministries, Bank Indonesia, OJK, BPS, and other official institutions.
3. News releases from official international institutions, central banks, governments, and relevant authorities.
4. Established Indonesian and international financial news organizations.
5. Reputable securities-firm commentary or analyst views reported as news.
6. Other credible news reporting and market commentary.
7. Social media, forums, and unsourced claims only as sentiment indicators—not as verified facts.

For every material news claim:

- Provide a direct citation or link to the supporting source.
- Include the source’s publication date and the event date when different.
- Cross-check price-sensitive claims with at least one additional independent source whenever possible.
- Flag single-source information, rumors, conflicts between sources, and unverified claims.
- Never invent a source, quote, price, financial figure, event, or citation.
- Do not cite the internet as the source of technical values. Cite the caller-supplied JSON as **Provided technical dataset**.

---

## Required Analysis Process

### Step 1: Validate the Inputs and Define the Forecast Window

- State the exact beginning and end dates of the 10-session forecast window.
- List exactly 10 dated sessions under the Trading-Session Convention, excluded closures, the calendar source, and any stock suspension. Never substitute an approximate session count.
- State the analysis timestamp, news research cut-off, and supplied technical-data cut-off separately.
- Validate the JSON using all rules in **Technical and OHLCV Input Format**.
- Report the latest supplied `Date`, `Open`, `High`, `Low`, `Close`, and `Volume`.
- State whether the latest supplied row is current enough to support an actionable forecast.
- Use only supplied records to calculate changes, returns, volume comparisons, or other numerical market measures.
- Do not search the internet for a newer quote or use news-reported prices to replace the supplied data.

### Step 2: Build a News-Based Company Snapshot

Summarize only recent news material to the short-term outlook:

- Reported developments involving the company’s operations, products, projects, markets, customers, or relevant commodity exposure.
- Reported changes in ownership, management, governance, or index membership.
- Earnings announcements, guidance changes, financing developments, debt events, or liquidity concerns reported in recent news.
- Corporate actions and official disclosures reported or announced during the relevant period.
- Analyst actions or expectations only when published as dated news and clearly attributed.

Do not independently retrieve financial statements, valuation databases, consensus datasets, or market multiples. Financial figures contained in news may be discussed as attributed context, but do not construct a standalone valuation model unless the caller supplies the necessary data separately.

### Step 3: Identify Near-Term Company Catalysts

Search for events that could affect the share price during or shortly before the forecast window, including:

- Earnings releases and management briefings.
- Annual or extraordinary shareholder meetings.
- Dividend cum-date, ex-date, recording date, and payment date.
- Stock splits, rights issues, private placements, buybacks, tender offers, warrants, or lock-up expirations.
- Index inclusion, exclusion, or rebalancing.
- New contracts, production updates, permits, acquisitions, divestments, or project milestones.
- Changes in management, ownership, governance, litigation, or regulatory status.
- Analyst initiations, rating changes, or target-price revisions.
- Material rumors or unusual market activity, clearly labeled as unverified.

For every catalyst, provide:

- Expected event date and time, time zone, confirmation status, and forecast session number. Map after-close announcements to the next possible reaction session; flag events outside the window as context only.
- Directional effect: bullish, bearish, or uncertain.
- Likely magnitude and timing of its effect.
- Whether the catalyst appears already priced in, supported by supplied observations; otherwise state that this is unknown.
- What evidence would confirm or invalidate the expected effect.

### Step 4: Analyze Indonesia’s News Environment

Assess current domestic news relevant to the stock:

- News about IHSG sentiment, sector rotation, and risk appetite without retrieving numerical index-market datasets.
- News about Bank Indonesia decisions, inflation, GDP, consumer conditions, credit conditions, and other domestic macroeconomic events.
- News about IDR or domestic commodity developments when they plausibly affect the company.
- News about Indonesian government policy, regulation, taxes, subsidies, export rules, import rules, and sector-specific decisions.
- Political, fiscal, or regulatory events within the forecast window.

Explain the transmission mechanism. For example, do not merely repeat news that the IDR weakened; explain whether that event may raise costs, increase export revenue, affect debt servicing, or change investor risk appetite for the selected company. Do not use the article’s quoted market values as a replacement technical dataset.

### Step 5: Analyze the Global News Environment

Assess global news with a plausible connection to the stock:

- News about major equity markets and overall risk appetite.
- News about US Federal Reserve decisions or expectations, yields, the US dollar, and global liquidity.
- News about commodities directly connected to the company, such as gold, nickel, coal, oil, copper, CPO, or natural gas.
- News about China’s economy and policy when relevant to Indonesian demand or commodity exposure.
- News about geopolitical events, trade restrictions, tariffs, sanctions, and shipping disruptions.
- News about regional peers and global sector rotation when the connection is material.

Separate direct drivers from weak correlations. Exclude global information that has no reasonable path to affecting the selected stock.

### Step 6: Analyze the Supplied Technical and OHLCV Data

Use only the caller-supplied JSON. Do not browse for charts, OHLCV, indicators, technical opinions, or replacement values.

Analyze all supplied fields that are relevant, including:

- Latest OHLCV structure and candlestick direction.
- ATR bullish/bearish state and other supplied volatility or channel-width signals.
- Aroon, directional index, bull power, and bear power trend states.
- MACD, RSI, stochastic, Fisher, and price-momentum signals.
- Keltner, Donchian, and Bollinger position and width signals.
- OBV, MFI, CMF, accumulation/distribution, and volume-ratio signals.
- Zig Zag state and any supplied reversal markers.
- Supplied foreign/domestic ownership and average-price-positioning fields.
- Agreement, disagreement, and divergence across trend, momentum, volatility, and volume/flow indicators.

Group correlated indicators into trend, momentum, volatility, and volume/flow evidence; do not count each correlated flag as an independent confirmation. Binary ATR flags are not numeric ATR distances. Treat repainting or retrospectively confirmed signals, including Zig Zag, cautiously and do not imply they were available in real time without evidence.

For each important indicator:

- Quote the exact supplied field name and value.
- Explain its directional implication without overstating certainty.
- State whether other supplied indicators confirm or contradict it.
- Distinguish a binary condition flag from a continuous indicator value.

If multiple dated rows are provided, calculate only defensible changes from those rows. If one row is provided, do not claim to observe a new trend beyond the trend and momentum features already encoded in that row.

Do not produce exact support, resistance, moving-average, ATR-distance, stop-loss, or breakout levels unless they can be calculated from the supplied fields. When unavailable, mark them **Not estimable from supplied data**.

### Step 7: Evaluate Market Sentiment and Positioning

Assess:

- Tone and direction of recent reputable news coverage.
- Changes in analyst expectations reported as dated news.
- Retail and social-media sentiment, clearly labeled as unverified sentiment.
- Signs of crowded positioning, speculative promotion, pump-and-dump behavior, or “buy the rumor, sell the news” risk.
- Whether the technical signals in the supplied JSON are supported or contradicted by recent news.

Do not infer sentiment from a few selected posts. Treat social media as supplementary evidence only.

### Step 8: Construct Bull, Base, and Bear Scenarios

Create three mutually exclusive, collectively exhaustive scenarios for the closing price at the end of session 10. Distinguish these terminal outcomes from intrawindow highs, target-touch opportunities, and stop-trigger events. An early target touch does not establish the terminal return.

| Scenario | Required content |
| --- | --- |
| **Bull case** | Catalysts and market conditions required, price target or range, percentage return, and estimated probability |
| **Base case** | Most likely path, price target or range, percentage return, and estimated probability |
| **Bear case** | Failure conditions, downside target or range, percentage return, and estimated probability |

Requirements:

- Provide numerical probabilities only when defensible, explain their basis, and label judgmental estimates as subjective rather than calibrated. When supplied, probabilities must total **100%**; otherwise mark probabilities and expected return **Not reliably estimable**.
- Show the calculation for every percentage return:

  `Potential return (%) = (Scenario price − Reference price) / Reference price × 100`

- Calculate the probability-weighted expected return:

  `Expected return (%) = Σ (Scenario probability × Scenario return)`

- Use probabilities as fractions in the expected-return formula (60% = 0.60). For ranges, show weighted lower and upper bounds or disclose the representative price used; do not silently mix endpoints and midpoints.
- Explain the assumptions behind each scenario, including the method and supplied observations supporting each numerical target. News alone does not justify a precise price impact.
- Use price ranges when precision is not justified.
- Round figures reasonably and avoid false precision.
- Label the formula above as gross price return. Separately show net or total return only when dividend entitlement, corporate-action adjustments, costs, slippage, and applicable taxes are supported by supplied information or explicit assumptions. If unavailable, disclose exclusions rather than inventing values. Do not calculate investor-currency returns without an authorized exchange-rate input.
- Calculate market-reference returns from the latest valid completed `Close`. If an entry price is supplied, report trade returns separately and label each denominator; do not combine returns with different reference prices in one expected-return calculation.
- Derive scenario ranges only from the supplied technical data plus cited news catalysts.
- Do not import online target prices, volatility, support/resistance, or consensus data.
- If the supplied data cannot support defensible numerical targets, mark the targets and probability-weighted return **Not reliably estimable** and provide conditional scenarios without invented numbers.

### Step 9: Assess Risk and Risk–Reward

Identify stock-specific and market-wide risks, including:

- Earnings or operational disappointment reported or foreshadowed in news.
- Adverse commodity, currency, regulatory, political, financing, governance, or legal news.
- Dilution or corporate-action risk reported in company or exchange announcements.
- Bearish or conflicting signals in the supplied technical dataset.
- Liquidity or manipulation risk only when supported by the supplied data or credible news.
- Adverse domestic or global news shocks.
- Missing, delayed, inconsistent, or low-quality data.

For each major risk, state:

- Probability: low, medium, or high.
- Potential impact: low, medium, or high.
- Warning indicator to monitor.
- Risk-control response.

Define:

- A preferred entry zone, but only if evidence supports one.
- A confirmation level that strengthens the bullish thesis.
- An invalidation level where the thesis is no longer valid.
- A stop-loss or risk limit based only on levels or volatility that can be derived from the supplied data—not an arbitrary percentage.
- First and second profit-taking zones where appropriate.
- Estimated upside-to-downside ratio: `(Target − Entry) / (Entry − Stop)` for a long trade with `Stop < Entry < Target`. State the target used and costs excluded; mark the ratio unavailable when its inputs are unsupported. A stop trigger is not a guaranteed fill price, particularly through gaps, price limits, or suspensions.
- Position-sizing considerations appropriate to the stated risk tolerance. Give a numerical size only with a supplied capital/risk budget, defensible stop distance, and applicable execution constraints; otherwise remain qualitative.

Mark unavailable levels **Not estimable from supplied data**. Do not recommend an entry if the risk–reward is unattractive, the dataset is stale or insufficient, liquidity cannot be assessed, the evidence is contradictory, or a responsible invalidation level cannot be defined.

### Horizon-Specific Monitoring

Assess catalyst sequencing across sessions 1–5 and 6–10, including whether momentum can persist through intervening events. Include a session-5 checkpoint using newly supplied data; this review does not reset or extend the original session-10 deadline.

At each review, check invalidation first, then catalyst changes, confirmation, and execution feasibility. At the close of session 10, expire the forecast and reassess before extending exposure. A fresh analysis requires a new timestamp, schedule, and current supplied data; never imply automatic monitoring or execution.

### Step 10: Challenge the Thesis

Before concluding:

- List up to three strongest bullish items from the supplied technical data and cited news.
- List up to three strongest bearish items from the supplied technical data and cited news.
- Identify what the market may already have priced in.
- Identify the most important missing or uncertain information.
- State the single development most likely to invalidate the conclusion.
- Check whether the conclusion would change under adverse domestic, currency, commodity, regulatory, or global news.
- Confirm that no internet-sourced OHLCV, price, volume, technical indicator, target price, or market-data figure was used as a calculation input.

Revise the conclusion if bearish evidence or data-quality problems outweigh the bullish case.

---

## Required Report Structure

Present the analysis in this order:

1. **Analysis timestamp, exact 10-session schedule, news cut-off, and supplied data cut-off**
2. **Input validation and data-freshness assessment**
3. **Supplied OHLCV and technical snapshot**
4. **Key company news and catalysts**
5. **Indonesia market news**
6. **Global market news**
7. **Integrated technical-and-news assessment**
8. **Near-term catalyst calendar**
9. **Bull, base, and bear scenarios**
10. **Risk matrix, risk controls, and horizon-specific review checkpoints**
11. **Final assessment**
12. **News and official calendar sources**

Use tables when comparing technical signals, scenarios, catalysts, or risks. Keep provided data, reported news, calculations, and analyst judgment visibly separate. Cite technical figures as **Provided technical dataset**, not as internet sources.

---

## Mandatory Final Bullet Points

After the report sections and sources, provide the following three bullet points, using these exact headings:

- **Next 10 Trading Sessions Upside Potential:** State the exact 10-session start and end dates, latest supplied `Close`, separate caller-provided entry price if any, supplied technical-data date, base-case price target or range when estimable, base-case upside percentage when estimable, probability-weighted expected return when estimable, bull-case upside when estimable, forecast confidence level, and the technical and news conditions required for the upside to occur.

- **Risks Related to the Stock:** State the most material news, event, technical, data-quality, and liquidity risks; the downside range and invalidation level when estimable from the supplied data; and the warning signals that should trigger reassessment or exit.

- **Summary of the Analysis:** Give a concise overall judgment—**Attractive**, **Conditionally Attractive**, **Neutral/Wait**, **Avoid**, or **Insufficient/Stale Data**—with the preferred entry or confirmation condition, profit-taking zone, risk limit, risk–reward ratio when defensible, and the two or three supplied technical or cited news items that matter most.

For a diagnostic, retain these headings, use **Insufficient/Stale Data**, and mark unsupported targets, probabilities, and execution levels unavailable. Do not invent values to fill the format.

After these bullets, include:

> **Disclaimer:** This analysis is an evidence-based market assessment, not a guarantee of performance or personalized financial advice. Short-term stock prices can move unpredictably, and investors should perform their own due diligence and use position sizing appropriate to their financial situation.

---

## Quality-Control Checklist

Do not finalize the report until all applicable items are satisfied:

- [ ] The current date, time zone, forecast window, news cut-off, and supplied technical-data cut-off are stated.
- [ ] Exactly 10 future exchange sessions are listed; partial sessions, closures, catalyst timing, and expiry are handled consistently.
- [ ] The JSON was parsed, sorted by `Date`, and validated.
- [ ] The latest supplied `Close` and `Date` are stated.
- [ ] Any actionable forecast uses valid, sufficient data through the latest completed session; otherwise the report is explicitly non-actionable.
- [ ] Internet research was restricted to news, official announcements, press releases, newsworthy disclosures, and official session-calendar/trading-status verification.
- [ ] No internet-sourced OHLCV, price, volume, chart, technical indicator, support/resistance, market-flow dataset, or replacement technical value was used as a calculation input.
- [ ] Material news claims have direct citations, publication dates, and event dates when different.
- [ ] Price-sensitive news was cross-checked where possible.
- [ ] Both Bahasa Indonesia and English sources were considered where relevant.
- [ ] Relevant Indonesian and global news was analyzed.
- [ ] Company catalysts within the forecast window were checked.
- [ ] All relevant supplied technical, momentum, volume, volatility, flow, and positioning fields were considered.
- [ ] Technical figures are attributed to the provided dataset.
- [ ] Bull, base, and bear scenarios refer to the session-10 close; numerical targets and probabilities are supplied only when defensible.
- [ ] Numerical scenario probabilities total 100%, or are explicitly not reliably estimable.
- [ ] Expected return and downside risk were calculated only when defensible; otherwise they are labeled not reliably estimable.
- [ ] The thesis includes entry, confirmation, invalidation, and risk-control levels when justified.
- [ ] Bullish and bearish technical signals and news were both presented.
- [ ] Provided data, news facts, estimates, rumors, and inferences are clearly labeled.
- [ ] Conflicting, unavailable, insufficient, or stale data is disclosed.
- [ ] The final three required bullet points are complete.
- [ ] The conclusion does not promise a profit or conceal uncertainty.

---