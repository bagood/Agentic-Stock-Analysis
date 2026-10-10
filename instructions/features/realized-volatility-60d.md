---
feature_name: "Realized Volatility 60D"
family: "Volatility"
---

# Realized Volatility 60D

## Definition

population std(log return 1D,60) * sqrt(252)

## Measurement and timing

**Unit and scale:** annualized decimal volatility

**Historical lookback:** 60 returns plus prior close

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.20 as 20% annualized volatility. The sqrt(252) factor annualizes the historical estimate; it is not a 5-, 10-, or 20-session expected return.
- Use these features for movement magnitude and comparisons across lookbacks. Volatility alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Realized Volatility 20D](realized-volatility-20d.md)
- [Realized Volatility 5D](realized-volatility-5d.md)
- [Volatility 20D to 60D Ratio](volatility-20d-to-60d-ratio.md)
- [Volatility 5D to 20D Ratio](volatility-5d-to-20d-ratio.md)

Family navigation: [Volatility](INDEX.md#volatility). Read the [agent guide](README.md) for shared interpretation rules.
