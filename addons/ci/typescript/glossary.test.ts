import * as fs from "fs";
import * as path from "path";

// Glossary checks. Pure TypeScript: no child process.
// Same rules as addons/ci/python/test_openspec_rules.py. Keep the messages in step.

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
const glossaryPath = path.join(root, "openspec", "glossary.md");
const ontologyPath = path.join(root, "openspec", "ontology.json");

interface Row { term: string; definition: string; api: string[]; synonyms: string[] }

function parseGlossary(): Row[] {
  if (!fs.existsSync(glossaryPath)) throw new Error("openspec/glossary.md not found");
  const rows: Row[] = [];
  let inTable = false;
  for (const line of fs.readFileSync(glossaryPath, "utf8").split(/\r?\n/)) {
    if (!line.trim().startsWith("|")) continue;
    const cells = line.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
    if (!inTable) { inTable = cells[0].toLowerCase() === "term"; continue; }
    if (cells.every((c) => /^:?-+:?$/.test(c))) continue;
    if (cells[0].startsWith("Example:")) continue;
    rows.push({
      term: cells[0],
      definition: cells[1] || "",
      api: (cells[2] || "").replace(/`/g, "").split(",").map((s) => s.trim()).filter(Boolean),
      synonyms: (cells[3] || "").split(",").map((s) => s.trim()).filter(Boolean),
    });
  }
  return rows;
}

// Specs plus open changes. Archive is history and is skipped.
function specFiles(): string[] {
  const out: string[] = [];
  const walk = (dir: string) => {
    if (!fs.existsSync(dir)) return;
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".md")) out.push(p);
    }
  };
  walk(path.join(root, "openspec", "specs"));
  const changes = path.join(root, "openspec", "changes");
  if (fs.existsSync(changes)) {
    for (const e of fs.readdirSync(changes, { withFileTypes: true })) {
      if (e.isDirectory() && e.name !== "archive") walk(path.join(changes, e.name));
    }
  }
  return out;
}

// Blank out fenced code blocks (keeps line numbers) and, optionally, inline code.
function stripCode(text: string, inline: boolean): string {
  let t = text.replace(/^(```|~~~)[\s\S]*?^\1[^\n]*$/gm, (m) => m.replace(/[^\n]/g, ""));
  if (inline) t = t.replace(/`[^`\n]*`/g, "");
  return t;
}

const rel = (p: string) => path.relative(root, p).split(path.sep).join("/");
const satellite = /^store:/m.test(fs.readFileSync(path.join(root, "openspec", "config.yaml"), "utf8"));
const rows = satellite ? [] : parseGlossary();

// A satellite repository declares `store: <id>` and keeps no specs. Glossary checks run in the spec home.
(satellite ? describe.skip : describe)("Glossary", () => {
  it("gives every term a definition", () => {
    const bad = rows.filter((r) => !r.definition).map((r) => `glossary term '${r.term}' has no definition`);
    expect(bad).toEqual([]);
  });

  it("keeps forbidden synonyms out of specs and open changes", () => {
    const bad: string[] = [];
    for (const f of specFiles()) {
      const lines = stripCode(fs.readFileSync(f, "utf8"), true).split(/\r?\n/);
      for (const r of rows) for (const syn of r.synonyms) {
        const re = new RegExp("\\b" + syn.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b", "i");
        lines.forEach((l, i) => {
          // API names may equal a forbidden word: the concept and the resource are different things
          if (/^\s*(Ontology|Implemented in):/.test(l)) return;
          if (re.test(l)) bad.push(`forbidden synonym '${syn}' (use '${r.term}') in ${rel(f)}:${i + 1}`);
        });
      }
    }
    expect(bad).toEqual([]);
  });

  it("maps Ontology references to the Ontology export, when one exists", () => {
    if (!fs.existsSync(ontologyPath)) return;
    const known = new Set<string>(JSON.parse(fs.readFileSync(ontologyPath, "utf8")));
    const bad: string[] = [];
    for (const r of rows) {
      for (const name of r.api) {
        if (name.toLowerCase() !== "not modelled" && !known.has(name)) {
          bad.push(`glossary API name '${name}' is not in openspec/ontology.json (term '${r.term}')`);
        }
      }
    }
    for (const f of specFiles()) {
      const text = stripCode(fs.readFileSync(f, "utf8"), false);
      for (const m of text.matchAll(/^\s*Ontology:\s*(.+)$/gm)) {
        for (const raw of m[1].split(",")) {
          const name = raw.trim().replace(/`/g, "");
          if (name && !name.startsWith("<") && !known.has(name)) {
            bad.push(`Ontology reference '${name}' in ${rel(f)} is not in openspec/ontology.json`);
          }
        }
      }
    }
    expect(bad).toEqual([]);
  });
});
