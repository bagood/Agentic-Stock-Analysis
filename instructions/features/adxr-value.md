---
feature_name: "ADXR Value"
family: "Directional movement and ADX"
---

# ADXR Value

## Definition

Average directional movement rating

## Measurement and timing

**Unit and scale:** index points

**Historical lookback:** 14; recursive smoothing (ADXR also prior ADX)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Do not replace ADXR with ADX; they are separately supplied strength measures.
- Separate directional balance (Plus versus Minus Directional Index) from trend strength (ADX/ADXR). Strength alone does not specify a rising or falling price trend.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [ADX Value](adx-value.md)
- [ADX Strong Trend](adx-strong-trend.md)
- [Plus Directional Index](plus-directional-index.md)
- [Positive Direction](positive-direction.md)

Family navigation: [Directional movement and ADX](INDEX.md#directional-movement-and-adx). Read the [agent guide](README.md) for shared interpretation rules.
