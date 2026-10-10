---
feature_name: "Bollinger Width"
family: "Bollinger bands"
---

# Bollinger Width

## Definition

(upper band - lower band) / centerline

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 20, standard-deviation multiplier 2

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Width Bollinger Increasing](width-bollinger-increasing.md)
- [Width Bollinger Decreasing](width-bollinger-decreasing.md)
- [Bollinger Oversold](bollinger-oversold.md)
- [Bollinger Percent B](bollinger-percent-b.md)

Family navigation: [Bollinger bands](INDEX.md#bollinger-bands). Read the [agent guide](README.md) for shared interpretation rules.
