---
feature_name: "Non Regular Value Share 60D"
family: "Non-regular trading"
---

# Non Regular Value Share 60D

## Definition

sum(Non Regular Value,60) / sum(typical_price*Volume,60)

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 60 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- typical_price = (High + Low + Close) / 3. Preserve that price basis where it appears in the definition.
- Keep non-regular activity separate from regular-session activity. Shares, standardized activity, and average trade size describe activity without identifying buying or selling direction.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Volume](volume.md)
- [Non Regular Value ZScore 60D](non-regular-value-zscore-60d.md)
- [Non Regular Value Share 20D](non-regular-value-share-20d.md)
- [Non Regular Volume Share 60D](non-regular-volume-share-60d.md)

Family navigation: [Non-regular trading](INDEX.md#non-regular-trading). Read the [agent guide](README.md) for shared interpretation rules.
