---
feature_name: "Non Regular Volume ZScore 60D"
family: "Non-regular trading"
---

# Non Regular Volume ZScore 60D

## Definition

zscore(Non Regular Volume,60)

## Measurement and timing

**Unit and scale:** standard deviations

**Historical lookback:** 60 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the value in standardized units, not percentages. zscore uses rolling population standard deviation (ddof=0); a zero denominator produces null.
- Keep non-regular activity separate from regular-session activity. Shares, standardized activity, and average trade size describe activity without identifying buying or selling direction.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Volume](volume.md)
- [Non Regular Frequency ZScore 60D](non-regular-frequency-zscore-60d.md)
- [Non Regular Volume ZScore 5D](non-regular-volume-zscore-5d.md)
- [Non Regular Value ZScore 60D](non-regular-value-zscore-60d.md)

Family navigation: [Non-regular trading](INDEX.md#non-regular-trading). Read the [agent guide](README.md) for shared interpretation rules.
