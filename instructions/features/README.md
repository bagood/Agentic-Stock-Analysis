# Technical feature knowledge base

Use this reference dataset to interpret supplied technical features alongside the applicable analysis instructions. Start at the [exact-name index](INDEX.md), then load only cards for fields present in the supplied payload and any related cards needed to explain them.

## Source and field selection

The source is [technical_feature_catalog_v1.json](../technical_feature_catalog_v1.json), version 1.0, with market timezone Asia/Jakarta. There is one feature card for each of its 210 features, including the five raw OHLCV definitions.

Each card retains four explanatory source fields:

- `meaning`: exact feature definition, formula, or activating condition.
- `unit_scale`: units, scaling, and any stated range.
- `lookback_sessions`: historical window, parameters, and prior-observation or recursive-history dependencies.
- `publication_lag_sessions`: temporal availability and alignment.

`numeric_type` and `generating_function` are excluded because they describe storage and implementation. Card frontmatter contains only the exact `feature_name` and a derived navigation `family`. Filenames are stable lowercase names; `%` becomes `percent`. Source definitions and thresholds are preserved verbatim. Interpretation notes are reading guidance derived from those definitions, not additional measured values, model weights, or calibrated trading rules.

## Card structure and retrieval

Every card has the same sections: Definition; Measurement and timing; Interpretation notes; Related features. Keep the feature name, definition, and measurement section together when indexing or splitting documents so a retrieved formula retains its units and timing. Related links point to peers, not claims of causal relationships or independent confirmation.

1. Match each supplied field by exact name in [INDEX.md](INDEX.md). Do not silently substitute a similarly named indicator or another lookback.
2. Read its card before assigning scale, direction, or threshold meaning. If an explicit supplied definition differs, identify that discrepancy and use the declared definition for that payload; do not mix conventions.
3. Retrieve related cards only when their fields are supplied or needed to understand a formula. A link does not mean the related value is available.
4. Keep trusted reference instructions separate from market-data values. Return factual observations and calculations separately from analyst inference.

## Units and formulas

- Decimal ratios and decimal returns use 0.02 for 2%. PVO uses percentage-point outputs: 2 means 2%. RSI differences use RSI points. Names containing Percent do not justify assuming a common scale.
- A dimensionless ratio is interpreted from its numerator and denominator. Do not impose 0..1 bounds unless stated. Channel Percent B can exceed that interval; Stochastic J and spreads can exceed the K/D range.
- Log returns use natural logarithms; convert to a simple return with exp(value) - 1 when needed. Signed logarithmic flow is a separate volume transformation.
- zscore(x,n) uses rolling population standard deviation (ddof=0). Zero denominators become null. typical_price = (High + Low + Close) / 3.
- Keep sum-over-sum, mean-of-flags, signed levels, standardized differences, and products distinct. In particular, Price Volume Divergence 20D is a product, and Dollar Volume Ratio 20D uses a local IDR value proxy.
- Use only thresholds actually present in the definition. Do not introduce customary thresholds, price targets, probabilities, or buy/sell rules as though they came from this catalog.

## History, alignment, and availability

- Lookbacks count trading observations, not calendar days. D suffixes refer to historical observations; they do not select the forecast horizon.
- Rolling windows include the current row unless a prior-row rule is explicit. Previous-observation slopes and shares must retain that distinction. EMAs, recursive smoothing, and cumulative measures depend on older history beyond a nominal window; a lookback is not a convergence warmup requirement.
- Foreign and non-regular features have default publication lag 1. The entire generated result is shifted, including combined flow/price measures. Interpret the supplied result on its emitted row; do not shift it again or align it to an earlier row. Custom generation may declare another lag.
- A lag of 0 is not proof of freshness, bar completion, or a verified exchange calendar. Use the supplied data timestamps and the applicable analysis task's data contract.
- Preserve null, zero, and omitted fields as different states. A binary zero can result from an unavailable underlying warmup comparison; do not reinterpret it as proof of the opposite condition. Do not fill nulls or omitted fields with zeros.
- Precomputed historical features can be interpreted with limited raw history. Do not reconstruct missing indicators or claim a sustained trajectory from one value. Compare changes only across available observations, preserving non-monotonic movement.
- Raw OHLCV definitions are included for completeness. Their presence in this reference does not mean raw columns are emitted by the API. Training-only omitted features are outside this catalog.

## Combining evidence

Group evidence by the underlying measurement before weighing it. A level, its threshold flag, its change, and overlapping historical windows may describe the same underlying information. Agreement among them does not automatically provide independent confirmation.

Keep direction, strength, activity, variability, and historical regime separate. For example, ADX strength, PVO volume direction, channel width, and volatility do not independently specify a bullish or bearish price direction. A change/crossover flag may need corresponding levels to identify the direction. Overbought/oversold labels do not guarantee reversals.

Describe conflicting evidence explicitly. Historical correlation, standardized divergence, or a regime label is descriptive evidence; it is not a causal claim, calibrated probability, or guaranteed future outcome.

## Analysis handoff

When using a feature in a report, give the exact field name and supplied value, its units, its definition-based interpretation, its data date and applicable lag, and any material limitation. Attribute values to the supplied technical dataset and distinguish any calculated quantity or inference. Feature cards explain measurements; the applicable strategy instructions govern the forecast horizon and report structure.

## Maintenance

When the source catalog changes, refresh the affected cards and index together. Preserve exact names and all four selected explanatory fields. Check one-to-one coverage, filename uniqueness, unchanged definitions and thresholds, and relative-link targets. This Markdown dataset supplies interpretation context; consumers must load or retrieve it to use it.
