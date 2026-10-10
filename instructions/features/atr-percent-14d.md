---
feature_name: "ATR Percent 14D"
family: "Volatility"
---

# ATR Percent 14D

## Definition

EWM(true range, alpha=1/14, adjust=False, min_periods=14) / Close

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 14; recursive history and prior close

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Use these features for movement magnitude and comparisons across lookbacks. Volatility alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Realized Volatility 60D](realized-volatility-60d.md)
- [Realized Volatility 20D](realized-volatility-20d.md)
- [Realized Volatility 5D](realized-volatility-5d.md)
- [Volatility 5D to 20D Ratio](volatility-5d-to-20d-ratio.md)

Family navigation: [Volatility](INDEX.md#volatility). Read the [agent guide](README.md) for shared interpretation rules.
