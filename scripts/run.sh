#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
HOST=${2:-127.0.0.1}

export PYTHONPATH="$(pwd)":${PYTHONPATH:-}
uvicorn src.app.main:app --host "$HOST" --port "$PORT" --reload


