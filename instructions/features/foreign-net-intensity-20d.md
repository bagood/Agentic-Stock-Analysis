---
feature_name: "Foreign Net Intensity 20D"
family: "Foreign flow"
---

# Foreign Net Intensity 20D

## Definition

sum(Foreign Buy - Foreign Sell) / sum(Volume) over 20 observations

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Volume](volume.md)
- [Foreign Net Intensity EMA 5D Minus 20D](foreign-net-intensity-ema-5d-minus-20d.md)
- [Foreign Net Value Intensity 20D](foreign-net-value-intensity-20d.md)
- [Foreign Net Intensity 1D](foreign-net-intensity-1d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
