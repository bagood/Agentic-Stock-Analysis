---
feature_name: "Foreign Net Intensity EMA 5D Minus 20D"
family: "Foreign flow"
---

# Foreign Net Intensity EMA 5D Minus 20D

## Definition

EMA5(Net Intensity 1D) - EMA20(Net Intensity 1D)

## Measurement and timing

**Unit and scale:** ratio difference

**Historical lookback:** 5/20 EMA; recursive history

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- This is a difference between ratio-valued quantities, not their percentage rate of change. Preserve the stated ordering of the subtraction.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Foreign Net Intensity 1D](foreign-net-intensity-1d.md)
- [Foreign Net Intensity 5D](foreign-net-intensity-5d.md)
- [Foreign Net Intensity 20D](foreign-net-intensity-20d.md)
- [Foreign Net Intensity Acceleration 5D](foreign-net-intensity-acceleration-5d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
