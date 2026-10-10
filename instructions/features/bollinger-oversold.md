---
feature_name: "Bollinger Oversold"
family: "Bollinger bands"
---

# Bollinger Oversold

## Definition

1 when Close <= lower band; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 20, standard-deviation multiplier 2

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- The label records the stated threshold or band condition. It does not guarantee a reversal or supply a trade instruction.
- Distinguish position within the channel from channel width. Width expansion or contraction alone does not identify price direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Bollinger Percent B](bollinger-percent-b.md)
- [Bollinger Width](bollinger-width.md)
- [Width Bollinger Increasing](width-bollinger-increasing.md)
- [Bollinger Overbought](bollinger-overbought.md)

Family navigation: [Bollinger bands](INDEX.md#bollinger-bands). Read the [agent guide](README.md) for shared interpretation rules.
