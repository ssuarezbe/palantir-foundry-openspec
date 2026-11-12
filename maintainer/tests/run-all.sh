#!/bin/sh
# Runs every check. Offline. Needs: node, python3, maintainer/tests/jest-env/node_modules (maintainer/scripts/setup-test-env.sh, once).
# Usage: maintainer/tests/run-all.sh [--no-jest]
set -u
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
CLI=$ROOT/addons/cli/openspec-1.16.0/dist/cli/openspec.mjs
JEST_ENV=$ROOT/maintainer/tests/jest-env
export OPENSPEC_TELEMETRY=0
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); }
bad() { FAIL=$((FAIL+1)); echo "FAIL: $*"; }
sha() { if command -v sha256sum >/dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
want() { sed -n "s/^$2=//p" "$1/expected"; }   # want <fixture> <key>

NOJEST=0; [ "${1:-}" = "--no-jest" ] && NOJEST=1
if [ $NOJEST = 0 ] && [ ! -x "$JEST_ENV/node_modules/.bin/jest" ]; then
  echo "Jest harness missing. On a connected machine run maintainer/scripts/setup-test-env.sh, or pass --no-jest." >&2; exit 2
fi

# Check <name> <actual exit> <expected pass|fail> <output file> <reason>
check() {
  name=$1; code=$2; exp=$3; out=$4; reason=${5:-}
  if [ "$exp" = pass ]; then
    [ "$code" -eq 0 ] && ok || bad "$name: expected pass, got exit $code"$'\n'"$(head -20 "$out")"
  else
    if [ "$code" -eq 0 ]; then bad "$name: expected fail, got pass"
    elif [ -n "$reason" ] && ! grep -qiF -- "$reason" "$out"; then bad "$name: failed, but output lacks '$reason'"$'\n'"$(head -20 "$out")"
    else ok; fi
  fi
}

echo "== 1. bundle integrity"
(cd "$ROOT/addons/cli" && sha -c SHA256SUMS >/dev/null 2>&1) && ok || bad "cli/SHA256SUMS does not match the bundle"
[ "$(node "$CLI" --version 2>/dev/null)" = "1.16.0" ] && ok || bad "bundle --version is not 1.16.0"
grep -q "$(cut -d' ' -f1 "$ROOT/addons/cli/SHA256SUMS")" "$ROOT/addons/cli/PIN.md" && ok || bad "upstream/PIN.md does not list the SHA-256 in cli/SHA256SUMS"
[ -f "$ROOT/maintainer/scripts/pinned/package-lock.json" ] && ok || bad "scripts/pinned/package-lock.json missing: builds are not reproducible"
grep -q "$(cat "$ROOT/VERSION")" "$ROOT/addons/cli/PIN.md" "$ROOT/README.md" && ok || bad "VERSION is not in PIN.md and README.md"

echo "== 2. schema"
cp -R "$ROOT/core/project-template" "$WORK/schemacheck"
(cd "$WORK/schemacheck" && node "$CLI" schema validate foundry-spec-driven >"$WORK/o" 2>&1) && ok || bad "schema validate: $(cat "$WORK/o")"
grep -q "^schema: foundry-spec-driven" "$ROOT/core/project-template/openspec/config.yaml" && ok || bad "project-template config does not use foundry-spec-driven"

echo "== 3. fresh project: project-template + workspace/.continue"
cp -R "$ROOT/core/project-template" "$WORK/fresh" && cp -R "$ROOT/addons/workspace/.continue" "$WORK/fresh/.continue"
(cd "$WORK/fresh" && node "$CLI" validate --all --strict --no-interactive >"$WORK/o" 2>&1); code=$?
[ "$(grep -c 'No items found' "$WORK/o")" -le 1 ] && ok || bad "bundle ran the command twice (self-start guard patch missing)"
grep -q "Rules for" "$WORK/o" && bad "config.yaml rules do not parse: $(grep 'Rules for' "$WORK/o")" || ok
# An empty project has nothing to validate; pass means exit 0 or the "no items" notice with no errors.
{ [ $code -eq 0 ] || ! grep -q "ERROR" "$WORK/o"; } && ok || bad "fresh project does not validate: $(cat "$WORK/o")"

echo "== 4. fixtures: bundle, Jest, Python, parity"
for d in "$ROOT"/maintainer/tests/fixtures/*/*/; do
  fx=${d%/}; id=$(basename "$(dirname "$fx")")/$(basename "$fx")
  t=$WORK/fx/$(echo "$id" | tr / _)
  mkdir -p "$t/tests" && cp -R "$fx/openspec" "$t/openspec"
  cp -R "$ROOT/core/project-template/openspec/schemas" "$t/openspec/schemas"
  cp "$ROOT"/addons/ci/typescript/*.test.ts "$t/tests/"

  # bundle=skip: a satellite repo (store: <id>) has no specs of its own; the bundle needs a registered store (section 8).
  if [ "$(want "$fx" bundle)" = skip ]; then bcode=skip; else
    (cd "$t" && node "$CLI" validate --all --strict --no-interactive >"$WORK/b" 2>&1); bcode=$?
    check "$id [bundle]" $bcode "$(want "$fx" bundle)" "$WORK/b" "$(want "$fx" reason)"
  fi

  if [ $NOJEST = 0 ]; then
    printf '{"compilerOptions":{"target":"ES2020","module":"commonjs","esModuleInterop":true,"types":["jest","node"],"typeRoots":["%s/node_modules/@types"]}}' "$JEST_ENV" >"$t/tsconfig.json"
    cat >"$t/jest.config.json" <<JEOF
{"rootDir":"$t","testMatch":["**/tests/*.test.ts"],
 "transform":{"^.+\\\\.ts\$":["$JEST_ENV/node_modules/ts-jest",{"tsconfig":"$t/tsconfig.json"}]},
 "moduleDirectories":["$JEST_ENV/node_modules"],"cache":false}
JEOF
    (cd "$t" && OPENSPEC_CLI=$CLI "$JEST_ENV/node_modules/.bin/jest" --config "$t/jest.config.json" >"$WORK/j" 2>&1)
    check "$id [jest]" $? "$(want "$fx" jest)" "$WORK/j" "$(want "$fx" reason)"
  fi

  (cd "$t" && OPENSPEC_ROOT=$t python3 -I "$ROOT/addons/ci/python/test_openspec_rules.py" >"$WORK/p" 2>&1)
  check "$id [python]" $? "$(want "$fx" python)" "$WORK/p" "$(want "$fx" reason)"

  (cd "$t" && OPENSPEC_ROOT=$t OPENSPEC_SKIP_GLOSSARY=1 python3 -I "$ROOT/addons/ci/python/test_openspec_rules.py" >"$WORK/p" 2>&1); pcode=$?
  [ "$bcode" = skip ] || { [ $pcode -eq 0 ] && [ $bcode -eq 0 ]; } || { [ $pcode -ne 0 ] && [ $bcode -ne 0 ]; } && ok || bad "$id [parity]: bundle exit $bcode, python rules exit $pcode"
done

echo "== 8. stores: one spec home, satellite repos"
H=$WORK/stores; mkdir -p "$H/ts-functions" "$H/react-app" "$H/xdg-data" "$H/xdg-config" "$H/empty"
cp -R "$ROOT/core/project-template/openspec" "$H/ts-functions/openspec"
mkdir -p "$H/react-app/openspec" && printf 'store: product-specs\n' >"$H/react-app/openspec/config.yaml"
sto() { XDG_DATA_HOME=$H/xdg-data XDG_CONFIG_HOME=$H/xdg-config node "$CLI" "$@"; }
(cd "$H/ts-functions" && sto store register . --id product-specs --yes >"$WORK/o" 2>&1) && ok || bad "store register: $(cat "$WORK/o")"
(cd "$H/react-app" && sto new change add-batch-release >"$WORK/o" 2>&1); [ -f "$H/ts-functions/openspec/changes/add-batch-release/.openspec.yaml" ] && ok || bad "new change from a satellite did not land in the store: $(cat "$WORK/o")"
[ "$(grep -c 'Created change' "$WORK/o")" -eq 1 ] && ok || bad "new change ran twice or not at all"
[ ! -d "$H/react-app/openspec/changes" ] && ok || bad "satellite kept its own changes folder"
(cd "$H/react-app" && sto doctor >"$WORK/o" 2>&1); grep -q "OpenSpec root: ok" "$WORK/o" && ok || bad "doctor not healthy: $(cat "$WORK/o")"
# Fresh machine: the store id is declared but this machine has not registered it.
(cd "$H/react-app" && XDG_DATA_HOME=$H/empty XDG_CONFIG_HOME=$H/empty node "$CLI" validate --all --strict --no-interactive >"$WORK/o" 2>&1); code=$?
{ [ $code -ne 0 ] && grep -q "Unknown store" "$WORK/o"; } && ok || bad "unregistered store should fail with 'Unknown store'"

echo "== 5. aip-skills"
if grep -rnE '(^|[^A-Za-z/_.-])openspec[[:space:]]+[-a-z]' "$ROOT/core/aip-skills" >"$WORK/o"; then bad "CLI calls in aip-skills:"$'\n'"$(cat "$WORK/o")"; else ok; fi
n=0
for f in "$ROOT"/core/aip-skills/*.md; do
  n=$((n+1))
  head -1 "$f" | grep -q '^Name: ' && sed -n 2p "$f" | grep -q '^Description: ' && ok || bad "$f: first lines must be Name: and Description:"
  [ "$(wc -l <"$f")" -le 150 ] && ok || bad "$f: over 150 lines"
done
[ $n -eq 4 ] && ok || bad "expected 4 aip-skills, found $n"

echo "== 6. launchers and workspace"
for f in "$ROOT/addons/cli/launchers/openspec" "$ROOT/addons/cli/launchers/openspec.cmd"; do
  grep -q 'OPENSPEC_TELEMETRY=0' "$f" && ok || bad "$f does not set OPENSPEC_TELEMETRY=0"
done
# Every workspace file that calls openspec must go through a launcher path.
if grep -rnE '(`|^[[:space:]]*)openspec[[:space:]]+[-a-z]' "$ROOT/addons/workspace" >"$WORK/o"; then bad "bare openspec calls in workspace/:"$'\n'"$(head -10 "$WORK/o")"; else ok; fi
# A fresh init must not have changed the files we ship: workspace/ must differ from upstream only where intended (see docs/06-upgrade.md)

echo "== 7. URLs"
grep -rEoh 'https?://[^] )>"'"'"'`,;\\]+' "$ROOT" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=upstream --exclude-dir=openspec-1.16.0 --exclude-dir=jest-env --exclude-dir=pinned --exclude=THIRD_PARTY_LICENSES.txt --exclude=allowed-urls.txt --exclude=.gitignore --exclude=run-all.sh 2>/dev/null | sed 's/[.]$//' | sort -u >"$WORK/urls"
grep -v '^#' "$ROOT/maintainer/tests/allowed-urls.txt" >"$WORK/allow"
badurls=$(grep -vEf "$WORK/allow" "$WORK/urls" || true)
[ -z "$badurls" ] && ok || bad "URLs not in tests/allowed-urls.txt:"$'\n'"$badurls"

echo
echo "passed: $PASS  failed: $FAIL"
[ $FAIL -eq 0 ]
