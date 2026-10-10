---
feature_name: "MACD Non-Near 0 Positive"
family: "MACD"
---

# MACD Non-Near 0 Positive

## Definition

1 when raw histogram >= threshold; threshold is median absolute raw MACD histogram over last 50 rows, min 10, falling back to expanding median; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 12/26/9 EMA plus 50-row rolling/expanding threshold

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish MACD level, signal, histogram, and histogram change. The Near 0 flags use an adaptive raw-histogram threshold, not a fixed threshold on the normalized Percent fields.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [MACD Histogram Percent](macd-histogram-percent.md)
- [MACD Near 0](macd-near-0.md)
- [MACD Non-Near 0 Negative](macd-non-near-0-negative.md)
- [MACD Histogram Change 5D](macd-histogram-change-5d.md)

Family navigation: [MACD](INDEX.md#macd). Read the [agent guide](README.md) for shared interpretation rules.
