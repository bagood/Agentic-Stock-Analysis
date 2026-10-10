# Analysis instructions

The strategy files in this folder define the analysis task and report requirements. The [technical feature agent guide](features/README.md) and [exact-name feature index](features/INDEX.md) provide a reference dataset with one Markdown card per feature in [technical_feature_catalog_v1.json](technical_feature_catalog_v1.json).

For technical analysis, load the agent guide once and retrieve the cards for the exact fields supplied in the technical payload. Use each card's definition, units, historical lookback, and publication lag before interpreting the value. Follow related-feature links when needed, while keeping overlapping evidence and unavailable values distinct.
