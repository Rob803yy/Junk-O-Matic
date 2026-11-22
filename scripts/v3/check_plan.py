"""Check the V3-PLAN-R0 information package; not a V3 runtime/field test.

Run from any directory with Python 3.10+: python scripts/v3/check_plan.py
Uses only the standard library. Does not open/review license contents or edit
V2 sources, existing receipts, Office documents or held PDFs.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = "902b8baeac3b8d834a162f9c4661b4664d3f53da"
RECEIPT = ROOT / "reports/v3/planning-validation.json"
METADATA = {"AGENTS.md", "README.md", "docs/README.md",
            "docs/v2/README.md", "docs/repository-layout.md"}
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
checks: list[dict] = []


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check(name: str, condition: bool, detail: object) -> None:
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


def main() -> int:
    scope = read("docs/v3/scope.json")
    plans = read("docs/v3/deliverable-plan.json")
    files = read("docs/v3/file-impact-register.json")["files"]
    components = read("docs/v3/bom-plan.json")["components"]
    requirements = read("docs/v3/requirements.json")["requirements"]
    baseline_bom = read("docs/v2/bom.json")
    baseline = {}
    for entry in git("ls-tree", "-r", "-l", BASE).splitlines():
        head, path = entry.split("\t", 1)
        mode, kind, sha, size = head.split()
        baseline[path] = {"sha": sha, "size": int(size)}

    check("owner mission and design/deployment distinction",
          scope["scope_status"] == "confirmed"
          and scope["design_status"] == "proposed"
          and scope["deployment_status"] == "not_verified"
          and scope["owner_selected_scope"] == (
              "Assisted V3: camera detection, operator alerts and reliable logging; "
              "manual RC controls motion")
          and scope["baseline_main_commit"] == BASE,
          "Only the assisted mission is confirmed; no deployment is asserted.")
    check("scope exclusions and inherited constraints",
          len(scope["excluded"]) == 5 and len(scope["invariants"]) == 8,
          "Reviewable scope/exclusion/invariant records present; not physical proof.")
    check("all baseline paths and Git identities",
          len(files) == len(baseline) == 232
          and len({f["path"] for f in files}) == len(files)
          and {f["path"] for f in files} == set(baseline)
          and all(f["git_blob_sha1"] == baseline[f["path"]]["sha"]
                  and f["bytes"] == baseline[f["path"]]["size"] for f in files),
          {"baseline_commit": BASE, "tracked_files": len(baseline)})
    license_rows = [f for f in files if f["path"].lower().startswith("license")]
    check("license content excluded",
          len(license_rows) == 1 and license_rows[0]["action"] == "preserve_unreviewed",
          "Git path/object metadata listed only; license content not opened.")

    ds = plans["deliverables"]
    ids = {d["id"] for d in ds}
    rids = {r["id"] for r in requirements}
    check("deliverable coverage and requirement references",
          len(ds) == len(ids) == 23 and len(requirements) == len(rids) == 16
          and all(set(d["requirement_ids"]) <= rids for d in ds)
          and all(f["plan_id"] is None or f["plan_id"] in ids for f in files),
          {"deliverable_groups": len(ds), "requirements": len(requirements)})
    unresolved = [p for d in ds for p in d["baseline_paths"]
                  if not any(b == p or b.startswith(p.rstrip("/") + "/") for b in baseline)]
    check("deliverable baseline references resolve", not unresolved, unresolved)
    check("native implementation is not claimed",
          plans["native_artifacts_created"] is False
          and not (ROOT / "hardware/v3").exists()
          and not (ROOT / "software/v3").exists()
          and all(d["review_status"] == "proposed" for d in ds),
          "hardware/v3 and software/v3 are planned destinations, not delivered implementations.")
    check("open requirements do not inherit passes or measurements",
          all(r["verification_status"] == "not_verified"
              and all(r[k] is None for k in
                      ("numeric_target", "numeric_result", "evidence", "reviewer", "review_date"))
              for r in requirements),
          "16 requirements open; numeric targets/results/evidence/review dates blank.")

    byid = {c["id"]: c for c in components}
    inherited = baseline_bom["current"] + baseline_bom["future"]
    check("all BOM source records preserved without promotion",
          len(components) == len(byid) == 79
          and all(byid[c["id"]]["baseline_record"] == c
                  and byid[c["id"]]["inherited_status"] == c["status"]
                  and byid[c["id"]]["verified_installed_qty"]
                  == c.get("verified_installed_qty", c.get("installed_qty"))
                  and byid[c["id"]]["source_listed_qty"] == c.get("source_listed_qty")
                  for c in inherited),
          {"current": len(baseline_bom["current"]), "future": len(baseline_bom["future"]),
           "new_candidate": "CAM-MOUNT1"})
    proposed = {c["id"]: c["proposed_v3_qty"] for c in components if c["proposed_v3_qty"] is not None}
    check("proposed camera quantities distinct from fitted quantities",
          proposed == {"CAM1": 1, "CAM-MOUNT1": 1}
          and all(byid[k]["verified_installed_qty"] is None for k in proposed), proposed)

    for filename, records in [("file-impact-register.csv", files), ("bom-plan.csv", components)]:
        table = list(csv.DictReader(io.StringIO((ROOT / "docs/v3" / filename).read_text(encoding="utf-8-sig"))))
        def flatten(value: object) -> str:
            if value is None:
                return ""
            return "; ".join(value) if isinstance(value, list) else str(value)
        check(filename + " matches JSON view",
              len(table) == len(records)
              and all(all(row[k] == flatten(record[k]) for k in row)
                      for row, record in zip(table, records)),
              {"rows": len(table), "columns": list(table[0])})

    changed = set(git("diff", "--no-renames", "--name-only", BASE).splitlines())
    touched = changed & set(baseline)
    unexpected = sorted(touched - METADATA)
    added = changed - set(baseline)
    untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    allowed = ("docs/v3/", "scripts/v3/", "reports/v3/")
    unexpected += sorted(p for p in added | untracked if not p.startswith(allowed))
    check("V2 runtime/native/archive/Office/receipt preservation", not unexpected,
          {"baseline_navigation_edits": sorted(touched), "unexpected_changes": unexpected})
    held = read("docs/reconciliation/export-status.json")["held_pdfs"]
    check("held PDF hashes preserved",
          len(held) == 13 and all(hashlib.sha256((ROOT / p["path"]).read_bytes()).hexdigest()
                                 == p["sha256"] for p in held),
          {"held_pdfs": len(held), "regenerated": 0})

    broken = []
    for path in [*(ROOT / "docs/v3").glob("*.md"), *(ROOT / p for p in METADATA)]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            target = target.strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-zA-Z][\w+.-]*:", target):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.exists() and resolved != RECEIPT:
                broken.append(f"{path.relative_to(ROOT)}: {target}")
    check("planning and navigation Markdown links resolve", not broken, broken)

    workbook = ROOT / "docs/v3/editable/LitterBuggy_V3_Change_Register.xlsx"
    with zipfile.ZipFile(workbook) as z:
        names = [e.attrib["name"] for e in ET.fromstring(z.read("xl/workbook.xml")).findall("s:sheets/s:sheet", NS)]
        check("saved workbook sheet names", names == ["Deliverables", "File map", "BOM plan", "Requirements"], names)
        ss = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss = ["".join(e.itertext()) for e in ET.fromstring(z.read("xl/sharedStrings.xml"))]
        cells = []
        for i in range(1, 5):
            root = ET.fromstring(z.read(f"xl/worksheets/sheet{i}.xml"))
            values, errors = {}, []
            for c in root.findall("s:sheetData/s:row/s:c", NS):
                if c.get("t") == "e":
                    errors.append(c.attrib["r"])
                v = c.find("s:v", NS)
                value = v.text if v is not None else None
                if c.get("t") == "s" and value is not None:
                    value = ss[int(value)]
                elif c.get("t") == "inlineStr":
                    value = "".join(c.find("s:is", NS).itertext())
                values[c.attrib["r"]] = value
            pane = root.find("s:sheetViews/s:sheetView/s:pane", NS)
            check(names[i-1] + " saved workbook panes/errors",
                  not errors and pane is not None and pane.get("xSplit") == "1" and pane.get("ySplit") == "7",
                  {"formula_error_cells": errors, "freeze": "B8"})
            cells.append(values)
        tables = [ET.fromstring(z.read(p)).get("ref") for p in z.namelist()
                  if re.fullmatch(r"xl/tables/table\d+\.xml", p)]
        check("saved workbook table coverage", set(tables) == {"A7:J30", "A7:H239", "A7:I86", "A7:J23"}, tables)
        check("saved workbook calculated counts", cells[0].get("B5") == "232" and cells[0].get("E5") == "23",
              {"baseline_files": cells[0].get("B5"), "deliverables": cells[0].get("E5")})
        check("saved workbook IDs and baseline paths",
              all(cells[0].get(f"A{i}") == d["id"] for i, d in enumerate(ds, 8))
              and all(cells[1].get(f"A{i}") == f["id"] and cells[1].get(f"B{i}") == f["path"] for i, f in enumerate(files, 8))
              and all(cells[3].get(f"A{i}") == r["id"] for i, r in enumerate(requirements, 8)),
              "Every deliverable/file/requirement row matches the owning JSON.")
        def quantity_matches(value: object, source: object) -> bool:
            if source is None:
                return value is None
            if isinstance(source, (int, float)):
                return value is not None and float(value) == source
            return value == str(source)
        check("saved workbook source/fitted/proposed quantities",
              all(cells[2].get(f"A{i}") == c["id"]
                  and cells[2].get(f"C{i}") == c["inherited_status"]
                  and all(quantity_matches(cells[2].get(f"{col}{i}"), c[key])
                          for col, key in [("E", "source_listed_qty"), ("F", "verified_installed_qty"), ("G", "proposed_v3_qty")])
                  for i, c in enumerate(components, 8)),
              "79 component rows; unknown quantities remain empty.")
        check("saved workbook pending acceptance and reviews",
              all(cells[3].get(f"{col}{i}") is None for i in range(8, 24) for col in "FGIJ")
              and all(cells[3].get(f"H{i}") == "not_verified" for i in range(8, 24))
              and all(cells[0].get(f"H{i}") == "proposed" for i in range(8, 31)),
              "No zero targets/results or completed physical verification inserted.")

    passed = all(c["passed"] for c in checks)
    receipt = {"revision": "V3-PLAN-R0", "baseline_main_commit": BASE,
               "scope": "Planning records, coverage, preservation and saved workbook structure/data only.",
               "status": "passed" if passed else "failed", "checks": checks,
               "workbook_sha256": hashlib.sha256(workbook.read_bytes()).hexdigest(),
               "limitations": ["Native Excel was not opened; workbook was artifact-tool rendered and imported for readback.",
                               "No V3 detector, training, hardware, firmware upload, service installation or field test performed.",
                               "No PDFs regenerated; native/runtime derivatives remain planned."]}
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "checks": len(checks),
                      "failures": [c for c in checks if not c["passed"]],
                      "receipt": str(RECEIPT.relative_to(ROOT))}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
