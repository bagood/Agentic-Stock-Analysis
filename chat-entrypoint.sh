#!/bin/sh

set -eu

chat_codex_home="${CODEX_HOME:-/home/chatuser/.codex}"
mkdir -p "$chat_codex_home"

if [ -f /host-codex/auth.json ] && [ ! -e "$chat_codex_home/auth.json" ]; then
    cp /host-codex/auth.json "$chat_codex_home/auth.json"
fi

chown -R chatuser:chatuser "$chat_codex_home"
exec gosu chatuser "$@"
