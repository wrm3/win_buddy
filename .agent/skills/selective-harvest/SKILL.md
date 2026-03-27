---
name: selective-harvest
description: Analyze external sources (repos, articles, videos, research) and selectively harvest ideas, features, or patterns for your project. User chooses what to adopt -- nothing is integrated without explicit approval. Use when reviewing ANY external source for potential improvements.
---

# Selective Harvest Skill

Analyze external sources and present improvement opportunities as a curated menu. The user selects what they want -- only approved items become tasks. **Nothing changes without explicit user approval.**

## When to Use This Skill

Use this skill when the user wants to:
- Review an external repo for ideas (NOT merge it into our project)
- Analyze an article, video transcript, or research for applicable improvements
- Browse what a library/framework offers and pick specific features
- Evaluate a competing product for ideas worth adopting
- Process any external information source for selective adoption

**Trigger phrases**: "harvest", "what can we learn from", "analyze this for ideas", "what's useful in", "review this for improvements", "cherry-pick from", "what should we adopt from"

## When NOT to Use This Skill

DO NOT use this skill for:
- **Merging two of your own projects** → Use `@trent-analyze-codebase` instead
- **Full integration/absorption of an external codebase** → Use `@trent-analyze-codebase` instead
- **Simple code reviews** → Use `trent-code-reviewer` skill
- **Bug tracking** → Use `trent-qa` skill

### Critical Distinction: Harvest vs. Integration

| Aspect | Harvest (THIS skill) | Integration (`@trent-analyze-codebase`) |
|--------|---------------------|----------------------------------------|
| **Source** | External source you don't own | Your own projects being merged |
| **Goal** | Selectively adopt ideas | Full deep merge |
| **User role** | Active chooser at every step | Approves overall plan |
| **Default** | Nothing adopted unless approved | Everything mapped for integration |
| **Risk** | Low -- controlled, incremental | High -- architectural restructuring |
| **Output** | Menu of suggestions → user picks | Complete integration phase |
| **Scope** | Only what user says yes to | Comprehensive feature parity |

---

## The Harvest Process (5 Steps)

### Step 1: Load Project Context

**BEFORE looking at the external source**, build a complete picture of OUR project.

**Actions:**
1. Read `.trent/SUBSYSTEMS.md` -- understand all current subsystems
2. Read `.trent/TASKS.md` -- understand planned/in-progress work
3. Read `.trent/PLAN.md` -- understand the product vision
4. Read `.trent/PROJECT_CONTEXT.md` -- understand the mission

**Output to user:**
```markdown
## 📋 Project Context Loaded

**Project**: {project name}
**Mission**: {1 sentence from PROJECT_CONTEXT.md}
**Current Phase**: {active phase from TASKS.md}
**Active Subsystems**: {count} working, {count} planned
**Planned Work**: {count} pending tasks across {count} phases

**Key Subsystem Categories:**
- Infrastructure: {list}
- Backend Services: {list}
- Frontend: {list}
- Desktop: {list}
- External Tools: {list}

Ready to analyze the source. What am I looking at?
```

**If SUBSYSTEMS.md is outdated or missing information**, note it and suggest updating it after the harvest is complete.

---

### Step 2: Analyze the External Source

**Adapt analysis method to the source type:**

#### For a Repository/Codebase:
1. Scan the top-level structure
2. Identify the tech stack and entry points
3. Map major components and what they do
4. Note any novel patterns, architectures, or approaches
5. Identify configuration and security approaches

#### For an Article/Document:
1. Read and summarize the key points
2. Identify actionable ideas or techniques
3. Note any tools, libraries, or patterns mentioned
4. Identify applicability to our project

#### For a Video Transcript:
1. Extract key topics and demonstrations
2. Identify techniques or tools shown
3. Note any architectural patterns discussed
4. Identify applicability to our project

#### For Research/Paper:
1. Summarize findings and methodology
2. Identify applicable techniques
3. Note any implementations or tools referenced
4. Identify potential improvements to our system

**DO NOT** start creating tasks or planning integration during this step. Just understand the source.

---

### Step 3: Present the Harvest Menu

**This is the critical step that prevents scope creep.**

Present findings as a numbered menu of discrete suggestions, organized by category. Each suggestion must include:

```markdown
## 🌾 Harvest Menu: {Source Name}

### Category: {e.g., "AI Agent Capabilities"}

**H-01: {Short descriptive title}**
- **What it is**: {2-3 sentences explaining the capability/idea}
- **Where in source**: {file path, article section, or video timestamp}
- **How it helps us**: {1-2 sentences on benefit to OUR project}
- **Effort estimate**: {Small (hours) / Medium (1-2 days) / Large (3+ days)}
- **Affects subsystems**: {which of our subsystems would change}
- **Risk**: {Low / Medium / High} -- {brief reason}

**H-02: {Next suggestion}**
...

### Category: {e.g., "Security Patterns"}

**H-03: {Title}**
...

---

### Summary

| # | Suggestion | Effort | Risk | Category |
|---|-----------|--------|------|----------|
| H-01 | {title} | Small | Low | AI Agents |
| H-02 | {title} | Medium | Low | Security |
| H-03 | {title} | Large | Medium | Infrastructure |
...

**Total suggestions**: {count}
**Quick wins (Small + Low risk)**: {count}

---

**Your turn.** Reply with:
- Numbers you want (e.g., "H-01, H-03, H-07")
- "all" if you want everything (rare -- are you sure?)
- "none" to pass
- Or discuss any item (e.g., "tell me more about H-05")
```

### Menu Presentation Rules:

1. **Maximum 15-20 suggestions per harvest** -- if there are more, group into "top picks" and "also available"
2. **Order by impact** -- most valuable suggestions first
3. **Be honest about effort** -- don't underestimate
4. **Flag conflicts** -- if a suggestion contradicts our architecture, say so
5. **Suggest groupings** -- "H-01 and H-03 work well together"
6. **Never assume "take all"** -- the default is "take nothing"
7. **Mark items that overlap with existing planned work** in TASKS.md

---

### Step 4: User Selection & Discussion

**Wait for the user to respond.** They will:

- **Select specific items**: Create tasks only for those
- **Ask questions**: Provide more detail on specific suggestions
- **Modify suggestions**: Adapt ideas to fit our architecture
- **Reject items**: Acknowledge and move on
- **Request alternatives**: "I don't want H-03 as described, but what about doing it differently?"

**During discussion:**
- Stay focused on the user's selections
- Don't re-pitch rejected items
- If user says "yes to all" -- confirm: "That's {X} tasks across {Y} subsystems. Want me to proceed with all {X}, or review the Large/High-risk ones first?"
- Keep a running tally of what's approved

**After selections are finalized:**
```markdown
## ✅ Approved Harvest Items

| # | Suggestion | Effort | Status |
|---|-----------|--------|--------|
| H-01 | {title} | Small | ✅ Approved |
| H-03 | {title} | Medium | ✅ Approved |
| H-05 | {title} | Medium | ✅ Modified (user wants X instead of Y) |

**Total approved**: {count} items
**Estimated total effort**: {range}

Proceeding to create tasks...
```

---

### Step 5: Create Tasks (Approved Items Only)

**Only now do we create tasks**, and only for approved items.

**Process:**
1. Determine where tasks belong -- existing phase or new phase?
   - If items fit into an existing planned phase, add them there
   - If items represent a new capability area, create a new phase
   - **Ask the user** if unclear: "Should these go into Phase {N} or a new phase?"

2. Create task entries in `.trent/TASKS.md`
   - Follow trent task naming conventions
   - Include `[Harvest: {source_name}]` tag in task title for traceability
   - Priority based on user's emphasis during discussion

3. Create task spec files in `.trent/tasks/`
   - Reference the original harvest item (H-XX)
   - Reference the source (repo path, article URL, etc.)
   - Include specific implementation guidance from the source analysis

4. **Update SUBSYSTEMS.md** if any new subsystems are implied

**Task Title Format:**
```
Task {ID}: {Action verb} {component} - {description} [Harvest: {source_name}] [{PRIORITY}]
```

---

## Source-Specific Analysis Templates

### Repository Analysis Checklist
- [ ] Tech stack identified
- [ ] Entry points mapped
- [ ] Major subsystems listed with purposes
- [ ] Novel patterns/approaches noted
- [ ] Configuration approach documented
- [ ] Security mechanisms identified
- [ ] Dependencies of interest noted
- [ ] Build/deployment approach reviewed

### Article/Document Analysis Checklist
- [ ] Key thesis/points extracted
- [ ] Actionable techniques identified
- [ ] Referenced tools/libraries noted
- [ ] Applicability to our project assessed
- [ ] Counter-arguments or risks noted

### Video/Transcript Analysis Checklist
- [ ] Key demonstrations captured
- [ ] Tools/techniques shown
- [ ] Code patterns or architectures discussed
- [ ] Timestamps for important sections noted
- [ ] Applicability assessed

---

## Anti-Patterns (What NOT to Do)

### 🚫 Do NOT:
- Create tasks before user approves suggestions
- Assume the user wants everything
- Start modifying code during analysis
- Treat the source as authoritative over our architecture
- Create a full integration phase without user selection
- Suggest replacing our existing working subsystems
- Scope-creep from "harvest ideas" into "rebuild around this"
- Touch systems outside this project (other Docker stacks, other repos)

### ✅ Do:
- Present options clearly with effort/risk
- Wait for explicit approval
- Respect the user's "no"
- Keep our architecture as the foundation
- Only create tasks for approved items
- Tag harvested tasks for traceability
- Update SUBSYSTEMS.md if needed

---

## Integration with Other Skills

| Skill | When to Chain |
|-------|--------------|
| `trent-task-management` | After creating harvest tasks |
| `trent-planning` | If harvest reveals need for a new phase |
| `trent-code-reviewer` | When implementing harvested ideas |
| `trent-qa` | For tracking issues found during implementation |

---

## Example Workflow

### User:
```
@trent-harvest I downloaded this task management system to research/taskflow-main. 
What can we learn from it?
```

### AI Response Flow:
1. Load project context (SUBSYSTEMS.md, TASKS.md, PLAN.md)
2. Analyze research/taskflow-main
3. Present harvest menu with 8-12 suggestions
4. Wait for user selection

### User:
```
I like H-02 and H-07. Tell me more about H-04.
```

### AI:
- Provides detail on H-04
- Waits for decision on H-04
- Tracks H-02 and H-07 as approved

### User:
```
Ok yes to H-04 too. Skip the rest.
```

### AI:
- Creates 3 tasks (H-02, H-04, H-07) in TASKS.md
- Creates task spec files
- Confirms completion
- Does NOT create tasks for the other 5-9 rejected items

---

*This skill ensures that external sources enrich our project without hijacking it. The user is always in control of what gets adopted.*
