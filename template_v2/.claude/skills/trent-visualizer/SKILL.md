---
name: trent-visualizer
description: Open or generate task dependency visualization. Opens live visualizer at localhost:8082/admin/trent or generates a Mermaid flowchart inline when server is unavailable.
---
# trent-visualizer

## When to Use
User wants to see task dependencies, project flowchart, visualize trent project status, or asks for a diagram. @trent-visualizer command.

## Sub-mode A: Live Visualizer (MCP Server Running)

1. Check if `localhost:8082/admin/trent` is reachable
2. If YES: output URL and instruct user to open it
3. Verify `TRENT_PROJECT_PATH` env var points to current project
4. If mismatch: provide docker-compose.yml update instructions

```
🌐 Task Dependency Visualizer
URL: http://localhost:8082/admin/trent

Features:
- Interactive DAG with pan/zoom
- Click nodes for task details
- Toggle: DAG view ↔ Phase swimlanes
- Status color coding (green=done, blue=active, red=failed)
- Archived tasks shown with 📦 badge
```

## Sub-mode B: Mermaid Snapshot (Server Unavailable)

1. Scan paths in order:
   - `.trent/tasks/*.md` — active tasks
   - `.trent/phases/*/task*.md` — archived tasks

2. Extract from each file's YAML: `id, title, status, phase, dependencies`

3. Generate Mermaid flowchart:

```
flowchart TD
  subgraph Phase0["Phase 0: Setup"]
    T001["✅ task001\nProject Init"]
    T002["✅ task002\nConfigure Env"]
  end
  subgraph Phase1["Phase 1: Foundation"]
    T100["🔄 task100\nDB Schema"]
    T101["📋 task101\nAPI Layer"]
  end
  T001 --> T100
  T002 --> T100
  T100 --> T101

  style T001 fill:#15803d,color:#fff
  style T002 fill:#15803d,color:#fff
  style T100 fill:#1d4ed8,color:#fff
  style T101 fill:#475569,color:#fff
```

4. Status emoji and color mapping:
| Status | Emoji | Fill Color |
|---|---|---|
| completed | ✅ | `#15803d` (green) |
| in-progress | 🔄 | `#1d4ed8` (blue) |
| awaiting-verification | 🔍 | `#7c3aed` (purple) |
| pending | 📋 | `#475569` (slate) |
| failed | ❌ | `#dc2626` (red) |
| ghost (no file) | 👻 | `#1e293b` (dark, dashed) |

5. Include legend after diagram:
```
Legend: ✅ completed | 🔄 active | 🔍 verifying | 📋 pending | ❌ failed
```

## Fallback: TASKS.md Only
If no task files exist, parse TASKS.md for phase structure and render flat swimlanes (no edges — dependency data unavailable).
Show: `⚠️ Viewing from TASKS.md only — task files needed for dependency graph`
