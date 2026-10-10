---
feature_name: "PVO Signal"
family: "Percentage Volume Oscillator"
---

# PVO Signal

## Definition

EMA9 of PVO

## Measurement and timing

**Unit and scale:** percentage points (2 means 2%)

**Historical lookback:** 12/26/9 EMA; change adds 5 rows; recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 2 as 2%, not 200%. Changes and histogram differences remain in percentage-point units.
- PVO compares volume EMAs. Its sign describes their volume relationship and does not by itself establish price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [PVO Histogram](pvo-histogram.md)
- [PVO Value](pvo-value.md)
- [PVO Positive](pvo-positive.md)
- [PVO Histogram Change 5D](pvo-histogram-change-5d.md)

Family navigation: [Percentage Volume Oscillator](INDEX.md#percentage-volume-oscillator). Read the [agent guide](README.md) for shared interpretation rules.
