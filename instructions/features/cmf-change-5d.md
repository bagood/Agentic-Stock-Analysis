---
feature_name: "CMF Change 5D"
family: "Chaikin Money Flow"
---

# CMF Change 5D

## Definition

CMF(t) - CMF(t-5)

## Measurement and timing

**Unit and scale:** ratio difference

**Historical lookback:** 20 plus 5-row difference

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- This is a difference between ratio-valued quantities, not their percentage rate of change. Preserve the stated ordering of the subtraction.
- Distinguish CMF level, change, threshold flags, and zero-touch/crossover events. A crossover event alone does not specify its direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [CMF Value](cmf-value.md)
- [Strong Negative CMF](strong-negative-cmf.md)
- [Strong Positive CMF](strong-positive-cmf.md)
- [Negative CMF](negative-cmf.md)

Family navigation: [Chaikin Money Flow](INDEX.md#chaikin-money-flow). Read the [agent guide](README.md) for shared interpretation rules.
