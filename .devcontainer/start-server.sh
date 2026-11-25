#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .devcontainer/.runtime

# Keep a single server running even if this hook is called again.
nohup flock --nonblock .devcontainer/.runtime/server.lock \
    env HOST=0.0.0.0 uv run --locked app.py \
    > .devcontainer/.runtime/server.log 2>&1 < /dev/null &

echo "Task server starting on port 5000. Log: .devcontainer/.runtime/server.log"
