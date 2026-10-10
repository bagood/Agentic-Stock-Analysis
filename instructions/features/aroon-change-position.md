---
feature_name: "Aroon Change Position"
family: "Aroon"
---

# Aroon Change Position

## Definition

1 when (Aroon Up >= Aroon Down) differs from previous row; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 25 plus previous state

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Use the corresponding level or state features to identify the direction of the change.
- Use Up and Down for the two recency measures; use the oscillator for their difference. A position-change flag alone does not identify the new direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Aroon Up](aroon-up.md)
- [Aroon Down](aroon-down.md)
- [Aroon Oscillator](aroon-oscillator.md)
- [Aroon Down Trend](aroon-down-trend.md)

Family navigation: [Aroon](INDEX.md#aroon). Read the [agent guide](README.md) for shared interpretation rules.
