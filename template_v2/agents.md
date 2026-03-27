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

**Version**: 5.0.0
**Last Updated**: 2026-03-03
**Supported IDEs**: Cursor IDE (`.cursor/`), Claude Code (`.claude/`)
**Platform Parity**: Agents, skills, commands, and hooks are identical between both IDEs
