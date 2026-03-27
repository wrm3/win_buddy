---
name: trent-vault
description: Write and read notes in the trent vault — a file-based knowledge store shared across projects. Use when writing session summaries, research notes, decisions, corrections, harvest results, codebase analyses, or any persistent knowledge. Triggers on requests mentioning vault, knowledge base notes, session summary, research notes, or cross-project knowledge.
---

# trent-vault

The trent vault is a plain folder of `.md` files that serves as persistent memory across sessions and projects.

## Architecture Rule: Docker NEVER Touches the Vault

The vault is **local files only**. AI agents, hooks, and humans read and write vault files directly using native file operations on the host machine. The Docker MCP server has **zero vault access** — no bind mounts, no vault environment variables, no vault plugins.

Why: Docker bind mounts are unreliable across platforms (Windows drive letters, WSL2 FUSE caching, macOS OSXFS performance, Linux permissions). The vault must work identically on every OS, at home, at work, on any machine.

| Component | Vault Access | How |
|-----------|-------------|-----|
| AI agents (Cursor, Claude, Gemini) | **YES** | Native file read/write |
| PowerShell hooks | **YES** | Native file read/write |
| Humans | **YES** | Any text editor, file explorer |
| Docker MCP server | **NO** | Returns data; agent writes to vault |
| Firecrawl (Docker) | **NO** | Writes to DB; agent copies to vault |
| Video analyzer (Docker) | **NO** | Returns summary; agent writes to vault |

### Data Flow for Docker-Based Tools

```
1. Agent calls MCP tool (video_analyze, research_deep, etc.)
2. Docker processes the request, returns data to agent
3. Agent writes the result to the vault as a .md file
4. (Optional) Agent also ingests to DB for semantic search backup
```

The agent is always the one holding the pen. Docker is a compute service, not a filesystem.

## Project Identity

Every trent project has a UUID in `.trent/.project_id`. This ID is the **primary key** that ties a project to its vault namespace. All project-specific vault data lives under `projects/{project_id}_{project_name}/`.

### Reading the Project ID

```powershell
$ProjectId = (Get-Content ".trent/.project_id" -Raw).Trim()
```

```python
project_id = Path(".trent/.project_id").read_text().strip()
```

The project ID ensures that even if two projects share the same folder name, their vault data never collides. Moving a project between paths preserves all vault history because the UUID stays the same.

## Vault Path Resolution

1. Check `.env` in the project root for `TRENT_VAULT_PATH=<path>`
2. If set, use that path (shared vault accessible by all projects)
3. If not set, use `.trent/vault/` inside the current project (local mode)

```
# Shared mode (.env has TRENT_VAULT_PATH=G:\trent_vault)
G:\trent_vault\projects\44a32e82_trent_rules\sessions\2026-03-20_153000_abc12345.md

# Local mode (no .env entry)
{project}\.trent\vault\projects\{project_id}_{project_name}\sessions\...
```

## Folder Structure

```
{vault}/
├── projects/               # Per-project context (keyed by project_id)
│   └── {project_id}_{project_name}/
│       ├── _context.md     # Project overview, goals, stack (MOC for this project)
│       ├── sessions/       # Project-specific session history
│       ├── decisions/      # Architectural choices with rationale
│       ├── research/       # Project-specific research & analysis
│       │   ├── harvests/   # @trent-harvest results for this project
│       │   └── analyses/   # Codebase integration analyses
│       └── videos/         # Project-specific video summaries
├── research/               # GLOBAL research (cross-project)
│   ├── platforms/          # Crawled platform docs (agent copies from Firecrawl DB)
│   │   ├── claude-code/
│   │   └── cursor/
│   ├── topics/             # Research notes by topic
│   ├── harvests/           # Harvest results from external sources (global)
│   ├── analyses/           # Codebase analyses of external repos (global)
│   ├── papers/             # Paper summaries
│   └── sources/            # Raw source material
├── videos/
│   ├── summaries/          # Video analysis summaries
│   └── playlists/          # Playlist tracking
├── knowledge/
│   ├── corrections/        # Cross-project AI corrections
│   ├── preferences/        # User preferences and conventions
│   └── tech-stack/         # Patterns, gotchas, recipes
├── templates/              # Note templates for each type
│   ├── session.md
│   ├── decision.md
│   ├── harvest.md
│   ├── video.md
│   └── daily.md
└── daily/                  # Optional daily scratch notes
```

### Dual-Write Pattern (Project + Global)

When analyzing external sources (harvests, codebase analyses, GitHub repos), write to **two locations**:

1. **Project-specific**: `projects/{pid}_{name}/research/harvests/` or `analyses/`
2. **Global**: `research/harvests/` or `research/analyses/`

The global copy uses `[[link]]` cross-references back to the project that initiated it.

## Note Format

Every vault note MUST have YAML frontmatter:

```yaml
---
date: 2026-03-20
project: trent_rules
project_id: 44a32e82-4208-4b16-8341-e939782a9d0d
source: cursor/agent
tags: [session, docker, firecrawl]
aliases: [docker session, firecrawl fix]
type: session
---
```

### Required Fields

| Field | Values | Description |
|-------|--------|-------------|
| `date` | `YYYY-MM-DD` | Date the note was created |
| `project_id` | UUID from `.trent/.project_id` | Unique project identifier |
| `source` | `cursor/agent`, `claude/agent`, `cursor/hook`, `claude/hook`, `human` | Who created the note |
| `type` | `session`, `decision`, `correction`, `research`, `video`, `preference`, `context`, `daily`, `harvest`, `codebase-analysis` | Note category |

### Optional Fields

| Field | Description |
|-------|-------------|
| `project` | Human-readable project name (for display) |
| `tags` | Array of topic tags for filtering |
| `aliases` | Alternative names for this note (for linking) |
| `conversation_id` | Session/conversation ID |
| `turns` | Number of turns in the session |
| `platform` | `cursor` or `claude` |
| `url` | Source URL for research/video/harvest notes |
| `source_repo` | GitHub repo URL for harvest/codebase-analysis |
| `source_type` | `github`, `article`, `video`, `paper`, `repo-local` |

## Cross-References and Backlinks

Use `[[note-name]]` syntax to link between notes:

```markdown
This decision was informed by [[docker-env-override-bug]] and
the research in [[mcp-protocol-overview]].
```

Link targets are matched by filename (without `.md` extension) OR by `aliases` in frontmatter, across the entire vault.

**Backlinks**: When reading a note, also search for other notes that link TO it. This reveals connections the note author may not have been aware of.

## Writing Guidelines

### Session Summaries
Write to `projects/{pid}_{name}/sessions/{date}_{time}_{id_short}.md`:
- Always include `project_id` in frontmatter
- 3-5 bullet summary of what was accomplished
- Key decisions made (link to `decisions/` notes if significant)
- Unresolved issues or next steps
- Do NOT include full code — summarize what changed and why

### Decisions
Write to `projects/{pid}_{name}/decisions/{date}_{topic}.md`:
- What was decided and why
- Alternatives considered
- Trade-offs accepted
- Link to the session where it was discussed

### Harvest Results (@trent-harvest)
After presenting the harvest menu and user approves/reviews, write to **both**:

**Project copy**: `projects/{pid}_{name}/research/harvests/{date}_{source-name}.md`
**Global copy**: `research/harvests/{date}_{source-name}.md`

### Codebase Integration Analysis
After completing the 5-phase analysis, write to **both**:

**Project copy**: `projects/{pid}_{name}/research/analyses/{date}_{target-project}.md`
**Global copy**: `research/analyses/{date}_{target-project}.md`

### Video Summaries (Post-MCP-Tool Pattern)
1. Call `video_analyze` MCP tool — Docker processes, returns data
2. Agent formats the result as a vault note
3. Agent writes to `videos/summaries/{date}_{slug}_{video_id}.md`
4. Agent writes project copy to `projects/{pid}_{name}/videos/{date}_{slug}_{video_id}.md`

### Corrections
Write to `knowledge/corrections/{topic}.md`

### Research
Write to `research/topics/{topic}.md`

## File Naming

- Use lowercase with hyphens: `docker-env-override-bug.md`
- Prefix with date for chronological notes: `2026-03-20_session-summary.md`
- Keep names short but descriptive

## When to Write to the Vault

| Trigger | What to write | Project location | Global location |
|---------|---------------|------------------|-----------------|
| Session ends (hook) | Session summary | `projects/{pid}_{name}/sessions/` | — |
| Significant decision | Decision note | `projects/{pid}_{name}/decisions/` | — |
| @trent-harvest completes | Harvest results | `projects/{pid}_{name}/research/harvests/` | `research/harvests/` |
| Codebase analysis completes | Analysis summary | `projects/{pid}_{name}/research/analyses/` | `research/analyses/` |
| Video analyzed (MCP returns data) | Video summary | `projects/{pid}_{name}/videos/` | `videos/summaries/` |
| AI makes a mistake | Correction note | — | `knowledge/corrections/` |
| User states a preference | Preference note | — | `knowledge/preferences/` |
| Research completed | Research summary | — | `research/topics/` |

## Reading from the Vault

At session start or when context is needed, read relevant vault notes directly using native file operations.

```powershell
$pid = (Get-Content ".trent/.project_id" -Raw).Trim()
$vaultPath = $env:TRENT_VAULT_PATH
$projectFolder = Get-ChildItem "$vaultPath/projects/" -Directory | Where-Object { $_.Name -like "${pid}_*" }
```

- Check `projects/{pid}_{name}/_context.md` for project overview (MOC)
- Check `projects/{pid}_{name}/decisions/` for recent decisions
- Check `projects/{pid}_{name}/sessions/` for chat history
- Check `research/harvests/` for harvests from ALL projects
- Check `knowledge/corrections/` for known pitfalls
- Check `knowledge/preferences/` for user conventions

### Searching the Vault (Dual Path)

Agents have **two** search paths:

#### 1. Local File Search (native tools — always available)
- **Grep/ripgrep** for keyword search across all `.md` files
- **Glob** for finding notes by path pattern
- **Read** frontmatter to filter by type, tags, project_id, date

#### 2. Database Semantic Search (MCP tools — requires vault_sync)
- **vault_search** — Semantic (vector) or keyword search against the `vault_notes` DB table. Best for "find notes about X" queries.
- **vault_list** — Browse notes by type, project, tags, or path prefix. Best for "show me all video summaries" queries.
- **vault_read** — Read full note content from DB by path. Useful when you have a path from search results.

The database is a **searchable backup** of the vault. Local files are always the source of truth.

### Storing to the Vault (Write + Sync Pattern)

When creating a new vault note:

1. **Write the `.md` file** to the vault using native file operations
2. **Call `vault_sync`** MCP tool to index it in the database with embeddings

```
# Step 1: Agent writes the file to the vault
Write file → G:\trent_vault\videos\summaries\2026-03-12_my-video.md

# Step 2: Agent reads the file content
content = Read("G:\trent_vault\videos\summaries\2026-03-12_my-video.md")

# Step 3: Agent passes content to vault_sync MCP tool (Docker indexes it with embeddings)
vault_sync(path="videos/summaries/2026-03-12_my-video.md", content=<file content>, mode="ingest")
```

To delete a note from the DB:
```
vault_sync(path="videos/summaries/old-note.md", mode="delete")
```

Docker never reads the vault filesystem. The agent is always the bridge — it reads the local file and passes the content to the MCP tool for indexing.

### Vault Web UI

Browse the vault visually at `http://localhost:8082/vault` (when Docker MCP server is running).

The web UI operates on the **database** — it reads from `vault_notes`, not from local files. Run `vault_sync` to ensure the UI reflects the latest local file changes.

Features:
- **Browse** — Folder tree navigation
- **Search** — Keyword and semantic search
- **Graph** — Knowledge graph visualization (nodes = notes, edges = [[wikilinks]])
- **Stats** — Note counts by type, embedding coverage, link density

### Unified Search (vault_search_all)

The `vault_search_all` MCP tool searches **all** knowledge stores in one call:
- `vault_notes` — vault .md files indexed via vault_sync
- `memory_captures` where subject='platform_docs' — Firecrawl crawl output
- `agent_memory_captures` — session summaries and insights
- `agent_turns` — raw chat history

```
vault_search_all(query="docker bind mount issues", sources="all", limit=10)
```

Filter by source: `sources="vault,platform_docs"` or `sources="memory,sessions"`.

When MCP is unavailable (no Docker, at work), fall back to local file search:
```
Grep for keywords across vault .md files
Glob for path patterns
Read frontmatter for type/tag filtering
```

### Session Export (vault_export_sessions)

The `vault_export_sessions` MCP tool reads recent session summaries from the memory DB and returns them as vault-ready `.md` content. The agent then writes them to the vault.

```
vault_export_sessions(project_id="44a32e82-...", since_hours=24)
# Returns: [{filename, rel_path, content}, ...]
# Agent writes each to vault, then calls vault_sync
```

### Platform Docs Bridge

After a Firecrawl crawl, run the platform bridge hook to copy `.platforms/` snapshots into the vault:

```powershell
powershell -ExecutionPolicy Bypass -File .cursor/hooks/vault-bridge-platforms.ps1
```

This copies `.platforms/{platform}/*.md` → `{vault}/research/platforms/{platform}/`.

### Vault Path Auto-Migration

When `TRENT_VAULT_PATH` is not set in `.env`, all vault writes go to `.trent/vault/` (local mode). When the env var is later added, the `session-start.ps1` hook **automatically migrates** all local vault content to the shared location and cleans up `.trent/vault/`. No manual intervention needed.

### User Commands

| Command | Description |
|---------|-------------|
| `@trent-vault-search` | Search vault (semantic via DB, fallback to local grep) |
| `@trent-vault-store` | Write a note to vault and sync to DB |
| `@trent-vault-sync` | Bulk sync local vault files to DB |
| `@trent-vault-research` | Research a topic, write results to vault, sync to DB |
