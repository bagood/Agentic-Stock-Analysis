**1. Analysis Timestamp, News Cut-Off, and Supplied Data Cut-Off**

| Item | Detail |
|---|---|
| Company | PT Soechi Lines Tbk |
| Ticker / exchange | SOCI / Indonesia Stock Exchange |
| Analysis timestamp | 30 July 2026, 23:07 WIB |
| News research cut-off | 30 July 2026, 23:07 WIB |
| Supplied technical-data cut-off | 29 July 2026 |
| Forecast horizon | 31 July 2026 to 19 August 2026, 10-20 calendar days |
| Estimated IDX trading sessions | About 13 sessions: 31 Jul, 3-7 Aug, 10-14 Aug, 18-19 Aug |
| Investor currency | IDR |
| Entry price | No separate entry supplied; using latest supplied Close of IDR 418 |
| Risk tolerance | Moderate |

IDX is expected to be closed on Monday, 17 August 2026 for Indonesia Independence Day. Source: CalendarLabs IDX holiday calendar.

**2. Input Validation and Data-Freshness Assessment**

The provided data was parsed as a dated JSON object, converted into one dated record, and sorted by `Date`.

| Validation item | Result |
|---|---|
| Duplicate dates | None |
| Missing OHLCV fields | None |
| Positive prices | Passed |
| `High >= max(Open, Close)` | Passed: 428 >= 420 and 418 |
| `Low <= min(Open, Close)` | Passed: 402 <= 418 and 420 |
| `High >= Low` | Passed |
| Volume non-negative | Passed: 6,467,500 |
| Finite indicator values | Passed on supplied fields |
| Data freshness | Slightly stale: latest supplied row is 29 July 2026, while analysis is after the 30 July 2026 session |

Because the dataset is only one trading session behind, it is stale but not more than three trading sessions old. I can provide a conditional short-term forecast, but confidence is reduced. No internet-sourced price, volume, chart, support, resistance, flow, or technical value was used.

Latest supplied OHLCV, from **Provided technical dataset**:

| Date | Open | High | Low | Close | Volume |
|---|---:|---:|---:|---:|---:|
| 2026-07-29 | 420 | 428 | 402 | 418 | 6,467,500 |

**3. Supplied OHLCV and Technical Snapshot**

The latest candle closed below the open, at IDR 418 versus IDR 420, despite trading as high as IDR 428 and as low as IDR 402. That shows intraday volatility and some rejection from the upper area, but the close remained near the upper half of the day’s range.

| Signal group | Supplied fields | Interpretation |
|---|---|---|
| Trend | `Aroon Up Trend = 1.0`, `Aroon Down Trend = 0.0`, `Strong Plus Directional Index = 1.0`, `Weak Minus Directional Index = 1.0` | Trend structure is broadly bullish, but the weak-minus flag shows downside pressure has not disappeared. |
| Bull/bear power | `Bull Power Up Trend = 1.0`, `Bull Power 80% Positives = 1.0`, `Bear Power Trend = 0.0` | Bull power confirms upside bias. |
| MACD | `MACD Non-Near 0 Positive = 1.0`, `MACD Near 0 = 0.0` | Positive momentum condition is active. |
| Momentum | `Price Momentum 5D = 0.0718`, `10D = 0.1484`, `20D = 0.3571` | Short-term momentum is strongly positive across supplied windows. |
| RSI | `RSI Value = 65.85`, `RSI Up Trend = 1.0`, `RSI 7 = 71.13`, `RSI 21 = 59.43` | Momentum is constructive but nearing overheated conditions on short RSI. |
| Stochastic | `Stochastic K Value = 80.62`, `Stochastic Oscillator Overbought = 1.0` | Overbought flag increases pullback risk. |
| Channels | `Keltner Percent B = 0.871`, `Donchian Percent B = 0.808`, `Bollinger Percent B = 0.813`; all width-increasing flags = `1.0` | Price is high in its supplied channel ranges while volatility/channel width is expanding. This supports upside continuation if confirmed, but also means reversals can be sharp. |
| Volume/flow | `Volume Ratio 20D = 0.346`, `On Balance Volume Decreasing = 1.0`, `MFI Decreasing = 1.0` | The main technical warning: momentum is rising on weak relative volume and deteriorating OBV/MFI. |
| Accumulation | `Positive CMF = 1.0`, `Accumulation Distribution Line Increasing = 1.0` | Contradicts OBV/MFI weakness; suggests some accumulation remains present. |
| Reversal | `Fisher Up trend = 1.0`, `Fisher Reversal = 1.0`, `Zig Zag Increasing = 1.0` | Uptrend is active, but reversal flag requires caution. |
| Foreign/domestic positioning | `Foreign to Domestic 15 Days Ownership = -0.02198`, `60 Days = 0.03624`, `90 Days = 0.00068` | Short-term foreign/domestic ownership tilt is mildly negative, while 60-day is mildly positive. Exact scale is ambiguous. |

Support/resistance, ATR-distance, moving averages, and volatility-based stop levels are **not estimable from supplied data** beyond the latest OHLC range, because only one dated row is supplied and no numeric ATR value is provided.

**4. Key Company News and Catalysts**

Recent company-specific news is mainly financing and structure-related.

| News item | Date | Direction | Assessment |
|---|---:|---|---|
| SOCI issued / listed Sukuk Ijarah Berkelanjutan I Tahap I 2026; IDX listing began 9 July 2026. Reported nominal listed amount was Rp134.855 billion with 7.95% annual yield and maturity on 8 July 2029. | Published 8 July 2026 | Mildly bullish / uncertain | Supports funding visibility, but adds fixed financing obligations. Short-term equity impact may already be partly priced in. |
| Earlier sukuk offering materials described a maximum issue amount of Rp500 billion for Stage I, with 3-year and 5-year yield ranges of 7.35%-8.00%, and payment from investors on 7 July 2026. | Offering period 19-23 June 2026; payment 7 July 2026 | Neutral to mildly bullish | Financing execution matters, but no immediate equity target can be derived from this. |
| PEFINDO assigned SOCI corporate rating `idBBB+` stable and proposed Sukuk I 2026 rating `idAAA(sy)(sf)` for a maximum IDR3 trillion. | 26 June 2026 | Mildly bullish | Credit access is positive, though equity holders still face leverage and execution risk. |
| SOCI reportedly established new subsidiary PT Andalan Samudra Bahari, 99.99% owned, to support shipping operations; disclosure said no material financial/legal impact. | Published 9 July 2026 | Mildly bullish but low immediate magnitude | Operational optionality, but likely low short-term price impact unless followed by contracts or asset deployment. |
| June 2026 shareholder report showed controlling shareholders unchanged; one director increased ownership by 30,000 shares; number of shareholders declined. | Published 9-13 July 2026 | Mixed | Stability of control is neutral; director buying is mildly positive but small; fewer holders may suggest lower breadth. |

Official company website confirms SOCI is an integrated energy transportation company with more than 30 vessels and investor-relations disclosures available, but no newer price-sensitive company news was found on the accessible company announcement listing after 26 June 2026.

**5. Indonesia Market News**

Domestic market conditions are mixed and important for a smaller IDX name like SOCI.

Bank Indonesia held the BI Rate at 5.75% at the 21-22 July 2026 meeting and emphasized Rupiah stability, foreign portfolio inflows, and liquidity support. That is broadly supportive for domestic risk assets, but the same release noted elevated global uncertainty and currency-stability priorities.

Recent Indonesian market reporting also points to volatility around the Federal Reserve decision and Bank Indonesia leadership transition. RRI reported on 28 July 2026 that investors were in wait-and-see mode due to the Fed and BI transition. Financial Times and Wall Street Journal also reported this week that BI Governor Perry Warjiyo resigned unexpectedly, raising investor concern about central-bank independence and policy continuity.

Transmission to SOCI: higher macro uncertainty can reduce risk appetite for second-line stocks, while Rupiah instability can affect companies with foreign-currency costs, debt, vessels, fuel, or shipping-related exposure. The supplied JSON does not provide SOCI’s currency debt or cost split, so this remains a risk channel, not a quantified impact.

**6. Global Market News**

The main global variables relevant to SOCI are risk appetite, US monetary policy, the US dollar, oil/shipping conditions, and Middle East disruption risk.

Bank Indonesia’s July release cited renewed global uncertainty after US-Iran escalation in early July 2026, disruption around the Strait of Hormuz, and rising oil and commodity prices. For SOCI, which operates in shipping/energy transportation, this can cut both ways: stronger tanker/shipping demand or energy-logistics relevance may help sentiment, while higher fuel costs, insurance, financing costs, or geopolitical disruptions may pressure margins.

No reliable recent news source found in this search provided a direct, fresh SOCI-specific contract or operational update tied to the global shipping backdrop.

**7. Integrated Technical-and-News Assessment**

The technical setup is **momentum-positive but crowded/fragile**.

Bullish technical evidence is clear: `Aroon Up Trend = 1.0`, `Strong Plus Directional Index = 1.0`, `MACD Non-Near 0 Positive = 1.0`, `Price Momentum 20D = 0.3571`, and `Zig Zag Increasing = 1.0`. The stock has strong short-term momentum from the supplied data.

The problem is quality of participation. `Volume Ratio 20D = 0.346`, `On Balance Volume Decreasing = 1.0`, and `MFI Decreasing = 1.0` argue that the advance may lack broad volume confirmation. `Stochastic Oscillator Overbought = 1.0`, `RSI 7 = 71.13`, and `Fisher Reversal = 1.0` raise the risk of a pullback or failed breakout.

News is modestly supportive but not explosive. Sukuk funding and the stable PEFINDO rating support financing visibility, but no confirmed near-term contract, earnings catalyst, dividend catalyst, or material corporate action was found within the forecast window.

**8. Near-Term Catalyst Calendar**

| Date | Catalyst | Direction | Likely effect | Priced in? | Confirmation / invalidation |
|---|---|---|---|---|---|
| 31 Jul-19 Aug 2026 | Follow-through after recent momentum in supplied technical data | Bullish if volume improves | Short-term, potentially immediate | Partly | Confirmed by close above latest supplied high of IDR 428 with stronger supplied-volume confirmation in updated data |
| Ongoing after 9 Jul 2026 | Sukuk listing / funding use for vessel-related usufruct acquisition | Mildly bullish / uncertain | Low to medium | Likely partly | Confirmed by official follow-up on deployment, contracts, or earnings benefit |
| 31 Jul-19 Aug 2026 | BI transition and Fed/global-risk uncertainty | Bearish / uncertain | Medium | Not fully | Lower volatility and stable domestic risk appetite would reduce the risk |
| 17 Aug 2026 | IDX closed for Independence Day | Neutral | Trading interruption only | Known | No thesis effect except shorter trading window |

**9. Bull, Base, and Bear Scenarios**

Reference price = latest supplied Close = **IDR 418**.

Numerical scenario ranges are based only on the supplied latest OHLC range and supplied momentum/channel conditions. The latest supplied high is IDR 428, low is IDR 402, and daily range is IDR 26. Because only one dated row is supplied, these are approximate tactical ranges, not robust support/resistance levels.

| Scenario | Assumptions | Price range | Return calculation | Probability |
|---|---|---:|---|---:|
| Bull case | Momentum persists, price reclaims/holds above supplied high of 428, volume/OBV/MFI improve in updated data, macro news does not worsen | IDR 428-446 | Midpoint 437: `(437 - 418) / 418 x 100 = 4.5%` | 30% |
| Base case | Uptrend remains intact but overbought and weak-volume signals cap upside; price consolidates near upper supplied range | IDR 418-428 | Midpoint 423: `(423 - 418) / 418 x 100 = 1.2%` | 45% |
| Bear case | Overbought/reversal signals dominate, weak volume confirms distribution, price loses latest supplied low | IDR 392-402 | Midpoint 397: `(397 - 418) / 418 x 100 = -5.0%` | 25% |

Probability-weighted expected return:

`(30% x 4.5%) + (45% x 1.2%) + (25% x -5.0%) = 0.6%`

This expected return is only **roughly estimable** because the dataset has one dated row and is one trading session stale.

**10. Risk Matrix and Risk Controls**

| Risk | Probability | Impact | Warning indicator | Risk-control response |
|---|---|---|---|---|
| Momentum fades due to weak participation | Medium | High | Updated data continues to show low volume ratio, falling OBV/MFI | Avoid chasing; require confirmation above IDR 428 |
| Overbought pullback | Medium | Medium | `Stochastic Overbought = 1.0`, `RSI 7 = 71.13`, `Fisher Reversal = 1.0` persists | Use smaller position; take partial profit quickly |
| Macro risk from BI transition / Rupiah / Fed | Medium | Medium to high | Renewed IDX volatility or negative policy headlines | Reduce exposure or wait for calmer tape |
| Financing/leverage execution risk | Medium | Medium | Negative disclosure on sukuk deployment, vessel acquisition, debt servicing | Reassess thesis immediately |
| Data quality / staleness | Medium | High | No updated OHLCV after 29 July | Do not scale position without updated data |
| Liquidity risk | Medium | Medium | Supplied `Volume Ratio 20D = 0.346` | Use limit orders; avoid large size relative to normal liquidity |

Risk controls from supplied data only:

| Control | Level / status |
|---|---|
| Preferred entry zone | Not strongly supported. If acting, better near IDR 418 or on confirmed reclaim of IDR 428, not after an extended spike. |
| Confirmation level | Latest supplied high: IDR 428. A close above this level in updated supplied data would strengthen the bullish case. |
| Invalidation level | Latest supplied low: IDR 402. A break below this level weakens the short-term upside thesis. |
| Stop-loss / risk limit | IDR 402 is the only defensible supplied-data invalidation reference. ATR-based stop is not estimable. |
| First profit-taking zone | IDR 428, based on latest supplied high. |
| Second profit-taking zone | IDR 446, based on one latest daily range above close; lower confidence. |
| Upside/downside ratio | Using 437 bull midpoint vs 397 bear midpoint: upside +4.5%, downside -5.0%, ratio about 0.9:1. Not attractive unless confirmation improves. |
| Position sizing | Moderate risk tolerance: small-to-medium tactical size only; avoid full allocation before updated volume confirmation. |

**11. Final Assessment**

Overall judgment: **Neutral/Wait**.

SOCI has a technically constructive but fragile short-term setup. The strongest bullish items are `MACD Non-Near 0 Positive = 1.0`, `Price Momentum 20D = 0.3571`, and active trend flags such as `Aroon Up Trend = 1.0` and `Strong Plus Directional Index = 1.0`. Recent company news on sukuk funding and PEFINDO ratings is mildly supportive.

The strongest bearish items are `Volume Ratio 20D = 0.346`, `On Balance Volume Decreasing = 1.0`, and overbought/reversal warnings from `Stochastic Oscillator Overbought = 1.0`, `RSI 7 = 71.13`, and `Fisher Reversal = 1.0`. Domestic macro uncertainty around BI leadership and Fed watch also argues against aggressive chasing.

The market may already have priced in the sukuk news and recent momentum. The single most important invalidating development would be an updated close below IDR 402 with continued weak volume/OBV/MFI signals.

I confirm that no internet-sourced OHLCV, share price, volume, chart, technical indicator, target price, support/resistance, broker target, or market-flow dataset was used.

**12. News Sources**

| Source | Date | Use |
|---|---:|---|
| Bank Indonesia press release: BI-Rate held at 5.75% | 22 Jul 2026 | Domestic macro, Rupiah, liquidity, global uncertainty |
| IDX press release page | 24 Jul 2026 latest listed item | Market context |
| RRI: JCI volatility amid Fed watch and BI transition | 28 Jul 2026 | Domestic sentiment |
| Financial Times: BI governor resignation | 30 Jul 2026 | Domestic policy risk |
| Wall Street Journal: BI governor resignation | 27 Jul 2026 | Cross-check on BI transition |
| PEFINDO SOCI rating page | 26 Jun 2026 | SOCI credit rating and sukuk rating |
| BCA Sekuritas SOCI sukuk offer page | June-July 2026 | Sukuk terms and schedule |
| IndoPremier / IDX-linked AI report on SOCI sukuk listing | 8 Jul 2026 | Sukuk listing context, treated cautiously because AI-generated |
| IndoPremier report on SOCI subsidiary and shareholder registration | 9-13 Jul 2026 | Company disclosure context, treated cautiously where AI-generated |
| Soechi official website / investor-relations page | Crawled 3 days ago | Company identity and business context |
| CalendarLabs IDX holiday calendar | 2026 | IDX holiday context |

- **Next 10–20 Days Upside Potential:** Reference price is the latest supplied Close of **IDR 418** from **29 July 2026**. Base-case range is **IDR 418-428**, with midpoint upside of about **1.2%**. Probability-weighted expected return is roughly **0.6%**. Bull-case upside is about **4.5%** using midpoint IDR 437. Forecast confidence is **low-to-moderate** because the data is one trading session stale and only one dated row was supplied. Upside requires a move above **IDR 428**, improving volume/OBV/MFI confirmation in updated supplied data, and no worsening in BI/Fed/Rupiah-related sentiment.

- **Risks Related to the Stock:** Main risks are weak volume confirmation, overbought momentum, `Fisher Reversal = 1.0`, stale single-row data, financing/execution risk from sukuk deployment, and domestic macro volatility. Bear-case range is **IDR 392-402**. Invalidation is **IDR 402**, the latest supplied low. Warning signals are failure to hold IDR 402, continued `On Balance Volume Decreasing = 1.0`, continued `MFI Decreasing = 1.0`, weak `Volume Ratio 20D`, or negative company/BI/Rupiah news.

- **Summary of the Analysis:** **Neutral/Wait**. SOCI has strong supplied momentum signals, but the risk-reward is not compelling before confirmation because upside/downside is about **0.9:1** using scenario midpoints. Preferred action is to wait for updated data confirming a close above **IDR 428** with better volume/flow, or avoid chasing. First profit-taking zone is **IDR 428**; second is **IDR 446** with lower confidence. Risk limit is **IDR 402**. The most important inputs are positive MACD/momentum/trend flags, weak volume/OBV/MFI confirmation, and recent sukuk/credit-rating news.

> **Disclaimer:** This analysis is an evidence-based market assessment, not a guarantee of performance or personalized financial advice. Short-term stock prices can move unpredictably, and investors should perform their own due diligence and use position sizing appropriate to their financial situation.