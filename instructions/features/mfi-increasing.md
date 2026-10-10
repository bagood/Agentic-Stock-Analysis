---
feature_name: "MFI Increasing"
family: "Money Flow Index"
---

# MFI Increasing

## Definition

1 when normalized least-squares slope of previous 5 MFI observations > 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** MFI(14) plus prior 5-row slope

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish MFI level, threshold flags, and slopes of prior observations. A threshold flag alone does not establish a subsequent reversal.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [MFI Overbought](mfi-overbought.md)
- [MFI Decreasing](mfi-decreasing.md)
- [MFI Oversold](mfi-oversold.md)
- [MFI Value](mfi-value.md)

Family navigation: [Money Flow Index](INDEX.md#money-flow-index). Read the [agent guide](README.md) for shared interpretation rules.
