---
feature_name: "Strong Negative CMF"
family: "Chaikin Money Flow"
---

# Strong Negative CMF

## Definition

1 when CMF <= -0.25; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 20; crossover adds previous observation

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish CMF level, change, threshold flags, and zero-touch/crossover events. A crossover event alone does not specify its direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [CMF Value](cmf-value.md)
- [Negative CMF](negative-cmf.md)
- [Strong Positive CMF](strong-positive-cmf.md)
- [CMF Change 5D](cmf-change-5d.md)

Family navigation: [Chaikin Money Flow](INDEX.md#chaikin-money-flow). Read the [agent guide](README.md) for shared interpretation rules.
