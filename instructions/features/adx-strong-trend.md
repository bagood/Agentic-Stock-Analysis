---
feature_name: "ADX Strong Trend"
family: "Directional movement and ADX"
---

# ADX Strong Trend

## Definition

1 when ADX Value >= 25; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 14 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Separate directional balance (Plus versus Minus Directional Index) from trend strength (ADX/ADXR). Strength alone does not specify a rising or falling price trend.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [ADX Value](adx-value.md)
- [Positive Direction](positive-direction.md)
- [ADX Change 5D](adx-change-5d.md)
- [Plus Directional Index](plus-directional-index.md)

Family navigation: [Directional movement and ADX](INDEX.md#directional-movement-and-adx). Read the [agent guide](README.md) for shared interpretation rules.
