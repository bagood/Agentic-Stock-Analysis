---
feature_name: "Non Regular Block Activity"
family: "Non-regular trading"
---

# Non Regular Block Activity

## Definition

1 when Non Regular Volume ZScore 20D > 2; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- The condition is strictly greater than 2; equality does not activate the flag. This is a volume z-score flag, not evidence of a particular participant or trade direction.
- Keep non-regular activity separate from regular-session activity. Shares, standardized activity, and average trade size describe activity without identifying buying or selling direction.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Non Regular Volume ZScore 20D](non-regular-volume-zscore-20d.md)
- [Non Regular Volume Share 20D](non-regular-volume-share-20d.md)
- [Volume ZScore 20D](volume-zscore-20d.md)
- [Volume](volume.md)

Family navigation: [Non-regular trading](INDEX.md#non-regular-trading). Read the [agent guide](README.md) for shared interpretation rules.
