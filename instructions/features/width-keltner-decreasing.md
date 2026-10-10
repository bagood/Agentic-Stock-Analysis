---
feature_name: "Width Keltner Decreasing"
family: "Keltner channel"
---

# Width Keltner Decreasing

## Definition

1 when normalized least-squares slope of previous 5 widths < 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** EMA(20), ATR(10), multiplier 2; recursive history; plus prior 5-row slope

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Width Keltner Increasing](width-keltner-increasing.md)
- [Keltner Width](keltner-width.md)
- [Keltner Percent B](keltner-percent-b.md)
- [Keltner Overbought](keltner-overbought.md)

Family navigation: [Keltner channel](INDEX.md#keltner-channel). Read the [agent guide](README.md) for shared interpretation rules.
