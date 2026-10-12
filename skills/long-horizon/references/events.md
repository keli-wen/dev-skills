# events.jsonl

An append-only log of what happened in a run, one JSON object per line. `log.md` is for people; `events.jsonl` is for measuring runs and, later, learning from them. For now, record only; nothing reads it during the run.

```jsonc
{"ts": "2026-10-12T09:10:00+08:00", "session": 1, "type": "dispatch", "item": "A3", "attempt": 1, "actor": "orchestrator", "detail": "worktree, sonnet worker"}
{"ts": "2026-10-12T09:28:00+08:00", "session": 1, "type": "verify_reject", "item": "A3", "attempt": 1, "actor": "verifier", "reason": "test_fail", "detail": "comments in v1 files dropped"}
```

Fields: `ts`, `session`, `type`, `actor` (`orchestrator`, `worker`, `verifier`, `human`) always; `item`, `attempt`, `reason`, `detail`, `model`, `tokens` when they apply.

| `type` | When |
|---|---|
| `session_start`, `session_end` | a session begins or ends (resume included) |
| `spec_signed`, `review_amend` | the two human gates |
| `dispatch`, `worker_return` | an item goes out, a worker reports back |
| `verify_pass`, `verify_reject` | the orchestrator's rerun or the verifier's verdict |
| `redispatch` | the single tactical retry, with the rewritten contract summarised in `detail` |
| `discovered` | a new ledger item, `detail` says which item surfaced it |
| `blocked`, `human_answer` | a question is raised; the human answers it |
| `stop` | the run stops; `reason` is `all_passed`, `all_blocked`, `stagnation` or `budget` |

`reason` on `verify_reject`: `test_fail`, `check_missing`, `regression`, `scope_violation`, `envelope_violation`, `claim_unverified`, `other`.

Never write secrets, keys or credentials into an event. Summaries, not transcripts.
