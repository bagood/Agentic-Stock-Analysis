---
feature_name: "CMF Value"
family: "Chaikin Money Flow"
---

# CMF Value

## Definition

Sum(money-flow multiplier * Volume,20) / sum(Volume,20)

## Measurement and timing

**Unit and scale:** dimensionless ratio

**Historical lookback:** 20 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Interpret the ratio using its stated numerator and denominator. A value of 1 is equality of those quantities, not automatically a neutral market signal.
- Distinguish CMF level, change, threshold flags, and zero-touch/crossover events. A crossover event alone does not specify its direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Volume](volume.md)
- [Strong Negative CMF](strong-negative-cmf.md)
- [Strong Positive CMF](strong-positive-cmf.md)
- [CMF Change 5D](cmf-change-5d.md)

Family navigation: [Chaikin Money Flow](INDEX.md#chaikin-money-flow). Read the [agent guide](README.md) for shared interpretation rules.
