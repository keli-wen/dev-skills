# Keli's Agent Skills

[中文版 README](./README.zh-CN.md)

The agent skills I use day to day, organized after [mattpocock/skills](https://github.com/mattpocock/skills). The flagship is `lowband`: **human-agent collaboration under low cognitive bandwidth** — the agent's capability never degrades; its presentation, questioning, and decision routing adapt to the human's current state.

## Install

```bash
npx skills@latest add keli-wen/skills
```

Invoke with `/lowband` in Claude Code, `$lowband` in Codex (same for the other skills).

## Skills

| Skill | Status | One-liner |
|---|---|---|
| `lowband` | ✅ ready | Low-bandwidth mode: cockpit-only reporting, decisions become two-option questions with a recommendation |
| `handoff` | ✅ ready | Minimal-sufficient handoff: compress the task so the next agent can start directly |
| `multi-agent-driven` | ✅ ready | Type-aware dispatch of the current task to multiple subagents |
| `ctx-research` | ✅ ready | Deep research grounded in the project's context system, findings filed back |
| `grill-with-ctx` | 🤔 design open | Context-grounded, priority-aware grilling — see design notes below |

## Design conventions

### lowband is a cross-cutting mode, and it owns its overrides

Direction matters: other skills stay unmodified (they may be third-party and not editable), and lowband itself carries the downgrade policy — a generic question filter that applies to any skill, plus named overrides for known ones. See "Overrides for other skills and tools" in [`skills/lowband/SKILL.md`](./skills/lowband/SKILL.md).

Hard boundary: **lowband reduces interruptions; it never expands authorization.** Deleting, publishing, deploying, spending, and sending anything external need explicit user approval in every mode.

### Dependency direction (after Matt)

User-invoked skills may use model-invoked ones; sideways and upward calls are not allowed, which prevents loops. Current graph: `ctx-research` → `multi-agent-driven` → `handoff`.

### Bilingual policy

SKILL.md instructions are written in English (they are read by models and an international audience). Every skill mirrors the user's language at runtime, and lowband ships its cockpit template and calibration samples in both English and Chinese. READMEs: this file (EN) and [README.zh-CN.md](./README.zh-CN.md) (中文).

### grill-with-ctx — design notes (open)

Matt's grilling is three pieces, not two: `grilling` (a reusable interview engine, model-invoked), `grill-me` (a generic entry that leaves nothing behind), and `grill-with-docs` (an engineering entry that writes ADRs and the domain model as it goes). The real reason for the split is **what a session leaves behind**, not "with or without context".

My projects already have a durable layer (a `contexts/` system), so the plan is to merge the entries into one `grill-with-ctx`:

1. **Read before asking**: read the relevant contexts first; never ask what they already answer.
2. **Priority-aware**: rank questions by "would the answer change the plan's direction"; ask the important ones first, stop when marginal value clearly drops (Matt's version has no prioritization — this is the main difference).
3. **Write back**: decisions produced by the session land in contexts, so they are never asked again.

Open questions before implementing:

- Is "read ctx before asking" a grill feature, or a property every skill here should have?
- What exactly writes back, and in what form — decision records, assumption lists, or both?
- Where is the stop line between "grill until every branch is resolved" (Matt) and "stop at diminishing returns" (mine)?
