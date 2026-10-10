---
feature_name: "Up Volume Share 20D"
family: "Volume activity"
---

# Up Volume Share 20D

## Definition

sum(Volume where Close > previous Close,20) / sum(Volume,20)

## Measurement and timing

**Unit and scale:** fraction 0..1

**Historical lookback:** 20 plus prior close

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.60 as a 60% share. Keep the definition’s basis: a share of days and a share of volume are different measures.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Volume](volume.md)
- [Price Volume Divergence 20D](price-volume-divergence-20d.md)
- [Dollar Volume Ratio 20D](dollar-volume-ratio-20d.md)
- [Return Volume Correlation 20D](return-volume-correlation-20d.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
