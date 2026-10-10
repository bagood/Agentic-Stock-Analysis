---
feature_name: "Stochastic Oscillator Oversold"
family: "Stochastic oscillator"
---

# Stochastic Oscillator Oversold

## Definition

1 when K <= 20; 0 otherwise. Generator comparisons can yield 0 during underlying warmup.

## Measurement and timing

**Unit and scale:** binary 0/1

**Historical lookback:** 14/3/3

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- 1 means the stated condition is active; 0 means it is not active in the emitted value. Preserve null separately. A warmup comparison may also emit 0, so 0 alone does not prove the opposite market condition.
- The label records the stated threshold or band condition. It does not guarantee a reversal or supply a trade instruction.
- Distinguish K, D, J, and K-minus-D. The catalog range for K/D does not constrain J or their spread to 0..100.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Stochastic K Value](stochastic-k-value.md)
- [Stochastic D Value](stochastic-d-value.md)
- [Stochastic Oscillator Overbought](stochastic-oscillator-overbought.md)
- [Stochastic K Minus D](stochastic-k-minus-d.md)

Family navigation: [Stochastic oscillator](INDEX.md#stochastic-oscillator). Read the [agent guide](README.md) for shared interpretation rules.
