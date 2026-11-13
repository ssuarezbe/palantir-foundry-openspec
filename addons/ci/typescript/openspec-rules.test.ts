import * as fs from "fs";
import * as path from "path";

// Pure TypeScript port of the OpenSpec validation rules. No child process, no bundle, no Node 22.
// Use it INSTEAD of openspec.test.ts when Checks cannot run a child process or the bundle.
// Same rules and messages as addons/ci/python/test_openspec_rules.py. Keep them in step.
// Covers: a requirement needs a scenario and SHALL or MUST, a scenario needs a WHEN/GIVEN and a THEN,
// a change needs a delta unless .openspec.yaml has skip_specs: true. It does not cover every OpenSpec warning.

function findRoot(): string {
  if (process.env.OPENSPEC_ROOT) return process.env.OPENSPEC_ROOT;
  let dir = __dirname;
  while (!fs.existsSync(path.join(dir, "openspec", "config.yaml"))) {
    const parent = path.dirname(dir);
    if (parent === dir) throw new Error("openspec/config.yaml not found above " + __dirname);
    dir = parent;
  }
  return dir;
}

const root = findRoot();
const os = path.join(root, "openspec");
const rel = (p: string) => path.relative(root, p).split(path.sep).join("/");
const satellite = /^store:/m.test(fs.readFileSync(path.join(os, "config.yaml"), "utf8"));

function mdFiles(base: string): string[] {
  const out: string[] = [];
  const walk = (dir: string) => {
    if (!fs.existsSync(dir)) return;
    for (const e of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => (a.name < b.name ? -1 : 1))) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".md")) out.push(p);
    }
  };
  walk(base);
  return out;
}

function openChanges(): string[] {
  const d = path.join(os, "changes");
  if (!fs.existsSync(d)) return [];
  return fs.readdirSync(d, { withFileTypes: true })
    .filter((e) => e.isDirectory() && e.name !== "archive")
    .map((e) => path.join(d, e.name))
    .sort();
}

// A block ends at the next requirement or the next "## " section.
function requirementBlocks(text: string): Array<[string, string]> {
  const marks = [...text.matchAll(/^### Requirement:.*$/gm)];
  const out: Array<[string, string]> = [];
  marks.forEach((m, i) => {
    const start = m.index! + m[0].length;
    let end = i + 1 < marks.length ? marks[i + 1].index! : text.length;
    const nxt = /^## /m.exec(text.slice(start, end));
    if (nxt) end = start + nxt.index;
    out.push([m[0].trim(), text.slice(start, end)]);
  });
  return out;
}

// A trigger (WHEN or GIVEN) and an outcome (THEN), anywhere in the scenario, as in OpenSpec.
const TRIGGER_BOLD = /(?:\*\*|__)(?:WHEN|GIVEN):?(?:\*\*|__)/i;
const TRIGGER_BARE = /\b(?:WHEN|GIVEN)\b/;
const OUTCOME_BOLD = /(?:\*\*|__)THEN:?(?:\*\*|__)/i;
const OUTCOME_BARE = /\bTHEN\b/;

// Each "#### Scenario:" block, skipping fenced code. A scenario ends at the next heading of level 1-4.
function scenarioBodies(body: string): Array<[string, string]> {
  const out: Array<{ name: string; lines: string[] }> = [];
  let cur: { name: string; lines: string[] } | null = null;
  let fence = false;
  for (const line of body.split(/\r?\n/)) {
    if (/^(```|~~~)/.test(line)) { fence = !fence; continue; }
    if (fence) { if (cur) cur.lines.push(""); continue; }
    if (/^#{1,4}\s/.test(line)) cur = null;
    const m = /^####\s+Scenario:\s*(.*)$/.exec(line);
    if (m) { cur = { name: m[1].trim(), lines: [] }; out.push(cur); }
    else if (cur) cur.lines.push(line);
  }
  return out.map((s) => [s.name, s.lines.join("\n")]);
}

function checkBlock(where: string, header: string, body: string, errors: string[]) {
  const desc = body.split(/^####/m)[0];
  if (!/^#### Scenario:/m.test(body)) errors.push(`${where}: ${header} must include at least one scenario (#### Scenario:)`);
  if (!/\b(SHALL|MUST)\b/.test(desc)) errors.push(`${where}: ${header} should contain SHALL or MUST`);
  for (const [name, raw] of scenarioBodies(body)) {
    const trigger = TRIGGER_BOLD.test(raw) || TRIGGER_BARE.test(raw);
    const outcome = OUTCOME_BOLD.test(raw) || OUTCOME_BARE.test(raw);
    if (!(trigger && outcome)) {
      const missing = [["a WHEN/GIVEN step", trigger], ["a THEN step", outcome]].filter(([, ok]) => !ok).map(([m]) => m).join(" and ");
      errors.push(`${where}: ${header} scenario "${name}" is missing ${missing}`);
    }
  }
}

function deltaSections(text: string): Record<string, string> {
  const marks = [...text.matchAll(/^## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements\s*$/gm)];
  const out: Record<string, string> = {};
  marks.forEach((m, i) => {
    const end = i + 1 < marks.length ? marks[i + 1].index! : text.length;
    out[m[1]] = text.slice(m.index! + m[0].length, end);
  });
  return out;
}

// A satellite repository declares `store: <id>` and keeps no specs. Its specs are checked in the spec home.
(satellite ? describe.skip : describe)("OpenSpec rules (TypeScript port)", () => {
  it("keeps main specs valid", () => {
    const errors: string[] = [];
    for (const f of mdFiles(path.join(os, "specs"))) {
      if (path.basename(f) !== "spec.md") continue;
      for (const [header, body] of requirementBlocks(fs.readFileSync(f, "utf8"))) checkBlock(rel(f), header, body, errors);
    }
    expect(errors).toEqual([]);
  });

  it("keeps open changes valid", () => {
    const errors: string[] = [];
    for (const c of openChanges()) {
      const meta = path.join(c, ".openspec.yaml");
      const skip = fs.existsSync(meta) && /^skip_specs:\s*true\s*$/m.test(fs.readFileSync(meta, "utf8"));
      let deltas = 0;
      for (const f of mdFiles(path.join(c, "specs"))) {
        if (path.basename(f) !== "spec.md") continue;
        const secs = deltaSections(fs.readFileSync(f, "utf8"));
        for (const op of ["ADDED", "MODIFIED", "REMOVED"]) {
          for (const [header, body] of requirementBlocks(secs[op] || "")) {
            deltas++;
            if (op !== "REMOVED") checkBlock(rel(f), `${op} ${header}`, body, errors);
          }
        }
        deltas += (secs["RENAMED"] || "").match(/^\s*-\s*FROM:/gm)?.length ?? 0;
      }
      if (deltas === 0 && !skip) errors.push(`${rel(c)}: Change must have at least one delta (or set skip_specs: true in .openspec.yaml)`);
    }
    expect(errors).toEqual([]);
  });
});
