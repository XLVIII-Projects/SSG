#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
PYTHONPATH=src python3 src/main.py

cd public && python3 -m http.server 8888