#!/usr/bin/env bash
set -euo pipefail

find . -type f \( -name "*.nc" -o -name "*.out" -o -name "*.dat" \) -print -delete

