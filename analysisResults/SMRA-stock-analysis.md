**1. Analysis timestamp, news cut-off, and supplied data cut-off**

| Item | Detail |
|---|---|
| Company | PT Summarecon Agung Tbk |
| Ticker / exchange | SMRA / IDX |
| Analysis timestamp | 30 July 2026, 23:09 WIB, Asia/Jakarta |
| News research cut-off | 30 July 2026, 23:09 WIB |
| Supplied technical-data cut-off | 29 July 2026 |
| Forecast horizon | 10-20 calendar days: 31 July 2026 to 19 August 2026 |
| Estimated IDX sessions | About 13 trading sessions, excluding weekends and 17 August 2026 Independence Day market holiday |
| Investor currency | IDR |
| Risk tolerance | Moderate |
| Reference price | IDR 322, latest supplied `Close` |

**2. Input validation and data-freshness assessment**

The supplied technical dataset contains one dated record, `2026-07-29`. It was parsed as a date and treated as the latest valid row.

| Validation item | Result |
|---|---|
| Required OHLCV fields present | Pass |
| Prices positive | Pass |
| Volume non-negative | Pass |
| `High >= max(Open, Close)` | Pass: 330 >= 328 and 322 |
| `Low <= min(Open, Close)` | Pass: 316 <= 328 and 322 |
| `High >= Low` | Pass |
| Duplicate dates | None |
| Missing / non-finite values | None detected |
| Sorting issue | Not applicable; one record |
| Freshness | Stale by one completed trading session if 30 July 2026 trading has closed, but not more than three trading sessions old |

Latest supplied OHLCV, from **Provided technical dataset**:

| Date | Open | High | Low | Close | Volume |
|---|---:|---:|---:|---:|---:|
| 2026-07-29 | 328 | 330 | 316 | 322 | 10,582,300 |

Because the latest supplied data is one session behind the analysis timestamp, an actionable forecast is possible only with **reduced confidence**. A fresh 30 July 2026 OHLCV row would materially improve reliability.

**3. Supplied OHLCV and technical snapshot**

The latest candle closed below the open: `Open 328`, `Close 322`, with an intraday range of `316-330`. This is a bearish daily candle inside a broader mixed technical setup.

| Signal group | Supplied field and value | Implication |
|---|---|---|
| Trend | `Aroon Up Trend = 1.0`, `Aroon Down Trend = 0.0` | Uptrend condition active |
| Directional index | `Strong Plus Directional Index = 1.0`, `Weak Minus Directional Index = 1.0` | Positive directional force exists, but bearish pressure is not absent |
| Bull / bear power | `Bull Power Up Trend = 1.0`, `Bull Power 80% Positives = 1.0`, `Bear Power 80% Negatives = 0.0` | Bullish trend support |
| ATR state | `ATR Bullish = 0.0`, `ATR Bearish = 1.0` | Volatility/range condition is bearish |
| MACD | `MACD Non-Near 0 Positive = 1.0`, `MACD Near 0 = 0.0` | Momentum remains positive, not neutral |
| RSI | `RSI Value = 62.43`, `RSI Rate of Change 5 = -13.64`, `RSI Rate of Change 10 = 7.68` | RSI is constructive but short-term momentum has cooled |
| Stochastic | `Stochastic K Value = 64.38` | Mid-to-upper range, not overbought |
| Channels | `Keltner Percent B = 0.81`, `Donchian Percent B = 0.71`, `Bollinger Percent B = 0.75` | Price sits in the upper half of multiple envelopes |
| Volatility width | `Width Keltner Increasing = 1.0`, `Width Donchian Increasing = 1.0`, `Width Bollinger Increasing = 1.0` | Expansion phase; can support continuation but also increases downside risk |
| Volume / flow | `Volume Ratio 20D = 0.6293` | Latest volume is below its 20-day reference ratio |
| OBV | `On Balance Volume Decreasing = 1.0`, `OBV to MA20 Ratio = 1.0430` | OBV remains above MA20 but is deteriorating |
| MFI | `MFI Value = 78.90`, `MFI Decreasing = 1.0` | Money flow is elevated but rolling over |
| CMF | `Positive CMF = 1.0`, `Strong Positive CMF = 0.0` | Mild accumulation signal |
| A/D line | `Accumulation Distribution Line Decreasing = 1.0` | Distribution pressure contradicts CMF |
| Zig Zag | `Zig Zag Decreasing = 1.0` | Reversal/down-leg condition active |
| Price momentum | `Price Momentum 5D = -3.01%`, `Price Momentum 10D = +11.03%`, `Price Momentum 20D = +19.26%` | Strong 10-20 day momentum, but 5-day pullback |
| Foreign/domestic positioning | `Foreign to Domestic 15 Days Ownership = -0.2871`, `60 Days = -0.3783`, `90 Days = -1.2071` | Supplied positioning implies foreign ownership pressure versus domestic |

Technical read: SMRA has medium-term upside momentum, but the most recent row shows a short-term loss of thrust: bearish candle, bearish ATR flag, falling OBV/MFI/A-D, negative 5D momentum, and declining Zig Zag. This is not a clean breakout setup.

**4. Key company news and catalysts**

Recent company-specific news is moderately constructive but not enough to override the mixed technical deterioration.

| Date / publication | News | Directional read |
|---|---|---|
| 28 July 2026, Kontan | SMRA reportedly booked 1H26 pre-sales of Rp2.54 trillion, up 17.1% YoY; Serpong remained the main contributor with reported growth of 18.9% YoY. | Bullish for operating sentiment, but likely partly reflected because published before the 29 July supplied technical row |
| 17 June 2026, company news | Summarecon reported 2025 marketing sales of Rp5.53 trillion, above its Rp5 trillion target; 2025 revenue and net profit were also reported in the company release; 2026 marketing sales target set at Rp5.2 trillion. | Bullish medium-term context |
| 15 June 2026 / KSEI | Cash dividend of IDR 5 per share; cum date 22 June, record date 24 June, distribution date 10 July 2026. | Already passed; not a fresh 10-20 day catalyst |
| 11 June 2026, Detik | Management targeted 2026 marketing sales of Rp5.2 trillion despite BI-rate and rupiah pressure. | Mixed: target is supportive, macro headwind acknowledged |
| 12 July 2026, Kontan tag listing | Headline references SMRA bond maturity and Pefindo readiness of funds, but full detail was not independently verified in accessible search result. | Potential credit/liquidity catalyst, but insufficient detail from accessible source |

No clearly confirmed dividend, rights issue, split, AGM, or earnings event inside 31 July-19 August 2026 was found in accessible recent sources. The most relevant near-term catalyst is whether the market continues to reward the 1H26 pre-sales update or sells into it.

**5. Indonesia market news**

Domestic macro news is a material headwind for property developers.

Bank Indonesia’s 21-22 July 2026 meeting kept the BI-Rate at 5.75%, while emphasizing rupiah stability, foreign portfolio inflows, liquidity support, and macroprudential incentives including for construction, real estate, and housing. For SMRA, the supportive part is that BI is trying to preserve liquidity and credit flow; the negative part is that elevated rates can pressure mortgage affordability and property demand.

The Jakarta Post reported on 30 June 2026 that Indonesia’s property sector faced a tougher road, citing weaker home sales and pressure from higher rates. This is directly relevant to SMRA because pre-sales and buyer financing sensitivity matter for developers.

Reports from FT and WSJ in late July 2026 described investor unease after Bank Indonesia Governor Perry Warjiyo’s unexpected resignation. This is a market-wide risk for Indonesian equities and the rupiah. For SMRA, the transmission path is higher equity risk premium, weaker foreign appetite, and potentially tighter or costlier funding conditions if policy uncertainty persists.

**6. Global market news**

Global conditions are not a direct SMRA earnings driver in the way commodity prices are for miners, but they affect Indonesia through rates, the US dollar, capital flows, and risk appetite.

Recent global-rate uncertainty around the US Federal Reserve, reported by Investor’s Business Daily, matters because expectations of tighter US policy can support the dollar and pressure emerging-market currencies. For SMRA, a weaker rupiah and higher domestic rates can pressure construction costs, imported inputs, consumer confidence, and mortgage affordability.

This is an indirect but meaningful link. It does not justify using global equity data or online prices as technical inputs.

**7. Integrated technical-and-news assessment**

The short-term setup is **Conditionally Attractive**, not outright attractive.

Bullish evidence: 10D and 20D supplied price momentum remain strong, trend indicators are still positive, and recent news reports solid pre-sales momentum. Bearish evidence: the latest candle is weak, ATR bearish is active, 5D momentum is negative, OBV/MFI/A-D are deteriorating, volume participation is light versus the supplied 20D ratio, and domestic macro risk is elevated.

This combination favors a **confirmation-based approach**. Buying without a fresh confirmation risks entering during a pullback after a strong 20-day move.

**8. Near-term catalyst calendar**

| Expected date | Catalyst | Direction | Magnitude / timing | Priced in? | Confirmation / invalidation |
|---|---|---|---|---|---|
| 31 Jul-19 Aug 2026 | Market digestion of reported 1H26 pre-sales strength | Bullish if buyers return | Short-term sentiment effect | Partly priced in; news was published 28 July | Confirmation: move above latest supplied high 330 with stronger supplied volume data |
| 31 Jul-19 Aug 2026 | Domestic rate/rupiah/policy sentiment after BI leadership uncertainty | Bearish/uncertain | Can affect IDX risk appetite quickly | Not fully knowable | Invalidation: renewed broad foreign outflow/rupiah stress reported in news |
| 17 Aug 2026 | IDX closed for Independence Day | Neutral | Reduces sessions/liquidity around holiday | Known | Watch liquidity before/after holiday |
| Any update in window | Further SMRA pre-sales, bond, project, or earnings-related disclosure | Uncertain | Could reprice stock if material | Not known | Needs official IDX/company confirmation |

**9. Bull, base, and bear scenarios**

Because only one OHLCV row is supplied, exact support/resistance and statistically defensible price targets are **not reliably estimable**. The only defensible levels from the supplied data are the latest row’s `Low 316`, `Close 322`, and `High 330`.

| Scenario | Conditions | Price target / range | Return calculation | Probability |
|---|---|---:|---|---:|
| Bull case | Price reclaims latest supplied high; pre-sales news continues to be rewarded; domestic sentiment stabilizes | Not reliably estimable; minimum confirmation above 330 | If 330 is used only as confirmation: `(330 - 322) / 322 x 100 = +2.5%` | 30% |
| Base case | Consolidation after strong 20D momentum; news supportive but volume/flow not confirming | Not reliably estimable; likely around 316-330 technical reference band | At 322: `(322 - 322) / 322 x 100 = 0.0%`; range endpoints: 316 = -1.9%, 330 = +2.5% | 45% |
| Bear case | Weak 5D momentum extends; distribution/OBV/MFI weakness dominates; macro risk worsens | Not reliably estimable; latest supplied low 316 is first invalidation reference | `(316 - 322) / 322 x 100 = -1.9%` to first reference level | 25% |

Probability-weighted expected return is **not reliably estimable** because scenario price targets beyond the latest single-day high/low cannot be derived responsibly from one supplied OHLCV row.

**10. Risk matrix and risk controls**

| Risk | Probability | Impact | Warning indicator | Risk-control response |
|---|---|---|---|---|
| Pullback after strong 20D move | Medium | Medium | Failure to hold latest supplied low 316 | Avoid new entry or reduce exposure |
| Weak volume confirmation | Medium | Medium | `Volume Ratio 20D = 0.6293` remains low in updated supplied data | Require volume confirmation before adding |
| Distribution pressure | Medium | Medium | `OBV Decreasing = 1`, `MFI Decreasing = 1`, `A/D Line Decreasing = 1` persist | Treat rallies as suspect until flow improves |
| Macro/rate pressure on property | Medium | High | New BI/rupiah/rate stress news | Lower position size; avoid chasing |
| Data freshness | Medium | Medium | No updated OHLCV after 29 July | Do not rely on this beyond a diagnostic window |
| Liquidity/manipulation risk | Not estimable | Not estimable | Insufficient supplied liquidity history | Need updated multi-day volume dataset |

Risk controls, using only supplied levels:

| Control | Level / assessment |
|---|---|
| Preferred entry zone | Not cleanly estimable; only a cautious reference is 316-322 if updated data confirms stabilization |
| Confirmation level | Above latest supplied high: 330 |
| Invalidation level | Below latest supplied low: 316 |
| Stop-loss / risk limit | Not fully estimable from supplied data; a rules-based exit below 316 is the only supplied-price invalidation reference |
| First profit-taking zone | Not reliably estimable |
| Second profit-taking zone | Not reliably estimable |
| Upside-to-downside ratio | Not defensible beyond 330 vs 316 single-row reference |
| Position sizing | Moderate risk: smaller-than-normal starter only after confirmation; avoid full allocation without fresh data |

**11. Final assessment**

Judgment: **Neutral/Wait to Conditionally Attractive**.

SMRA has a credible bullish narrative from reported 1H26 pre-sales strength and still-positive 10D/20D momentum in the supplied dataset. However, the latest supplied technical row shows short-term deterioration: bearish candle, bearish ATR flag, negative 5D momentum, weak volume ratio, falling OBV/MFI/A-D, and `Zig Zag Decreasing = 1.0`.

The responsible approach is to wait for confirmation above the latest supplied high of 330, ideally with updated supplied OHLCV showing stronger volume and improved flow indicators. Without that, the risk-adjusted setup is not strong enough for a moderate-risk investor to chase.

Strongest bullish items:
| Source | Item |
|---|---|
| Provided technical dataset | `Price Momentum 10D = +11.03%`, `Price Momentum 20D = +19.26%` |
| Provided technical dataset | `Aroon Up Trend = 1.0`, `Strong Plus Directional Index = 1.0`, positive MACD flag |
| Kontan / company context | Reported 1H26 pre-sales growth and Serpong strength |

Strongest bearish items:
| Source | Item |
|---|---|
| Provided technical dataset | `ATR Bearish = 1.0`, bearish latest candle |
| Provided technical dataset | `Price Momentum 5D = -3.01%`, `Zig Zag Decreasing = 1.0` |
| News | Property-sector pressure from elevated rates and domestic policy/rupiah uncertainty |

No internet-sourced OHLCV, price, volume, technical indicator, target price, or market-data figure was used as a technical input.

**12. News sources**

- Bank Indonesia, 22 July 2026: BI-Rate held at 5.75%: https://www.bi.go.id/en/publikasi/ruang-media/news-release/Pages/sp_2814226.aspx  
- Summarecon official news, 17 June 2026: 2025 marketing sales and 2026 target: https://www.summarecon.com/media/news/summarecon-remains-committed-to-prioritizing-innovation-and-quality-in-facing-economic-challenges  
- Summarecon announcements page, crawled last week: dividend and public expose announcements: https://www.summarecon.com/index.php/investor-info/announcements  
- KSEI SMRA corporate action page, crawled 2 days ago: dividend schedule: https://web.ksei.co.id/services/registered-securities/shares/lc/SMRA?setLocale=id-ID  
- Kontan, 28 July 2026: SMRA 1H26 pre-sales and Serpong contribution: https://insight.kontan.co.id/news/kawasan-serpong-tetap-jadi-andalan-pt-summarecon-agung-tbk-smra  
- Detik Properti, 11 June 2026: SMRA 2026 sales target amid BI-rate/rupiah pressure: https://www.detik.com/properti/foto-berita/d-8528296/bi-rate-naik-summarecon-bidik-sales-rp-5-2-t  
- The Jakarta Post, 30 June 2026: Indonesia property-sector headwinds: https://www.thejakartapost.com/business/2026/06/30/a-tougher-road-ahead-for-the-property-sector  
- IDX trading hours: https://www.idx.id/en/products-services/trading-hours-and-mechanism/  
- IDX 2026 holiday reference, including 17 August 2026 closure: https://market-holiday.com/markets/idx/holidays/2026  
- WSJ, published 3 days before analysis: BI governor resignation: https://www.wsj.com/economy/central-banking/indonesia-central-bank-chief-resigns-unexpectedly-36620c11  
- FT, published 30 July 2026: Indonesia market and policy uncertainty: https://www.ft.com/content/b081b88e-5f8b-4a04-9a7f-67cda439e237  
- Investor’s Business Daily, 29 July 2026: Fed-rate uncertainty: https://www.investors.com/news/federal-reserve-meeting-july-surprise-rate-hike-possible-sp-500/  

- **Next 10–20 Days Upside Potential:** Reference price is IDR 322 from the supplied technical-data date of 29 July 2026. Base-case target is **not reliably estimable** from one supplied OHLCV row; the practical base reference is consolidation around the supplied 316-330 range, or -1.9% to +2.5% versus 322. Probability-weighted expected return is **not reliably estimable**. Bull-case upside is only defensibly framed as confirmation above 330, equal to at least `(330 - 322) / 322 x 100 = +2.5%` before any further upside can be assessed. Forecast confidence: **Low-to-moderate** because technical data is one session stale and only one OHLCV row was provided. Upside requires renewed buying above 330, stronger updated volume/flow, and no deterioration in Indonesian rate/rupiah/property-sector news.

- **Risks Related to the Stock:** Main risks are short-term technical deterioration, stale one-session technical data, weak supplied volume ratio, falling OBV/MFI/A-D, property-sector sensitivity to high rates, rupiah/policy uncertainty, and insufficient multi-day liquidity history. Downside beyond the latest supplied low is **not reliably estimable**; first invalidation reference is below 316. Warning signals are failure to reclaim 330, break below 316, continued negative 5D momentum, continued decreasing OBV/MFI/A-D, and adverse BI/rupiah or property-demand news.

- **Summary of the Analysis:** **Neutral/Wait** shifting to **Conditionally Attractive** only on confirmation above 330 with stronger updated supplied volume/flow data. Preferred entry is not cleanly estimable; a cautious moderate-risk approach would wait for confirmation rather than chase. Profit-taking zones and full risk-reward ratio are **not defensibly estimable** from the supplied data. The most important items are positive 10D/20D momentum, reported 1H26 pre-sales strength, and the contradiction from bearish ATR/negative 5D momentum/falling volume-flow indicators.

> **Disclaimer:** This analysis is an evidence-based market assessment, not a guarantee of performance or personalized financial advice. Short-term stock prices can move unpredictably, and investors should perform their own due diligence and use position sizing appropriate to their financial situation.