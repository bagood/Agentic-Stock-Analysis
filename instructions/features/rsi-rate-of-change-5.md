---
feature_name: "RSI Rate of Change 5"
family: "RSI"
---

# RSI Rate of Change 5

## Definition

RSI(t) - RSI(t-5); not percentage change

## Measurement and timing

**Unit and scale:** RSI points

**Historical lookback:** RSI(14) plus 5-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 5 as a five-point RSI difference, not a 5% return or percentage change.
- Keep RSI levels, point differences, and different lookbacks separate. Use the thresholds stated in each definition rather than substituting other RSI conventions.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [RSI Value](rsi-value.md)
- [RSI Rate of Change 10](rsi-rate-of-change-10.md)
- [RSI 21](rsi-21.md)
- [RSI 7 Minus 21](rsi-7-minus-21.md)

Family navigation: [RSI](INDEX.md#rsi). Read the [agent guide](README.md) for shared interpretation rules.
