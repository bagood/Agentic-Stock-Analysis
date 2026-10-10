---
feature_name: "Fisher Transform"
family: "Fisher transform"
---

# Fisher Transform

## Definition

Ehlers Fisher transform of price

## Measurement and timing

**Unit and scale:** dimensionless transform units

**Historical lookback:** 10; recursive smoothing; trigger adds 1 and change adds 5 rows

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Distinguish the transform, previous-value trigger, spread, and change. A reversal flag identifies a comparison change without specifying the new direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Fisher Transform Trigger](fisher-transform-trigger.md)
- [Fisher Change 5D](fisher-change-5d.md)
- [Fisher Spread](fisher-spread.md)
- [Fisher Up trend](fisher-up-trend.md)

Family navigation: [Fisher transform](INDEX.md#fisher-transform). Read the [agent guide](README.md) for shared interpretation rules.
