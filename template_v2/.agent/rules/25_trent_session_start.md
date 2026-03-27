---
description: "Session start protocol — quick sync validation and context display"
globs:
alwaysApply: true
---

# Session Start Protocol

## Display at Session Start (when .trent/ exists)
```
📌 SESSION CONTEXT
Mission: [from PROJECT_CONTEXT.md, 1 line]
Goals: G-01: [name] | G-02: [name]
Phase: [current phase]
Ideas: [N] active (from IDEA_BOARD.md)
```

## Sync Validation (Run When User Mentions Tasks/Phases/Status)

**Step 1: Goals Check**
- No PROJECT_GOALS.md or has `{Goal name}` placeholders → auto-generate from PROJECT_CONTEXT.md

**Step 2: Task Sync**
- Compare TASKS.md entries to `.trent/tasks/` AND `.trent/phases/phase*/` files
- Active tasks ([📋][🔄][🔍]): look in tasks/ only
- Completed tasks ([✅]): look in tasks/ AND phases/phase*/
- Phantom = in TASKS.md but file not found in either location

**Step 3: Phase Sync**
- Every TASKS.md phase header → check `phases/phaseN_*.md` exists (definition file, not archive folder)

**Step 4: SUBSYSTEMS.md Staleness**
- Collect `subsystems:` values from task files → compare to SUBSYSTEMS.md
- Missing entries → flag and offer to add stubs

**Step 5: ACTIVE_BACKLOG.md**
- Older than 26 hours → flag as stale, offer regeneration

**Fix issues BEFORE proceeding with user request.**

## Idea Capture Triggers (IMMEDIATE, any time)
Capture to IDEA_BOARD.md when user says:
`"make a note"` | `"remember this"` | `"idea:"` | `"what if we"` | `"someday"` | `"for later"` | `"eventually"`
