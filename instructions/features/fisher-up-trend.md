---
feature_name: "Fisher Up trend"
family: "Fisher transform"
---

# Fisher Up trend

## Definition

1 when Fisher >= 2; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 10 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Distinguish the transform, previous-value trigger, spread, and change. A reversal flag identifies a comparison change without specifying the new direction.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Fisher Transform](fisher-transform.md)
- [Fisher Down Trend](fisher-down-trend.md)
- [Fisher Change 5D](fisher-change-5d.md)
- [Fisher Transform Trigger](fisher-transform-trigger.md)

Family navigation: [Fisher transform](INDEX.md#fisher-transform). Read the [agent guide](README.md) for shared interpretation rules.
