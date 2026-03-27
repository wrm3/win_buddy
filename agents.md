# agents.md - trent

> **AI Development System for Cursor IDE & Claude Code**
> This file follows the agents.md format for AI agent instructions.
> Compatible with both Cursor (`.cursor/`) and Claude Code (`.claude/`).

---

## Project Overview

**trent** - A comprehensive AI-powered development system

**Purpose**: Provide a unified development environment for **Cursor IDE** and **Claude Code** with agent capabilities, skills, and task management.

**Core Features**:
- **Task Management**: Create, track, and complete tasks with status tracking
- **Project Planning**: PRD creation, feature specifications, scope management
- **Quality Assurance**: Bug tracking, severity classification, resolution tracking
- **Specialized Agents**: 22 agents for different development roles
- **Development Skills**: 16 skills covering AI/ML, code review, planning, and more
- **Dual IDE Support**: Full parity between `.cursor/` and `.claude/` configurations

---

## Project Structure

```
.trent/                        # Core task management (READ THIS FIRST)
├── PLAN.md                    # Product Requirements Document
├── TASKS.md                   # Master task checklist with status
├── BUGS.md                    # Bug tracking
├── PROJECT_CONTEXT.md         # Project mission and goals
├── SUBSYSTEMS.md              # Component registry
├── tasks/                     # Individual task files (task{id}_name.md)
└── phases/                    # Phase documentation

.cursor/                       # Cursor IDE configuration
├── skills/                    # 16 AI Skills
├── agents/                    # 22 Specialized agents
├── rules/                     # .mdc format rules (numbered 00-81)
├── commands/                  # 22 @trent-* commands
└── hooks/                     # PowerShell automation hooks

.claude/                       # Claude Code configuration (parity with .cursor/)
├── skills/                    # 16 AI Skills (same as .cursor/)
├── agents/                    # 22 Specialized agents (same as .cursor/)
├── rules/                     # .md format rules (same content, .md extension)
├── commands/                  # 22 /trent-* commands
├── hooks/                     # PowerShell automation hooks
├── hooks.json                 # Hook event configuration
└── settings.local.json        # MCP and permissions config

docker/                        # MCP Server (Docker)
├── trent/                     # Main server code + plugins
└── docker-compose.yml

templates/                     # Install templates (trent-only, canonical source)
templates_full/                # Full install templates (all skills/agents)

docs/                          # Project documentation
```

---

## Available Agents (22)

### Core Development

| Agent | Description | Best For |
|-------|-------------|----------|
| `backend-developer` | API design, server logic, database integration | Backend APIs, business logic |
| `frontend-developer` | React, TypeScript, UI components | User interfaces, responsive design |
| `full-stack-developer` | End-to-end implementation | Complete features |
| `api-designer` | REST/GraphQL API design | API contracts |
| `solution-architect` | System architecture, tech selection | Architectural decisions |

### Quality & Testing

| Agent | Description | Best For |
|-------|-------------|----------|
| `qa-engineer` | Test planning, quality metrics | Quality assurance |
| `code-reviewer` | Code quality, best practices | Code reviews |

### AI & ML

| Agent | Description | Best For |
|-------|-------------|----------|
| `ai-model-developer` | AI/ML model development | Model creation |
| `ai-model-trainer` | Model training and fine-tuning | Training pipelines |
| `mlops-engineer` | ML operations and deployment | ML infrastructure |

### IDE & Config

| Agent | Description | Best For |
|-------|-------------|----------|
| `claude-cli` | Claude CLI operations | Claude Code automation |
| `cursor-cli` | Cursor CLI operations | Cursor IDE automation |
| `claude-config-maintainer` | .claude/ config management | Claude project setup |
| `cursor-config-maintainer` | .cursor/ config management | Cursor project setup |

### Specialized

| Agent | Description | Best For |
|-------|-------------|----------|
| `orchestrator` | Multi-agent coordination | Complex multi-agent tasks |
| `agent-creator` | Create new agent definitions | Meta/system |
| `skill-creator` | Create new skill definitions | Meta/system |
| `trent-project-initializer` | Project setup and scaffolding | New project init |
| `trent-task-expander` | Task breakdown, complexity assessment | Task decomposition |
| `codebase-analyst` | Deep merge your own projects | Project integration |
| `harvest-analyst` | Harvest ideas from external sources | Selective improvements |
| `silicon-valley-superfan` | HBO Silicon Valley expert | Show trivia and references |

---

## Available Skills (16)

### Core Task Management
- `trent-task-management` - Task lifecycle and status management
- `trent-planning` - PRD creation, phase management, and project planning
- `trent-qa` - Bug tracking and quality assurance
- `trent-code-reviewer` - Comprehensive code reviews
- `trent-ideas-goals` - Idea board and project goals management

### AI & ML
- `ai-ml-development` - AI/ML model training, development, and deployment

### Integration & Tools
- `github-integration` - GitHub workflows and automation
- `mcp-builder` - MCP server development

### Codebase Analysis
- `codebase-integration-analysis` - Deep project merging and architecture mapping
- `selective-harvest` - Harvest improvements from external sources

### IDE Configuration
- `claude-code-project-config` - .claude/ project configuration management
- `cursor-project-config` - .cursor/ project configuration management

### Utilities
- `project-setup` - Project initialization
- `skill-creator` - Create new skills
- `agent-creator` - Create new agent definitions
- `silicon-valley-superfan` - HBO Silicon Valley knowledge base

---

## MCP Tools (Docker Server)

| Tool | Description |
|------|-------------|
| `rag_search` | Semantic search in knowledge base |
| `rag_ingest_text` | Add content to knowledge base |
| `rag_list_subjects` | List available knowledge bases |
| `oracle_query` | Read-only SQL on Oracle (SELECT, DESCRIBE) |
| `oracle_execute` | Write SQL on Oracle (INSERT, UPDATE, DDL) |
| `md_to_html` | Convert markdown to styled HTML |
| `trent_install` | Install full trent environment to a project (auto-generates .trent/.project_id) |
| `trent_rules_update` | Update IDE configs/rules (preserves .trent/ task data) |
| `trent_plan_reset` | Reset .trent/ to blank template (requires confirm=True) |
| `trent_server_status` | Health check |
| `memory_ingest_session` | Tier-1 passive capture: ingest raw turns from file adapters (Cursor, Claude Code) |
| `memory_capture_session` | Tier-2 active capture: AI self-reports session summary (Gemini, VS Code) |
| `memory_search` | Semantic search over captured session memory |
| `memory_sessions` | List recent sessions for a project |
| `memory_context` | Return token-budgeted context block for session-start injection |
| `vault_sync` | Index a vault .md file into the database (agent passes content) |
| `vault_search` | Semantic/keyword search against vault_notes table |
| `vault_search_all` | **Unified search** across vault_notes + platform_docs + agent_memory + sessions |
| `vault_read` | Read full note content from DB by path |
| `vault_list` | Browse/filter vault notes by type, project, tags, path prefix |
| `vault_export_sessions` | Export recent session summaries as vault-ready .md content |

---

## Task Management

### Task File Format

```yaml
---
id: {number}
title: 'Task Title'
type: feature|bug_fix|refactor|documentation
status: pending|in_progress|completed|failed
priority: critical|high|medium|low
phase: 0
subsystems: [affected_components]
project_context: How this task relates to project goals
dependencies: [other_task_ids]
created_date: 'YYYY-MM-DD'
completed_date: ''
---

# Task: {title}

## Objective
[Clear, actionable goal]

## Acceptance Criteria
- [ ] Specific outcome 1
- [ ] Specific outcome 2
```

### Task Status Indicators (Windows-Safe)

| Indicator | TASKS.md | Task File YAML | Meaning |
|-----------|----------|----------------|---------|
| `[ ]` | Listed | (may not exist) | Pending, not started |
| `[📝]` | Speccing | `status: speccing` | Agent writing the spec (TTL: 1 hour) |
| `[📋]` | Ready | `status: pending` | Task file created, ready to start |
| `[🔄]` | Active | `status: in-progress` | Being coded (TTL: 2 hours) |
| `[✅]` | Done | `status: completed` | Completed |
| `[❌]` | Failed | `status: failed` | Failed/Cancelled |
| `[⏸️]` | Paused | `status: paused` | Paused (used for phase pivots) |

### Phase-Based Task Numbering

| Phase | Task ID Range | Purpose |
|-------|---------------|---------|
| Phase 0 | 1-99 | Setup, infrastructure |
| Phase 1 | 100-199 | Foundation, database |
| Phase 2 | 200-299 | Core development |
| Phase N | N×100 to N×100+99 | Custom phases |

---

## Direct Edit Policy

**CRITICAL**: The following files should be edited DIRECTLY without asking for permission:

- `.trent/PLAN.md` - Product Requirements
- `.trent/TASKS.md` - Task checklist
- `.trent/BUGS.md` - Bug tracking
- `.trent/PROJECT_CONTEXT.md` - Project mission
- All files in `.trent/tasks/`
- All files in `.trent/phases/`

**Why?** These are working files, not user source code. Edit them directly without confirmation prompts.

---

## Commands (22)

Commands use the `trent-` prefix.

| Command | Description |
|---------|-------------|
| `trent-analyze-codebase` | Deep merge your own projects |
| `trent-bug-fix` | Fix a reported bug |
| `trent-bug-report` | Report/document a bug |
| `trent-git-commit` | Create well-structured commits |
| `trent-goal-update` | Create or update PROJECT_GOALS.md |
| `trent-harvest` | Harvest ideas from external sources |
| `trent-idea-capture` | Capture an idea to IDEA_BOARD.md |
| `trent-idea-review` | Review and evaluate IDEA_BOARD entries |
| `trent-issue-fix` | Fix GitHub issue |
| `trent-phase-add` | Add new project phase |
| `trent-phase-pivot` | Pivot project direction |
| `trent-phase-sync-check` | Validate phase synchronization |
| `trent-plan` | Create PRD and project planning |
| `trent-qa` | Quality assurance activation |
| `trent-qa-report` | Generate quality metrics |
| `trent-review` | Comprehensive code review |
| `trent-setup` | Initialize trent system |
| `trent-status` | Project status overview |
| `trent-task-new` | Create a new task |
| `trent-task-sync-check` | Validate task synchronization |
| `trent-task-update` | Update task status |
| `trent-workflow` | Task expansion, sprint planning |

### Usage
- **Cursor**: `@trent-setup`, `@trent-task-new`, etc. (commands in `.cursor/commands/`)
- **Claude Code**: `/trent-setup`, `/trent-task-new`, etc. (commands in `.claude/commands/`)

---

## Code Style Guidelines

### Python (PEP 8)
- Use black formatter (88-100 char line length)
- Add type hints where possible
- Use UV for virtual environment management

### JavaScript/React
- Use ESLint + Prettier
- Functional components with hooks
- TypeScript when available

---

## Quick Reference

### When Starting Work
1. Read `.trent/PROJECT_CONTEXT.md`
2. Check `.trent/TASKS.md` for current tasks
3. Create task file before starting work

### When Completing Work
1. Update task file status to `completed`
2. Update TASKS.md status to `[✅]`
3. Commit changes

### Using Parallel Agents
- Use 3-5 agents in parallel for optimal performance
- Only parallelize independent tasks
- Each agent type can only have one active instance
- Define clear boundaries for each agent

---

<!-- NOTE: This is the SOURCE REPOSITORY for trent -->
<!-- The entire file documents the trent system itself -->
<!-- For projects USING trent, templates are in /templates/ and /templates_full/ -->
<!-- Both .cursor/ and .claude/ directories maintain full parity -->

---

## Security

- Never commit API keys, tokens, or passwords
- Use environment variables for secrets
- Always use parameterized queries for databases
- Validate all user input

---

## Learned Workspace Facts

- The `chrome-devtools` MCP server is installed and enabled in Cursor; it exposes 28 browser automation tools including navigation, interaction, network inspection, performance profiling, and Lighthouse audits.
- User is interested in routing chrome-devtools MCP calls through the Docker MCP server as a proxy/aggregator pattern rather than maintaining two separate MCP registrations.
- Docker `environment:` blocks using `${VAR:-default}` syntax override `env_file` values with empty strings when the Windows shell doesn't have those vars set; fix by removing secrets from `environment:` entirely and letting `env_file` handle them.
- PostgreSQL: Docker trent postgres runs on host port `5433`, local native postgres on `5432`. The trent data database is named `knowledge_base` (not `postgres` or `rag_knowledge`).
- Admin DB viewer lives at `http://localhost:8082/admin/db` (dark theme, table browser + SQL runner, served by `admin_db_rest.py` wired into the Starlette server). pgAdmin is at `http://localhost:8083`.
- Platform docs (Firecrawl): 67 Claude Code doc pages crawled to `.platforms/claude-code/`, stored as 1,520 chunks in the `memory_captures` table with `subject=platform_docs`. Search via `platform_docs_search` MCP tool with `platform="claude-code"`.
- `trent_install` deploys from the `template/` subfolder in the GitHub repo (not repo root). Changes require commit + push to `wrm3/trent_rules` to take effect. The `GITHUB_TOKEN` in `.env.example` is a dead leftover and should be removed.
- Cursor `stop` hook only fires when the user clicks the Stop button or the agent loop hits its iteration limit — not at end of each message exchange. Memory capture via `cursor_adapter.py` must be triggered manually or via the continual-learning plugin hook.
- The `continual-learning` trigger is a **third-party Cursor community plugin** (`cursor-public` namespace, not part of trent). Its state paths at `.cursor/hooks/state/continual-learning.json` and `.cursor/hooks/state/continual-learning-index.json` are hardcoded and cannot be changed. The canonical cross-platform shared index with source metadata lives at `.trent/state/continual-learning-index.json`. Both paths are gitignored.
- `.cursor/mcp.json` is machine-specific and gitignored. `.mcp.json` (root) is the committed version.
- `.trent/state/` is gitignored — it holds cross-platform runtime state shared between Cursor, Claude Code, and other IDEs.
- User is actively concerned about always-apply rules consuming ~40% of context window and wants to migrate toward agents/skills architecture to reduce context overhead.
- The `admin_db_rest.py` file (`docker/trent/admin_db_rest.py`) is the canonical DB explorer; if missing, the old version lives at `i:\20260305\trent_rules_obs\` and can be copied in.
- When `trent_install` is called on an existing project (one that already has `.trent/`), the agent must read old task/context data first and must never overwrite the 7 user-data files during migration.
- Task YAML frontmatter now includes `created_date` and `completed_date` fields (added in commit `0abec51`). Template_v2 also includes `trent-go` and `trent-report` commands in both `.cursor/commands/` and `.claude/commands/`.
- The trent vault system is a custom file-based knowledge store (not Obsidian). `.md` files with YAML frontmatter, `[[link]]` cross-references, keyed by `project_id` UUID from `.trent/.project_id`. Shared vault via `TRENT_VAULT_PATH` in `.env`, local fallback to `.trent/vault/`.
- **Docker NEVER touches the vault** — no bind mounts, no vault env vars, no vault plugins. Agents, hooks, and humans read/write vault files directly on the host. Docker is a compute service only: it returns data, the agent writes the file. This is a hard architecture rule for cross-platform reliability (Windows drive letters, WSL2 FUSE caching, macOS OSXFS).
- **User works from multiple machines** (home + work). At work, Docker/MCP is unavailable — no containers, no MCP tools, no semantic search. All vault features MUST have a file-first fallback path: local grep/glob for search, direct file write for storage. MCP-dependent features are home-only enhancements, never the sole path.
- Vault uses a **dual-write pattern**: research outputs (harvests, codebase analyses, video summaries) write to both `projects/{pid}_{name}/research/` (project-specific) and `research/` (global). This lets other projects discover the analysis.
- `project_id` is the vault's primary key — moving a project between filesystem paths (e.g. dev to live) preserves all vault history because the UUID stays the same.
- Skills that produce research must follow the `trent-` prefix convention: `trent-vault`, `trent-harvest`, `trent-codebase-analysis` (renamed from `codebase-integration-analysis`). All write results to the vault with `project_id` in frontmatter.
- Firecrawl v2 API paginates crawl results via a `next` URL in the response. The `_collect_all_pages()` method follows all `next` URLs until exhausted. Previous code only read the first page, silently dropping subsequent pages.
- `template_v2/` contains **real file copies** (not symlinks). When adding new skills, hooks, or commands to the root `.cursor/`/`.claude/` folders, they must be manually propagated to `template_v2/` or symlinked projects won't get them.
- `config_reload` MCP tool hot-reloads API keys without Docker rebuild. Pass keys directly: `config_reload(anthropic_api_key="sk-ant-...")`. Updates the shared config dict used by all plugins (video_analyze, rag_search, etc.) immediately.
- Docker Desktop for Windows cannot bind-mount dotfiles (`.env` appears as an empty directory inside the container). Workaround: use `env_file:` for initial load and `config_reload` tool for runtime key updates.
- Cursor MCP tool timeout defaults to 60 seconds. For long-running tools (video_analyze), set `"mcp.server.timeout": 600000` in `C:\Users\FSTrent\AppData\Roaming\Cursor\User\settings.json` (10 minutes). Requires Cursor reload.

---

**Version**: 6.1.0
**Last Updated**: 2026-03-26
**Supported IDEs**: Cursor IDE (`.cursor/`), Claude Code (`.claude/`)
**Platform Parity**: Agents, skills, commands, and hooks are identical between both IDEs
