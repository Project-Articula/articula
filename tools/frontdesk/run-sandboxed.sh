#!/usr/bin/env bash
# Run the front desk inside a bubblewrap sandbox.
#
# What the sandbox guarantees:
#   * the process cannot see any file in $HOME except
#       - its own token file   (read-only)
#       - its own state dir    (read-write)
#       - this checkout        (read-only)
#   * no new privileges, own PID namespace, temp dirs are private
# What it does not guarantee:
#   * network isolation — GitHub and the local model endpoint are needed.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOKEN_FILE="${FRONTDESK_TOKEN_FILE:-$HOME/.config/articula/github-frontdesk-token}"
STATE_DIR="${FRONTDESK_STATE_DIR:-$HOME/.local/state/articula/frontdesk}"
mkdir -p "$STATE_DIR"

exec bwrap \
  --dev-bind / / \
  --tmpfs "$HOME" \
  --ro-bind "$TOKEN_FILE" "$TOKEN_FILE" \
  --bind "$STATE_DIR" "$STATE_DIR" \
  --ro-bind "$HERE/.." "$HERE/.." \
  --proc /proc --dev /dev --tmpfs /tmp \
  --unshare-pid --die-with-parent --new-session \
  --setenv FRONTDESK_TOKEN_FILE "$TOKEN_FILE" \
  --setenv FRONTDESK_STATE_DIR "$STATE_DIR" \
  python3 "$HERE/bot.py" "$@"
