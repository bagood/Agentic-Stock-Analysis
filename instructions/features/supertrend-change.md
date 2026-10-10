---
feature_name: "SuperTrend Change"
family: "SuperTrend"
---

# SuperTrend Change

## Definition

1 when Bullish flag changes from previous row (initial diff filled with 0); 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** ATR(10) plus previous state

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Use the corresponding level or state features to identify the direction of the change.
- Use the Bullish and Bearish flags to identify the reported band state. The Change flag records a state change without specifying its direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [SuperTrend Bullish](supertrend-bullish.md)
- [SuperTrend Bearish](supertrend-bearish.md)

Family navigation: [SuperTrend](INDEX.md#supertrend). Read the [agent guide](README.md) for shared interpretation rules.
