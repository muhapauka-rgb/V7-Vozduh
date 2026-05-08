#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "===== V7 LOCAL CHECKS ====="
date -u +"%Y-%m-%dT%H:%M:%SZ"

echo
echo "===== BASH SYNTAX ====="
while IFS= read -r file; do
  [ -n "$file" ] || continue
  first="$(head -n1 "$file" 2>/dev/null || true)"
  case "$first" in
    *python*) continue ;;
    '#!'*bash*|'#!'*sh*) ;;
    *) continue ;;
  esac
  bash -n "$file"
  echo "ok bash $file"
done < <(find . -maxdepth 3 -type f \( -path './v7-*' -o -path './hardening/v7-*' \) ! -name '*.md' | sort)

echo
echo "===== PYTHON SYNTAX ====="
PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-/private/tmp/v7_pycache}" python3 -W error -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper client/v7-smart-client-profile-generate public/v7-public-gateway client/v7-client-speed-api

echo
echo "===== GIT DIFF WHITESPACE ====="
git diff --check

echo
echo "V7_LOCAL_CHECKS=OK"
