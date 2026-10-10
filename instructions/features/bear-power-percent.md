---
feature_name: "Bear Power Percent"
family: "Elder Ray bull and bear power"
---

# Bear Power Percent

## Definition

(Low - EMA13) / Close

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** EMA(13); recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Distinguish power levels, prior-observation slopes, and the share of positive or negative observations. These describe different aspects of the same underlying series.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Bear Power 80% Negatives](bear-power-80-percent-negatives.md)
- [Bear Power Trend](bear-power-trend.md)
- [Bull Power Percent](bull-power-percent.md)
- [Bull Power Up Trend](bull-power-up-trend.md)

Family navigation: [Elder Ray bull and bear power](INDEX.md#elder-ray-bull-and-bear-power). Read the [agent guide](README.md) for shared interpretation rules.
