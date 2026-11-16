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

  // Rows of every table in ontology.md and logic.md whose header starts with "API name": [names, terms].
  // A link row names both sides ("a / b"); a term cell may hold several terms.
  function modelRows(file: string): Array<[string[], string[]]> {
    const out: Array<[string[], string[]]> = [];
    let termCol = -1, inTable = false;
    for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
      if (!line.trim().startsWith("|")) { inTable = false; continue; }
      const cells = line.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      if (!inTable) {
        inTable = /^api name/i.test(cells[0]);
        termCol = cells.findIndex((c) => /^glossary term/i.test(c));
        continue;
      }
      if (cells.every((c) => /^:?-+:?$/.test(c)) || cells[0].startsWith("`<") || cells[0].startsWith("<")) continue;
      const names = cells[0].replace(/`/g, "").split(/[\/,]/).map((s) => s.trim()).filter(Boolean);
      const terms = termCol < 0 ? [] : (cells[termCol] || "").replace(/`/g, "").split(",").map((s) => s.trim()).filter((t) => t && t.toLowerCase() !== "not modelled");
      out.push([names, terms]);
    }
    return out;
  }

  // The template headers are the contract: a renamed heading or column would silently escape the row checks.
  const REQUIRED: Record<string, string[]> = { "ontology.md": ["Object types", "Link types"], "logic.md": ["Actions"] };
  function headerIssues(file: string): string[] {
    const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
    const body = lines.filter((l, i) => !(i === 0 && l.startsWith("# ")) && l.trim() !== "");
    if (body[0]?.trim() === "None") return []; // the whole file is "None" and a reason
    const out: string[] = [];
    for (const name of REQUIRED[path.basename(file)]) {
      const start = lines.findIndex((l) => l.trim() === "## " + name);
      if (start < 0) { out.push(`${rel(file)}: section '## ${name}' is missing (keep the template headings)`); continue; }
      let end = lines.findIndex((l, i) => i > start && /^## /.test(l));
      if (end < 0) end = lines.length;
      const sec = lines.slice(start + 1, end);
      const header = sec.find((l) => l.trim().startsWith("|"));
      if (!header) { if (!sec.some((l) => l.trim() === "None")) out.push(`${rel(file)}: '## ${name}' has no table and no "None"`); continue; }
      const cells = header.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      if (!/^api name/i.test(cells[0]) || !cells.some((c) => /^glossary term/i.test(c))) out.push(`${rel(file)}: the table under '## ${name}' must keep the headers 'API name' and 'Glossary term'`);
    }
    return out;
  }

  it("keeps ontology.md and logic.md consistent with the glossary and the specs", () => {
    const bad: string[] = [];
    const byTerm = new Map(rows.map((r) => [r.term, r.api]));
    const known = fs.existsSync(ontologyPath) ? new Set<string>(JSON.parse(fs.readFileSync(ontologyPath, "utf8"))) : null;
    const changes = path.join(root, "openspec", "changes");
    if (!fs.existsSync(changes)) return;
    for (const e of fs.readdirSync(changes, { withFileTypes: true })) {
      if (!e.isDirectory() || e.name === "archive") continue;
      const dir = path.join(changes, e.name);
      const files = ["ontology.md", "logic.md"].map((f) => path.join(dir, f)).filter((f) => fs.existsSync(f));
      if (files.length === 0) continue;
      const listed = new Set<string>();
      for (const f of files) {
        bad.push(...headerIssues(f));
        for (const [names, terms] of modelRows(f)) {
          names.forEach((n) => listed.add(n));
          for (const t of terms) {
            const api = byTerm.get(t);
            if (!api) bad.push(`glossary term '${t}' in ${rel(f)} is not in openspec/glossary.md`);
            else if (!names.some((n) => api.includes(n))) bad.push(`'${names.join(" / ")}' in ${rel(f)} is tagged with term '${t}', but that glossary row does not list it`);
          }
        }
      }
      const walk = (d: string) => {
        if (!fs.existsSync(d)) return;
        for (const s of fs.readdirSync(d, { withFileTypes: true })) {
          const p = path.join(d, s.name);
          if (s.isDirectory()) walk(p);
          else if (s.name === "spec.md") {
            for (const m of stripCode(fs.readFileSync(p, "utf8"), false).matchAll(/^\s*Ontology:\s*(.+)$/gm)) {
              for (const raw of m[1].split(",")) {
                const n = raw.trim().replace(/`/g, "");
                if (n && !n.startsWith("<") && !listed.has(n) && !(known && known.has(n))) bad.push(`Ontology reference '${n}' in ${rel(p)} is not listed in ontology.md or logic.md of the change`);
              }
            }
          }
        }
      };
      walk(path.join(dir, "specs"));
    }
    expect(bad).toEqual([]);
  });

  // The gate: a change with tasks.md may not have a blocking question that is still open.
  it("has no blocking open question in a change that already has tasks", () => {
    const bad: string[] = [];
    const changes = path.join(root, "openspec", "changes");
    if (!fs.existsSync(changes)) return;
    for (const e of fs.readdirSync(changes, { withFileTypes: true })) {
      const dir = path.join(changes, e.name);
      const q = path.join(dir, "open-questions.md");
      if (!e.isDirectory() || e.name === "archive" || !fs.existsSync(path.join(dir, "tasks.md")) || !fs.existsSync(q)) continue;
      let col: string[] | null = null;
      for (const line of fs.readFileSync(q, "utf8").split(/\r?\n/)) {
        if (!line.trim().startsWith("|")) continue;
        const cells = line.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
        if (!col) { if (cells[0].toLowerCase() === "id") col = cells.map((c) => c.toLowerCase()); continue; }
        if (cells.every((c) => /^:?-+:?$/.test(c))) continue;
        if ((cells[col.indexOf("blocking")] || "").toLowerCase() === "yes" && (cells[col.indexOf("status")] || "").toLowerCase() === "open") {
          bad.push(`open question '${cells[0]}' is blocking and open in ${rel(q)}, but the change already has tasks.md`);
        }
      }
    }
    expect(bad).toEqual([]);
  });
});
