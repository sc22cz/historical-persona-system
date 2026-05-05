#!/bin/bash
set -e

# Load .env if it exists
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Error: ANTHROPIC_API_KEY not set."
  echo "Create a .env file in this directory with:"
  echo "  ANTHROPIC_API_KEY=sk-ant-..."
  exit 1
fi

echo "Starting backend on http://localhost:8000"
echo "Starting frontend on http://localhost:5173"
echo ""

npm start
