---
feature_name: "Open Gap Percent"
family: "Price returns and momentum"
---

# Open Gap Percent

## Definition

(Open-previous Close)/previous Close

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 2 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Keep historical returns, opening gaps, intraday moves, and close location separate. A historical lookback does not define a future forecast horizon.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [High Low Range Percent](high-low-range-percent.md)
- [Intraday Return Percent](intraday-return-percent.md)
- [Log Return 10D](log-return-10d.md)
- [Price Momentum 20D](price-momentum-20d.md)

Family navigation: [Price returns and momentum](INDEX.md#price-returns-and-momentum). Read the [agent guide](README.md) for shared interpretation rules.
