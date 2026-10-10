---
feature_name: "Return Volume Correlation 20D"
family: "Volume activity"
---

# Return Volume Correlation 20D

## Definition

corr(log return 1D, Volume change 1D,20)

## Measurement and timing

**Unit and scale:** correlation -1..1

**Historical lookback:** 20 plus prior observation

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Positive and negative values describe the sign of the historical association; zero describes no linear association in that window. Correlation does not establish causation or forecast direction.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Log Return 1D](log-return-1d.md)
- [Volume Change 1D](volume-change-1d.md)
- [Volume ZScore 20D](volume-zscore-20d.md)
- [Volume](volume.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
