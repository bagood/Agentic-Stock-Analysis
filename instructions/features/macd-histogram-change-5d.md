---
feature_name: "MACD Histogram Change 5D"
family: "MACD"
---

# MACD Histogram Change 5D

## Definition

MACD Histogram Percent(t) - MACD Histogram Percent(t-5)

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 12/26/9 EMA; change adds 5-row difference; recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Distinguish MACD level, signal, histogram, and histogram change. The Near 0 flags use an adaptive raw-histogram threshold, not a fixed threshold on the normalized Percent fields.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [MACD Histogram Percent](macd-histogram-percent.md)
- [MACD Non-Near 0 Positive](macd-non-near-0-positive.md)
- [MACD Percent](macd-percent.md)
- [MACD Non-Near 0 Negative](macd-non-near-0-negative.md)

Family navigation: [MACD](INDEX.md#macd). Read the [agent guide](README.md) for shared interpretation rules.
