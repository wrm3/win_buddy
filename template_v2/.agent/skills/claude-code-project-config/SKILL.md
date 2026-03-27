---
name: claude-code-project-config
description: Maintain and configure the .claude/ project structure for Claude Code. Covers CLAUDE.md, settings.json, rules/, agents/, skills/, commands/, hooks, permissions, MCP config, and auto-memory. Includes self-updating capability by checking official docs. This skill should be used when creating, editing, or auditing any .claude/ configuration files, setting up a new Claude Code project, or troubleshooting Claude Code settings.
---

# Claude Code Project Configuration

Create, maintain, audit, and update `.claude/` project configurations. Self-updating — checks official docs for latest features before making changes.

## Self-Update Protocol

**Before making any structural changes to .claude/, always check the latest docs:**

1. Fetch https://docs.anthropic.com/en/docs/claude-code/overview — main docs
2. Fetch https://docs.anthropic.com/en/docs/claude-code/settings — settings reference
3. Fetch https://docs.anthropic.com/en/docs/claude-code/hooks — hooks reference
4. Fetch https://docs.anthropic.com/en/docs/claude-code/sub-agents — agents reference
5. Fetch https://docs.anthropic.com/en/docs/claude-code/skills — skills reference
6. Fetch https://docs.anthropic.com/en/docs/claude-code/memory — memory & rules reference
7. Fetch https://docs.anthropic.com/en/docs/claude-code/permissions — permissions reference
8. Fetch https://docs.anthropic.com/en/docs/claude-code/mcp — MCP reference

Compare fetched content against `reference/claude_code_structure.md`. If any new features, files, or settings are found, update the reference file AND this SKILL.md before proceeding.

## Complete .claude/ Structure

```
project-root/
├── CLAUDE.md                      # Project instructions (always loaded)
├── CLAUDE.local.md                # Personal prefs (gitignored)
├── .mcp.json                      # Project-level MCP servers
│
└── .claude/
    ├── CLAUDE.md                  # Alt location for instructions
    ├── settings.json              # Project settings (committed)
    ├── settings.local.json        # Personal overrides (gitignored)
    ├── rules/                     # Modular instruction files
    │   └── *.md                   # Path-filtered or global
    ├── agents/                    # Custom subagent definitions
    │   └── *.md                   # YAML frontmatter + markdown
    ├── skills/                    # Skills (slash commands + resources)
    │   └── */SKILL.md             # With optional scripts/, references/, assets/
    ├── commands/                  # Legacy commands (deprecated, use skills/)
    │   └── *.md
    ├── agent-memory/              # Persistent agent memory
    │   └── {agent}/MEMORY.md
    └── worktrees/                 # Git worktree sessions (auto-generated)
```

## CLAUDE.md Authoring

Located at `./CLAUDE.md` or `./.claude/CLAUDE.md`. Loaded every conversation.

### Template

```markdown
# Project Name

## Overview
[1-2 sentences about what the project does]

## Tech Stack
- **Backend**: [framework + language]
- **Frontend**: [framework + language]
- **Database**: [engine]
- **Package Manager**: [tool]

## Key Directories
[Critical paths the AI needs to know]

## Development Commands
[Build, test, run commands]

## Coding Conventions
[Style, naming, patterns]

## Important Rules
[Things to never do, always do]
```

## settings.json Reference

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run *)", "Read(./src/**)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Bash(rm -rf *)", "Read(./.env)"],
    "defaultMode": "acceptEdits"
  },
  "env": { "NODE_ENV": "development" },
  "hooks": { },
  "sandbox": { "enabled": true },
  "model": "claude-sonnet-4-6",
  "enableAllProjectMcpServers": true
}
```

### Permission Modes
| Mode | Behavior |
|---|---|
| `acceptEdits` | Auto-approve edits, ask for other tools |
| `askEdits` | Ask before editing |
| `askTools` | Ask before ANY tool |
| `denyAll` | Block all tools |
| `bypassPermissions` | Skip all checks |

## Rules — .claude/rules/*.md

Path-specific or global instructions split from CLAUDE.md:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Rules
- Validate all inputs
- Use standard error format
```

If no `paths:` frontmatter, rule applies globally.

## Agents — .claude/agents/*.md

```yaml
---
name: my-agent
description: What this agent does
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
permissionMode: default
memory: user
---

# Agent instructions (markdown)
```

| Field | Required | Values |
|---|---|---|
| `name` | Yes | kebab-case identifier |
| `description` | Yes | One-line purpose |
| `tools` | Yes | Comma-separated tool list |
| `model` | Yes | sonnet, opus, haiku |
| `permissionMode` | No | default, bypassPermissions |
| `memory` | No | user, project, none |

## Skills — .claude/skills/*/SKILL.md

```yaml
---
name: skill-name
description: When and how to use this skill
---

# Skill instructions (markdown)
```

### Skill Directory Structure
```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Executable code (not loaded into context)
├── references/       # Docs loaded on demand
└── assets/           # Used in output, not loaded
```

## Hooks — Configured in settings.json

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "npx prettier --write $FILE" }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "prompt", "prompt": "Is this command safe?" }]
    }]
  }
}
```

### Hook Events
SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, SubagentStart, SubagentStop, Stop, PreCompact, SessionEnd

### Hook Types
- `command` — Shell command
- `prompt` — LLM decision (Haiku)
- `agent` — Spawns subagent

## MCP Configuration

**Project**: `.mcp.json` at project root
**User**: `~/.claude.json`

```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

## Auto-Memory — MEMORY.md

Located at `~/.claude/projects/{hash}/memory/MEMORY.md`. Auto-generated. First 200 lines loaded every session.

## Maintenance Workflows

### Audit Existing Config
1. Read all files in `.claude/`
2. Check settings.json against latest schema
3. Verify all agents have required frontmatter
4. Verify all skills have SKILL.md
5. Check for orphaned commands (should be skills)
6. Report findings

### Add New Agent
1. Create `.claude/agents/{name}.md` with frontmatter
2. Add to CLAUDE.md agent registry if exists
3. Mirror to `.cursor/agents/` if dual-platform

### Add New Skill
1. Create `.claude/skills/{name}/SKILL.md`
2. Add `references/` if needed
3. Mirror to `.cursor/skills/`

### Update Permissions
1. Read current `.claude/settings.json`
2. Modify `permissions.allow/ask/deny` arrays
3. Write back

## Reference Files
- `reference/claude_code_structure.md` — Full structure reference (self-updated from official docs)
