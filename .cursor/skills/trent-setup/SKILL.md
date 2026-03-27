---
name: trent-setup
description: Initialize the trent task management system in a new project. Creates all required folder structure and template files.
---
# trent-setup

## When to Use
First-time setup of trent in a project. @trent-setup command.

## Steps

1. **Detect if existing** (check before creating anything):
   ```
   □ .trent/TASKS.md exists AND > 20 lines?
   □ .trent/tasks/ has > 5 files?
   □ PROJECT_CONTEXT.md has non-template content?
   → YES: EXISTING project → ask: Merge / Skip / Reset (DESTRUCTIVE)
   → NO: FRESH install → proceed
   ```

2. **Call trent_install MCP tool** (if available):
   ```python
   trent_install(project_path="{absolute_path}", use_v2=True)
   ```

3. **If trent_install unavailable**, create manually:
   - Folders: `.trent/`, `.trent/tasks/`, `.trent/phases/`, `.trent/templates/`, `docs/`, `temp_scripts/`
   - Files: Use trent-project-manager INITIALIZE mode for all file generation

4. **Generate .project_id**:
   ```bash
   python -c "import uuid; print(uuid.uuid4())" > .trent/.project_id
   ```

5. **Verify structure**:
   ```
   .trent/ ✅
   ├── PLAN.md ✅
   ├── TASKS.md ✅
   ├── PROJECT_CONTEXT.md ✅
   ├── BUGS.md ✅
   ├── SUBSYSTEMS.md ✅
   ├── ARCHITECTURE_CONSTRAINTS.md ✅
   ├── PROJECT_GOALS.md ✅
   ├── IDEA_BOARD.md ✅
   ├── .project_id ✅
   ├── tasks/ ✅
   └── phases/ ✅
   docs/ ✅
   temp_scripts/ ✅
   ```

6. **Print next steps**:
   - Review PROJECT_CONTEXT.md and confirm mission
   - Review SUBSYSTEMS.md and adjust detected components
   - Create first task with @trent-task-new
   - Start Phase 0 planning
