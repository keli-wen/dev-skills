# Keli's Agent Skills

[中文版 README](./README.zh-CN.md)

The agent skills I use day to day, organized after [mattpocock/skills](https://github.com/mattpocock/skills).

## Install

```bash
npx skills@latest add keli-wen/skills
```

Invoke with `/lowband` in Claude Code, `$lowband` in Codex (same for the other skills).

## Skills

| When you… | Use |
|---|---|
| are mentally drained but need the work to keep moving — the agent reports cockpit-style and turns decisions into two-option questions with a recommendation | `lowband` |
| hand the current task to another agent or session and want it to start directly, without duplicated sources of truth | `handoff` |
| want the current task fanned out to several subagents, with the pattern chosen by task type | `multi-agent-driven` |
| need deep research that starts from your project's existing contexts and files verified findings back into them | `ctx-research` |
| have conclusions in the chat that deserve to become a properly-placed context document | `to-ctx` |
| want to be interrogated about a plan, context-aware and important-questions-first | `ctx-grill` (🤔 design open, see notes below) |

## Design conventions

### lowband is a cross-cutting mode, and it owns its overrides

Direction matters: other skills stay unmodified (they may be third-party and not editable), and lowband itself carries the downgrade policy — a generic question filter that applies to any skill, plus named overrides for known ones. See "Overrides for other skills and tools" in [`skills/lowband/SKILL.md`](./skills/lowband/SKILL.md).

Hard boundary: **lowband reduces interruptions; it never expands authorization.** Deleting, publishing, deploying, spending, and sending anything external need explicit user approval in every mode.

### Dependency direction (after Matt)

User-invoked skills may use model-invoked ones; sideways and upward calls are not allowed, which prevents loops. Current graph: `ctx-research` → `multi-agent-driven` → `handoff`, plus `ctx-research` → `to-ctx` for filing results.

### The ctx-* family

`ctx-*` skills share one contract: **read the project's durable context layer before acting, and write durable results back**. Members: `ctx-research` (ready) and `ctx-grill` (design open). `to-ctx` is the family's shared write path — family skills end with it, and it also works standalone.

### Composition: pipe notation

Stage skills chain with `|`, read left to right: `A | B` means "run A, then feed its result to B in the same session".

```
/ctx-research <topic> | /to-ctx        # research, then file the findings
/ctx-research <topic> | /handoff       # research, then hand off to the next agent
/multi-agent-driven <task> | /to-ctx   # fan out, then file the integrated result
```

This is an agent-interpreted convention, not shell parsing — it works because the runtime is the model. Modes don't pipe, they wrap: switch `lowband` on and any chain runs under it.

### Bilingual policy

`skills/` (English) is canonical: models and an international audience read it, and every skill mirrors the user's language at runtime, so Chinese users get Chinese output either way. `skills-zh/` carries Chinese translations of the same skills for people who prefer reading or installing Chinese instructions; it is regenerated from `skills/` after changes, and on any conflict `skills/` wins. The two share skill names, so install one of them, not both. READMEs: this file (EN) and [README.zh-CN.md](./README.zh-CN.md) (中文).

### ctx-grill — design notes (open)

Matt's grilling is three pieces, not two: `grilling` (a reusable interview engine, model-invoked), `grill-me` (a generic entry that leaves nothing behind), and `grill-with-docs` (an engineering entry that writes ADRs and the domain model as it goes). The real reason for the split is **what a session leaves behind**, not "with or without context".

My projects already have a durable layer (a `contexts/` system), so the plan is to merge the entries into one `ctx-grill`:

1. **Read before asking**: read the relevant contexts first; never ask what they already answer.
2. **Priority-aware**: rank questions by "would the answer change the plan's direction"; ask the important ones first, stop when marginal value clearly drops (Matt's version has no prioritization — this is the main difference).
3. **Write back**: decisions produced by the session land in contexts, so they are never asked again.

Open questions before implementing:

- Is "read ctx before asking" a grill feature, or a property every skill here should have?
- What exactly writes back, and in what form — decision records, assumption lists, or both?
- Where is the stop line between "grill until every branch is resolved" (Matt) and "stop at diminishing returns" (mine)?
