#!/usr/bin/env bash
set -e

python3 src/main.py

ls -la public
cd public
pwd

sleep 1
python3 -m http.server 8888 --bind 0.0.0.0

