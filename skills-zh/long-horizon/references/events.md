# events.jsonl

一次运行里发生了什么的 append-only 记录，一行一个 JSON 对象。`log.md` 给人读；`events.jsonl` 用来度量运行，以后也用来从运行中学习。目前只记录，运行期间没有任何东西读它。

```jsonc
{"ts": "2026-10-12T09:10:00+08:00", "session": 1, "type": "dispatch", "item": "A3", "attempt": 1, "actor": "orchestrator", "detail": "worktree, sonnet worker"}
{"ts": "2026-10-12T09:28:00+08:00", "session": 1, "type": "verify_reject", "item": "A3", "attempt": 1, "actor": "verifier", "reason": "test_fail", "detail": "v1 文件里的注释丢了"}
```

字段：`ts`、`session`、`type`、`actor`（`orchestrator`、`worker`、`verifier`、`human`）必填；`item`、`attempt`、`reason`、`detail`、`model`、`tokens` 适用时填。

| `type` | 什么时候 |
|---|---|
| `session_start`、`session_end` | 一个 session 开始或结束（含恢复） |
| `spec_signed`、`review_amend` | 两道人工闸门 |
| `dispatch`、`worker_return` | 派出一项、worker 回报 |
| `verify_pass`、`verify_reject` | 编排者复跑或验证者的结论 |
| `redispatch` | 那一次战术重试，`detail` 里概括重写后的契约 |
| `discovered` | 新增台账项，`detail` 写是哪一项引出的 |
| `blocked`、`human_answer` | 提出问题；人给出回答 |
| `stop` | 运行停止；`reason` 为 `all_passed`、`all_blocked`、`stagnation` 或 `budget` |

`verify_reject` 的 `reason`：`test_fail`、`check_missing`、`regression`、`scope_violation`、`envelope_violation`、`claim_unverified`、`other`。

事件里绝不写密钥、key 或凭据。写摘要，不写对话原文。
