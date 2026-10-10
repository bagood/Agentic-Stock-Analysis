---
feature_name: "Log Return 3D"
family: "Price returns and momentum"
---

# Log Return 3D

## Definition

log(Close(t)) - log(Close(t-3))

## Measurement and timing

**Unit and scale:** natural-log return

**Historical lookback:** 3-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- This is a log return. If a simple percentage return is needed, use 100 * (exp(value) - 1); do not relabel the raw value as an exact simple return.
- Keep historical returns, opening gaps, intraday moves, and close location separate. A historical lookback does not define a future forecast horizon.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Log Return 10D](log-return-10d.md)
- [Log Return 1D](log-return-1d.md)
- [Log Return 5D](log-return-5d.md)
- [Log Return 20D](log-return-20d.md)

Family navigation: [Price returns and momentum](INDEX.md#price-returns-and-momentum). Read the [agent guide](README.md) for shared interpretation rules.
