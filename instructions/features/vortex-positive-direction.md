---
feature_name: "Vortex Positive Direction"
family: "Vortex"
---

# Vortex Positive Direction

## Definition

1 when Vortex Spread > 0; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 14 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Use Positive and Negative together; the spread states their difference. A direction flag gives the comparison result without its magnitude.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Vortex Spread](vortex-spread.md)
- [Vortex Positive](vortex-positive.md)
- [Vortex Negative](vortex-negative.md)

Family navigation: [Vortex](INDEX.md#vortex). Read the [agent guide](README.md) for shared interpretation rules.
