#!/bin/sh
# Connected build machine only. Needs node, npm, bun, python3, zip.
# Usage: maintainer/scripts/build.sh [--release]
set -eu
VER=1.16.0
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WORK=${TMPDIR:-/tmp}/openspec-build-$$
OUT=$ROOT/addons/cli/openspec-$VER
mkdir -p "$WORK" && cd "$WORK"
# The npm package ships no lockfile, so its dependencies would resolve fresh on every build and the bundle
# would change. maintainer/scripts/pinned/ holds the lock of record. Delete it only to repin on purpose (then update PIN.md).
if [ -f "$ROOT/maintainer/scripts/pinned/package-lock.json" ]; then
  cp "$ROOT/maintainer/scripts/pinned/package.json" "$ROOT/maintainer/scripts/pinned/package-lock.json" .
  npm ci --ignore-scripts --no-audit --no-fund
else
  npm init -y >/dev/null
  npm install --save-exact --ignore-scripts --no-audit --no-fund "@fission-ai/openspec@$VER"
  mkdir -p "$ROOT/maintainer/scripts/pinned" && cp package.json package-lock.json "$ROOT/maintainer/scripts/pinned/"
  echo "NOTE: wrote maintainer/scripts/pinned/. Commit it and record the new hashes in addons/cli/PIN.md." >&2
fi
P=node_modules/@fission-ai/openspec
rm -rf "$OUT" && mkdir -p "$OUT/dist/cli"
bun build "$P/bin/openspec.js" --target=node --format=esm --outfile "$OUT/dist/cli/openspec.mjs"
# Patch 1 of 2. The bundle sits at dist/cli/, not dist/core/x/, so upstream's "../../../schemas" lands outside <dir>.
# Patch that one path so schemas/ resolves inside <dir>. Fail loudly if upstream changed.
OLD='path8.dirname(currentFile), "..", "..", "..", "schemas"'
grep -qF "$OLD" "$OUT/dist/cli/openspec.mjs" || { echo "schemas path patch did not match" >&2; exit 1; }
sed -i.bak 's|path8.dirname(currentFile), "..", "..", "..", "schemas"|path8.dirname(currentFile), "..", "..", "schemas"|' "$OUT/dist/cli/openspec.mjs"
rm "$OUT/dist/cli/openspec.mjs.bak"
# Second patch: upstream index.js runs the CLI when it is the entry file, and bin/openspec.js runs it again.
# In a one-file bundle both fire and every command runs twice. Disable the self-run guard.
GUARD='if \(process\.argv\[1\] && path[0-9]+\.resolve\(process\.argv\[1\]\) === fileURLToPath[0-9]*\(import\.meta\.url\)\) \{'
[ "$(grep -cE "$GUARD" "$OUT/dist/cli/openspec.mjs")" = 1 ] || { echo "self-run guard patch did not match exactly once" >&2; exit 1; }
sed -E -i.bak "s/$GUARD/if (false) {/" "$OUT/dist/cli/openspec.mjs"
rm "$OUT/dist/cli/openspec.mjs.bak"
cp "$P/package.json" "$OUT/package.json"
cp -R "$P/schemas" "$OUT/schemas"
cp "$P/LICENSE" "$WORK/OPENSPEC_LICENSE"
node -e 'const l=require("./package-lock.json").packages["node_modules/@fission-ai/openspec"];console.log(l.integrity)' > "$WORK/integrity.txt"
npm audit signatures > "$WORK/audit.txt" 2>&1 || true
# Licence texts of every package bundled into openspec.mjs.
node -e '
const fs=require("fs"),path=require("path");
const out=[];
const walk=d=>{for(const n of fs.readdirSync(d)){
  const p=path.join(d,n); if(n.startsWith("."))continue;
  if(n.startsWith("@")){walk(p);continue}
  const pj=path.join(p,"package.json"); if(!fs.existsSync(pj))continue;
  const j=JSON.parse(fs.readFileSync(pj));
  const lic=fs.readdirSync(p).find(f=>/^(licen[sc]e|copying)/i.test(f));
  out.push({name:j.name,version:j.version,license:typeof j.license==="string"?j.license:JSON.stringify(j.license||j.licenses),text:lic?fs.readFileSync(path.join(p,lic),"utf8").trim():"(no licence file in package; licence field above)"});
}};
walk("node_modules");
out.sort((a,b)=>a.name.localeCompare(b.name));
fs.writeFileSync(process.argv[1],out.map(o=>"=== "+o.name+"@"+o.version+" ("+o.license+")\n\n"+o.text+"\n").join("\n"));
fs.writeFileSync(process.argv[2],out.map(o=>"| "+o.name+" | "+o.version+" | "+o.license+" |").join("\n")+"\n");
' "$ROOT/addons/cli/THIRD_PARTY_LICENSES.txt" "$WORK/deps-table.md"
cp "$WORK/deps-table.md" "$ROOT/addons/cli/bundled-dependencies.md"
cd "$ROOT/addons/cli"
shasum -a 256 openspec-$VER/dist/cli/openspec.mjs > SHA256SUMS
echo "integrity: $(cat "$WORK/integrity.txt")"
echo "sha256:    $(cut -d' ' -f1 SHA256SUMS)"
echo "audit signatures:"; cat "$WORK/audit.txt"
mkdir -p "$ROOT/maintainer/upstream" && cp "$WORK/OPENSPEC_LICENSE" "$ROOT/maintainer/upstream/OPENSPEC_LICENSE"
if [ "${1:-}" = "--release" ]; then
  # Lean zip for teams: top-level files, docs, core and addons. Maintainer files stay in Git.
  cd "$ROOT/.."
  N=palantir-foundry-openspec-$(cat "$ROOT/VERSION")
  rm -f "$N.zip"
  (cd "$ROOT" && zip -qr "../$N.zip" README.md CHANGELOG.md VERSION LICENSE THIRD_PARTY_NOTICES.md docs core addons -x '*/node_modules/*' '*.pyc' '*__pycache__/*' '.DS_Store' '*/.DS_Store')
  shasum -a 256 "$N.zip" | tee "$N.zip.sha256"
fi
