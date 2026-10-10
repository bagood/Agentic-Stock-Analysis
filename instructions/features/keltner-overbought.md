---
feature_name: "Keltner Overbought"
family: "Keltner channel"
---

# Keltner Overbought

## Definition

1 when Close >= upper band; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** EMA(20), ATR(10), multiplier 2; recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- The label records the stated threshold or band condition. It does not guarantee a reversal or supply a trade instruction.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Keltner Percent B](keltner-percent-b.md)
- [Width Keltner Increasing](width-keltner-increasing.md)
- [Width Keltner Decreasing](width-keltner-decreasing.md)
- [Keltner Oversold](keltner-oversold.md)

Family navigation: [Keltner channel](INDEX.md#keltner-channel). Read the [agent guide](README.md) for shared interpretation rules.
