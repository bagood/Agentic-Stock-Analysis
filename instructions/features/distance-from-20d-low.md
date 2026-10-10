---
feature_name: "Distance From 20D Low"
family: "Historical price position"
---

# Distance From 20D Low

## Definition

(Close - min(Low,20)) / min(Low,20)

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Use the stated historical extreme or rolling distribution as the reference. Proximity to an extreme or a large z-score alone does not establish a future reversal or breakout.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Distance From 60D Low](distance-from-60d-low.md)
- [Distance From 20D High](distance-from-20d-high.md)
- [Distance From 60D High](distance-from-60d-high.md)
- [Price ZScore 20D](price-zscore-20d.md)

Family navigation: [Historical price position](INDEX.md#historical-price-position). Read the [agent guide](README.md) for shared interpretation rules.
