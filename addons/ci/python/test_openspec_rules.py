"""Standard-library port of OpenSpec validation rules plus the glossary rules.

For repositories without Node. Run:  python3 test_openspec_rules.py
Root: OPENSPEC_ROOT, else the nearest parent of this file with openspec/config.yaml.
OPENSPEC_SKIP_GLOSSARY=1 runs the OpenSpec rules only (used for parity checks).
Rules and messages match addons/ci/typescript/glossary.test.ts.
"""
import json
import os
import re
import unittest
from pathlib import Path


def find_root() -> Path:
    if os.environ.get("OPENSPEC_ROOT"):
        return Path(os.environ["OPENSPEC_ROOT"])
    d = Path(__file__).resolve().parent
    while not (d / "openspec" / "config.yaml").exists():
        if d.parent == d:
            raise RuntimeError("openspec/config.yaml not found above " + __file__)
        d = d.parent
    return d


ROOT = find_root()
OS = ROOT / "openspec"
SKIP_GLOSSARY = os.environ.get("OPENSPEC_SKIP_GLOSSARY") == "1"
# A satellite repository declares `store: <id>` and keeps no specs. Its specs are checked in the spec home.
SATELLITE = re.search(r"^store:", (OS / "config.yaml").read_text(encoding="utf8"), re.M) is not None


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def md_files(base: Path):
    return sorted(base.rglob("*.md")) if base.exists() else []


def open_changes():
    d = OS / "changes"
    if not d.exists():
        return []
    return sorted(p for p in d.iterdir() if p.is_dir() and p.name != "archive")


def spec_files():
    out = md_files(OS / "specs")
    for c in open_changes():
        out += md_files(c)
    return out


# ---- OpenSpec rules ---------------------------------------------------------

REQ = re.compile(r"^### Requirement:.*$", re.M)
SECTION = re.compile(r"^## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements\s*$", re.M)


def requirement_blocks(text: str):
    """Yield (header, body) for each requirement block."""
    marks = [m for m in REQ.finditer(text)]
    # a block ends at the next requirement or the next "## " section
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        nxt = re.search(r"^## ", text[m.end():end], re.M)
        if nxt:
            end = m.end() + nxt.start()
        yield m.group(0).strip(), text[m.end():end]


# Same step detection as OpenSpec: a trigger (WHEN or GIVEN) and an outcome (THEN), anywhere in the scenario.
TRIGGER_BOLD = re.compile(r"(?:\*\*|__)(?:WHEN|GIVEN):?(?:\*\*|__)", re.I)
TRIGGER_BARE = re.compile(r"\b(?:WHEN|GIVEN)\b")
OUTCOME_BOLD = re.compile(r"(?:\*\*|__)THEN:?(?:\*\*|__)", re.I)
OUTCOME_BARE = re.compile(r"\bTHEN\b")


def scenario_bodies(body: str):
    """Yield (name, text) for each '#### Scenario:' block, skipping fenced code. A scenario ends at the next heading of level 1-4."""
    out, cur, fence = [], None, False
    for line in body.splitlines():
        if re.match(r"^(```|~~~)", line):
            fence = not fence
            continue
        if fence:
            if cur is not None:
                cur[1].append("")
            continue
        if re.match(r"^#{1,4}\s", line):
            cur = None
        m = re.match(r"^####\s+Scenario:\s*(.*)$", line)
        if m:
            cur = (m.group(1).strip(), [])
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return [(n, "\n".join(t)) for n, t in out]


def check_block(where: str, header: str, body: str, errors: list):
    desc = re.split(r"^####", body, maxsplit=1, flags=re.M)[0]
    if not re.search(r"^#### Scenario:", body, re.M):
        errors.append(f"{where}: {header} must include at least one scenario (#### Scenario:)")
    if not re.search(r"\b(SHALL|MUST)\b", desc):
        errors.append(f"{where}: {header} should contain SHALL or MUST")
    for name, raw in scenario_bodies(body):
        trigger = TRIGGER_BOLD.search(raw) or TRIGGER_BARE.search(raw)
        outcome = OUTCOME_BOLD.search(raw) or OUTCOME_BARE.search(raw)
        if not (trigger and outcome):
            missing = " and ".join(m for m, ok in (("a WHEN/GIVEN step", trigger), ("a THEN step", outcome)) if not ok)
            errors.append(f'{where}: {header} scenario "{name}" is missing {missing}')


def delta_sections(text: str):
    """Return {operation: section text}."""
    marks = list(SECTION.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[m.group(1)] = text[m.end():end]
    return out


@unittest.skipIf(SATELLITE, "satellite repository: specs live in the store")
class OpenSpecRules(unittest.TestCase):
    def test_main_specs(self):
        errors = []
        for f in md_files(OS / "specs"):
            if f.name != "spec.md":
                continue
            text = f.read_text(encoding="utf8")
            # OpenSpec warns (an error under --strict) on a Purpose under 50 characters or a TBD placeholder.
            m = re.search(r"^## Purpose\s*$([\s\S]*?)(?=^## |\Z)", text, re.M)
            if not m:
                errors.append(f"{rel(f)}: Spec must have a Purpose section")
            elif len(m.group(1).strip()) < 50 or m.group(1).strip().upper().startswith("TBD"):
                errors.append(f"{rel(f)}: Purpose section is too brief (less than 50 characters) or still a placeholder")
            for header, body in requirement_blocks(text):
                check_block(rel(f), header, body, errors)
        self.assertEqual(errors, [])

    def test_changes(self):
        errors = []
        for c in open_changes():
            meta = c / ".openspec.yaml"
            skip = meta.exists() and re.search(r"^skip_specs:\s*true\s*$", meta.read_text(encoding="utf8"), re.M)
            deltas = 0
            for f in md_files(c / "specs"):
                if f.name != "spec.md":
                    continue
                secs = delta_sections(f.read_text(encoding="utf8"))
                for op in ("ADDED", "MODIFIED", "REMOVED"):
                    for header, body in requirement_blocks(secs.get(op, "")):
                        deltas += 1
                        if op != "REMOVED":
                            check_block(rel(f), f"{op} {header}", body, errors)
                deltas += len(re.findall(r"^\s*-\s*FROM:", secs.get("RENAMED", ""), re.M))
            if deltas == 0 and not skip:
                errors.append(f"{rel(c)}: Change must have at least one delta (or set skip_specs: true in .openspec.yaml)")
        self.assertEqual(errors, [])


# ---- Glossary rules ---------------------------------------------------------

def parse_glossary():
    p = OS / "glossary.md"
    if not p.exists():
        raise AssertionError("openspec/glossary.md not found")
    rows, in_table = [], False
    for line in p.read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not in_table:
            in_table = cells[0].lower() == "term"
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        if cells[0].startswith("Example:"):
            continue
        cells += [""] * (4 - len(cells))
        rows.append({
            "term": cells[0],
            "definition": cells[1],
            "api": [n.strip() for n in cells[2].replace("`", "").split(",") if n.strip()],
            "synonyms": [s.strip() for s in cells[3].split(",") if s.strip()],
        })
    return rows


def strip_code(text: str, inline: bool) -> str:
    t = re.sub(r"^(```|~~~)[\s\S]*?^\1[^\n]*$", lambda m: re.sub(r"[^\n]", "", m.group(0)), text, flags=re.M)
    return re.sub(r"`[^`\n]*`", "", t) if inline else t


def model_rows(f: Path):
    """Rows of every table in ontology.md or logic.md whose header starts with "API name": (names, terms).
    A link row names both sides ("a / b"); a term cell may hold several terms."""
    out, term_col, in_table = [], -1, False
    for line in f.read_text(encoding="utf8").splitlines():
        if not line.strip().startswith("|"):
            in_table = False
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if not in_table:
            in_table = cells[0].lower().startswith("api name")
            term_col = next((i for i, x in enumerate(cells) if x.lower().startswith("glossary term")), -1)
            continue
        if all(re.fullmatch(r":?-+:?", x) for x in cells) or cells[0].startswith(("`<", "<")):
            continue
        names = [n.strip() for n in re.split(r"[/,]", cells[0].replace("`", "")) if n.strip()]
        terms = [] if term_col < 0 or term_col >= len(cells) else [t.strip() for t in cells[term_col].replace("`", "").split(",") if t.strip() and t.strip().lower() != "not modelled"]
        out.append((names, terms))
    return out


# The template headers are the contract: a renamed heading or column would silently escape the row checks.
REQUIRED = {"ontology.md": ["Object types", "Link types"], "logic.md": ["Actions"]}


def header_issues(f: Path):
    lines = f.read_text(encoding="utf8").splitlines()
    body = [l for i, l in enumerate(lines) if not (i == 0 and l.startswith("# ")) and l.strip()]
    if body and body[0].strip() == "None":  # the whole file is "None" and a reason
        return []
    out = []
    for name in REQUIRED[f.name]:
        starts = [i for i, l in enumerate(lines) if l.strip() == "## " + name]
        if not starts:
            out.append(f"{rel(f)}: section '## {name}' is missing (keep the template headings)")
            continue
        start = starts[0]
        end = next((i for i, l in enumerate(lines) if i > start and l.startswith("## ")), len(lines))
        sec = lines[start + 1:end]
        header = next((l for l in sec if l.strip().startswith("|")), None)
        if header is None:
            if not any(l.strip() == "None" for l in sec):
                out.append(f"{rel(f)}: '## {name}' has no table and no \"None\"")
            continue
        cells = [x.strip() for x in header.strip().strip("|").split("|")]
        if not cells[0].lower().startswith("api name") or not any(x.lower().startswith("glossary term") for x in cells):
            out.append(f"{rel(f)}: the table under '## {name}' must keep the headers 'API name' and 'Glossary term'")
    return out


@unittest.skipIf(SKIP_GLOSSARY or SATELLITE, "glossary rules skipped")
class GlossaryRules(unittest.TestCase):
    def test_definitions(self):
        bad = [f"glossary term '{r['term']}' has no definition" for r in parse_glossary() if not r["definition"]]
        self.assertEqual(bad, [])

    def test_forbidden_synonyms(self):
        bad = []
        rows = parse_glossary()
        for f in spec_files():
            lines = strip_code(f.read_text(encoding="utf8"), True).splitlines()
            for r in rows:
                for syn in r["synonyms"]:
                    pat = re.compile(r"\b" + re.escape(syn) + r"\b", re.I)
                    for i, line in enumerate(lines, 1):
                        # API names may equal a forbidden word: the concept and the resource are different things
                        if re.match(r"\s*(Ontology|Implemented in):", line):
                            continue
                        if pat.search(line):
                            bad.append(f"forbidden synonym '{syn}' (use '{r['term']}') in {rel(f)}:{i}")
        self.assertEqual(bad, [])

    def test_ontology_names(self):
        p = OS / "ontology.json"
        if not p.exists():
            return
        known = set(json.loads(p.read_text(encoding="utf8")))
        bad = []
        for r in parse_glossary():
            for name in r["api"]:
                if name.lower() != "not modelled" and name not in known:
                    bad.append(f"glossary API name '{name}' is not in openspec/ontology.json (term '{r['term']}')")
        for f in spec_files():
            text = strip_code(f.read_text(encoding="utf8"), False)
            for m in re.finditer(r"^\s*Ontology:\s*(.+)$", text, re.M):
                for raw in m.group(1).split(","):
                    name = raw.strip().replace("`", "")
                    if name and not name.startswith("<") and name not in known:
                        bad.append(f"Ontology reference '{name}' in {rel(f)} is not in openspec/ontology.json")
        self.assertEqual(bad, [])

    def test_model_consistency(self):
        """Resources tagged with a glossary term are on that term's row; Ontology: names are listed in ontology.md or logic.md."""
        bad = []
        by_term = {r["term"]: r["api"] for r in parse_glossary()}
        p = OS / "ontology.json"
        known = set(json.loads(p.read_text(encoding="utf8"))) if p.exists() else None
        for c in open_changes():
            files = [c / f for f in ("ontology.md", "logic.md") if (c / f).exists()]
            if not files:
                continue
            listed = set()
            for f in files:
                bad += header_issues(f)
                for names, terms in model_rows(f):
                    listed.update(names)
                    for t in terms:
                        if t not in by_term:
                            bad.append(f"glossary term '{t}' in {rel(f)} is not in openspec/glossary.md")
                        elif not any(n in by_term[t] for n in names):
                            bad.append(f"'{' / '.join(names)}' in {rel(f)} is tagged with term '{t}', but that glossary row does not list it")
            for f in md_files(c / "specs"):
                if f.name != "spec.md":
                    continue
                text = strip_code(f.read_text(encoding="utf8"), False)
                for m in re.finditer(r"^\s*Ontology:\s*(.+)$", text, re.M):
                    for raw in m.group(1).split(","):
                        n = raw.strip().replace("`", "")
                        if n and not n.startswith("<") and n not in listed and not (known and n in known):
                            bad.append(f"Ontology reference '{n}' in {rel(f)} is not listed in ontology.md or logic.md of the change")
        self.assertEqual(bad, [])

    def test_index_lists_cited_names(self):
        """Drift: every Ontology: name in a main spec has a row under Resources in openspec/INDEX.md (or openspec/index/*.md)."""
        main = OS / "INDEX.md"
        if not main.exists():
            return
        files = [main] + sorted((OS / "index").glob("*.md"))
        indexed, bad = set(), []
        for f in files:
            in_table = False
            for line in f.read_text(encoding="utf8").splitlines():
                if not line.strip().startswith("|"):
                    in_table = False
                    continue
                cells = [x.strip() for x in line.strip().strip("|").split("|")]
                if not in_table:
                    in_table = cells[0].lower().startswith("api name")
                    continue
                if all(re.fullmatch(r":?-+:?", x) for x in cells) or cells[0].startswith("Example:"):
                    continue
                indexed.update(n.strip() for n in cells[0].replace("`", "").split(",") if n.strip())
        for f in md_files(OS / "specs"):
            if f.name != "spec.md":
                continue
            text = strip_code(f.read_text(encoding="utf8"), False)
            for m in re.finditer(r"^\s*Ontology:\s*(.+)$", text, re.M):
                for raw in m.group(1).split(","):
                    n = raw.strip().replace("`", "")
                    if n and not n.startswith("<") and n not in indexed:
                        bad.append(f"Ontology reference '{n}' in {rel(f)} has no row under Resources in openspec/INDEX.md")
        self.assertEqual(bad, [])

    def test_rulebook_review(self):
        """Once openspec/rulebook/ holds real rules, a change with tasks.md records each applicable rule in design.md."""
        ids = set()
        for f in sorted((OS / "rulebook").glob("*.md")):
            if f.name == "README.md":
                continue
            in_table = False
            for line in f.read_text(encoding="utf8").splitlines():
                if not line.strip().startswith("|"):
                    in_table = False
                    continue
                cells = [x.strip() for x in line.strip().strip("|").split("|")]
                if not in_table:
                    in_table = cells[0].lower() == "id"
                    continue
                if all(re.fullmatch(r":?-+:?", x) for x in cells) or cells[0].startswith("Example:"):
                    continue
                ids.add(cells[0].replace("`", ""))
        if not ids:
            return
        bad = []
        for c in open_changes():
            design = c / "design.md"
            if not (c / "tasks.md").exists() or not design.exists():
                continue
            lines = design.read_text(encoding="utf8").splitlines()
            start = next((i for i, l in enumerate(lines) if l.strip() == "## Rulebook review"), None)
            if start is None:
                bad.append(f"{rel(design)}: has no '## Rulebook review', but openspec/rulebook/ has rules")
                continue
            end = next((i for i, l in enumerate(lines) if i > start and l.startswith("## ")), len(lines))
            rows, in_table = 0, False
            for line in lines[start + 1:end]:
                if not line.strip().startswith("|"):
                    in_table = False
                    continue
                cells = [x.strip() for x in line.strip().strip("|").split("|")]
                if not in_table:
                    in_table = cells[0].lower() == "rule"
                    continue
                if all(re.fullmatch(r":?-+:?", x) for x in cells):
                    continue
                rid = cells[0].replace("`", "")
                if rid.startswith("<"):
                    continue
                rows += 1
                cells += [""] * (4 - len(cells))
                result = cells[1].lower()
                if rid not in ids:
                    bad.append(f"rule '{rid}' in {rel(design)} is not in openspec/rulebook/")
                if result not in ("complies", "deviates", "open"):
                    bad.append(f"rule '{rid}' in {rel(design)} has result '{cells[1]}' (use complies, deviates or open)")
                elif result != "complies" and not cells[3]:
                    bad.append(f"rule '{rid}' in {rel(design)} is '{result}' and needs a reason or an open question")
            if rows == 0:
                bad.append(f"{rel(design)}: '## Rulebook review' has no rule rows, but openspec/rulebook/ has rules")
        self.assertEqual(bad, [])

    def test_blocking_open_questions(self):
        """The gate: a change with tasks.md may not have a blocking question that is still open."""
        bad = []
        for c in open_changes():
            q = c / "open-questions.md"
            if not (c / "tasks.md").exists() or not q.exists():
                continue
            col = None
            for line in q.read_text(encoding="utf8").splitlines():
                if not line.strip().startswith("|"):
                    continue
                cells = [x.strip() for x in line.strip().strip("|").split("|")]
                if col is None:
                    if cells[0].lower() == "id":
                        col = [x.lower() for x in cells]
                    continue
                if all(re.fullmatch(r":?-+:?", x) for x in cells):
                    continue
                cells += [""] * (len(col) - len(cells))
                if cells[col.index("blocking")].lower() == "yes" and cells[col.index("status")].lower() == "open":
                    bad.append(f"open question '{cells[0]}' is blocking and open in {rel(q)}, but the change already has tasks.md")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
