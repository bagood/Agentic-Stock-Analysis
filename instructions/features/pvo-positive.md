---
feature_name: "PVO Positive"
family: "Percentage Volume Oscillator"
---

# PVO Positive

## Definition

1 when PVO > 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 12/26/9 EMA; recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- PVO compares volume EMAs. Its sign describes their volume relationship and does not by itself establish price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [PVO Value](pvo-value.md)
- [PVO Signal](pvo-signal.md)
- [PVO Histogram](pvo-histogram.md)
- [PVO Histogram Change 5D](pvo-histogram-change-5d.md)

Family navigation: [Percentage Volume Oscillator](INDEX.md#percentage-volume-oscillator). Read the [agent guide](README.md) for shared interpretation rules.
