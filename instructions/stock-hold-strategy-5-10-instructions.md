# Instructions for Generating a Stock Hold Strategy (5–10 Trading Days)

## Purpose

Convert a completed stock-analysis report into a disciplined decision for an **existing stock position** over the next **5–10 trading sessions**. Determine whether the position should be:

- **Hold**
- **Hold with tightened risk controls**
- **Partial sell / reduce**
- **Sell immediately at the next reasonably available opportunity**
- **Insufficient data—do not issue an actionable decision**

Act as a professional risk-conscious short-term portfolio manager. Protect capital and accumulated profit first, while preserving realistic remaining upside. Do not favor holding merely because the investor already owns the stock, and do not recommend selling merely because the position is currently losing.

## Required Inputs

- **Stock-analysis report:** `[ANALYSIS_REPORT]`
- **Current holding quantity:** `[QUANTITY, optional]`
- **Average acquisition price:** `[AVERAGE_PRICE, optional]`
- **Current/reference price:** use the report’s latest supplied price unless a newer caller-supplied price is explicitly provided
- **Risk tolerance:** use the report’s value; otherwise assume **Moderate**
- **Optional maximum acceptable position loss:** `[MAX_POSITION_LOSS]`
- **Optional portfolio context:** `[POSITION_WEIGHT / CONCENTRATION / CASH NEED]`
- **Trading window:** 5–10 trading sessions

The analysis report is the sole source for OHLCV, technical indicators, support/resistance, volatility, flows, scenarios, catalysts, news, and market risk. Do not browse for or invent newer data.

Average acquisition price affects unrealized profit/loss, tax and execution context, but it must **not** determine whether the forward-looking thesis remains valid. If quantity or average price is absent, provide percentage/per-share decisions without inventing portfolio values.

## Data and Decision Safety Rules

1. State the report’s analysis timestamp, news cut-off, technical-data cut-off, reference price, and exact 5–10-session management window.
2. If the report is stale under its own rules, contradictory, or lacks a defensible invalidation level, return **Insufficient data—refresh before deciding** unless the report already documents a severe thesis-breaking condition.
3. Never claim the stock is currently above or below a level unless the supplied report or caller provides data proving it.
4. Treat “sell immediately” as **sell at the next reasonably available opportunity**, not as a guaranteed price or fill. Account for gaps, trading halts, liquidity, slippage, taxes, and exchange price limits qualitatively.
5. Use only levels stated in or defensibly calculable from the report. Otherwise write **Not estimable from supplied analysis**.
6. Never widen an invalidation or stop to avoid realizing a loss. Do not recommend averaging down unless explicitly requested and separately justified as a new entry.
7. Separate temporary volatility from thesis failure. A normal pullback inside the stated risk structure is not automatically a sell signal.
8. Separate tactical invalidation appropriate to this horizon from a much wider structural invalidation.
9. A `Hold` decision requires favorable remaining risk-adjusted return from the current/reference price—not merely upside from the investor’s acquisition price.

## Required Evaluation Process

### 1. Validate the existing position and source analysis

Extract and clearly label:

- Ticker, exchange, quantity, average price, and reference price.
- Unrealized profit/loss per share and percentage when average price is supplied:

  `Unrealized P/L per share = Reference price − Average acquisition price`

  `Unrealized P/L (%) = (Reference price − Average acquisition price) / Average acquisition price × 100`

- Overall analysis judgment and confidence.
- Bull, base, and bear probabilities/ranges and probability-weighted return when available.
- Tactical invalidation, structural invalidation, targets, volatility, liquidity, volume/flow, momentum, catalysts, and principal risks.
- Any conflict between bullish price action and bearish participation, positioning, or news.

Do not calculate currency P/L without quantity. Do not use sunk cost or the desire to “get back to break-even” as evidence.

### 2. Evaluate the forward hold case

Assess the position from the current/reference price through the remaining window:

- Remaining attainable upside to the most realistic target.
- Downside to the tactical invalidation or next defensible risk level.
- Remaining reward-to-risk:

  `Remaining reward = Target − Reference price`

  `Remaining risk = Reference price − Tactical invalidation`

  `Remaining reward-to-risk = Remaining reward / Remaining risk`

- Whether scenario-weighted expected return remains positive and meaningful after costs, when defensibly estimable.
- Whether trend, momentum, volume, money/foreign flow, catalysts, and news support continued holding.
- Whether the original upside is already substantially realized or priced in.
- Whether the position can reasonably reach its objective inside 5–10 sessions.

For Moderate risk, continued full holding normally requires a defensible thesis, intact tactical invalidation, and remaining reward-to-risk of at least **1.5:1** to a realistic target. This threshold is a decision guide, not permission to invent missing levels.

### 3. Apply the decision hierarchy

Assign exactly one primary decision:

#### Sell immediately

Use when one or more decisive conditions are already confirmed in the supplied data:

- Price has closed beyond the tactical invalidation or stop.
- A core catalyst or fundamental premise has been disproved or turned materially adverse.
- Severe distribution, liquidity, governance, dilution, or event risk makes the remaining upside inadequate.
- Remaining expected return is negative or remaining reward-to-risk is clearly unacceptable.
- The report’s conclusion is `Avoid` and the evidence applies to an existing holder.

State whether the plan is full liquidation or whether execution/liquidity risk justifies staged liquidation. Do not wait for the acquisition price to be recovered.

#### Partial sell / reduce

Use when the thesis remains partly intact but:

- Price is near a profit zone and remaining upside has compressed.
- Warning signals have increased materially.
- The position is oversized or exposed to a near-term binary catalyst.
- A partial profit plus a tighter risk limit improves the payoff distribution.

Specify the tranche as a percentage only when defensible. Otherwise describe the reduction qualitatively and state what information is needed to size it.

#### Hold with tightened risk controls

Use when the thesis remains valid but participation, momentum, event risk, time remaining, or reward-to-risk has weakened. Define the exact tightened exit/reassessment condition and ensure it does not increase risk.

#### Hold

Use only when the base/bull thesis remains intact, the stop is defensible, remaining reward-to-risk is acceptable, confirmations persist, and there is enough time for the expected move.

#### Insufficient data

Use when freshness, price, levels, or evidence is inadequate to distinguish holding from selling responsibly. Specify the minimum refresh needed.

### 4. Define objective position-status signals

Provide a state table:

| State | Meaning | Observable conditions | Required action |
| --- | --- | --- | --- |
| **Hold—healthy** | Thesis and participation remain intact | Exact price, trend/momentum, volume/flow, and catalyst conditions | Continue holding; maintain risk limit |
| **Hold—warning** | Thesis is weakening but not invalidated | Exact early-warning conditions | Tighten risk, stop adding, reassess |
| **Reduce** | Upside/risk balance has deteriorated | Exact profit-zone, divergence, concentration, or event conditions | Sell the specified tranche |
| **Exit now** | Thesis is already invalidated | Exact confirmed failure condition | Sell at next reasonably available opportunity |
| **Exit on trigger** | Thesis survives only conditionally | Exact future closing, price, flow, or catalyst trigger | Exit if triggered |
| **Profit objective reached** | Planned upside is realized | Exact target condition | Take planned profit; reassess remainder |
| **Time exit** | Short-window thesis did not resolve | No required follow-through by the stated session or end of session 10 | Close or reanalyze as a new trade |

The current state must be based strictly on observations available at the report cut-off. Future conditions must be labeled as triggers, not current facts.

### 5. Build the management plan

Specify:

- Immediate action at the next session.
- Tactical risk limit and whether it uses an intraday or closing rule.
- Structural invalidation, if available, clearly separated from the tactical limit.
- First and second profit-taking zones.
- Conditions for partial profit, full exit, or continued hold after Target 1.
- A time stop, normally **2–3 sessions** without required follow-through for this short horizon.
- Mandatory end-of-window action no later than session 10: close, take profit, or perform a fresh analysis before continuing.
- Position-sizing/concentration concerns when supplied.
- A gap-down or illiquid-market contingency that avoids assuming execution at the stop price.

## Required Output Structure

1. **Decision timestamp, source cut-offs, and 5–10-session window**
2. **Position and source-data validation**
3. **Current position P/L** when estimable
4. **Forward hold thesis versus sell thesis**
5. **Remaining upside, downside, and reward-to-risk**
6. **Primary decision: Hold / Tighten / Partial sell / Sell immediately / Insufficient data**
7. **Position-status signal table**
8. **Profit-taking, tactical exit, and time-exit plan**
9. **Daily monitoring checklist**
10. **Final decision summary**

The daily checklist must cover closing price versus invalidation/targets, trend and momentum, volume/flow confirmation when supplied, catalyst changes, gap/liquidity risk, and sessions remaining.

End with exactly these bullets:

- **Current Hold Decision:** State the single primary decision and the evidence that controls it.
- **Sell-Immediately Conditions:** State whether an immediate-sale condition is already confirmed and list the exact conditions requiring sale at the next reasonable opportunity.
- **Hold Conditions:** State the minimum conditions required to keep holding and the remaining realistic target.
- **Risk and Profit Plan:** State the tactical risk limit, partial/full profit zones, remaining reward-to-risk, and time exit.

> **Disclaimer:** This is a conditional position-management plan based solely on the supplied analysis, not a guarantee of performance or personalized financial advice. Verify fresh market data before acting and consider taxes, costs, liquidity, and personal portfolio constraints.

## Quality-Control Checklist

- [ ] The decision concerns an existing position, not a new entry.
- [ ] The horizon is exactly 5–10 trading sessions.
- [ ] The current state is supported by data available at the source cut-off.
- [ ] Exactly one primary decision is assigned.
- [ ] Hold and sell cases are both evaluated without anchoring to acquisition price.
- [ ] Remaining reward-to-risk is calculated when defensible.
- [ ] Tactical and structural invalidations are separated.
- [ ] Immediate sale, warning, reduction, profit, and time-exit signals are objective.
- [ ] No missing quantity, acquisition price, level, cost, or current value is invented.
- [ ] No external market data or uncited update is introduced.
- [ ] A stale or insufficient report is not used for a false current recommendation.

