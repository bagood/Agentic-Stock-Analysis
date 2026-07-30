#!/bin/sh

set -eu

: "${INSTRUCTIONS_PATH:=instructions/stock-upside-analysis-instructions.md}"
: "${BASE_URL:=}"
: "${TECHNICAL_URL:=${BASE_URL}/technical}"
: "${RECOMMENDATION_URL:=${BASE_URL}/analytics/daily_recommendations?rolling_window=10dd}"
: "${MINIMUM_SCORE:=0.5}"

mkdir -p /root/.codex
if [ -d /host-codex ] && [ ! -e /root/.codex/config.toml ]; then
    cp -R /host-codex/. /root/.codex/
fi

cat > /app/.env <<EOF
INSTRUCTIONS_PATH=${INSTRUCTIONS_PATH}
BASE_URL=${BASE_URL}
TECHNICAL_URL=${TECHNICAL_URL}
RECOMMENDATION_URL=${RECOMMENDATION_URL}
MINIMUM_SCORE=${MINIMUM_SCORE}
EOF

exec "$@"
