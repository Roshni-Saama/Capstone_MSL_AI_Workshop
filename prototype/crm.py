"""Read-only helpers for the fictional CRM fixture and its dated snapshot."""
from datetime import date

TASK_STATUSES = {"Open", "In progress", "Awaiting review", "Completed"}


def validate_crm_records(records):
    seen_ids = set()
    for record in records:
        kol_id = record["kol_id"]
        profile = record.get("crm_profile")
        if not isinstance(profile, dict) or not profile.get("crm_record_id"):
            raise ValueError("Each synthetic record needs CRM profile metadata.")
        snapshot = date.fromisoformat(profile["snapshot_date"])
        date.fromisoformat(profile["profile_reviewed_on"])
        interactions = record.get("interactions", [])
        tasks = record.get("tasks", [])
        requests = record.get("medical_requests", [])
        if not interactions or not tasks or not requests:
            raise ValueError("Synthetic CRM needs interactions, tasks and requests.")
        engagement_ids = {row["engagement_id"] for row in interactions}
        task_ids = {row["task_id"] for row in tasks}
        for rows, id_field in [(interactions, "engagement_id"), (tasks, "task_id"),
                               (requests, "request_id")]:
            for row in rows:
                identifier = row[id_field]
                if row.get("kol_id") != kol_id:
                    raise ValueError("CRM child record belongs to a different KOL.")
                if identifier in seen_ids:
                    raise ValueError("Duplicate synthetic CRM child identifier.")
                seen_ids.add(identifier)
        for interaction in interactions:
            if date.fromisoformat(interaction["date"]) > snapshot:
                raise ValueError("Prior interaction cannot occur after the snapshot.")
            if interaction["task_id"] not in task_ids:
                raise ValueError("Interaction references an unknown task.")
        for task in tasks:
            if task["engagement_id"] not in engagement_ids:
                raise ValueError("Task references an unknown engagement.")
            if task["status"] not in TASK_STATUSES:
                raise ValueError("Unknown synthetic task status.")
            created = date.fromisoformat(task["created_on"])
            due = date.fromisoformat(task["due_date"])
            if due < created or created > snapshot:
                raise ValueError("Invalid synthetic task dates.")
            if task["status"] == "Completed":
                if not task.get("completed_on") or not task.get("closure_note"):
                    raise ValueError("Completed task needs dated synthetic closure evidence.")
                completed = date.fromisoformat(task["completed_on"])
                if completed < created or completed > snapshot:
                    raise ValueError("Invalid synthetic completion date.")
            elif task.get("completed_on") or task.get("closure_note"):
                raise ValueError("Unfinished task must not claim completion.")
        for request in requests:
            if request["engagement_id"] not in engagement_ids or request["task_id"] not in task_ids:
                raise ValueError("Request references unknown CRM records.")
            if date.fromisoformat(request["received_on"]) > snapshot:
                raise ValueError("Request cannot occur after the snapshot.")


def task_rows(record):
    snapshot = date.fromisoformat(record["crm_profile"]["snapshot_date"])
    return [{"Task ID": task["task_id"], "Task": task["title"], "Owner": task["owner_role"],
             "Status": task["status"], "Due date": task["due_date"],
             "Overdue": task["status"] != "Completed" and date.fromisoformat(task["due_date"]) < snapshot,
             "Completed on": task.get("completed_on") or "Not completed",
             "Closure evidence": task.get("closure_note") or "None recorded"}
            for task in record["tasks"]]


def crm_summary(record):
    rows = task_rows(record)
    return {"interactions": len(record["interactions"]),
            "active_tasks": sum(row["Status"] != "Completed" for row in rows),
            "overdue_tasks": sum(row["Overdue"] for row in rows),
            "requests": len(record["medical_requests"])}


def format_crm_details(record):
    profile = record["crm_profile"]
    lines = ["CRM profile and latest task snapshot (not scientific evidence):",
             f"CRM record: {profile['crm_record_id']}; snapshot: {profile['snapshot_date']}",
             f"Territory: {profile['territory']}; assigned role: {profile['assigned_msl_role']}",
             f"Preferred channel: {profile['preferred_channel']}",
             f"Scientific interests (topics only): {', '.join(profile['scientific_interests'])}",
             "Current tasks (interaction notes above are historical snapshots):"]
    for row in task_rows(record):
        lines.append(f"- {row['Task ID']}: {row['Task']} Owner: {row['Owner']}; status: {row['Status']}; due: {row['Due date']}; overdue at snapshot: {row['Overdue']}.")
    lines.append("Medical-information requests (questions, not clinical findings):")
    for request in record["medical_requests"]:
        lines.append(f"- {request['request_id']}: {request['question']} Status: {request['status']}; response: {request['response_status']}.")
    return "\n".join(lines)
