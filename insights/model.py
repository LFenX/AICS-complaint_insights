from __future__ import annotations

import base64
import re

from .time_rules import SHANGHAI, received_at

FACT_COLUMNS = ("source_id", "mail_pk", "inbound_mail_id", "ai_artifact_id", "mailbox", "folder_id", "folder_track", "direction",
                "received_at", "business_date", "time_shift_hours", "subject", "from_address", "language", "region", "intent",
                "category_ai", "category_normalized", "level_one", "level_two", "issue_type_id", "priority_ai", "analysis_state",
                "analysis_version", "summary_zh", "raw_message_id", "smtp_message_id", "thread_id", "has_attachment")
ISSUE_COLUMNS = ("source_id", "mail_pk", "issue_point_key", "source_binding_id", "is_primary", "level_one", "level_two", "issue_type_id", "binding_status", "severity", "definition")


def decode_folder(value: str) -> str:
    def convert(match):
        text = match.group(1)
        if not text:
            return "&"
        try:
            return base64.b64decode(text.replace(",", "/") + "=" * (-len(text) % 4)).decode("utf-16-be")
        except (ValueError, UnicodeError):
            return match.group(0)
    return re.sub(r"&([^-]*)-", convert, value)


def folder_track(value: str | None) -> str:
    name = decode_folder(value or "INBOX").strip()
    folded = name.lower().removeprefix("[gmail]/")
    if name in {"INBOX", "收件箱"}:
        return "INBOX"
    if folded in {"sent", "sent items", "sent mail", "已发送", "已发邮件", "发件箱"}:
        return "SENT"
    return {"垃圾邮件": "SPAM", "已归档": "ARCHIVED", "草稿箱": "DRAFT", "已删除": "TRASH"}.get(name, "OTHER")


def category_levels(code: str, entry: dict | None = None) -> tuple[str, str]:
    if entry:
        return entry.get("level_one") or "PEND", entry.get("level_two") or ""
    return (code.split(".")[0], code if "." in code else "") if code else ("PEND", "")


def project_mail(source_id: str, raw: dict, inbound: dict | None, ai: dict | None, bindings: list[dict], mailboxes: dict[str, str], catalog: dict, fallback_skew: int):
    ai = ai or {}
    instant, shift = received_at(raw, fallback_skew)
    state = ai.get("analysisState") or "UNANALYZED"
    normalized = ai.get("category") if ai.get("categorySource", "AI") == "AI" else ai.get("categoryAi")
    ai_code = ai.get("categoryAi")
    classification = normalized or ai_code or "PEND"
    level_one, level_two = category_levels(classification, catalog.get(classification))
    group_id = ai.get("taxonomyGroupId") or ai.get("issueTypeId") or ""
    selected = [row for row in bindings if row.get("source", "AI") == "AI"]
    selected.sort(key=lambda row: (not row.get("isPrimary", False), row.get("issuePointKey", "")))
    primary = selected[0] if selected else None
    if primary:
        group_id = primary.get("catalogIssueTypeId") or primary.get("candidateId") or group_id
        if classification in {"PEND", ""} and primary.get("levelOne"):
            level_one, level_two = primary["levelOne"], primary.get("levelTwo") or ""
    if group_id and group_id in catalog and classification == "PEND":
        level_one, level_two = category_levels(classification, catalog[group_id])
    if state != "DONE":
        # Keep partial suggestions in their original fields; only completed analysis
        # contributes to the classified reporting buckets.
        level_one, level_two, group_id = "PEND", "", ""
    track = folder_track(raw.get("folder_id"))
    direction = "SENT" if track == "SENT" else "EXCLUDED" if track in {"DRAFT", "TRASH"} else "RECEIVED"
    pk = int(raw["id"])
    fact = dict(zip(FACT_COLUMNS, [source_id,pk,(inbound or {}).get("id"),ai.get("id"),mailboxes.get(str(raw.get("mailbox_id")), "UNKNOWN"),
                                 raw.get("folder_id") or "INBOX",track,direction,instant,instant.astimezone(SHANGHAI).date() if instant else None,shift,
                                 raw.get("subject") or "",raw.get("from_address") or "",ai.get("language") or "",ai.get("region"),ai.get("intent"),
                                 ai_code,normalized,level_one,level_two,group_id,ai.get("priorityAi"),state,ai.get("analysisVersion"),ai.get("summaryZh") or "",
                                 raw.get("message_id"),raw.get("smtp_message_id"),raw.get("thread_id"),bool(raw.get("has_attachment"))]))
    issues = []
    for index,row in enumerate(selected):
        issue_id = row.get("catalogIssueTypeId") or row.get("candidateId") or ""
        entry = catalog.get(issue_id, {})
        issues.append(dict(zip(ISSUE_COLUMNS,[source_id,pk,row["issuePointKey"],row.get("id"),index == 0,
                                             row.get("levelOne") or entry.get("level_one") or level_one,
                                             row.get("levelTwo") or entry.get("level_two") or level_two,
                                             issue_id,row.get("bindingStatus") or "UNKNOWN",row.get("severity"),row])))
    if not issues:
        issues.append(dict(zip(ISSUE_COLUMNS,[source_id,pk,"__primary__",None,True,level_one,level_two,group_id,
                                             "RESOLVED" if state == "DONE" and group_id else state,None,{"synthetic":True,"reason":"无逐问题绑定，保留邮件主分类与分析状态"}])))
    return fact, issues
