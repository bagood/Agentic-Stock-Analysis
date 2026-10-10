---
feature_name: "High Low Range Percent"
family: "Price returns and momentum"
---

# High Low Range Percent

## Definition

(High-Low)/Close

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 1 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Keep historical returns, opening gaps, intraday moves, and close location separate. A historical lookback does not define a future forecast horizon.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Intraday Return Percent](intraday-return-percent.md)
- [Open Gap Percent](open-gap-percent.md)
- [Log Return 10D](log-return-10d.md)
- [Price Momentum 20D](price-momentum-20d.md)

Family navigation: [Price returns and momentum](INDEX.md#price-returns-and-momentum). Read the [agent guide](README.md) for shared interpretation rules.
