#!/usr/bin/env python3
"""Build addons/workspace/ from maintainer/upstream/generated/: keep four workflows, point every openspec CLI call at the launcher.

Convention: a repo that uses this kit holds cli/ at tools/openspec/, so the launcher is
./tools/openspec/launchers/openspec (tools\\openspec\\launchers\\openspec.cmd on Windows cmd).
The launcher sets OPENSPEC_TELEMETRY=0. Natural-language triggers such as "openspec propose"
inside quotes are left alone.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LAUNCHER = "./tools/openspec/launchers/openspec"
SUBS = "list|new|status|instructions|context|schemas|schema|store|validate|archive|show|init|change|spec|config|doctor|view"
CALL = re.compile(r'(?<![\w/.\-"])openspec (?=(?:%s)\b)' % SUBS)
TOOL = re.compile(r"Bash\(openspec:\*\)")

# Four workflows (explore, propose, apply, archive), matching core/aip-skills/.
# openspec-sync-specs stays as a skill only: the archive skill runs it inline. sync and update have no entry point.
FLOWS = ("explore", "propose", "apply", "archive")
SKILLS = {"openspec-explore", "openspec-propose", "openspec-apply-change", "openspec-archive-change", "openspec-sync-specs"}


def keep(rel: Path) -> bool:
    top = rel.parts[0]
    if top == "commands":
        return rel.stem in FLOWS
    if top == "prompts":
        return rel.stem.removeprefix("opsx-") in FLOWS
    if top == "skills":
        return rel.parts[1] in SKILLS
    return True


for tool, sub in (("claude", ".claude"), ("continue", ".continue")):
    src = ROOT / "maintainer" / "upstream" / "generated" / tool / sub
    dst = ROOT / "addons" / "workspace" / sub
    shutil.rmtree(dst, ignore_errors=True)
    for f in sorted(src.rglob("*")):
        if not f.is_file() or not keep(f.relative_to(src)):
            continue
        out = dst / f.relative_to(src)
        out.parent.mkdir(parents=True, exist_ok=True)
        text = f.read_text(encoding="utf8")
        text = CALL.sub(LAUNCHER + " ", text)
        text = TOOL.sub("Bash(%s:*)" % LAUNCHER, text)
        out.write_text(text, encoding="utf8")
    print("wrote", dst.relative_to(ROOT))
