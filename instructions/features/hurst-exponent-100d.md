---
feature_name: "Hurst Exponent 100D"
family: "Market regime"
---

# Hurst Exponent 100D

## Definition

Estimated price-series persistence exponent

## Measurement and timing

**Unit and scale:** dimensionless exponent

**Historical lookback:** 100 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Use the catalog thresholds to describe the historical regime. Regime labels do not specify price direction or guarantee that the regime will persist.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Regime Persistent](regime-persistent.md)
- [Regime Choppy](regime-choppy.md)
- [Regime Mean Reverting](regime-mean-reverting.md)
- [Regime Trending](regime-trending.md)

Family navigation: [Market regime](INDEX.md#market-regime). Read the [agent guide](README.md) for shared interpretation rules.
