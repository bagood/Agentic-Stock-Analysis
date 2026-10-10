#!/bin/sh

set -eu

: "${DETAILED_ANALYSIS_RESULT:=detailedAnalysisResults}"
: "${ENTRY_STRATEGY_RESULT:=entryStrategyResults}"
: "${HOLD_STRATEGY_RESULT:=holdStrategyResults}"
: "${ML_BASE_URL:=}"
: "${ORGANIZER_BASE_URL:=http://localhost:8000}"
: "${MINIMUM_SCORE:=0.5}"

# File-backed credentials are portable; macOS keychain entries are not.
: "${CODEX_HOME:=/root/.codex}"
export CODEX_HOME
# codex exec supports CODEX_API_KEY directly; keep OPENAI_API_KEY compatibility.
if [ -n "${OPENAI_API_KEY:-}" ] && [ -z "${CODEX_API_KEY:-}" ]; then
    CODEX_API_KEY=$OPENAI_API_KEY
    export CODEX_API_KEY
fi
mkdir -p "$CODEX_HOME"
if [ ! -e "$CODEX_HOME/auth.json" ] && [ -f /host-codex/auth.json ]; then
    umask 077
    cp /host-codex/auth.json "$CODEX_HOME/auth.json"
    chmod 600 "$CODEX_HOME/auth.json"
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
