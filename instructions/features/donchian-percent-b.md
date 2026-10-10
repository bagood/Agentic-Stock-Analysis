---
feature_name: "Donchian Percent B"
family: "Donchian channel"
---

# Donchian Percent B

## Definition

(Close - lower band) / (upper band - lower band)

## Measurement and timing

**Unit and scale:** dimensionless ratio; may be outside 0..1

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 0 means Close is at the lower band; 1 means it is at the upper band. Values below 0 or above 1 are allowed; do not clamp them or confuse this scale with oscillator points.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Donchian Width](donchian-width.md)
- [Donchian Oversold](donchian-oversold.md)
- [Donchian Overbought](donchian-overbought.md)
- [Width Donchian Increasing](width-donchian-increasing.md)

Family navigation: [Donchian channel](INDEX.md#donchian-channel). Read the [agent guide](README.md) for shared interpretation rules.
