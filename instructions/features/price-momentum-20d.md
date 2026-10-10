---
feature_name: "Price Momentum 20D"
family: "Price returns and momentum"
---

# Price Momentum 20D

## Definition

Close(t)/Close(t-20) - 1

## Measurement and timing

**Unit and scale:** decimal return

**Historical lookback:** 20-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Keep historical returns, opening gaps, intraday moves, and close location separate. A historical lookback does not define a future forecast horizon.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Price Momentum 10D](price-momentum-10d.md)
- [Price Momentum 5D](price-momentum-5d.md)
- [Log Return 20D](log-return-20d.md)
- [Log Return 10D](log-return-10d.md)

Family navigation: [Price returns and momentum](INDEX.md#price-returns-and-momentum). Read the [agent guide](README.md) for shared interpretation rules.
