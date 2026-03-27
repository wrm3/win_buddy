---
name: trent-task-update
description: Step-by-step workflow for updating task status, both in task file and TASKS.md atomically.
---
# trent-task-update

## When to Use
Changing task status (start working, mark complete, pause, fail).

## Status Transitions
```
[ ] → [📋] → [🔄] → [🔍] → [✅]
              ↓         ↓
             [⏸️]       [📋] (verification failed — reset)
             [❌]
```

## Steps

1. **Read current state** (both files):
   - `.trent/tasks/taskNNN_*.md` → current YAML `status:`
   - `.trent/TASKS.md` → current indicator for task NNN
   - Verify they match — if not, fix mismatch first (file is source of truth)

2. **Apply transition**:

| Action | File YAML | TASKS.md |
|---|---|---|
| Start working | `status: in-progress` | `[🔄]` |
| Submit for verification | `status: awaiting-verification` | `[🔍]` |
| Mark complete (verifier only) | `status: completed` | `[✅]` |
| Pause | `status: paused` | `[⏸️]` |
| Mark failed | `status: failed` | `[❌]` |

3. **For in-progress**: also set:
```yaml
claimed_by: "{agent_id}"
claimed_at: "YYYY-MM-DDTHH:MM:SSZ"
claim_ttl_minutes: {estimated * 1.5}
claim_expires_at: "YYYY-MM-DDTHH:MM:SSZ"
```

4. **For completed**: also set:
```yaml
completed_date: "YYYY-MM-DD"
```
   Then run full completion workflow (see trent-task-manager):
   - Validate acceptance criteria
   - Offer git commit
   - Check project files impact

5. **Regenerate dependency graph** (if dependencies changed or task completed):
   - If the task's `dependencies` field was modified, OR the task moved to `completed`/`failed`:
     regenerate `.trent/DEPENDENCY_GRAPH.md` using the `trent-dependency-graph` skill
   - A completed task may unblock others — the graph must reflect this

6. **Print sync confirmation**:
```
Task Sync Confirmation:
- Task {ID} file: status: {new_status} ✅
- TASKS.md entry: [{indicator}] ✅
- Dependency graph: {updated ✅ | no dependency changes, skipped}
- Sync verified: ✅
```
