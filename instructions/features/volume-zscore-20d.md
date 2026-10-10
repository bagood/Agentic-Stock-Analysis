---
feature_name: "Volume ZScore 20D"
family: "Volume activity"
---

# Volume ZScore 20D

## Definition

zscore(Volume,20)

## Measurement and timing

**Unit and scale:** standard deviations

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the value in standardized units, not percentages. zscore uses rolling population standard deviation (ddof=0); a zero denominator produces null.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Volume](volume.md)
- [Volume ZScore 60D](volume-zscore-60d.md)
- [Up Volume Share 20D](up-volume-share-20d.md)
- [Price Volume Divergence 20D](price-volume-divergence-20d.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
