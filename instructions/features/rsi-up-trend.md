---
feature_name: "RSI Up Trend"
family: "RSI"
---

# RSI Up Trend

## Definition

1 when RSI >= 65; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 14 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Keep RSI levels, point differences, and different lookbacks separate. Use the thresholds stated in each definition rather than substituting other RSI conventions.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [RSI Value](rsi-value.md)
- [RSI Down Trend](rsi-down-trend.md)
- [RSI 21](rsi-21.md)
- [RSI Rate of Change 5](rsi-rate-of-change-5.md)

Family navigation: [RSI](INDEX.md#rsi). Read the [agent guide](README.md) for shared interpretation rules.
