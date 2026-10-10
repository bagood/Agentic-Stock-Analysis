---
feature_name: "OBV to MA20 Ratio"
family: "On Balance Volume"
---

# OBV to MA20 Ratio

## Definition

OBV / mean(OBV,20)

## Measurement and timing

**Unit and scale:** dimensionless ratio

**Historical lookback:** cumulative history plus 20 rows

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the ratio using its stated numerator and denominator. A value of 1 is equality of those quantities, not automatically a neutral market signal.
- The denominator is the mean of signed cumulative OBV, not its mean absolute value. A ratio above 1 alone does not establish positive OBV or accumulation.
- Distinguish cumulative OBV slope, its ratio to a moving average, and normalized change. Cumulative history and denominator choice affect interpretation.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [OBV Change 5D Normalized](obv-change-5d-normalized.md)
- [On Balance Volume Increasing](on-balance-volume-increasing.md)
- [On Balance Volume Decreasing](on-balance-volume-decreasing.md)

Family navigation: [On Balance Volume](INDEX.md#on-balance-volume). Read the [agent guide](README.md) for shared interpretation rules.
