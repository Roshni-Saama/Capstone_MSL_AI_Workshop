# Synthetic CRM data

Every person, organization, assignment, date, request and completion record is invented. This is workshop interaction context, not clinical evidence or real CRM data. No real contact or patient details are included.

The application reads [kol_records.json](../kol_records.json), schema version 2, with a fixed snapshot date of **23 October 2026**. CSV files here are human-readable exports of that fixture; editing CSV alone does not change the app. Keep exports synchronized with any future JSON edits.

| File | Records | Purpose |
| --- | --- | --- |
| [profiles.csv](profiles.csv) | 3 | Fictional profiles, institution IDs, interests, territory, assigned role and channel |
| [interactions.csv](interactions.csv) | 9 | Dated engagement history, observations and separate interpretations |
| [tasks.csv](tasks.csv) | 9 | Latest task status, owner role, due date and synthetic administrative closure |
| [medical_requests.csv](medical_requests.csv) | 6 | Fictional evidence questions, linked tasks and response status |

Identifiers link records using kol_id, engagement_id and task_id. An interaction contains the task status at that historical meeting; the tasks array contains the latest fixture status. Dates and IDs do not imply that the application sent a response or completed a task.

Overdue means unfinished and due before the fixed snapshot date; tasks due on the snapshot day are not overdue. Completed tasks are excluded even when their due date is in the past. The app does not update the fixture or calculate this against the execution host date.

In the prototype, select a KOL and inspect CRM profile, Interaction timeline, Follow-up tasks and Medical requests. In OpenAI mode the chosen KOL's CRM context is included only in the KOL Context Agent request; it is not scientific evidence. See [scenario walkthroughs](../../test_scenarios/use_cases.md).
