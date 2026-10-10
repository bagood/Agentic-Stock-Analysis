---
feature_name: "Aroon Up"
family: "Aroon"
---

# Aroon Up

## Definition

Recency of highest high

## Measurement and timing

**Unit and scale:** points; Up/Down 0..100, oscillator -100..100

**Historical lookback:** 25 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Use Up and Down for the two recency measures; use the oscillator for their difference. A position-change flag alone does not identify the new direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Aroon Up Trend](aroon-up-trend.md)
- [Aroon Change Position](aroon-change-position.md)
- [Aroon Down](aroon-down.md)
- [Aroon Down Trend](aroon-down-trend.md)

Family navigation: [Aroon](INDEX.md#aroon). Read the [agent guide](README.md) for shared interpretation rules.
