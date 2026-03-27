---
name: claude-cli
description: Comprehensive Claude Code CLI reference including all flags, headless mode, Agent SDK (Python + TypeScript), multi-agent patterns, permission bypass, session management, MCP configuration, and cross-invocation with Cursor CLI. Use when working with Claude Code from the terminal, building agents with the Agent SDK, configuring headless/CI pipelines, or orchestrating multi-agent workflows.
---

# Claude Code CLI

Complete reference for the `claude` command-line interface. Self-updating -- check official docs before making structural changes.

## Self-Update Protocol

Before making changes to CLI-related configurations, fetch latest docs:
1. https://docs.anthropic.com/en/docs/claude-code/cli-reference
2. https://docs.anthropic.com/en/docs/claude-code/headless
3. https://docs.anthropic.com/en/docs/claude-code/sub-agents
4. https://docs.anthropic.com/en/docs/claude-code/permissions
5. https://docs.anthropic.com/en/docs/claude-code/mcp
6. https://docs.claude.com/en/api/agent-sdk/overview

---

## Installation

```bash
npm install -g @anthropic-ai/claude-code
```

---

## Core Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive REPL |
| `claude "query"` | Interactive with initial prompt |
| `claude -p "query"` | Non-interactive (print mode) |
| `claude -c` / `--continue` | Resume most recent conversation |
| `claude -r ID` / `--resume ID` | Resume specific session |
| `claude update` | Update to latest version |
| `claude auth login` | Authenticate |
| `claude auth status` | Check auth state |
| `claude mcp add NAME` | Add MCP server |
| `claude mcp list` | List MCP servers |
| `claude mcp remove NAME` | Remove MCP server |
| `claude agents` | List configured subagents |

---

## CLI Flags Reference

### Session Flags
| Flag | Description |
|------|-------------|
| `-c, --continue` | Resume last conversation |
| `-r, --resume ID` | Resume specific session by ID or name |
| `--fork-session` | Branch from existing session (keeps history, new thread) |
| `--session-id UUID` | Use specific session UUID |
| `--from-pr NUMBER` | Resume session linked to a PR |
| `--no-session-persistence` | Don't save session (ephemeral) |

### Permission Flags
| Flag | Description |
|------|-------------|
| `--dangerously-skip-permissions` | Auto-approve ALL tools (no prompts) |
| `--permission-mode MODE` | Set permission behavior (see Permission System) |
| `--allowedTools TOOL [TOOL...]` | Pre-authorize specific tools |
| `--disallowedTools TOOL [TOOL...]` | Block specific tools |
| `--tools TOOL [TOOL...]` | Restrict available tool set entirely |

### System Prompt Flags (mutually exclusive groups)
| Flag | Description |
|------|-------------|
| `--system-prompt TEXT` | Replace ALL default instructions |
| `--system-prompt-file PATH` | Replace from file |
| `--append-system-prompt TEXT` | Add to defaults (recommended) |
| `--append-system-prompt-file PATH` | Append from file |

### Output Flags
| Flag | Description |
|------|-------------|
| `--output-format text\|json\|stream-json` | Output format (with `-p`) |
| `--input-format text\|stream-json` | Input format for piping |
| `--json-schema SCHEMA` | Validate output against JSON schema |
| `--verbose` | Enable detailed logging |

### Execution Flags
| Flag | Description |
|------|-------------|
| `--model NAME` | Choose model (opus, sonnet, haiku) |
| `--max-turns N` | Limit agentic turns (with `-p`) |
| `--max-budget-usd N` | Spending cap |
| `--max-input-tokens N` | Input token limit |
| `-w, --worktree NAME` | Start in isolated git worktree |
| `--cwd PATH` | Set working directory |

### Agent Flags
| Flag | Description |
|------|-------------|
| `--agents JSON` | Define subagents via JSON object |
| `--teammate-mode` | Enable agent team coordination |

### MCP Flags
| Flag | Description |
|------|-------------|
| `--mcp-config PATH` | Load MCP config from file |
| `--strict-mcp-config` | Fail if MCP servers can't start |
| `--env KEY=VALUE` | Set env vars for MCP servers |

---

## Permission System

### Permission Modes

| Mode | Behavior |
|------|----------|
| `plan` | Read-only, no edits, no commands |
| `acceptEdits` | Auto-approve file edits, prompt for bash |
| `askEdits` | Prompt for edits and bash |
| `askTools` | Prompt for all tool usage |
| `denyAll` | Deny all tool requests |
| `bypassPermissions` | Auto-approve everything (same as `--dangerously-skip-permissions`) |

### AllowedTools Pattern Syntax

```bash
# Approve specific tool types
--allowedTools "Read" "Edit" "Write"

# Bash with command patterns (glob matching)
--allowedTools "Bash(npm *)"          # npm commands only
--allowedTools "Bash(git *)"          # git commands only
--allowedTools "Bash(python -m *)"    # python module execution

# Deny patterns (prefix with !)
--allowedTools "Bash(!rm *)"          # block rm
--allowedTools "Bash(!sudo *)"        # block sudo
--allowedTools "Bash(!curl *)"        # block curl

# Combine multiple
--allowedTools "Read" "Edit" "Bash(npm *)" "Bash(git *)" "Bash(!rm *)"
```

### Settings File Configuration

```json
// .claude/settings.json (project, committed)
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(npm test)", "Bash(git *)"],
    "deny": ["Bash(rm *)", "Bash(sudo *)"]
  }
}
```

```json
// .claude/settings.local.json (personal, gitignored)
{
  "permissions": {
    "allow": ["Bash(docker *)"]
  }
}
```

### Unattended Agent Execution

For agents that must run without permission prompts:

```bash
# Full bypass (use in isolated environments only)
claude -p "implement feature X" \
  --dangerously-skip-permissions \
  --allowedTools "Read" "Edit" "Write" "Bash(npm *)" "Bash(git *)" \
  --disallowedTools "Bash(rm -rf *)" "Bash(sudo *)" \
  --max-turns 50 \
  --max-budget-usd 5
```

Best practice: always pair `--dangerously-skip-permissions` with `--allowedTools` whitelist and `--disallowedTools` blacklist. Never use bypass without restrictions outside a sandbox.

---

## Headless / Non-Interactive Mode

### Basic Usage

```bash
# Simple query
claude -p "Find all TODO comments"

# Pipe input
cat src/app.ts | claude -p "Review for security issues"

# JSON output for parsing
claude -p "List all API endpoints" --output-format json

# With tool restrictions
claude -p "Run tests and fix failures" \
  --allowedTools "Read" "Edit" "Bash(npm test)" \
  --output-format json
```

### Multi-Turn Headless

```bash
# First turn
claude -p "Create a user model" --output-format json > turn1.json

# Continue same session
claude -p "Add validation to the model" --continue --output-format json

# Resume specific session
claude -p "Add tests" --resume "session-abc123"
```

### CI/CD Pipeline Pattern

```bash
# GitHub Actions example
claude -p "Fix all ESLint errors in src/" \
  --dangerously-skip-permissions \
  --allowedTools "Read" "Edit" "Bash(npx eslint *)" \
  --max-turns 20 \
  --output-format json
```

---

## Multi-Agent Patterns

### 1. Dynamic Subagents (`--agents` flag)

```bash
claude --agents '{
  "agents": [
    {
      "name": "security-reviewer",
      "description": "Reviews code for security vulnerabilities",
      "instructions": "Focus on OWASP Top 10, injection, XSS, auth issues",
      "tools": ["Read", "Grep", "Glob"],
      "model": "sonnet"
    },
    {
      "name": "test-writer",
      "description": "Writes unit tests for changed files",
      "tools": ["Read", "Write", "Bash(npm test)"],
      "model": "sonnet"
    }
  ]
}'
```

Subagent JSON fields:
- `name` (required): kebab-case identifier
- `description` (required): when to use this agent
- `instructions`: system prompt addition
- `tools`: allowed tools list
- `disallowedTools`: blocked tools
- `model`: model override
- `skills`: skills to load
- `mcpServers`: MCP servers available
- `maxTurns`: turn limit

### 2. File-Based Agents (`.claude/agents/*.md`)

```markdown
---
name: backend-developer
description: Backend APIs, business logic, database work
tools: ["Read", "Edit", "Write", "Bash", "Grep", "Glob"]
model: sonnet
---

# Backend Developer

You are a backend specialist. Focus on API design, database queries,
and server-side logic. Follow project conventions in CLAUDE.md.
```

### 3. Parallel Execution via Worktrees

```bash
# Launch parallel agents in isolated worktrees
claude -w backend-work -p "Implement user API endpoints" \
  --dangerously-skip-permissions --allowedTools "Read" "Edit" "Write" "Bash(npm *)" &

claude -w frontend-work -p "Build user profile component" \
  --dangerously-skip-permissions --allowedTools "Read" "Edit" "Write" "Bash(npm *)" &

# Wait for both
wait

# Merge results
git merge backend-work --no-edit
git merge frontend-work --no-edit
git worktree remove .claude/worktrees/backend-work
git worktree remove .claude/worktrees/frontend-work
```

### 4. Agent Teams (`--teammate-mode`)

Enables coordination between agents via shared task state:

```bash
claude --teammate-mode -p "Coordinate implementation of auth feature" \
  --agents '{"agents": [
    {"name": "api-dev", "description": "Backend API", "tools": ["Read","Edit","Bash(npm *)"]},
    {"name": "ui-dev", "description": "Frontend UI", "tools": ["Read","Edit","Bash(npm *)"]}
  ]}'
```

---

## Agent SDK

### Python SDK

```bash
pip install claude-agent-sdk
# or: uv add claude-agent-sdk
```

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        allowed_tools=["Read", "Edit", "Bash(npm test)"],
        model="sonnet",
        cwd="/path/to/project",
        max_turns=30,
    )

    async for message in query(
        prompt="Implement sorting algorithm with tests",
        options=options,
    ):
        if message.type == "assistant":
            print(message.content)
        elif message.type == "result":
            print(f"Done. Cost: ${message.cost_usd:.4f}")

anyio.run(main)
```

### TypeScript SDK

```bash
npm install @anthropic-ai/claude-agent-sdk
```

```typescript
import { query, ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

const options: ClaudeAgentOptions = {
  permissionMode: "bypassPermissions",
  allowedTools: ["Read", "Edit", "Bash(npm test)"],
  model: "sonnet",
  cwd: "/path/to/project",
};

for await (const message of query("Implement auth module", options)) {
  if (message.type === "assistant") {
    console.log(message.content);
  }
}
```

### SDK Permission Modes

| Mode | Python | TypeScript | Behavior |
|------|--------|------------|----------|
| Default | `"default"` | `"default"` | Prompt user (interactive) |
| Accept edits | `"acceptEdits"` | `"acceptEdits"` | Auto-approve edits, prompt bash |
| Bypass | `"bypassPermissions"` | `"bypassPermissions"` | Auto-approve all |
| Don't ask | N/A | `"dontAsk"` | TS-only: deny instead of prompt |

---

## Session Management

| Action | Command |
|--------|---------|
| Continue last | `claude -c` or `claude --continue` |
| Resume by ID | `claude -r "session-id"` |
| Resume interactively | `claude --resume` (shows picker) |
| Fork session | `claude --fork-session` |
| Resume from PR | `claude --from-pr 123` |
| Named session | `claude --session-id "my-uuid"` |
| Ephemeral (no save) | `claude -p "query" --no-session-persistence` |

---

## MCP Configuration

### CLI Management

```bash
claude mcp add my-server --command "python" --args "server.py"
claude mcp add my-server --url "http://localhost:8080/mcp"
claude mcp list
claude mcp remove my-server
```

### Config Files (priority order)

1. `.mcp.json` (project root, highest priority)
2. `.claude/settings.local.json` under `mcpServers` key
3. `~/.claude.json` (user-global, lowest priority)

### Runtime Flags

```bash
claude --mcp-config ./custom-mcp.json        # Load specific config
claude --strict-mcp-config                     # Fail if servers can't start
claude --env DB_URL=postgres://localhost/mydb   # Env vars for MCP servers
```

---

## Cross-Invocation: Calling Cursor from Claude Code

### Via Bash Tool

```bash
# Launch Cursor agent on a task
agent -p "implement database migration" --output-format json

# Cloud Agent handoff (if Cursor CLI available)
agent -c "long-running refactor task"
```

### Via Cursor Cloud Agents API

```bash
# From Claude Code, use Bash to call Cursor's API
CURSOR_AUTH=$(echo -n "$CURSOR_API_KEY:" | base64)

curl -s -X POST "https://api.cursor.com/v0/agents" \
  -H "Authorization: Basic $CURSOR_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Implement user authentication",
    "repository": "github.com/org/repo",
    "branch": "feature/auth"
  }'
```

### Coordination via trent

Both CLIs can read/write `.trent/TASKS.md`. Use it as shared task state:
1. Claude Code marks task `[🔄]` in TASKS.md
2. Cursor agent reads TASKS.md, picks up `[📋]` tasks
3. Both update atomically when done

---

## Slash Commands (Interactive Mode)

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/compact` | Summarize conversation to save context |
| `/init` | Create starter CLAUDE.md |
| `/allowed-tools` | Manage allowed tools |
| `/resume` | Pick session to continue |
| `/rename` | Rename current session |

---

## Troubleshooting

- **Windows**: Use `;` not `&&` for command chaining. Set UTF-8: `$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8`
- **Permission denied**: Use `--allowedTools` to pre-authorize, or `--dangerously-skip-permissions` in sandboxed environments
- **MCP timeout**: Set `MCP_TIMEOUT=60000` env var for slow-starting servers
- **Context overflow**: Use `/compact` to summarize and free context space
