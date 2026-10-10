---
feature_name: "Non Regular Average Trade Volume 1D"
family: "Non-regular trading"
---

# Non Regular Average Trade Volume 1D

## Definition

Non Regular Volume / Non Regular Frequency

## Measurement and timing

**Unit and scale:** shares per trade

**Historical lookback:** 1 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Keep non-regular activity separate from regular-session activity. Shares, standardized activity, and average trade size describe activity without identifying buying or selling direction.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Volume](volume.md)
- [Non Regular Average Trade Value 1D](non-regular-average-trade-value-1d.md)
- [Non Regular Volume Share 1D](non-regular-volume-share-1d.md)
- [Non Regular Value Share 1D](non-regular-value-share-1d.md)

Family navigation: [Non-regular trading](INDEX.md#non-regular-trading). Read the [agent guide](README.md) for shared interpretation rules.
