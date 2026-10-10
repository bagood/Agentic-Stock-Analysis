---
feature_name: "Foreign Net Intensity Acceleration 5D"
family: "Foreign flow"
---

# Foreign Net Intensity Acceleration 5D

## Definition

Net Intensity(t) - 2*Net Intensity(t-5) + Net Intensity(t-10)

## Measurement and timing

**Unit and scale:** ratio difference

**Historical lookback:** 10-row second difference

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- This is a difference between ratio-valued quantities, not their percentage rate of change. Preserve the stated ordering of the subtraction.
- This is a second difference. Its sign describes a change in net-intensity movement, not necessarily the sign of net intensity itself.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Foreign Net Intensity 1D](foreign-net-intensity-1d.md)
- [Foreign Net Intensity 5D](foreign-net-intensity-5d.md)
- [Foreign Net Intensity 10D](foreign-net-intensity-10d.md)
- [Foreign Net Intensity EMA 5D Minus 20D](foreign-net-intensity-ema-5d-minus-20d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
