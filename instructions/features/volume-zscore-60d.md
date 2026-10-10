---
feature_name: "Volume ZScore 60D"
family: "Volume activity"
---

# Volume ZScore 60D

## Definition

zscore(Volume,60)

## Measurement and timing

**Unit and scale:** standard deviations

**Historical lookback:** 60 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the value in standardized units, not percentages. zscore uses rolling population standard deviation (ddof=0); a zero denominator produces null.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Volume](volume.md)
- [Volume ZScore 20D](volume-zscore-20d.md)
- [Return Volume Correlation 60D](return-volume-correlation-60d.md)
- [Volume Change 1D](volume-change-1d.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
