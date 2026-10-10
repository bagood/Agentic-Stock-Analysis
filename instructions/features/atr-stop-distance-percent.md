---
feature_name: "ATR Stop Distance Percent"
family: "ATR trailing stop"
---

# ATR Stop Distance Percent

## Definition

(Close - ATR stop) / Close

## Measurement and timing

**Unit and scale:** decimal ratio

**Historical lookback:** ATR(21), multiplier 3; recursive history

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Read 0.02 as 2% and -0.02 as -2%. Keep the formula’s numerator and denominator when explaining the percentage.
- Read stop-presence flags together with stop distance. A presence flag does not provide the numeric stop price.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [ATR Bullish](atr-bullish.md)
- [ATR Bearish](atr-bearish.md)
- [Close](close.md)

Family navigation: [ATR trailing stop](INDEX.md#atr-trailing-stop). Read the [agent guide](README.md) for shared interpretation rules.
