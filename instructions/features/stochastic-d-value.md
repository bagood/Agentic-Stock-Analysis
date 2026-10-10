---
feature_name: "Stochastic D Value"
family: "Stochastic oscillator"
---

# Stochastic D Value

## Definition

Stochastic D signal

## Measurement and timing

**Unit and scale:** points; K/D 0..100; J and spread may exceed that range

**Historical lookback:** 14/3/3

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Distinguish K, D, J, and K-minus-D. The catalog range for K/D does not constrain J or their spread to 0..100.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Stochastic K Minus D](stochastic-k-minus-d.md)
- [Stochastic K Value](stochastic-k-value.md)
- [Stochastic Oscillator Oversold](stochastic-oscillator-oversold.md)
- [Stochastic J](stochastic-j.md)

Family navigation: [Stochastic oscillator](INDEX.md#stochastic-oscillator). Read the [agent guide](README.md) for shared interpretation rules.
