---
feature_name: "ADL Change 5D Normalized"
family: "Accumulation Distribution Line"
---

# ADL Change 5D Normalized

## Definition

(ADL(t)-ADL(t-5)) / mean(abs(ADL),20)

## Measurement and timing

**Unit and scale:** dimensionless ratio

**Historical lookback:** cumulative history plus 20 rows and 5-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the ratio using its stated numerator and denominator. A value of 1 is equality of those quantities, not automatically a neutral market signal.
- Distinguish cumulative ADL slope from its normalized change. These features depend on cumulative history and are not raw money-flow amounts.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Accumulation Distribution Line Increasing](accumulation-distribution-line-increasing.md)
- [Accumulation Distribution Line Decreasing](accumulation-distribution-line-decreasing.md)

Family navigation: [Accumulation Distribution Line](INDEX.md#accumulation-distribution-line). Read the [agent guide](README.md) for shared interpretation rules.
