from __future__ import annotations

from pathlib import Path
import hashlib
import json

FILES = ("taxonomy-v2.json", "severity-baseline.json", "embedding-adjudication-decisions.json")


def load_static(directory: Path) -> tuple[dict[str, dict], list[dict], str]:
    files = []
    docs = {}
    for filename in FILES:
        blob = (directory / filename).read_bytes()
        document = json.loads(blob)
        digest = hashlib.sha256(blob).hexdigest()
        files.append({"filename": filename, "sha256": digest, "content": document})
        docs[filename] = document
    taxonomy, baselines, decisions = (docs[name] for name in FILES)
    entries = {}
    for row in taxonomy["levelOne"]:
        entries[row["code"]] = {"category_id": row["code"], "level": 1, "name": row["name"], "parent_id": None,
                                "level_one": row["code"], "level_two": "", "status": "ACTIVE", "origin": "FROZEN", "definition": row}
    for row in taxonomy["levelTwo"]:
        entries[row["code"]] = {"category_id": row["code"], "level": 2, "name": row["name"], "parent_id": row["code"].split(".")[0],
                                "level_one": row["code"].split(".")[0], "level_two": row["code"], "status": "ACTIVE", "origin": "FROZEN", "definition": row}
    semantics = {row["id"]: row for row in decisions["decisions"]}
    semantics.update({row["id"]: row for row in taxonomy["newIssueTypeIds"]})
    levels = {key: row["code"] for row in taxonomy["levelTwo"] for key in row.get("issueTypeIds", [])}
    for row in taxonomy["newIssueTypeIds"]:
        if row.get("levelTwo"):
            levels[row["id"]] = row["levelTwo"]
    for row in baselines["baselines"]:
        key = row["id"]
        level_two = levels.get(key, semantics.get(key, {}).get("levelTwo", ""))
        entries[key] = {"category_id": key, "level": 3, "name": row["name"], "parent_id": level_two or None,
                        "level_one": level_two.split(".")[0], "level_two": level_two, "status": "ACTIVE", "origin": "FROZEN",
                        "definition": {**semantics.get(key, {}), **row}}
    entries["PEND"] = {"category_id": "PEND", "level": 1, "name": "待分析或待判断", "parent_id": None,
                       "level_one": "PEND", "level_two": "", "status": "PENDING", "origin": "SYSTEM", "definition": {"reason": "保留尚未完成分析或未确定分类的原始邮件"}}
    digest = hashlib.sha256(json.dumps([(f["filename"], f["sha256"]) for f in files]).encode()).hexdigest()
    return entries, files, digest


def add_dynamic(entries: dict[str, dict], candidates: list[dict], legacy: list[dict]) -> dict[str, dict]:
    result = dict(entries)
    for row in candidates:
        result[row["id"]] = {"category_id": row["id"], "level": 3, "name": row["name"], "parent_id": row.get("levelTwo"),
                             "level_one": row.get("levelOne", ""), "level_two": row.get("levelTwo", ""),
                             "status": row["status"], "origin": "DYNAMIC", "definition": row}
    for row in legacy:
        if row["id"] in result:
            continue
        parent = row.get("canonicalParentCategory", "")
        result[row["id"]] = {"category_id": row["id"], "level": 3, "name": row["canonicalName"], "parent_id": parent or None,
                             "level_one": parent.split(".")[0], "level_two": parent if "." in parent else "",
                             "status": row["status"], "origin": "LEGACY", "definition": row}
    return result
