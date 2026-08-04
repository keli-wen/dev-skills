---
name: handoff
description: 当另一个 agent 或 session 要接管任务或继续未完成工作时，生成最小充分交接。触发语：/handoff、「把任务交给下一个 agent」「生成 handoff」「让另一个 session 继续」、session 转移、任务所有权转移，或当前上下文退化时重开一个干净 session（交接给未来的自己）。持久 artifact 用引用不用复制，输出前抹掉 secrets。
metadata:
  short-description: 最小充分的任务交接
---

# handoff

把当前任务压缩成下一位 agent 可以直接开工的 prompt。issue、context 文档、PR、commit 和 diff 是事实源；handoff 只提供入口、当前状态和必要的未落盘增量。

同一套压缩有三个使用方向：把所有权转移给另一个 agent / session；给派发者的 spawn 契约提供纪律（见 `/fan-out`）；以及重启你自己——当前上下文退化时（失败探索的噪声在污染决策），生成一份朝向自己新 session 的 handoff，好过在噪声里继续。compact 本质上就是交接给未来的自己。

**语言**：跟随用户的语言。

## 核心规则

- 先复用持久 artifact；不要把已有的 spec、issue 或 checklist 复制成又一份事实源。
- 默认在对话里返回结果；用户明确要求时才写文件。
- 不设固定长度。标准是：下一位 agent 能开工，且没有事实被重复。
- 未经明确同意，不创建或更新 issue、不写外部系统、不发消息。
- 用户要 handoff 不代表授权 commit、push、开 PR 或改远端状态。

## 工作流

1. **定义交接**：下一位 agent 的目标、范围内外、任务是未开始还是进行中。
2. **盘点持久 artifact**（只读）：tracking issue、关联 PR、权威 context/ADR 文档、当前 branch/worktree、commit、diff、最近的验证结果。记录每个 artifact 的路径或 URL 和状态，不复述正文。
3. **issue 同意关卡**：没有 tracking issue 时先告诉用户，问是按目标仓库的流程建一个，还是生成 self-contained 的 handoff。不要悄悄建。已有 issue 但过期时，把差异标为未落盘增量，不要悄悄改它。
4. **按引用压缩**：每条信息三选一——已在持久 artifact 里 → 只给路径/URL 加状态加定位；没落盘但继续干活必需 → 简短写出，标为未落盘决策或 blocker；与下一步无关 → 省略。artifact 和实际状态冲突时，点名冲突并说明以哪个证据为准。
5. **进行中的任务**：写清 branch/worktree、base、dirty files、已完成/未完成、最近验证、失败或 blocker、准确的下一步。只摘可执行的失败结论和命令，不贴整段终端日志。没验证过的不许说成已完成。
6. **安全清理**：抹掉 API key、token、密码、connection string、带凭证的 URL 和任务不需要的个人信息。保留变量名，值换成 `<redacted>`。发现疑似已泄露的 secret，只说需要轮换，不复述原值。
7. **输出**一段可复制的 handoff prompt，按需组合这些 section（空的省略）：Goal / Sources of truth / Current state / 未落盘决策与 blocker / Next action / Suggested skills。让下一位 agent 先读事实源再动手。只推荐目标仓库里任务真正需要的 skill，不凭空加关卡。

## 边界

- 独立的 explorer / 并行子任务，spawn prompt 已写清目标、边界和输出的，不需要先做 handoff。
- handoff 不替代 issue filing、context 写作、实现、验证或 PR 流程；它只压缩状态、把下一步路由过去。
