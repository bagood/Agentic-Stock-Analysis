---
feature_name: "Bull Power 80% Positives"
family: "Elder Ray bull and bear power"
---

# Bull Power 80% Positives

## Definition

1 when at least 8 of previous 10 Bull Power observations are > 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** EMA(13) plus prior 10 rows

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish power levels, prior-observation slopes, and the share of positive or negative observations. These describe different aspects of the same underlying series.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Bear Power 80% Negatives](bear-power-80-percent-negatives.md)
- [Bull Power Up Trend](bull-power-up-trend.md)
- [Bull Power Percent](bull-power-percent.md)
- [Bear Power Trend](bear-power-trend.md)

Family navigation: [Elder Ray bull and bear power](INDEX.md#elder-ray-bull-and-bear-power). Read the [agent guide](README.md) for shared interpretation rules.
