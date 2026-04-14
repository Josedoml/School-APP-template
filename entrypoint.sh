#!/bin/sh
set -e

# Resolve PORT with an explicit default so the value is always a plain integer
PORT="${PORT:-8000}"

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
