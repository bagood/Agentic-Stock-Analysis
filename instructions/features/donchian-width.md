---
feature_name: "Donchian Width"
family: "Donchian channel"
---

# Donchian Width

## Definition

(upper band - lower band) / centerline

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Width Donchian Increasing](width-donchian-increasing.md)
- [Width Donchian Decreasing](width-donchian-decreasing.md)
- [Donchian Oversold](donchian-oversold.md)
- [Donchian Overbought](donchian-overbought.md)

Family navigation: [Donchian channel](INDEX.md#donchian-channel). Read the [agent guide](README.md) for shared interpretation rules.
