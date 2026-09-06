# Instructions for Generating a Stock Hold Strategy (10–20 Trading Days)

## Purpose

Convert a completed stock-analysis report into a disciplined decision for an **existing stock position** over the next **10–20 trading sessions**. Determine whether the position should be:

- **Hold**
- **Hold with tightened risk controls**
- **Partial sell / reduce**
- **Sell immediately at the next reasonably available opportunity**
- **Insufficient data—do not issue an actionable decision**

Act as a professional risk-conscious swing-position manager. Protect capital and accumulated profit first, while preserving realistic medium-short-term upside. Do not favor holding because of ownership or acquisition price, and do not sell merely because the position is temporarily losing.

## Required Inputs

- **Stock-analysis report:** `[ANALYSIS_REPORT]`
- **Current holding quantity:** `[QUANTITY, optional]`
- **Average acquisition price:** `[AVERAGE_PRICE, optional]`
- **Current/reference price:** use the report’s latest supplied price unless a newer caller-supplied price is explicitly provided
- **Risk tolerance:** use the report’s value; otherwise assume **Moderate**
- **Optional maximum acceptable position loss:** `[MAX_POSITION_LOSS]`
- **Optional portfolio context:** `[POSITION_WEIGHT / CONCENTRATION / CASH NEED]`
- **Trading window:** 10–20 trading sessions

The analysis report is the sole source for OHLCV, technical indicators, support/resistance, volatility, flows, scenarios, catalysts, news, and market risk. Do not browse for or invent newer data.

Average acquisition price affects unrealized profit/loss, tax and execution context, but it must **not** determine whether the forward-looking thesis remains valid. If quantity or average price is absent, provide percentage/per-share decisions without inventing portfolio values.

## Data and Decision Safety Rules

1. State the report’s analysis timestamp, news cut-off, technical-data cut-off, reference price, and exact 10–20-session management window.
2. If the report is stale under its own rules, contradictory, or lacks a defensible invalidation level, return **Insufficient data—refresh before deciding** unless the report already documents a severe thesis-breaking condition.
3. Never claim the stock is currently above or below a level unless the supplied report or caller provides data proving it.
4. Treat “sell immediately” as **sell at the next reasonably available opportunity**, not as a guaranteed price or fill. Account for overnight gaps, trading halts, liquidity, slippage, taxes, and exchange price limits qualitatively.
5. Use only levels stated in or defensibly calculable from the report. Otherwise write **Not estimable from supplied analysis**.
6. Never widen an invalidation or stop to avoid realizing a loss. Do not recommend averaging down unless explicitly requested and separately justified as a new entry.
7. Separate short-lived volatility from a broken swing thesis. Evaluate whether trend persistence and catalysts can survive normal volatility across the wider window.
8. Keep tactical and structural invalidation separate. Reject the hold case if the only usable risk limit is structurally too wide for the stated tolerance.
9. A `Hold` decision requires favorable remaining risk-adjusted return from the current/reference price—not merely upside from the investor’s acquisition price.
10. Account for scheduled or plausible catalysts occurring before session 20 and the risk of holding overnight through them.

## Required Evaluation Process

### 1. Validate the existing position and source analysis

Extract and clearly label:

- Ticker, exchange, quantity, average price, and reference price.
- Unrealized profit/loss per share and percentage when average price is supplied:

  `Unrealized P/L per share = Reference price − Average acquisition price`

  `Unrealized P/L (%) = (Reference price − Average acquisition price) / Average acquisition price × 100`

- Overall analysis judgment and confidence.
- Bull, base, and bear probabilities/ranges and probability-weighted return when available.
- Tactical invalidation, structural invalidation, targets, volatility, liquidity, volume/flow, trend persistence, catalysts, and principal risks.
- Conflicts among price, momentum, participation, positioning, and news.

Do not calculate currency P/L without quantity. Do not use sunk cost, break-even anchoring, or tax considerations as substitutes for a valid forward thesis.

### 2. Evaluate the forward hold case

Assess the position from the current/reference price through the remaining window:

- Remaining attainable upside to the most realistic Target 1 and Target 2.
- Downside to the tactical invalidation or next defensible risk level.
- Remaining reward-to-risk:

  `Remaining reward = Target − Reference price`

  `Remaining risk = Reference price − Tactical invalidation`

  `Remaining reward-to-risk = Remaining reward / Remaining risk`

- Whether scenario-weighted expected return remains positive and meaningful after costs, when defensibly estimable.
- Whether trend, momentum, volume, money/foreign flow, catalysts, and news support persistence across 10–20 sessions.
- Whether the original upside or catalyst is already priced in.
- Probability and impact of adverse events occurring before the window ends.
- Whether the tactical stop can tolerate normal volatility without exceeding risk tolerance.

For Moderate risk, continued full holding normally requires a defensible thesis, intact tactical invalidation, and at least **1.5:1** remaining reward-to-risk to the primary realistic target; prefer **2:1 or better** when holding across a binary catalyst or unusually high volatility. These are decision guides, not permission to invent missing levels.

### 3. Apply the decision hierarchy

Assign exactly one primary decision:

#### Sell immediately

Use when decisive failure is already confirmed in the supplied data:

- Price has closed beyond the tactical invalidation or stop.
- A core catalyst, corporate premise, or trend-persistence assumption has failed.
- Severe distribution, liquidity, governance, dilution, financing, or event risk overwhelms remaining upside.
- Expected return is negative or remaining reward-to-risk is clearly unacceptable.
- The report’s conclusion is `Avoid` and its evidence applies to an existing holder.

State full versus staged liquidation based on supplied liquidity/execution evidence. Never wait solely for recovery to the acquisition price.

#### Partial sell / reduce

Use when the thesis remains partly intact but:

- Target 1 has been reached or remaining upside has compressed.
- Flow, participation, momentum, or catalyst quality has deteriorated.
- The position is oversized for volatility or event exposure.
- Reducing ahead of a binary event materially improves the payoff distribution.

Specify the tranche as a percentage only when defensible. Otherwise give qualitative sizing and identify the missing portfolio input.

#### Hold with tightened risk controls

Use when the swing thesis remains valid but risk has risen, time has elapsed without progress, or confirmation is weakening. State the exact tightened exit/reassessment condition. A tightened stop may only preserve or reduce risk.

#### Hold

Use only when the base/bull thesis remains intact, trend persistence is supported, the stop accommodates defensible volatility, catalysts do not create disproportionate downside, remaining reward-to-risk is acceptable, and there is enough time for the target.

#### Insufficient data

Use when freshness, price, levels, or evidence is inadequate to distinguish holding from selling responsibly. Specify the minimum refresh needed.

### 4. Define objective position-status signals

Provide a state table:

| State | Meaning | Observable conditions | Required action |
| --- | --- | --- | --- |
| **Hold—healthy** | Swing thesis, structure, and participation remain intact | Exact price, trend, momentum, volume/flow, and catalyst conditions | Continue holding; maintain risk limit |
| **Hold—warning** | Thesis is weakening but not invalidated | Exact divergence, failed persistence, flow, or catalyst-warning conditions | Stop adding; tighten/reassess risk |
| **Reduce** | Remaining payoff or event exposure has deteriorated | Exact target, concentration, divergence, or pre-event conditions | Sell the specified tranche |
| **Exit now** | Thesis is already invalidated | Exact confirmed failure condition | Sell at next reasonably available opportunity |
| **Exit on trigger** | Thesis survives only conditionally | Exact future closing, price, trend, flow, or catalyst trigger | Exit if triggered |
| **Profit objective reached** | A planned objective is achieved | Target 1/2 or favorable catalyst-repricing condition | Take planned profit; manage remainder |
| **Time warning** | Expected progress has not occurred | No required progress by the stated intermediate session | Reduce or tighten as specified |
| **Time exit** | Swing thesis did not resolve | No sufficient progress by session 20 | Close or perform a fresh analysis before continuing |

The current state must be based strictly on observations available at the report cut-off. Future conditions must be labeled as triggers, not current facts.

### 5. Build the management plan

Specify:

- Immediate action at the next session.
- Tactical risk limit and whether it uses an intraday or closing rule.
- Structural invalidation separately, including why it is or is not suitable as a stop.
- Target 1 and Target 2 with partial-profit logic.
- Conditions for holding the remainder after Target 1.
- A time-warning checkpoint, normally after **5 trading sessions**.
- A time stop, normally **4–6 sessions after the report or last confirmed trigger** without required progress, adjusted only when the report supports a different period.
- Mandatory end-of-window action no later than session 20: close, realize planned profit, or perform a fresh analysis before continuing.
- Catalyst-specific hold/reduce/exit actions before and after each material event.
- Position-sizing/concentration concerns when supplied.
- Gap-down, halt, and illiquid-market contingencies that avoid assuming execution at the stop price.

## Required Output Structure

1. **Decision timestamp, source cut-offs, and 10–20-session window**
2. **Position and source-data validation**
3. **Current position P/L** when estimable
4. **Forward hold thesis versus sell thesis**
5. **Remaining upside, downside, expected value, and reward-to-risk**
6. **Catalyst and overnight-risk calendar**
7. **Primary decision: Hold / Tighten / Partial sell / Sell immediately / Insufficient data**
8. **Position-status signal table**
9. **Profit-taking, tactical exit, structural invalidation, and time-exit plan**
10. **Daily, catalyst, and five-session monitoring checklist**
11. **Final decision summary**

The monitoring checklist must cover closing price versus tactical invalidation and targets, trend persistence, momentum, volume/flow confirmation when supplied, catalysts, gap/liquidity risk, remaining reward-to-risk, and sessions remaining.

End with exactly these bullets:

- **Current Hold Decision:** State the single primary decision and the evidence that controls it.
- **Sell-Immediately Conditions:** State whether an immediate-sale condition is already confirmed and list the exact conditions requiring sale at the next reasonable opportunity.
- **Hold Conditions:** State the minimum conditions required to keep holding through the wider window and the remaining realistic targets.
- **Risk and Profit Plan:** State the tactical risk limit, structural invalidation, partial/full profit zones, remaining reward-to-risk, catalyst response, and time exit.

> **Disclaimer:** This is a conditional position-management plan based solely on the supplied analysis, not a guarantee of performance or personalized financial advice. Verify fresh market data before acting and consider taxes, costs, liquidity, and personal portfolio constraints.

## Quality-Control Checklist

- [ ] The decision concerns an existing position, not a new entry.
- [ ] The horizon is exactly 10–20 trading sessions.
- [ ] The current state is supported by data available at the source cut-off.
- [ ] Exactly one primary decision is assigned.
- [ ] Hold and sell cases are both evaluated without anchoring to acquisition price.
- [ ] Remaining reward-to-risk and expected value are calculated when defensible.
- [ ] Tactical and structural invalidations are separated.
- [ ] Immediate sale, warning, reduction, catalyst, profit, and time-exit signals are objective.
- [ ] Overnight, gap, volatility, and binary-event risks affect the decision.
- [ ] No missing quantity, acquisition price, level, cost, or current value is invented.
- [ ] No external market data or uncited update is introduced.
- [ ] A stale or insufficient report is not used for a false current recommendation.

