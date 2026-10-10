---
feature_name: "ADX Change 5D"
family: "Directional movement and ADX"
---

# ADX Change 5D

## Definition

ADX(t) - ADX(t-5)

## Measurement and timing

**Unit and scale:** points

**Historical lookback:** ADX(14) plus 5-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Preserve point units. For subtraction or change features, the sign follows the ordering in the definition and is not a percentage return.
- Separate directional balance (Plus versus Minus Directional Index) from trend strength (ADX/ADXR). Strength alone does not specify a rising or falling price trend.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [ADX Value](adx-value.md)
- [ADXR Value](adxr-value.md)
- [ADX Strong Trend](adx-strong-trend.md)
- [Plus Directional Index](plus-directional-index.md)

Family navigation: [Directional movement and ADX](INDEX.md#directional-movement-and-adx). Read the [agent guide](README.md) for shared interpretation rules.
