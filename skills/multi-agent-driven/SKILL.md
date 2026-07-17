---
name: multi-agent-driven
description: Dispatch the current task to multiple subagents based on task type. Use when the user says "multi-agent this", "fan out", "用多智能体做", "派发出去", or when a task decomposes into genuinely independent subtasks. Uses handoff discipline for spawn contracts.
metadata:
  short-description: Type-aware multi-agent dispatch
---

# multi-agent-driven

Turn the current task into a coordinated multi-agent run. You stay the orchestrator: decompose, dispatch, integrate. Do not do the subtasks inline, and do not fan out work that one context can hold comfortably.

**Language**: mirror the user's language.

## Steps

1. **Classify the task and pick the pattern**:
   - research / investigation → parallel explorers with distinct angles (by source, by subsystem, by time window), then synthesize
   - implementation across many sites → discover the full work list first, then one agent per site in a pipeline; isolate with worktrees when agents mutate the same repo in parallel
   - review / audit → dimension-parallel finders, then an adversarial verifier per finding
   - design decision → 2–3 independent proposal agents with different priorities (MVP-first, risk-first, user-first), then a judge pass
   - debugging → parallel hypothesis testers, each trying to falsify one hypothesis
2. **Write each spawn prompt as a task contract** (handoff discipline): goal, inputs by reference (paths / issues / URLs, not pasted content), boundaries (what NOT to touch), expected output shape.
3. **Dispatch**: independent agents go out in parallel; dependent stages form a pipeline without artificial barriers. Prefer the platform's native orchestration (Claude Code: Agent tool or Workflow; elsewhere: sequential subagent calls).
4. **Integrate**: read the results yourself, resolve conflicts between agents, verify the merged outcome (rerun tests, spot-check claims), and report one integrated conclusion — not a pile of agent outputs.

## Rules

- Decomposition follows context coupling: subtasks that need each other's intermediate context stay in one agent; only genuinely independent slices get separate agents. When in doubt, fewer agents.
- Every fan-out states its coverage: what was included, what was dropped. No silent truncation.
- Subagent results are claims, not facts. Verify before integrating: rerun the test, reopen the file, recheck the quote.
- Dependency direction is one-way: this skill may use `handoff`; it never invokes user-facing skills.
