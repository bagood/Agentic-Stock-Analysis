---
feature_name: "Dollar Volume Ratio 20D"
family: "Volume activity"
---

# Dollar Volume Ratio 20D

## Definition

Close*Volume / mean(Close*Volume,20); local IDR traded-value proxy despite name

## Measurement and timing

**Unit and scale:** dimensionless ratio

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the ratio using its stated numerator and denominator. A value of 1 is equality of those quantities, not automatically a neutral market signal.
- Despite its name, the numerator is a local IDR traded-value proxy. Do not treat it as USD volume or apply currency conversion from the name.
- Distinguish volume levels relative to history, volume changes, and return/volume relationships. Elevated activity alone does not specify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Volume](volume.md)
- [Volume Ratio 20D](volume-ratio-20d.md)
- [Up Volume Share 20D](up-volume-share-20d.md)
- [Price Volume Divergence 20D](price-volume-divergence-20d.md)

Family navigation: [Volume activity](INDEX.md#volume-activity). Read the [agent guide](README.md) for shared interpretation rules.
