---
feature_name: "Stochastic J"
family: "Stochastic oscillator"
---

# Stochastic J

## Definition

3*K - 2*D

## Measurement and timing

**Unit and scale:** points; K/D 0..100; J and spread may exceed that range

**Historical lookback:** 14/3/3

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Distinguish K, D, J, and K-minus-D. The catalog range for K/D does not constrain J or their spread to 0..100.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Stochastic K Value](stochastic-k-value.md)
- [Stochastic D Value](stochastic-d-value.md)
- [Stochastic K Minus D](stochastic-k-minus-d.md)
- [Stochastic Oscillator Oversold](stochastic-oscillator-oversold.md)

Family navigation: [Stochastic oscillator](INDEX.md#stochastic-oscillator). Read the [agent guide](README.md) for shared interpretation rules.
