---
feature_name: "ATR Bearish"
family: "ATR trailing stop"
---

# ATR Bearish

## Definition

1 when ATR buy-stop is present; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** ATR(21), multiplier 3; recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- Read stop-presence flags together with stop distance. A presence flag does not provide the numeric stop price.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [ATR Bullish](atr-bullish.md)
- [ATR Stop Distance Percent](atr-stop-distance-percent.md)

Family navigation: [ATR trailing stop](INDEX.md#atr-trailing-stop). Read the [agent guide](README.md) for shared interpretation rules.
