# CLAUDE.md - trent

## Project Overview
trent is an AI-powered task management and development system for Cursor IDE and Claude Code. It provides structured task tracking, project planning, quality assurance, and workflow management through a file-based system with enforced synchronization.

## This Repository's Purpose
This is the **source repository** for the trent system. It contains:
- The complete rule set for task management
- 19 specialized trent agents (agents/skills architecture — 95% context reduction)
- 32+ skills covering task management, QA, planning, video/3D, and more
- 8 slim always-apply rules per platform (was 5,420 lines, now 281 lines)
- Templates for installing trent in other projects
- MCP server for RAG, research, Oracle, and video analysis tools

When making changes here, consider:
1. Parity: Changes to `.cursor/` must also apply to `.agent/` and `.claude/` and `.codex/` and `.opencode/` and vice versa
2. Does this affect the docker/templates/ files?
3. Does this need to update agents.md trent section?
4. Should this trigger a version bump?

## Tech Stack
- **Rules**: `.claude/rules/*.md` (Claude Code) / `.cursor/rules/*.mdc` (Cursor)
- **Skills**: Markdown with YAML frontmatter in `.claude/skills/` and `.cursor/skills/`
- **MCP Server**: Python with FastMCP, PostgreSQL/pgvector for RAG, Oracle support
- **Task Files**: Markdown with YAML frontmatter
- **Package Management**: UV for Python

## Key Directories
```
.cursor/                # Cursor IDE configuration
.claude/                # Claude Code configuration (rules, skills, agents)
.agent/                 # Gemini/Antigravity configuration
.trent/                 # Task management data (TASKS.md, tasks/, phases/)
docker/                 # MCP server (Docker)
docs/                   # Project documentation
temp_scripts/           # Test and utility scripts
```

## MCP Tools Available
| Tool | Description |
|------|-------------|
| `rag_search` | Semantic search in knowledge base |
| `rag_ingest_text` | Add content to knowledge base |
| `rag_list_subjects` | List available knowledge bases |
| `research_deep` | Comprehensive research with Perplexity |
| `research_search` | Web search for research |
| `oracle_query` | Read-only SQL on Oracle |
| `oracle_execute` | Write SQL on Oracle |
| `mediawiki_page` | MediaWiki CRUD operations |
| `mediawiki_search` | Search MediaWiki |
| `trent_install` | Install full trent environment |
| `trent_rules_update` | Update IDE configs/rules |
| `trent_plan_reset` | Reset .trent/ to blank template |
| `trent_server_status` | Health check |
| `trent_health_report` | Compute health score for a trent project (vNext) |
| `platform_docs_search` | Search Firecrawl-crawled platform docs (vNext, optional) |
| `md_to_html` | Convert markdown to HTML |
| `memory_ingest_session` | Ingest raw turns from file adapters |
| `memory_capture_session` | AI self-reports session summary |
| `memory_search` | Semantic search over session memory |
| `memory_sessions` | List recent sessions for a project |
| `memory_context` | Token-budgeted context block |
| `check_crawl_freshness` | Check if platform docs are fresh (prevents redundant crawls) |
| `update_crawl_registry` | Record completed platform doc crawl in registry |

## Development Commands
```bash
cd docker && docker compose up -d              # Start MCP server
docker ps | grep trent_rules_docker            # Check status
docker logs trent_rules_docker -f              # View logs
cd docker && docker-compose up -d --build trent_rules_docker  # Rebuild
```

## Rules & Configuration
**New hybrid architecture** — agents/skills replace monolithic rules:

- **Always-apply rules** (8 files, ~281 lines): `00_always`, `01_documentation`, `02_git_workflow`, `08_powershell`, `09_python_venv`, `25_trent_session_start`, `33_enforcement_catchall`, `silicon_valley_personality`
- **Trent agents** (19 files): `trent-task-manager`, `trent-planner`, `trent-qa-engineer`, `trent-workflow-manager`, `trent-infrastructure`, `trent-autonomous`, `trent-verifier`, `trent-self-improvement`, `trent-project-files`, `trent-platform-parity`, `trent-multi-agent`, `trent-memory`, `trent-cursor-cli`, `trent-claude-cli`, `trent-codebase-analyst`, `trent-ideas-goals`, `trent-code-reviewer`, `trent-python-dev`, `trent-project-manager`
- **Skills** (32+ files): `trent-task-new`, `trent-plan`, `trent-review`, `trent-sprint`, + 13 video/3D skills (manim, remotion, storyboard, etc.)

**MCP Tools new in v6:**
- `check_crawl_freshness` — check if platform docs need re-crawling
- `update_crawl_registry` — mark platform docs as freshly crawled

## Security
- Never commit API keys, tokens, or passwords
- Use environment variables for secrets
- Always use parameterized queries
- Oracle credentials passed per-query via tool parameters

---
**Version**: 6.0.0
**Last Updated**: 2026-03-09
**Supported IDEs**: Cursor, Claude Code, Gemini, Codex, OpenCode
