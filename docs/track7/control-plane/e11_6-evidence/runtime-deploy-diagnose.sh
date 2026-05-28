#!/usr/bin/env bash
set -euo pipefail

src_tmp="/tmp/v7-egress-diagnose.e11_6.new"
dst="/usr/local/bin/v7-egress-diagnose"

echo "# E11.6 v7-egress-diagnose deploy verification"
echo "timestamp_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo
echo "## source tmp"
stat -c 'owner=%U group=%G mode=%a size=%s mtime=%y path=%n' "$src_tmp"
sha256sum "$src_tmp"
bash -n "$src_tmp"
echo "tmp_bash_n_rc=$?"

echo
echo "## destination before"
stat -c 'owner=%U group=%G mode=%a size=%s mtime=%y path=%n' "$dst"
sha256sum "$dst"

install -o root -g root -m 0755 "$src_tmp" "$dst"

echo
echo "## destination after"
stat -c 'owner=%U group=%G mode=%a size=%s mtime=%y path=%n' "$dst"
sha256sum "$dst"
bash -n "$dst"
echo "dst_bash_n_rc=$?"

echo
echo "## command path excerpts after"
grep -nE 'wg show|awg show|latest-handshakes|curl_ok_but_handshake_stale|curl_ok_but_wireguard_handshake_unavailable' "$dst" || true
