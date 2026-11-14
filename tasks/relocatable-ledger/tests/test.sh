#!/bin/bash
set -euo pipefail
chown -R 0:0 /tests
chmod 700 /tests
mkdir -p /logs/verifier
chmod 700 /logs/verifier
chown 0:0 /app/project/CMakeLists.txt
chmod 644 /app/project/CMakeLists.txt
python3 /tests/grade.py
