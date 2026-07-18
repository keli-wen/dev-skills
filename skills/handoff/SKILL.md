---
name: handoff
description: Generate a minimal-sufficient handoff when another agent or session will take ownership of a task or continue unfinished work. Use for /handoff, "把任务交给下一个 agent", "生成 handoff", "让另一个 session 继续", session transfer, task ownership transfer, or restarting in a fresh context when the current session has degraded (a handoff to your future self). Reuses durable artifacts by reference instead of copying them, and redacts secrets.
metadata:
  short-description: Minimal-sufficient task handoff
---

# handoff

Compress the current task into a prompt the next agent can start from directly. Issues, context docs, PRs, commits, and diffs are the sources of truth; the handoff only provides entry points, current state, and the necessary not-yet-persisted delta.

The same compression works in three directions: transferring ownership to another agent or session; disciplining spawn contracts when a dispatcher delegates slices (see `multi-agent-driven`); and restarting yourself — when the current context has degraded (noise from failed explorations polluting decisions), a handoff aimed at your own fresh session beats continuing in the noise. Compaction is just a handoff to your future self.

**Language**: mirror the user's language.

## Core rules

- Reuse durable artifacts first; never copy an existing spec, issue, or checklist into a fourth source of truth.
- Return the handoff in the conversation by default; write a file only when the user asks.
- No fixed length. The standard is: the next agent can start working, and no fact is duplicated.
- Do not create or update issues, write to external systems, or send messages without explicit consent.
- A handoff request does not imply authorization to commit, push, open PRs, or change remote state.

## Workflow

1. **Define the transfer**: the next agent's goal, what is in and out of scope, and whether the task is not-yet-started or in progress.
2. **Discover durable artifacts** (read-only): tracking issue, linked PR, authoritative context/ADR docs, current branch/worktree, commits, diff, latest verification results. Record each artifact's path or URL and status; do not restate its content.
3. **Issue consent gate**: if no tracking issue exists, tell the user and ask whether to file one (per the target repo's workflow) or produce a self-contained handoff. Do not file silently. If an existing issue is stale, flag the difference as unpersisted delta instead of silently editing it.
4. **Compress by reference**: for each piece of information — already in a durable artifact → give path/URL + status + anchor only; not persisted but required to continue → state it briefly, marked as unpersisted decision / blocker; irrelevant to the next step → omit. If artifacts conflict with observed state, name the conflict and say which evidence wins.
5. **In-progress tasks**: include branch/worktree, base, dirty files, done/not-done, latest verification, failures or blockers, and the exact next step. Quote only actionable failure conclusions and commands, never whole terminal logs. Never claim unverified work as done.
6. **Safety pass**: strip API keys, tokens, passwords, connection strings, credential-bearing URLs, and PII the task does not need. Keep variable names, replace values with `<redacted>`. If a secret looks already-leaked, say it needs rotation without repeating the value.
7. **Output** a copyable handoff prompt with the applicable sections (omit empty ones): Goal / Sources of truth / Current state / Unpersisted decisions & blockers / Next action / Suggested skills. Tell the next agent to read the sources of truth before acting. Suggest only the target repo's skills that the task actually needs; do not invent gates.

## Boundaries

- Independent explorer/parallel subtasks whose spawn prompt already states goal, boundaries, and output do not need a handoff first.
- Handoff replaces neither issue filing, context writing, implementation, verification, nor PR workflows; it only compresses state and routes the next step.
