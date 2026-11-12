#!/bin/sh
# Connected build machine only. Regenerate maintainer/upstream/generated for a new OpenSpec version and show the diff.
# Usage: scripts/sync-upstream.sh <version> [--write]
# Without --write it only prints the diff. With --write it replaces maintainer/upstream/generated and rebuilds addons/workspace/.
set -eu
VER=${1:?usage: sync-upstream.sh <version> [--write]}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WORK=${TMPDIR:-/tmp}/openspec-sync-$$
export OPENSPEC_TELEMETRY=0
mkdir -p "$WORK/pkg" && cd "$WORK/pkg"
npm init -y >/dev/null
npm install --ignore-scripts --no-audit --no-fund "@fission-ai/openspec@$VER"
for t in claude continue; do
  mkdir -p "$WORK/generated/$t" && (cd "$WORK/generated/$t" && node "$WORK/pkg/node_modules/@fission-ai/openspec/bin/openspec.js" init --tools "$t" . >/dev/null)
done
diff -ru "$ROOT/maintainer/upstream/generated" "$WORK/generated" || true
if [ "${2:-}" = "--write" ]; then
  rm -rf "$ROOT/maintainer/upstream/generated" && cp -R "$WORK/generated" "$ROOT/maintainer/upstream/generated"
  python3 "$ROOT/maintainer/scripts/make-workspace.py"
  echo "Updated maintainer/upstream/generated and addons/workspace/. Next: see maintainer/UPGRADE.md."
fi
