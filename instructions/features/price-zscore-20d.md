---
feature_name: "Price ZScore 20D"
family: "Historical price position"
---

# Price ZScore 20D

## Definition

(Close - mean(Close,20)) / population std(Close,20)

## Measurement and timing

**Unit and scale:** standard deviations

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the value in standardized units, not percentages. zscore uses rolling population standard deviation (ddof=0); a zero denominator produces null.
- Use the stated historical extreme or rolling distribution as the reference. Proximity to an extreme or a large z-score alone does not establish a future reversal or breakout.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Price ZScore 60D](price-zscore-60d.md)
- [Distance From 20D Low](distance-from-20d-low.md)
- [Distance From 20D High](distance-from-20d-high.md)
- [Distance From 60D High](distance-from-60d-high.md)

Family navigation: [Historical price position](INDEX.md#historical-price-position). Read the [agent guide](README.md) for shared interpretation rules.
