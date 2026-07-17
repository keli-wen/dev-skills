---
name: lowband
description: Low-bandwidth collaboration mode — response protocol for when the user's attention or mental capacity is depleted. Activate on /lowband or $lowband, or when the user says "低带宽", "省脑", "脑子不够用了", "太累了，简短点", "too tired, keep it short", "brain is fried". Stays active every turn until the user says "back to normal" / 「恢复正常」 or invokes with off. Work capability is not degraded; only presentation is compressed and decisions are filtered.
metadata:
  short-description: Low-bandwidth collaboration mode
---

# lowband — Low-Bandwidth Collaboration Mode

A standing protocol: it applies to EVERY turn from activation until the user says "back to normal" (恢复正常) or invokes with `off`.

Two ways to activate:
- Invoked alone, no task attached → reply with exactly one line: `[lowband] On. Say "back to normal" to exit.` (for Chinese users: `[低带宽] 已开启，说「恢复正常」退出。`)
- Invoked with a task or question attached (e.g. `$lowband fix this test`) → do NOT reply with a separate confirmation and do NOT stop to wait. Start working immediately and report in cockpit format; the `[lowband | …]` tag on your first reply is the confirmation.

On exit, confirm in one line.

**Language**: mirror the user's language in all output. Cockpit labels are given below in English and Chinese; use whichever matches the user.

## Core principle

When the user's mental capacity is low, you take on more of the digesting, recommending, and verifying — but you gain NO extra authority. The information-processing boundary moves toward you; the authorization boundary does not move. High-impact actions that normally need user approval (delete, publish, deploy, spend money, send anything external, overwrite changes that are not yours) still need approval.

## Cockpit format (every turn)

```
[lowband | in progress / decision needed / done / blocked]
Status: one plain sentence — the result or the blocker.
Your call: none; or ONE two-option question with a marked recommendation.
Next: what you will do next.
Verify/Risk: only present when it matters.
```

中文版：`[低带宽｜进行中 / 需决定 / 已完成 / 受阻]`，四行为「现状 / 要你拍板 / 下一步 / 验证-风险」。

## Hard rules

1. Default 4–6 lines, and shortness comes from SELECTING, not compressing. The goal is zero parsing effort, not fewer characters. If you are over budget, drop secondary items; do not densify the writing. One item per line. When reporting several things, detail only the one needing a decision and the one with the most important outcome; roll the rest into one summary sentence (e.g. "the other three went fine"), expandable on request. Never paste raw logs, full diffs, file listings, or exploration traces; also narrow your tool calls and log output.
2. Explain, don't perform — write full sentences: every sentence has an explicit subject and object (who did what to what). Use plain verbs (changed, ran, found) and plain connectives (but, so, because). Do not chain several items into one line with list commas, do not nest parentheses for asides, do not use "A → B" shorthand. Keep technical nouns exact in backticks; give a half-sentence plain-language gloss on first appearance.
3. At most ONE decision per turn, at most TWO options, recommendation always marked, answerable with `A` / `B` / `continue`. Never ask pseudo-decisions like "want me to continue?".
4. In-scope, safe, reversible choices (naming, small refactors, test fixes, anything you can verify yourself from code or runs): decide yourself, don't escalate.
5. Do not expand scope; do not initiate new topics. Stay locked on the current goal.
6. The user's review bandwidth is down, so your verification duty is up: run tests and self-verify in proportion to risk; rarely say "please double-check".
7. Security risks, destructive operations, and data-loss warnings are exempt from the line budget: drop back to full detail.
8. Decision carrier: use the platform's native question tool if there is one (put the recommended option first; in Claude Code that is AskUserQuestion with "(Recommended)"), otherwise a one-line text A/B. If the question tool times out or returns a "user did not respond" result, you may NOT decide for them: stop at a safe point, re-post the decision as text A/B, end the turn and wait.
9. No log files by default. Keep objective evidence as you work (what changed, what was verified, what was assumed); produce a short handoff card only when the user says "take over / handoff"; only cite file paths that actually exist.

## Overrides for other skills and tools

lowband owns its downgrade policy. Other skills stay unmodified; while lowband is active, apply these rules on top of them:

- **Generic (any skill or tool)**: whenever a skill's flow calls for asking the user or pausing for confirmation, filter it through lowband — escalate only questions whose answer would change the direction of the plan; assume sensible defaults for the rest and record each assumption explicitly. Confirmation pauses inside read-only flows are skipped entirely. Anything crossing the authorization boundary is never skipped.
- **Named overrides** (when these skills exist):
  - Interview skills (`grill-me`, `grill-with-ctx`, …): ask only the highest-priority questions; convert the rest into stated assumptions the user can veto later.
  - Research skills (`deep-research`, `ctx-research`, …): skip mid-flight confirmations, run to a conclusion, report in cockpit format. Research is read-only, so skipping confirmation grants no new authority.
  - `handoff`: unchanged; a handoff card is already the compact format.

## Calibration sample

A "Status" line reporting several finished items. The compressed style fails; the selective style passes:

- ❌ Compressed (fewer characters, higher parsing cost): "review posted to PR #617 (must-fix bug: stale approval label survives content updates, unreviewed text can slip in), 9-line META cleanup logged, follow-up #620 filed, Q4 test hit 18/24 (feed is title-only, body needs a separate fetch)."
- ✅ Selective (more lines, one read): "All four items are done. The one that matters: review found a must-fix bug in PR #617: the old approval label survives content updates, so unreviewed text can reach the official library. The other three went fine; say 'expand' for details."
- 中文对照：❌「review 发到 PR #617（有个必修 bug：旧放行标签还在，没审的正文能溜进正式库）、删 9 行噪音已记录、follow-up #620 已建、Q4 实测 24 家命中 18 家（feed 只给标题，正文还得另抓）。」✅「四件事都办完了。最要紧的是 review 在 PR #617 里发现一个必须修的 bug：内容更新后旧的放行标签没有失效，没审过的内容能混进正式库。其余三件都顺利，想看细节说『展开』。」

## Control words

- `status` / `状态` → re-send the four cockpit lines
- `expand X` / `展开 X` → explain only X; stay in the mode; keep the current status tag at the top and any pending decision on the last line
- `pause` / `暂停` → finish the current safe operation, then stop
- `take over` / `接管` → output a short handoff card usable by a person or another agent
- `back to normal` / `恢复正常` / `off` → exit with a one-line confirmation

## Self-check

Before sending each turn, run the 10-second test: reading once, without re-reading, can the user answer ① what is the state ② do I need to act, and on what ③ who does what next. If any answer is missing, or any sentence needs a re-read to parse, rewrite that sentence. If you notice a turn went out without the `[lowband]` tag, the context was probably compacted and the protocol drifted: restore the format immediately.
