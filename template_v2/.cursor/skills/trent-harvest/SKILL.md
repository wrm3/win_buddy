---
name: trent-harvest
description: Analyze an external source (repo, article, video, research) and present selective improvement ideas. User explicitly approves what to adopt — nothing changes without approval.
---
# trent-harvest

## When to Use
@trent-harvest [URL or path]. User wants to review an external source for ideas to adopt.

## Steps

1. **Fetch the source**:
   - URL → WebFetch or RAG search
   - GitHub repo → explore key files (README, key source files, architecture)
   - Article/blog → extract key points
   - Video → use youtube-video-analysis skill

2. **Map the source** (read before judging):
   - What does it do?
   - Key features/patterns/approaches
   - Tech stack
   - Architecture highlights
   - Anything notably clever or novel?

3. **Compare to current project**:
   - What do we already have? (no point adopting duplicates)
   - What gaps does this fill?
   - What patterns are better than ours?
   - What would be over-engineering for our scale?

4. **Generate harvest menu** (user picks what to adopt):
```markdown
# 🌾 Harvest Menu: [Source Name]

## Overview
[2-3 sentence summary of source and what's valuable about it]

---

### Item 1: [Feature/Pattern Name]
**Type**: Feature | Pattern | Architecture | Config | Tooling
**Effort**: Small (< 2h) | Medium (2-8h) | Large (1-2 days)
**Value**: [Why this improves our project]
**Risk**: Low | Medium | High
**What to adopt**: [Specific description]

---

### Item 2: [Next Item]
...

---

## Quick Wins (Small effort, high value)
1. Item N
2. Item M

## Skip List (Already have / Over-engineering)
- [What to NOT adopt and why]
```

5. **Wait for user selection**:
   - "adopt item 1 and item 3" → create tasks for those only
   - "adopt all quick wins" → create tasks for quick wins
   - Nothing changes until user explicitly approves

6. **For each adopted item**: use trent-task-new to create task, reference harvest source in task notes

7. **Write harvest results to vault** (always, even if nothing adopted):

   Read `.trent/.project_id` to get the project UUID. Resolve the vault path (check `.env` for `TRENT_VAULT_PATH`, else use `.trent/vault/`).

   Write to **two locations** (dual-write pattern):

   **Project copy**: `{vault}/projects/{project_id}_{project_name}/research/harvests/{date}_{source-name}.md`
   **Global copy**: `{vault}/research/harvests/{date}_{source-name}.md`

   Both files use this template:
   ```yaml
   ---
   date: YYYY-MM-DD
   project: {project_name}
   project_id: {from .trent/.project_id}
   source: cursor/agent
   type: harvest
   source_type: github | article | video | paper
   source_repo: {URL if applicable}
   url: {source URL}
   tags: [harvest, {topic tags}]
   ---

   # Harvest: {Source Name}

   ## Source
   - **URL**: {url}
   - **Type**: {github | article | video | paper}
   - **Analyzed for project**: [[{project_name}]]

   ## Overview
   {2-3 sentence summary}

   ## Adopted Items
   - Item N: {description} → Task #{id}

   ## Skipped Items
   - {what was not adopted and why}

   ## Key Patterns Discovered
   - {reusable patterns worth remembering across projects}
   ```

   The global copy allows other projects to discover and reference this harvest. Use `[[link]]` syntax to cross-reference the project and any related notes.
