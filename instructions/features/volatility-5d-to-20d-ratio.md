---
feature_name: "Volatility 5D to 20D Ratio"
family: "Volatility"
---

# Volatility 5D to 20D Ratio

## Definition

Realized Volatility 5D / Realized Volatility 20D

## Measurement and timing

**Unit and scale:** dimensionless ratio

**Historical lookback:** 20 returns plus prior close

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the ratio using its stated numerator and denominator. A value of 1 is equality of those quantities, not automatically a neutral market signal.
- Use these features for movement magnitude and comparisons across lookbacks. Volatility alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Realized Volatility 5D](realized-volatility-5d.md)
- [Realized Volatility 20D](realized-volatility-20d.md)
- [Volatility 20D to 60D Ratio](volatility-20d-to-60d-ratio.md)
- [Realized Volatility 60D](realized-volatility-60d.md)

Family navigation: [Volatility](INDEX.md#volatility). Read the [agent guide](README.md) for shared interpretation rules.
