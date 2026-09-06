#!/bin/sh

set -eu

: "${OUTPUT_DIR:=detailedAnalysisResults}"
: "${ENTRY_STRATEGY_OUTPUT_DIR:=entryStrategyResults}"
: "${BASE_URL:=}"
: "${MINIMUM_SCORE:=0.5}"

mkdir -p /root/.codex
if [ -d /host-codex ] && [ ! -e /root/.codex/config.toml ]; then
    cp -R /host-codex/. /root/.codex/
fi

cat > /app/.env <<EOF
OUTPUT_DIR=${OUTPUT_DIR}
ENTRY_STRATEGY_OUTPUT_DIR=${ENTRY_STRATEGY_OUTPUT_DIR}
BASE_URL=${BASE_URL}
MINIMUM_SCORE=${MINIMUM_SCORE}
EOF

exec "$@"
