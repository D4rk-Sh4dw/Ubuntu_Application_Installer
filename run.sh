#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")"
uv run python src/main.py
