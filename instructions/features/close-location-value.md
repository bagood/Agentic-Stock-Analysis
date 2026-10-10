---
feature_name: "Close Location Value"
family: "Price returns and momentum"
---

# Close Location Value

## Definition

(2*Close-Low-High)/(High-Low)

## Measurement and timing

**Unit and scale:** dimensionless; usually -1..1

**Historical lookback:** 1 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- With a nonzero session range, +1 places Close at High, -1 at Low, and 0 at the midpoint. A zero range leaves the denominator unavailable.
- Keep historical returns, opening gaps, intraday moves, and close location separate. A historical lookback does not define a future forecast horizon.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Log Return 10D](log-return-10d.md)
- [Price Momentum 20D](price-momentum-20d.md)
- [Log Return 3D](log-return-3d.md)
- [High Low Range Percent](high-low-range-percent.md)

Family navigation: [Price returns and momentum](INDEX.md#price-returns-and-momentum). Read the [agent guide](README.md) for shared interpretation rules.
