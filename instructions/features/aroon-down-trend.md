---
feature_name: "Aroon Down Trend"
family: "Aroon"
---

# Aroon Down Trend

## Definition

1 when Aroon Down >= 70; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 25 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Use Up and Down for the two recency measures; use the oscillator for their difference. A position-change flag alone does not identify the new direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Aroon Down](aroon-down.md)
- [Aroon Up Trend](aroon-up-trend.md)
- [Aroon Change Position](aroon-change-position.md)
- [Aroon Up](aroon-up.md)

Family navigation: [Aroon](INDEX.md#aroon). Read the [agent guide](README.md) for shared interpretation rules.
