---
feature_name: "Foreign Participation 1D"
family: "Foreign flow"
---

# Foreign Participation 1D

## Definition

sum(Foreign Buy + Foreign Sell) / (2*sum(Volume)) over 1 observations

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** 1 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- The denominator includes a factor of 2. Do not interpret this as the unhalved sum of buy share and sell share.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Volume](volume.md)
- [Foreign Participation 20D](foreign-participation-20d.md)
- [Foreign Participation 5D](foreign-participation-5d.md)
- [Foreign Participation 60D](foreign-participation-60d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
