---
feature_name: "Low"
family: "Raw OHLCV"
---

# Low

## Definition

Raw session low

## Measurement and timing

**Unit and scale:** IDR per share

**Historical lookback:** 1 trading observation(s)

**Publication lag (trading sessions):** 0

Lookbacks count trading observations, not calendar days or forecast sessions. Rolling windows include the current row unless the definition explicitly uses prior rows. Nominal lookback is not a convergence warmup guarantee.

## Interpretation notes

- Use the raw session prices and volume as observations. Their definitions alone do not establish adjustment basis or future price movement.
- Catalog lag 0 means no extra publication shift is specified. It does not establish that a supplied session bar is complete or that data are current.

## Related features

- [Open](open.md)
- [Volume](volume.md)
- [Close](close.md)
- [High](high.md)

Family navigation: [Raw OHLCV](INDEX.md#raw-ohlcv). Read the [agent guide](README.md) for shared interpretation rules.
