---
feature_name: "Foreign Flow Return Correlation 60D"
family: "Foreign flow"
---

# Foreign Flow Return Correlation 60D

## Definition

corr(Net Intensity 1D, log return 1D,60)

## Measurement and timing

**Unit and scale:** correlation -1..1

**Historical lookback:** 60 plus prior close

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Positive and negative values describe the sign of the historical association; zero describes no linear association in that window. Correlation does not establish causation or forecast direction.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Foreign Net Intensity 1D](foreign-net-intensity-1d.md)
- [Log Return 1D](log-return-1d.md)
- [Foreign Flow Price Divergence 60D](foreign-flow-price-divergence-60d.md)
- [Foreign Net Intensity 60D](foreign-net-intensity-60d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
