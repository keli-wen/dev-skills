---
name: long-horizon
description: Execute a spec'd goal in one long autonomous run — hours of agent work pushing a whole acceptance ledger, with humans only at the two gates, spec before and review after. Use for /long-horizon, "make this a long-horizon goal", "run this across sessions", or when resuming work in a repo that already has a `.long-horizon/` workspace. Admission is interactive and iterative; the run is fan-out-driven and side-effect-bounded by an authorization envelope; progress is evidence-gated; a live report.html shows the ledger as a DAG.
metadata:
  short-description: Spec-gated autonomous goal execution
---

# long-horizon

One goal, two human gates, one long run. The human and the agent iterate on the spec until it is signed; then the run pushes the whole ledger autonomously for hours inside an authorization envelope; then the human reviews a report and adjusts. The orchestrating context dispatches and verifies — it does not execute. Durable state lives in `.long-horizon/<goal-slug>/`, and three value gates hold throughout: admission (no verifiable Done-when, no entry), evidence (progress exists only when verified), exit (stopping is designed, not a failure).

**Language**: mirror the user in chat; workspace files follow the project's documentation language; the report's UI labels follow the session.

**Load-on-use**: every `/name` in this document is an invocation — before doing that work, load that skill's full document (the Skill tool, or read its SKILL.md); never act from its one-line description.

## Workspace — `.long-horizon/<goal-slug>/`

- One directory per goal, slug-named; one goal active at a time. On any resume, identity-check first: read `goal.md` — if it describes a different goal than yours, stop and ask.
- `goal.md` — frozen spec: goal, non-goals, invariants, Done-when with a runnable check per clause, and the **authorization envelope**. Changing it is a human-gated re-spec, never a side effect.
- `ledger.json` — acceptance items `{id, desc, verify, passes, evidence, deps, discovered-from}`. Every item is born `passes: false`.
- `log.md` — append-only: decisions, dead ends, dispatch notes. Failed attempts stay in — they are evidence.
- `events.jsonl` — append-only, one JSON event per line: dispatches, verification verdicts with reasons, redispatches, discoveries, blocks, human answers, stops. Schema in `references/events.md`. Record only; it is the raw material for measuring runs and, later, learning from them.
- `next.md` — resume pointer: what is in flight, what is ready next.
- `report.html` — live oversight view, built from the bundled template; contract below.
- The workspace stays **out of git**: gitignore it (and add formatter ignores) at admission — a tracked workspace pollutes every work-branch diff. Durability comes from code commits, graduation, and the report. On graduation, distill through `/to-ctx`, then archive the directory instead of deleting it: keep `goal.md`, `ledger.json`, `events.jsonl`, `log.md` and the final `report.html`, because later runs learn from them.

## Gate 1 — Spec (interactive; iterate as long as it takes)

1. Run the goal through `/ctx-grill`. Iterate freely with the user until the spec holds:
   - every Done-when clause names a runnable check — no check, no entry;
   - non-goals and invariants written;
   - the **authorization envelope** — what the run may do unattended. Default: committing to work branches, opening PRs, pushing its own branches — allowed; merging, deleting outside the workspace, sending anything external, spending — forbidden. Tighten or loosen only here, explicitly.
   - the **verification setup** — ask once: which checks the orchestrator reruns itself, which acceptance items get a black-box verifier agent, and the verifier model tier (default: a mid-tier model);
   - the initial ledger, with dependencies.
2. Refuse goals that fit one sitting — do them normally instead.
3. On sign-off: write the workspace and start the run.

## The run — autonomous, hours

- **Orchestrate, don't execute.** Load `/fan-out` and dispatch ledger items as task contracts to subagents; keep only the spec, the ledger, evidence summaries, and decisions in your own context — workers absorb the exploration noise. This is structural, not optional: a whole ledger's execution does not fit one context window.
- **Schedule off the DAG**: dispatch the ready set (all deps passed); independent items in parallel — worktree isolation when they mutate the same repo; coupled clusters go to one worker.
- **Verify before flipping**: worker claims are never evidence. Mechanical checks (tests, lint, build) — rerun them yourself. Behavioral acceptance — a black-box verifier subagent (the spec'd tier) that sees only the artifact and the acceptance criteria.
- **A failure buys one rewrite, never a repeat**: when a dispatched item fails — the worker errors out, or verification rejects its claim — redispatch it once with the contract rewritten around the failure evidence: what was attempted, which check failed, how it failed. Change the angle or change the worker; never resend the same contract verbatim. One tactical retry per item per dispatch round; if the retry fails too, the item counts as unmoved for stagnation accounting and the failure goes into `log.md` — it does not earn a third attempt in that round.
- **Every flip appends an event and refreshes the report's data block** — the report is the human's live dashboard while the run is in flight.
- **Discovery is expected**: new problems become new ledger items (`discovered-from`) and join the schedule. A question that would change the spec's direction becomes a blocked item with the question written down — and the run continues on every branch that does not depend on it.
- If the harness has a native goal mechanism, feed it: "all ledger items pass or blocked, or stop after N hours".
- **Stop** when: all items pass; everything remaining hangs on blocked; two dispatch rounds, tactical retries included, move nothing (stagnation — never a third identical attempt); or budget runs out. Always end with the final report and a `/handoff`.

## Gate 2 — Review

The human reads the report and comments. Adjustments become spec amendments or ledger edits — the only path by which acceptance rows may be reworded or deleted. The next run resumes from the workspace, identity check first.

## Interruption is survivable, not the rhythm

Assume any moment may be the last: context death, crash, budget cut. A fresh orchestrator reads the workspace, identity-checks `goal.md`, and resumes from `ledger.json` + `next.md`. That is what the files are for — not for handing the goal back to the human every few items.

## Report — a fixed template, a data-only refresh

Start from `assets/report-template.html`; do not design your own. At admission, copy it into the workspace as `report.html`, write its `lh-labels` block once in the session's language (keep the keys, translate the values), and fill its `lh-data` block from the state files; then run `scripts/check-report.py` on it and shorten any label it names. From then on, every refresh rewrites `lh-data` and nothing else: no markup, style or script edits inside a run. The schema, what the template computes for itself, and a refresh snippet are in `references/report.md`. If the board lacks something, use `custom_panels`; improvements to the template go back to the skill.

The template already meets the contract; keep it that way:

- **A view, never a store**: generation is one-way; everything shown must already exist in the state files. Must show: the goal and its Done-when; every ledger item with status; **the dependency structure drawn as a graph — critical path and blocking cut-points visible at a glance, not only a list**; blocked items and their questions, prominently; key decisions; last-updated and session count.
- **Self-contained**: a single file that opens from `file://` and makes no external requests.
- **Data apart from rendering**: one embedded data block; routine refreshes touch only that block, not the markup.

## Rules

- The envelope is hard in every phase: nothing irreversible, nothing outside it.
- Ledger rows are write-protected for the agent: flip `passes`, append `evidence`, add new items; rewording or deleting rows happens only in review, by the human.
- `passes` flips on verification, not on code written.
- A chat correction that contradicts a workspace file is written back in the same turn — otherwise the stale file wins.
- Dependency direction: may use `/ctx-grill`, `/fan-out`, `/handoff`, and `/to-ctx`; long-horizon sits at the top of the graph and nothing invokes it.
