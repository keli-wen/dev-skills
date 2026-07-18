---
name: multi-agent-driven
description: Dispatch the current task to multiple subagents — after checking that fan-out is actually justified. Use when the user says "multi-agent this", "fan out", "用多智能体做", "派发出去", or when a task decomposes into genuinely independent subtasks. Decomposes along context coupling, uses handoff discipline for spawn contracts.
metadata:
  short-description: Coupling-aware multi-agent dispatch
---

# multi-agent-driven

Turn the current task into a coordinated multi-agent run — but only when fan-out actually pays. You stay the orchestrator: decompose, dispatch, integrate. Do not do the subtasks inline.

**Language**: mirror the user's language.

## Gate: is fan-out justified?

Multi-agent costs are real: agents burn several times the tokens of a chat, multi-agent systems an order of magnitude more, and every hand-off pays a communication tax — a sub-agent's summary hides the implicit decisions behind its actions, and orchestrator instructions lose nuance on the way down.

1. Exhaust the single context first: clearer instructions, compressed context, a narrower tool set. Many "needs multi-agent" problems are single-agent context management done badly.
2. Fan out only on real signals: the current context is degrading (noise from failed explorations polluting decisions), the information space is wider than one agent can cover, or the tool set is large enough that selection accuracy drops and it splits along clear specialties.
3. When unsure, don't split. A wrong split (information loss plus inconsistent decisions) costs more than a slightly bloated single context. Start with the simplest approach that works; add agents only when evidence supports it.

## Steps

1. **Decompose along context coupling, not function.** The boundary between agents must sit where shared context is minimal. Never split by work stage (one agent implements, one tests, one reviews) — that cuts exactly where coupling is highest and turns the run into a game of telephone. Low-coupling slices split well: independent search paths, doc digestion, black-box verification, separate research angles. High-coupling work stays in one agent, usually you: core implementation, architecture decisions, anything whose choices silently constrain other work.
2. **Pick the pattern by task type**:
   - research / investigation → parallel explorers with distinct angles (by source, by subsystem, by time window); tell each to start wide, then narrow
   - implementation across many sites → discover the full work list first, then one agent per site; worktree isolation when they mutate the same repo in parallel
   - review / audit → dimension-parallel finders, then an adversarial verifier per finding
   - design decision → 2–3 independent proposal agents with different priorities (MVP-first, risk-first, user-first), then a judge pass
   - debugging → parallel hypothesis testers, each trying to falsify one hypothesis
   - any of the above → a black-box verification subagent is almost always worth adding: it needs only the acceptance criteria and the artifact, making it the cheapest, most reliable split there is
3. **Write each spawn prompt as a task contract** (handoff discipline): explicit objective, inputs by reference (paths / issues / URLs, not pasted content), expected output shape, boundaries (what NOT to touch), and a tool hint when the agent might pick wrong. Vague delegation produces duplicated or misdirected work. Scale effort to complexity and say it in the contract: a simple lookup is one agent with a handful of tool calls; a comparison is two to four agents; only genuinely complex work justifies ten or more.
4. **Dispatch**: independent agents go out in parallel; dependent stages form a pipeline without artificial barriers. Parallelize at both levels — several agents at once, and several tool calls within each agent. Prefer the platform's native orchestration (Claude Code: Agent tool or Workflow; elsewhere: sequential subagent calls).
5. **Integrate**: read the results yourself and hunt for cross-agent inconsistencies first — sub-agents cannot see each other's implicit decisions, so individually correct outputs can still conflict (incompatible structures, duplicated work, contradicting assumptions). Resolve the conflicts, verify the merged outcome (rerun tests, spot-check claims), and report one integrated conclusion, not a pile of agent outputs.

## Rules

- Decisions that constrain more than one subtask (data structures, interfaces, naming, approach) are made by you BEFORE dispatch and stated in every affected contract — never left for sub-agents to make independently.
- Default to the strongest available model tier for substantive subagent work (opus-high / sonnet-max / xhigh-class); drop to a cheaper tier only for trivial mechanical stages. Name the tier explicitly in the dispatch.
- Every fan-out states its coverage: what was included, what was dropped. No silent truncation.
- Subagent results are claims, not facts. Verify before integrating: rerun the test, reopen the file, recheck the quote.
- Dependency direction is one-way: this skill may use `handoff`; it never invokes user-facing skills.
