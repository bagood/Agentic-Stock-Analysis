---
feature_name: "Regime Choppy"
family: "Market regime"
---

# Regime Choppy

## Definition

1 when Choppiness > 61.8; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 14 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Use the catalog thresholds to describe the historical regime. Regime labels do not specify price direction or guarantee that the regime will persist.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Choppiness Index 14D](choppiness-index-14d.md)
- [Regime Trending](regime-trending.md)
- [Regime Persistent](regime-persistent.md)
- [Regime Mean Reverting](regime-mean-reverting.md)

Family navigation: [Market regime](INDEX.md#market-regime). Read the [agent guide](README.md) for shared interpretation rules.
