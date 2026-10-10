---
feature_name: "Accumulation Distribution Line Decreasing"
family: "Accumulation Distribution Line"
---

# Accumulation Distribution Line Decreasing

## Definition

1 when normalized least-squares slope of previous 5 cumulative ADL observations < 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** cumulative history plus prior 5-row slope

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish cumulative ADL slope from its normalized change. These features depend on cumulative history and are not raw money-flow amounts.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Accumulation Distribution Line Increasing](accumulation-distribution-line-increasing.md)
- [ADL Change 5D Normalized](adl-change-5d-normalized.md)

Family navigation: [Accumulation Distribution Line](INDEX.md#accumulation-distribution-line). Read the [agent guide](README.md) for shared interpretation rules.
