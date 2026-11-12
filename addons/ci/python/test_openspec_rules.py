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
            for header, body in requirement_blocks(f.read_text(encoding="utf8")):
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
            "api": cells[2].replace("`", ""),
            "synonyms": [s.strip() for s in cells[3].split(",") if s.strip()],
        })
    return rows


def strip_code(text: str, inline: bool) -> str:
    t = re.sub(r"^(```|~~~)[\s\S]*?^\1[^\n]*$", lambda m: re.sub(r"[^\n]", "", m.group(0)), text, flags=re.M)
    return re.sub(r"`[^`\n]*`", "", t) if inline else t


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
            if r["api"] and r["api"].lower() != "not modelled" and r["api"] not in known:
                bad.append(f"glossary API name '{r['api']}' is not in openspec/ontology.json (term '{r['term']}')")
        for f in spec_files():
            text = strip_code(f.read_text(encoding="utf8"), False)
            for m in re.finditer(r"^\s*Ontology:\s*(.+)$", text, re.M):
                for raw in m.group(1).split(","):
                    name = raw.strip().replace("`", "")
                    if name and not name.startswith("<") and name not in known:
                        bad.append(f"Ontology reference '{name}' in {rel(f)} is not in openspec/ontology.json")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
