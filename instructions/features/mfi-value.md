---
feature_name: "MFI Value"
family: "Money Flow Index"
---

# MFI Value

## Definition

Typical-price money-flow index

## Measurement and timing

**Unit and scale:** points 0..100

**Historical lookback:** 14 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- typical_price = (High + Low + Close) / 3. Preserve that price basis where it appears in the definition.
- Distinguish MFI level, threshold flags, and slopes of prior observations. A threshold flag alone does not establish a subsequent reversal.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [MFI Overbought](mfi-overbought.md)
- [MFI Decreasing](mfi-decreasing.md)
- [MFI Oversold](mfi-oversold.md)
- [MFI Increasing](mfi-increasing.md)

Family navigation: [Money Flow Index](INDEX.md#money-flow-index). Read the [agent guide](README.md) for shared interpretation rules.
