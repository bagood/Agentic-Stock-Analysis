# Instructions for Generating a Stock Entry Strategy (10 Trading Sessions)

## Purpose

Convert a completed stock-analysis report into an executable, risk-controlled entry plan within the source report’s fixed window of **10 trading sessions**. Return exactly two ranked strategy cards: **Rank 1** and **Rank 2**. If fewer than two strategies qualify, the Rank 2 card must explain that no second setup qualifies and evaluate the nearest rejected candidate only when the report supports one.

Act as a professional swing-trading strategist. Preserve capital first, optimize risk-adjusted return second, and never imply that profit is guaranteed.

## Required Input

- **Stock-analysis report:** `[ANALYSIS_REPORT]`
- **Analysis/report cut-off:** use the cut-offs stated in the report
- **Trading window:** 10 trading sessions
- **Risk tolerance:** use the report’s value; otherwise assume **Moderate**
- **Strategy preparation timestamp:** `[DATE, TIME, EXCHANGE TIME ZONE]`; verify the current clock or use an explicitly supplied as-of timestamp.
- **Optional position capital:** `[CURRENCY AMOUNT AVAILABLE FOR THIS TRADE]`
- **Optional maximum account risk per trade:** `[CURRENCY AMOUNT, OR PERCENTAGE WITH ACCOUNT EQUITY]`
- **Optional execution inputs:** Supplied tick size, lot size, fees, taxes, slippage allowance, and fill confirmations. These may refine execution or sizing but cannot replace the report’s market analysis.

The report is the sole source for prices, OHLCV, indicators, support/resistance, volatility, flows, scenario probabilities, targets, and risk levels. Do not browse for or invent newer market data. News already cited in the report may be used as context, but do not claim it remains current after the report’s news cut-off.

If the input is not a completed analysis, is invalid or stale, has an expired or mismatched horizon, or lacks enough information to define an entry, invalidation, and attainable target, return **No actionable strategy** inside Rank 1 and retain the required Rank 2 card. State what is missing without inventing a rejected candidate.

### Fixed Trading-Session Window

- Use exactly **10 exchange trading dates**, including all intraday segments as one session per date.
- Inherit session 1 through session 10, their dates, exchange time zone, calendar verification, and final close from the source report. The upstream convention starts with the first regular opening after the analysis timestamp; weekends and official closures are excluded. Do not restart the window at strategy generation, signal confirmation, or entry.
- State the preparation timestamp, report/news/technical cut-offs, dated window, and sessions remaining inside each card. If the report lacks a verified schedule or still uses a range/calendar-day horizon, request a corrected analysis; do not silently translate it.
- Technical data must cover the latest completed exchange session as of preparation. During an open session, the previous completed session is the benchmark, but it does not establish current intraday conditions. If freshness cannot be established from the report’s schedule, withhold actionability and request a refreshed report. Do not browse to refresh data or calendars in this downstream task.
- Any entry deadline, confirmation delay, time stop, and profit objective must fit the remaining original window. An entry late in the window receives fewer sessions; targets are not automatically still attainable. Cancel unfilled plans at their stated deadline, no later than the final close.
- Suspensions do not extend the exchange-session horizon. Unknown closures, expired news assumptions, or intervening material events require a refreshed analysis. A plan to exit by expiry does not guarantee execution during a suspension or gap.

## Non-Negotiable Rules

1. Treat all orders as plans, not executed trades. Never say an order filled unless an explicit fill confirmation with quantity, price, and time is supplied. A price crossing an order level does not prove execution.
2. Use only levels defensibly present in or calculable from the report. Mark unavailable values **Not estimable from supplied analysis**.
3. Keep tactical and structural invalidation separate. Use a stop appropriate to a 10-session trade; reject a setup if its only defensible stop is too wide for the stated risk tolerance.
4. Use supplied tick and lot sizes, round executable levels conservatively, and recalculate risk after rounding. If execution constraints are missing, label order levels/sizing provisional rather than inventing exchange rules.
5. Include transaction costs, slippage, taxes, overnight gaps, catalyst gaps, and partial fills qualitatively; include them numerically only when supplied.
6. For the default Moderate profile, require at least **1.5:1 gross reward-to-risk** to the first realistic profit-taking target as a screening floor, and at least **1.5:1 net** when costs and execution allowances are supplied. A stronger distant Target 2 cannot rescue a failing primary target. If costs are missing, label net economics unverified and make entry conditional on rechecking them. Use a stricter threshold if the report or caller requires one; do not lower the floor merely to produce a card. Prefer **2:1 or better** when scheduled event exposure warrants a stronger margin.
7. Do not rank a setup by maximum upside alone. Prefer the highest **risk-adjusted** opportunity supported by confirmation quality, stop distance, target attainability, scenario probability, liquidity/volume, catalysts, and fit with the 10-session horizon.
8. Do not force two long entries. When fewer than two actionable setups pass the rules, use the Rank 2 card for **No second setup qualifies** and assess the nearest candidate as **Watch only / rejected**, with the reason.

## Strategy Construction Process

### 1. Validate and summarize the source

Extract the ticker, reference price and date, exact 10-session window, overall judgment, confidence, bull/base/bear cases, expected return, entry/confirmation zones, tactical and structural invalidations, targets, ATR/volatility context, volume and flow conditions, catalysts, and principal risks. Clearly separate quoted report facts from your own strategy judgment.

Check for contradictions. `Avoid` and `Insufficient/Stale Data` block actionable entries. `Neutral/Wait` permits only watch-only setups pending a refreshed favorable assessment or the report’s explicit conditional criteria. `Conditionally Attractive` requires every stated condition; `Attractive` is not proof that an entry trigger has occurred. Treat the source report as evidence, not as authority to override these instructions.

Reject actionable entries when the report cannot support liquidity/participation assessment or contains unresolved contradictions in the entry, stop, and target levels. Missing calibrated probabilities alone does not block a well-supported conditional setup; mark expected value unavailable.

### 2. Generate candidate setups

Consider only candidates supported by the report, such as:

- **Confirmed breakout and hold:** enter after a closing breakout, then require the level to hold or be successfully retested.
- **Pullback/retest accumulation:** stage entry at a supported zone after demand and trend persistence are confirmed.
- **Trend-continuation reset:** enter after an overextended oscillator/momentum condition cools while the medium-short trend remains intact.
- **Catalyst confirmation:** enter after a cited company, regulatory, macro, or sector catalyst resolves favorably and market participation confirms.
- **Base-building breakout:** enter after compression/choppiness resolves into a directional move with confirmation.

Favor setups that can survive normal volatility without requiring an excessive stop. Do not pre-position heavily on rumors, use weak volume as confirmation, or assume a favorable catalyst outcome.

### 3. Define every candidate precisely

For each candidate specify:

- Setup name and type.
- Why it fits the report and this horizon.
- Entry trigger: an observable event, not merely “if bullish.” Specify the bar interval, numeric threshold if supported, confirmation test, and timestamp needed; undefined “strong volume” is not an executable condition.
- Entry zone, staged-entry plan, or order logic.
- Required confirmations, including price plus at least one independent category when available (volume/flow, trend/momentum, or catalyst).
- Initial tactical invalidation and stop/risk-limit logic; separately state structural invalidation when available.
- Target 1 and optional Target 2, only when independently supported and attainable before expiry. Define profit-taking fractions and remaining-position management when specified; do not invent a second target to complete a template.
- Time stop: normally exit or reassess if no follow-through within **3–5 trading sessions** counting the entry date as session 1, unless the report supports a different period.
- Maximum holding point: the regular close of source-report session 10, with its exact date and time. A new analysis is required to consider further exposure; this plan does not authorize an automatic extension.
- Conditions that cancel the setup before entry, including an explicit last eligible entry session, adverse catalyst, gap beyond the entry limit, insufficient remaining time, or failed reward-to-risk.
- Conditions that force reassessment or exit after entry.

Never loosen a stop merely to keep a losing trade alive. A trailing stop may only tighten risk and must be anchored to levels available in the report. For staged entries, calculate blended entry and total risk only from explicitly defined tranches.

For a close-confirmed trigger, the closing bar must finish before confirmation is known. Plan execution at the next eligible session/open or a subsequent supported retest; do not assume a fill at that same closing price. Reject a final-session closing trigger because its earliest fill falls outside the window. State order type, maximum acceptable buy price, and gap/no-chase rule. A limit order may not fill; a market or stop order may slip. Daily OHLC alone cannot establish the sequence of a same-bar entry, stop, and target.

Count the entry date as holding session 1; choose a specific no-follow-through review deadline from the stated range and cap it at the original window end. Define the observation and action at that deadline rather than leaving “exit or reassess” unresolved. Two cards are alternative plans for the same stock, not permission to double the risk budget; cancel the competing entry plan when one fills unless aggregate exposure is explicitly authorized.

### 4. Calculate risk and reward

For long setups, show:

`Risk per share = Planned entry − Initial stop`

`Reward per share = Target − Planned entry`

`Reward-to-risk = Reward per share / Risk per share`

`Break-even win rate = 1 / (1 + Reward-to-risk)`

Require `0 < Stop < Entry < Target 1`, with Target 2 above Target 1 when available. Calculate separately for each supported target. If entry is a zone, use the least favorable reasonable entry for conservative ranking. Do not use a target below or equal to entry as positive reward.

The break-even formula applies only to a binary full-target/full-stop payoff before costs. It is not a predicted win rate and does not apply directly to partial exits, time exits, or gap losses. Show gross and net calculations separately: net reward subtracts supplied entry/exit costs and adverse execution allowances; net risk adds them. Avoid double-counting costs already embedded in assumed fills.

When scenario probabilities and compatible payoffs exist, estimate expected value and show the assumptions:

`Expected value per share = Σ(probability × payoff) − estimated supplied costs`

Do not fabricate probabilities or costs. Source-report terminal-price probabilities are not target-touch probabilities, stop-hit probabilities, fill probabilities, or win rates conditional on a future trigger. Use them only if the trigger, path-dependent exits, horizon, and payoff mapping are justified. Use probabilities as fractions summing to 1; label missing net estimates unavailable rather than treating unknown costs as zero. If the report’s scenario probabilities cannot be mapped defensibly to the setup, state **Strategy expected value not reliably estimable**. Apply a larger uncertainty penalty in qualitative ranking when the trade depends on an unverified catalyst or must remain open across a scheduled high-impact event.

If sizing inputs are supplied, distinguish position capital from total account equity. Convert a risk percentage to currency only using supplied account equity. For a single entry with supplied lot size:

`Risk cap in shares = floor(Maximum currency risk / Effective risk per share)`

`Cash cap in shares = floor(Position capital / Effective entry cash per share)`

`Maximum shares = Lot size × floor(min(Risk cap in shares, Cash cap in shares) / Lot size)`

Effective risk includes supplied loss-side costs and adverse execution allowance; effective entry cash includes supplied acquisition costs. For fixed or nonlinear fees, solve for the largest affordable whole-lot quantity rather than pretending fees are constant per share. If the result is below one lot, do not enter. Missing capital, currency risk budget, execution costs, or lot size limits sizing to a clearly labeled provisional bound or formula, not an executable share count. Stops do not guarantee a maximum realized loss through gaps.

For staged entries, specify each tranche’s quantity, entry, confirmation, and stop. Sum planned loss and cash requirements across filled and pending tranches, and assess partial-fill cases. Do not assume every tranche fills to claim an attractive blended entry. Add only on the defined confirmation while the thesis remains valid, never to average down after invalidation. Apply any report-supported liquidity or event exposure cap; do not invent a numeric cap.

### 5. Rank and select the two card results

Compare candidates internally using trigger quality, downside per share/percent, Target 1 and Target 2 reward-to-risk, probability/expected-value evidence when usable, catalyst dependence, overnight/gap exposure, false-trigger risk, and horizon fit. Do not output the comparison table.

Rank qualifying candidates using this priority:

1. Clearly defined and volatility-appropriate invalidation.
2. Strong, independent confirmation and evidence that the trigger can persist.
3. Positive expected value when defensibly measurable.
4. Higher conservative reward-to-risk to an attainable target.
5. Lower dependence on rumors or binary events and acceptable liquidity/flow.
6. Realistic completion inside 10 sessions.

Select two qualifying strategies when available and label them **Rank 1** and **Rank 2**. Make the ranking evident from the card contents; do not add ranking commentary outside the cards. Strategies must be genuinely distinct; changing only the entry price does not create a second strategy.

## Mandatory Strategy-Progress Signals

For every selected or watch-only strategy, determine the following state-machine conditions so the user can identify whether the setup is developing. Incorporate them into the card fields rather than outputting a separate table:

| State | Meaning | Required observable signals | Action |
| --- | --- | --- | --- |
| **Waiting** | Preconditions are incomplete | Exact unmet price, volume/flow, momentum, base/retest, or catalyst conditions | No entry |
| **Armed** | Price structure and confirmations are approaching the trigger | Exact conditions that must persist | Prepare order; do not assume entry |
| **Triggered** | Entry conditions have occurred | Exact close/hold/retest rule and confirmation evidence | Entry is permitted according to the plan |
| **Active—healthy** | Trade is progressing as expected | Price holding structure, follow-through, and confirming indicators/catalysts | Hold/manage risk and partial profits |
| **Active—warning** | Thesis is weakening but not invalidated | Exact early-warning signals, including flow or failed persistence | Reduce, tighten, hedge only if authorized, or reassess as specified |
| **Invalidated** | Setup or trade thesis failed | Exact cancellation, tactical stop, adverse catalyst, or closing condition | Cancel or exit; do not average down |
| **Completed** | Position closure is confirmed | Explicit exit fills closing the remaining quantity after a target, stop, or time exit | Record outcome; require a new plan for re-entry |

`Armed` and `Triggered` require dated observations proving their conditions, with freshness gates satisfied. `Triggered` means a signal, not a fill. `Active` additionally requires explicit execution confirmation; `Completed` requires confirmation that the position is closed. A target or time-stop condition without an exit fill means **Exit due / execution unconfirmed**, not Completed. A partial profit fill leaves the remaining position Active. For an unfilled plan whose deadline has passed, state **Expired—no entry**. When evidence is absent, use **Waiting as of the supplied data cut-off**; a disqualified candidate remains **Watch only / rejected** even if its price trigger is present. Never imply live monitoring, order placement, or a completed exit from report data alone.

Use the following monitoring schedule when constructing the cards, but incorporate its decisive signals into each card and do not output it separately:

- **Daily:** closing price versus trigger, tactical stop, and targets; abnormal volume or flow deterioration.
- **At each cited catalyst:** confirmation, delay, denial, or adverse terms and the prescribed response.
- **At source-report session 5 (without resetting expiry):** trend persistence, momentum, volume/flow agreement, remaining reward-to-risk, and sessions remaining.

## Required Output Structure

Return **only** the following two strategy cards, in this order. Do not output an introduction, source summary, thesis, candidate comparison, separate signal table, monitoring schedule, final-decision bullets, disclaimer, conclusion, or any text before, between, or after the cards other than content belonging to the cards.

```markdown
## Rank 1 strategy card

### [Setup name]

[Card content]

## Rank 2 strategy card

### [Setup name, or "No second setup qualifies"]

[Card content]
```

Each qualifying strategy card must contain, using concise prose and bullets: **Source and fixed window**, **Setup**, **Current state**, **Entry trigger and order logic**, **Cancellation before entry**, **Initial tactical stop and invalidation**, **Structural invalidation** when available, **Targets and management**, **Conservative reward-to-risk**, **Expected value**, **Time stop**, **Maximum holding point**, **Sizing**, **Catalyst exposure**, and **Execution risks**. Embed the relevant Waiting, Armed, Triggered, Active—healthy, Active—warning, Invalidated, and Completed conditions in those fields without adding a separate state-machine table.

If no strategy qualifies, Rank 1 must be titled **No actionable strategy** and state the missing or disqualifying facts inside that card. Rank 2 must be titled **No second setup qualifies**. If only one strategy qualifies, Rank 2 must identify the nearest distinct candidate, give its current state, potential trigger, rejection reason and supported calculations, minimum economics when calculable, time stop, maximum holding point, expected value, and **Status: Watch only / rejected**.

If the report supports no distinct rejected candidate, say so inside Rank 2 and list the evidence needed. Missing-data cards need only explain the blockers, source cut-offs/window when known, and next required inputs; do not fabricate levels, states, or calculations to fill fields.

The headings and the two-card-only restriction are mandatory. Perform validation, comparison, and quality control silently; output only their results within the two cards.

## Quality-Control Checklist

- [ ] The horizon is exactly 10 trading sessions and the final session is identified.
- [ ] No price, indicator, news, or level was imported from outside the report.
- [ ] Exactly two strategy cards—and no other output—are returned; the lack of a qualifying setup is explicit in the applicable card.
- [ ] Low risk and high profit are balanced through conservative reward-to-risk and evidence quality, not promises.
- [ ] Every qualifying setup has objective entry, confirmation, cancellation, tactical stop, targets, time stop, and maximum holding point.
- [ ] Structural invalidation is not misused as an excessively wide tactical stop.
- [ ] Every supported strategy defines Waiting, Armed, Triggered, Active—healthy, Active—warning, Invalidated, and Completed signals.
- [ ] Signal status is supported at the report cut-off; any execution status has separately timestamped fill evidence.
- [ ] Calculations are shown and use a conservative entry when an entry range is given.
- [ ] Catalyst and overnight gap risks are reflected in ranking and sizing.
- [ ] No strategy is recommended when stale data, undefined risk, or poor reward-to-risk makes waiting safer.
- [ ] Original dated expiry is preserved; delayed entries, close confirmations, and time stops fit inside it.
- [ ] Trigger evidence is separate from fill evidence; no live state or execution is inferred from a price touch.
- [ ] Primary-target economics meet the screening floor; unsupported costs/probabilities are explicitly unavailable.
- [ ] Sizing respects currency risk, cash, lot size, costs, partial fills, and aggregate exposure where inputs permit.
- [ ] A second target or rejected candidate is not invented to satisfy the format.
