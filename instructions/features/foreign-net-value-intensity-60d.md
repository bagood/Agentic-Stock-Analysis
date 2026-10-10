---
feature_name: "Foreign Net Value Intensity 60D"
family: "Foreign flow"
---

# Foreign Net Value Intensity 60D

## Definition

sum(typical_price*(Foreign Buy-Foreign Sell),60) / sum(typical_price*Volume,60)

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 60 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- typical_price = (High + Low + Close) / 3. Preserve that price basis where it appears in the definition.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Volume](volume.md)
- [Foreign Net Value Intensity 10D](foreign-net-value-intensity-10d.md)
- [Foreign Net Value Intensity 5D](foreign-net-value-intensity-5d.md)
- [Foreign Net Value Intensity 20D](foreign-net-value-intensity-20d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
