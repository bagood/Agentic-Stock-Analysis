---
feature_name: "Volume Change 1D"
family: "Volume activity"
---

# Volume Change 1D

## Definition

Volume(t)/Volume(t-1) - 1

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 1-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Volume](volume.md)
- [Volume Change 5D](volume-change-5d.md)
- [Up Volume Share 20D](up-volume-share-20d.md)
- [Price Volume Divergence 20D](price-volume-divergence-20d.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
