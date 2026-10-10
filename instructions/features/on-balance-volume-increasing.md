---
feature_name: "On Balance Volume Increasing"
family: "On Balance Volume"
---

# On Balance Volume Increasing

## Definition

1 when normalized least-squares slope of previous 5 cumulative OBV observations > 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** cumulative history plus prior 5-row slope

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish cumulative OBV slope, its ratio to a moving average, and normalized change. Cumulative history and denominator choice affect interpretation.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [On Balance Volume Decreasing](on-balance-volume-decreasing.md)
- [OBV Change 5D Normalized](obv-change-5d-normalized.md)
- [OBV to MA20 Ratio](obv-to-ma20-ratio.md)

Family navigation: [On Balance Volume](INDEX.md#on-balance-volume). Read the [agent guide](README.md) for shared interpretation rules.
