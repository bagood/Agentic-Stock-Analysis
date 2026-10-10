---
feature_name: "Foreign Flow Price Divergence 20D"
family: "Foreign flow"
---

# Foreign Flow Price Divergence 20D

## Definition

zscore(Net Intensity 1D,20) - zscore(log return 1D,20)

## Measurement and timing

**Unit and scale:** standard-deviation difference

**Historical lookback:** 20 plus prior close

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the value in standardized units, not percentages. zscore uses rolling population standard deviation (ddof=0); a zero denominator produces null.
- Positive means the flow z-score exceeds the return z-score; negative means the reverse. This is a standardized difference, not a return estimate.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Foreign Net Intensity 1D](foreign-net-intensity-1d.md)
- [Log Return 1D](log-return-1d.md)
- [Foreign Flow Return Correlation 20D](foreign-flow-return-correlation-20d.md)
- [Foreign Net Intensity 20D](foreign-net-intensity-20d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
