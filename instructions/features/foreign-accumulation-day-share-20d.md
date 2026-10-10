---
feature_name: "Foreign Accumulation Day Share 20D"
family: "Foreign flow"
---

# Foreign Accumulation Day Share 20D

## Definition

mean(1[Foreign Buy > Foreign Sell],20)

## Measurement and timing

**Unit and scale:** fraction 0..1

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 1

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.60 as a 60% share. Keep the definition’s basis: a share of days and a share of volume are different measures.
- Keep net buying/selling, participation, accumulation-day share, and flow/price relationships separate. Compare horizons without counting overlapping windows as independent evidence.
- The catalog default shifts the entire generated result by 1 trading session, including combined flow/price features. The supplied pipeline output is already lagged; do not shift it again. Explicit metadata for a custom lag takes precedence.

## Related features

- [Foreign Accumulation Day Share 60D](foreign-accumulation-day-share-60d.md)
- [Foreign Accumulation Day Share 10D](foreign-accumulation-day-share-10d.md)
- [Foreign Accumulation Day Share 5D](foreign-accumulation-day-share-5d.md)
- [Foreign Sell Share 20D](foreign-sell-share-20d.md)

Family navigation: [Foreign flow](INDEX.md#foreign-flow). Read the [agent guide](README.md) for shared interpretation rules.
