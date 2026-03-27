# agents.md - trent

> **AI Development System for Cursor IDE**  
> This file follows the agents.md format for AI agent instructions.

---

## 📋 Project Overview

**trent** - A comprehensive AI-powered development system

**Purpose**: Provide a unified development environment for Cursor IDE with extensive agent capabilities, skills, and task management.

**Core Features**:
- **Task Management**: Create, track, and complete tasks with status tracking
- **Project Planning**: PRD creation, feature specifications, scope management
- **Quality Assurance**: Bug tracking, severity classification, resolution tracking
- **Specialized Agents**: 18+ agents for different development roles
- **Development Skills**: 25+ skills covering databases, DevOps, research, and more

---

## 📁 Project Structure

```
.trent/              # Core task management (READ THIS FIRST)
├── PLAN.md                    # Product Requirements Document
├── TASKS.md                   # Master task checklist with status
├── BUGS.md                    # Bug tracking
├── PROJECT_CONTEXT.md         # Project mission and goals
├── SUBSYSTEMS.md              # Component registry
├── tasks/                     # Individual task files (task{id}_name.md)
└── templates/                 # Task/plan templates

.cursor/                       # Cursor IDE configuration
├── skills/                    # 25+ AI Skills
├── agents/                    # 18+ Specialized agents
│   └── sdk/                   # Agent SDK & primitives
├── rules/                     # .mdc format rules
└── commands/                  # Cursor commands

docs/                          # Project documentation
```

---

## 🤖 Available Agents

### Core Development Agents

| Agent | Description | Best For |
|-------|-------------|----------|
| `backend-developer` | API design, server logic, database integration | Backend APIs, business logic |
| `frontend-developer` | React, TypeScript, UI components | User interfaces, responsive design |
| `full-stack-developer` | End-to-end implementation | Complete features |
| `database-expert` | Schema design, query optimization | Database work |
| `api-designer` | REST/GraphQL API design | API contracts |

### DevOps & Infrastructure

| Agent | Description | Best For |
|-------|-------------|----------|
| `devops-engineer` | CI/CD, infrastructure as code | Deployment automation |
| `docker-specialist` | Containerization, Docker Compose | Container optimization |
| `kubernetes-specialist` | K8s cluster management, Helm | Kubernetes operations |
| `portainer-specialist` | Container management UI | Portainer management |
| `cicd-specialist` | Pipeline automation | CI/CD pipelines |
| `solution-architect` | System architecture, tech selection | Architectural decisions |
| `security-auditor` | Vulnerability assessment, compliance | Security reviews |

### Quality & Testing

| Agent | Description | Best For |
|-------|-------------|----------|
| `test-runner` | Automated testing, fix failures | Running and fixing tests |
| `qa-engineer` | Test planning, quality metrics | Quality assurance |
| `code-reviewer` | Code quality, best practices | Code reviews |
| `debugger` | Error diagnosis, root cause analysis | Debugging issues |

### Specialized Agents

| Agent | Description | Best For |
|-------|-------------|----------|
| `technical-writer` | Documentation, API docs | Technical documentation |
| `orchestrator` | Multi-agent coordination | Complex multi-agent tasks |
| `trent-task-expander` | Task breakdown, complexity assessment | Task decomposition |

---

## 🛠️ Available Skills

### Core Task Management
- `trent-task-management` - Task lifecycle and status management
- `trent-planning` - PRD creation, phase management, and project planning
- `trent-qa` - Bug tracking and quality assurance
- `trent-code-reviewer` - Comprehensive code reviews

### Database Development
- `hanx-database-tools` - MySQL database operations

### Research & Documentation
- `research-methodology` - Systematic research approaches

### Integration & Tools
- `github-integration` - GitHub workflows and automation
- `atlassian-integration` - Jira/Confluence integration
- `web-tools` - Web browsing and search
- `mcp-builder` - MCP server development

### Business & Startup
- `startup-resource-access` - Grants, accelerators, resources
- `startup-vc-fundraising` - Fundraising and pitch decks
- `startup-product-development` - Product development lifecycle
- `patent-filing-ai` - Patent documentation assistance

### Utilities
- `project-setup` - Project initialization
- `skill-creator` - Create new skills
- `template-skill` - Skill creation template
- `internal-comms` - Internal communications

---

## ✅ Task Management

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

- `[ ]` - Pending (not started)
- `[📋]` - Ready (task file created)
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed/Cancelled

### Phase-Based Task Numbering

| Phase | Task ID Range | Purpose |
|-------|---------------|---------|
| Phase 0 | 1-99 | Setup, infrastructure |
| Phase 1 | 100-199 | Foundation, database |
| Phase 2 | 200-299 | Core development |
| Phase N | N×100 to N×100+99 | Custom phases |

---

## 🚨 Direct Edit Policy

**CRITICAL**: The following files should be edited DIRECTLY without asking for permission:

### Files to Edit Freely
- `.trent/PLAN.md` - Product Requirements
- `.trent/TASKS.md` - Task checklist
- `.trent/BUGS.md` - Bug tracking
- `.trent/PROJECT_CONTEXT.md` - Project mission
- All files in `.trent/tasks/`
- All files in `.trent/phases/`

**Why?** These are working files, not user source code. Edit them directly without confirmation prompts.

---

## 🔧 Commands

Commands use the `trent-` prefix.

### All Commands

| Command | Description |
|---------|-------------|
| `trent-bug-report` | Report/document a bug |
| `trent-bug-fix` | Fix a reported bug |
| `trent-git-commit` | Create well-structured commits |
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
| `trent-task-update` | Update task status |
| `trent-task-sync-check` | Validate task synchronization |
| `trent-workflow` | Task expansion, sprint planning |

### Usage
- **Cursor**: `@trent-setup`, `@trent-task-new`, etc.

---

## 📝 Code Style Guidelines

### Python (PEP 8)
- Use black formatter (88-100 char line length)
- Add type hints where possible
- Write comprehensive docstrings

### JavaScript/React
- Use ESLint + Prettier
- Functional components with hooks
- TypeScript when available

---

## 📊 Documentation Standards

### File Naming Convention

**Format**: `YYYYMMDD_HHMMSS_Cursor_TOPIC_NAME.md`

**Example**: `docs/20260126_143000_Cursor_PROJECT_SETUP.md`

### File Location Rules

- **docs/** - All documentation except core planning
- **Project root** - Only README.md, LICENSE, CHANGELOG.md, agents.md
- **.trent/** - Only core planning documents

---

## 🔒 Security

- Never commit API keys, tokens, or passwords
- Use environment variables for secrets
- Always use parameterized queries for databases
- Validate all user input

---

## 📋 Quick Reference

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
<!-- For projects USING trent, see template/agents.md -->

---

**Version**: 3.2.0  
**Last Updated**: 2026-01-31  
**Supported IDEs**: Cursor
