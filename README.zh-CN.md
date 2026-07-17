# Keli's Agent Skills（中文）

[English README](./README.md)

我日常在用的 agent skills，组织方式参考 [mattpocock/skills](https://github.com/mattpocock/skills)。

## 安装

```bash
npx skills@latest add keli-wen/skills
```

Claude Code 里用 `/lowband` 调用，Codex 里用 `$lowband`，其余 skill 同理。

## Skills

| 什么时候用 | 用哪个 |
|---|---|
| 脑力耗尽但工作还得推进：agent 只给驾驶舱信息，决策做成带推荐项的二选一 | `lowband` |
| 把当前任务交给另一个 agent / session，让它不重复事实源、直接开工 | `handoff` |
| 想把当前任务按类型拆给多个 subagent 并行推进 | `multi-agent-driven` |
| 需要从项目已有 contexts 出发做深度研究，验证过的结论写回去 | `ctx-research` |
| 想被带着上下文、按重要性排序地追问方案 | `grill-with-ctx`（🤔 设计中） |

## 设计约定

### lowband 是横切模式，降级规则由它自己持有

方向很重要：其他 skill 保持原样（它们可能是第三方的，改不了），降级策略写在 lowband 自己身上——一条适用于任何 skill 的通用提问过滤规则，加上对已知 skill 的具名覆盖。详见 [`skills/lowband/SKILL.md`](./skills/lowband/SKILL.md) 的 "Overrides" 一节。

硬边界：**lowband 降低打扰，不扩大授权**。删除、发布、部署、付费、对外发送，任何模式下都要用户拍板。

### 依赖方向（借自 Matt）

用户调用的 skill 可以用 model-invoked 的 skill；平级和反向调用不允许，避免循环。当前依赖图：`ctx-research` → `multi-agent-driven` → `handoff`。

### 双语策略

SKILL.md 指令用英文写（读者是模型和国际用户）；所有 skill 在运行时跟随用户的语言输出，lowband 的驾驶舱模板和校准样本中英都带。README 双份：英文主文件加本文件。

### grill-with-ctx 设计笔记（未定稿）

Matt 的 grill 是三件套：`grilling`（可复用追问引擎）、`grill-me`（通用入口，问完不留东西）、`grill-with-docs`（工程入口，边问边写 ADR 和领域模型）。分层的真实理由是「问完留下什么」，不是「带不带上下文」。

我的项目已有 `contexts/` 持久层，所以计划合成一个 `grill-with-ctx`：先读 ctx 再问（不问已回答的）、按「答案会不会改变方案方向」排优先级（Matt 版没有优先级，这是主要差异）、敲定的写回 contexts。实现前待想清楚的问题见英文 README。
