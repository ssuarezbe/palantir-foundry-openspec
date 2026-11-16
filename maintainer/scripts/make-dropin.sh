#!/bin/sh
# Build drop-in/ : one folder per situation in docs/setup.md, laid out at final paths. Copy its contents over the repository root.
# Usage: maintainer/scripts/make-dropin.sh <output-dir>   (creates <output-dir>/drop-in)
set -eu
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
D=$1/drop-in
TS=$ROOT/addons/ci/typescript
rm -rf "$D"
for s in 1 2 3 4 5; do mkdir -p "$D/situation-$s"; cp -R "$ROOT/core/project-template/openspec" "$D/situation-$s/openspec"; done
for s in 2 5; do mkdir -p "$D/situation-$s/tools"; cp -R "$ROOT/addons/cli" "$D/situation-$s/tools/openspec"; done
mkdir -p "$D/situation-2/tests" "$D/situation-3/tests" "$D/situation-4/tests" "$D/probe/tests"
cp "$TS/openspec.test.ts" "$TS/glossary.test.ts" "$D/situation-2/tests/"
cp "$TS/openspec-rules.test.ts" "$TS/glossary.test.ts" "$D/situation-3/tests/"
cp "$ROOT/addons/ci/python/test_openspec_rules.py" "$D/situation-4/tests/"
cp "$TS/probe.test.ts" "$D/probe/tests/"
cp -R "$ROOT/addons/workspace/.continue" "$ROOT/addons/workspace/.claude" "$D/situation-5/"
cat > "$D/README.txt" <<'TXT'
Pick the folder for your situation (docs/setup.md section 1) and copy its CONTENTS over the repository root.
  probe        a one-off test that prints what Checks allows. Run it first if you do not know your situation.
  situation-1  AI FDE only: openspec/
  situation-2  TypeScript, Jest can run the CLI: openspec/, tools/openspec/, tests/
  situation-3  TypeScript, no child process: openspec/, tests/
  situation-4  Python: openspec/, tests/
  situation-5  Laptop or workspace: openspec/, tools/openspec/, .continue/ and .claude/ (delete the one you do not use)
tests/ is a suggestion: move the test files into the folder your test runner already scans.
Situations 2 and 3 still need the tsconfig change in docs/setup.md. Check .gitignore for "dist" (docs/setup.md section 2).
Delete tools/openspec/launchers/openspec.cmd on macOS and Linux, or leave it. Situation 6: see docs/multi-repo.md.
TXT
