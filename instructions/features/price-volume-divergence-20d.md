---
feature_name: "Price Volume Divergence 20D"
family: "Volume activity"
---

# Price Volume Divergence 20D

## Definition

Log Return 5D * Volume ZScore 20D

## Measurement and timing

**Unit and scale:** log return times standard deviations

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- This is a product, not a difference. A positive value can result from two positive or two negative inputs; inspect the components before describing the relationship.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Log Return 5D](log-return-5d.md)
- [Volume ZScore 20D](volume-zscore-20d.md)
- [Volume](volume.md)
- [Up Volume Share 20D](up-volume-share-20d.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
