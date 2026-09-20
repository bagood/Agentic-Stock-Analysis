#!/bin/sh

set -eu

: "${DETAILED_ANALYSIS_RESULT:=detailedAnalysisResults}"
: "${ENTRY_STRATEGY_RESULT:=entryStrategyResults}"
: "${HOLD_STRATEGY_RESULT:=holdStrategyResults}"
: "${ML_BASE_URL:=}"
: "${ORGANIZER_BASE_URL:=http://localhost:8000}"
: "${MINIMUM_SCORE:=0.5}"

mkdir -p /root/.codex
if [ -d /host-codex ] && [ ! -e /root/.codex/config.toml ]; then
    cp -R /host-codex/. /root/.codex/
fi

cat > /app/.env <<EOF
DETAILED_ANALYSIS_RESULT=${DETAILED_ANALYSIS_RESULT}
ENTRY_STRATEGY_RESULT=${ENTRY_STRATEGY_RESULT}
HOLD_STRATEGY_RESULT=${HOLD_STRATEGY_RESULT}
ML_BASE_URL=${ML_BASE_URL}
ORGANIZER_BASE_URL=${ORGANIZER_BASE_URL}
MINIMUM_SCORE=${MINIMUM_SCORE}
EOF

exec "$@"
