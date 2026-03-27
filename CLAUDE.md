# CLAUDE.md - trent

## Project Overview
trent is a comprehensive AI-powered task management and development system for Cursor IDE. It provides structured task tracking, project planning, quality assurance, and workflow management through a file-based system with enforced synchronization.

## Tech Stack
- **Rules**: Cursor `.mdc` format (Markdown Cursor)
- **Skills**: Markdown with YAML frontmatter
- **MCP Server**: Python with FastMCP, PostgreSQL/pgvector for RAG
- **Task Files**: Markdown with YAML frontmatter
- **Package Management**: UV for Python

## Key Directories
```
.cursor/
├── rules/           # .mdc rule files (10-17 are trent core)
├── skills/          # AI skill definitions
├── agents/          # Specialized agent definitions
└── commands/        # @trent-* commands

.trent/              # Task management data
├── PLAN.md          # Product Requirements Document
├── TASKS.md         # Master task list (source of truth)
├── PROJECT_CONTEXT.md
├── tasks/           # Individual task files
└── phases/          # Phase documentation

mcps/trent_docker/   # MCP server with RAG, research tools
template/            # Templates for new project installation
```

## Development Commands
```bash
# Start MCP server (Docker)
cd mcps/trent_docker && docker-compose up -d

# Check MCP server status
docker ps | grep trent

# View MCP logs
docker logs trent -f

# Rebuild after changes
docker-compose up -d --build trent
```

## Coding Conventions
- **Python**: PEP 8, black formatter, type hints
- **Markdown**: YAML frontmatter for metadata
- **Rules (.mdc)**: Must have `description`, `globs`, `alwaysApply` in frontmatter
- **Task files**: `task{id}_{name}.md` format, no underscore after "task"
- **Phase files**: `phase{N}_{name}.md` format

## Testing
- No automated test suite currently
- Manual validation through sync checks
- Use `@trent-task-sync-check` and `@trent-phase-sync-check`

## Important Notes
- **Direct Edit Policy**: Edit `.trent/` files without asking permission
- **Atomic Updates**: Always update TASKS.md AND task files together
- **Phase IDs**: Phase N uses task IDs N×100 to N×100+99
- **Self-Improvement**: Rule 16 triggers issue reporting when problems found
- **Section Markers**: agents.md has protected trent sections between HTML comments

---

<!-- TRENT SYSTEM CONTEXT - DO NOT EDIT MANUALLY -->
## Task Management (Trent)

This project uses trent for task management. Key points:

- **Task data**: `.trent/` folder contains all task files
- **Master list**: `.trent/TASKS.md` is the source of truth
- **Status flow**: [ ] → [📋] → [🔄] → [✅]
- **Phase IDs**: Phase N uses task IDs N×100 to N×100+99
- **Direct edits**: Edit `.trent/` files without asking permission
- **Sync required**: Always update both TASKS.md and task files together

When working on tasks:
1. Check `.trent/TASKS.md` for current status
2. Read task file in `.trent/tasks/` for details
3. Update both files atomically when changing status
<!-- END TRENT SYSTEM CONTEXT -->

---

<!-- Additional context below is safe for manual editing -->

## This Repository's Purpose

This is the **source repository** for the trent system. It contains:
- The complete rule set for task management
- Templates for installing trent in other projects
- MCP server for RAG and research tools
- Documentation and examples

When making changes here, consider:
1. Does this affect the template/ files?
2. Does this need to update agents.md trent section?
3. Should this trigger a version bump?
