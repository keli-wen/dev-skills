# Report template and data contract

`report.html` is built from `assets/report-template.html`. The template is fixed; a run only ever writes data into it.

## Three blocks, three owners

| Block | Who writes it | When |
|---|---|---|
| `<script id="lh-icons">` | the skill | never during a run |
| `<script id="lh-labels">` | the orchestrator | once, at admission |
| `<script id="lh-data">` | the orchestrator | on every flip and at the end of a session |

- **At admission**: copy the template to `.long-horizon/<goal-slug>/report.html`. If the session's language differs from the template's, rewrite `lh-labels` once: keep every key, translate the values, set `lang`. Then replace the example `lh-data` with the real goal.
- **On every refresh**: rewrite `lh-data` and nothing else. No edits to markup, CSS, script or icons inside a run. If the board lacks something, use `custom_panels`; improvements to the template go back to the skill.
- **One way only**: everything in `lh-data` must already exist in the state files (`goal.md`, `ledger.json`, `log.md`, `next.md`, `events.jsonl`). The report is a view, never a store.

Refresh snippet (writes `data.json` into the block):

```bash
python3 - .long-horizon/<goal-slug> <<'PY'
import json, re, sys, pathlib
ws = pathlib.Path(sys.argv[1]); html = (ws / "report.html").read_text()
data = json.dumps(json.loads((ws / "data.json").read_text()), ensure_ascii=False).replace("</", "<\\/")
html, n = re.subn(r'(<script id="lh-data" type="application/json">).*?(</script>)', lambda m: m.group(1) + data + m.group(2), html, flags=re.S)
assert n == 1; (ws / "report.html").write_text(html)
PY
```

## `lh-data` schema

```jsonc
{
  "schema": "long-horizon/report@1",
  "goal": { "slug", "title", "statement", "phase": "draft|running|review|stopped", "sessions", "updated", "repo"?, "base"? },
  "groups": [ { "id", "label", "hint"?, "color"?, "icon"? } ],          // swim lanes; icon keys below
  "done_when": [ { "id", "text", "check", "items": ["<ledger id>"], "passes"? } ],
  "non_goals": [ "..." ], "invariants": [ "..." ],
  "envelope": { "allowed": [ "..." ], "forbidden": [ "..." ] },
  "verification": { "orchestrator": "...", "verifier": "..." },
  "open_questions": [ { "id", "text", "recommend", "blocks": ["<ledger id>"], "asking"? } ],   // spec phase only
  "ledger": [ {
    "id", "title", "desc", "verify", "passes", "evidence": [ "..." ], "deps": [ "..." ], "discovered-from",
    "group"?, "status"?: "in-flight|blocked|failed", "question"?, "attempts"?, "human"?, "issue"?, "pr"?, "est"?
  } ],
  "decisions": [ { "when", "text" } ],
  "log": [ { "when", "kind": "dispatch|verify|fail|blocked|session|spec", "text" } ],   // newest first, keep it short
  "theme": { "accent"? },
  "custom_panels": [ { "title", "kind": "kv|list|text", "items"? , "text"? } ]
}
```

- `ledger` rows mirror `ledger.json`; the optional fields live there too, so the report stays a view.
- `status` is only for states `passes` cannot express. Leave it out for items that are simply waiting.
- `question` marks an item as needing the human; it shows in the "needs you" inbox.
- `human: true` marks a manual step (for example "merge PR #241").

## What the template computes (never store these)

Ready items (all deps passed), the critical path (longest unfinished chain, weighted by `est`, default 1), bottlenecks (unfinished items holding back the most unfinished descendants), counts, Done-when progress, and the horizon strip.

## Icons

`groups[].icon` takes one of: `prep`, `visual`, `copy`, `engine`, `usage`, `wrap`. The inbox uses `spec`, `decide`, `act`, `retry`; the brand mark is `horizon`. Icons are hand-drawn masks: the ink follows the text colour and the fill takes the lane or status colour, so both themes work.
