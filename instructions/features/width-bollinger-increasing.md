---
feature_name: "Width Bollinger Increasing"
family: "Bollinger bands"
---

# Width Bollinger Increasing

## Definition

1 when normalized least-squares slope of previous 5 widths > 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 20, standard-deviation multiplier 2; plus prior 5-row slope

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Bollinger Width](bollinger-width.md)
- [Width Bollinger Decreasing](width-bollinger-decreasing.md)
- [Bollinger Oversold](bollinger-oversold.md)
- [Bollinger Percent B](bollinger-percent-b.md)

Family navigation: [Bollinger bands](INDEX.md#bollinger-bands). Read the [agent guide](README.md) for shared interpretation rules.
