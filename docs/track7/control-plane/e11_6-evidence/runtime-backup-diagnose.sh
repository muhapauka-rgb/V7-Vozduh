#!/usr/bin/env bash
set -euo pipefail

src="/usr/local/bin/v7-egress-diagnose"
ts="$(date -u '+%Y%m%dT%H%M%SZ')"
backup_dir="/opt/v7/backups/e11_6-diagnose"
backup="${backup_dir}/v7-egress-diagnose.${ts}.bak"

mkdir -p "$backup_dir"

echo "# E11.6 v7-egress-diagnose backup manifest"
echo "timestamp_utc=${ts}"
echo "source=${src}"
echo "backup_path=${backup}"
echo
echo "## source before"
stat -c 'owner=%U group=%G mode=%a size=%s mtime=%y path=%n' "$src"
sha256sum "$src"

cp -p "$src" "$backup"

echo
echo "## backup after"
stat -c 'owner=%U group=%G mode=%a size=%s mtime=%y path=%n' "$backup"
sha256sum "$backup"
echo
echo "rollback_command=cp -p ${backup} ${src}"
