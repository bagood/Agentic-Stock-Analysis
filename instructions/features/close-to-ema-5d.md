---
feature_name: "Close to EMA 5D"
family: "Moving-average distance and spread"
---

# Close to EMA 5D

## Definition

(Close - EMA5) / EMA5

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** EMA(5); recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Use the stated EMA and denominator. Close-to-EMA distance and fast-to-slow EMA spread measure different comparisons.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Close to EMA 20D](close-to-ema-20d.md)
- [Close to EMA 50D](close-to-ema-50d.md)
- [Close to EMA 10D](close-to-ema-10d.md)
- [EMA 5D to 20D Spread](ema-5d-to-20d-spread.md)

Family navigation: [Moving-average distance and spread](INDEX.md#moving-average-distance-and-spread). Read the [agent guide](README.md) for shared interpretation rules.
