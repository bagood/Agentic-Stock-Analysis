---
feature_name: "RSI Value"
family: "RSI"
---

# RSI Value

## Definition

Relative strength index

## Measurement and timing

**Unit and scale:** points 0..100

**Historical lookback:** 14; recursive smoothing

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Keep RSI levels, point differences, and different lookbacks separate. Use the thresholds stated in each definition rather than substituting other RSI conventions.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [RSI 21](rsi-21.md)
- [RSI Rate of Change 5](rsi-rate-of-change-5.md)
- [RSI 7 Minus 21](rsi-7-minus-21.md)
- [RSI Up Trend](rsi-up-trend.md)

Family navigation: [RSI](INDEX.md#rsi). Read the [agent guide](README.md) for shared interpretation rules.
