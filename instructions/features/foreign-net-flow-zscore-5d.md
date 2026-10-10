---
feature_name: "Foreign Net Flow ZScore 5D"
family: "Foreign flow"
---

# Foreign Net Flow ZScore 5D

## Definition

zscore(Foreign Buy - Foreign Sell,5)

## Measurement and timing

**Unit and scale:** standard deviations

**Historical lookback:** 5 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the value in standardized units, not percentages. zscore uses rolling population standard deviation (ddof=0); a zero denominator produces null.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Foreign Net Flow ZScore 60D](foreign-net-flow-zscore-60d.md)
- [Foreign Net Flow ZScore 10D](foreign-net-flow-zscore-10d.md)
- [Foreign Net Flow ZScore 20D](foreign-net-flow-zscore-20d.md)
- [Foreign Net Flow Signed Log](foreign-net-flow-signed-log.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
