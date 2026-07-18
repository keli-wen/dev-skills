# Keli's Agent Skills（中文）

[English README](./README.md)

我日常在用的 agent skills，组织方式参考 [mattpocock/skills](https://github.com/mattpocock/skills)。

## 安装

```bash
npx skills@latest add keli-wen/skills
```

Claude Code 里用 `/lowband` 调用，Codex 里用 `$lowband`，其余 skill 同理。默认装英文版 `skills/`；想读中文指令的装 `skills-zh/`（两者同名，装其一即可）。

## Skills

| 什么时候用 | 用哪个 |
|---|---|
| 脑力耗尽但工作还得推进：agent 只给驾驶舱信息，决策做成带推荐项的二选一 | `lowband` |
| 把当前任务交给另一个 agent / session，让它不重复事实源、直接开工 | `handoff` |
| 想把当前任务按类型拆给多个 subagent 并行推进 | `multi-agent-driven` |
| 需要从项目已有 contexts 出发做深度研究，验证过的结论写回去 | `ctx-research` |
| 对话里的结论值得变成一份放对位置的规范 context 文档 | `to-ctx` |
| 想被带着上下文、按重要性排序地追问方案 | `ctx-grill`（🤔 设计中） |

## 设计约定

### lowband 是横切模式，降级规则由它自己持有

方向很重要：其他 skill 保持原样（它们可能是第三方的，改不了），降级策略写在 lowband 自己身上：一条适用于任何 skill 的通用提问过滤规则，加上对已知 skill 的具名覆盖。详见 [`skills/lowband/SKILL.md`](./skills/lowband/SKILL.md) 的 "Overrides" 一节。

硬边界：**lowband 降低打扰，不扩大授权**。删除、发布、部署、付费、对外发送，任何模式下都要用户拍板。

### 依赖方向（借自 Matt）

用户调用的 skill 可以用 model-invoked 的 skill；平级和反向调用不允许，避免循环。当前依赖图：`ctx-research` → `multi-agent-driven` → `handoff`，另有 `ctx-research` → `to-ctx` 负责归档。

### ctx-* 家族

`ctx-*` 的 skill 共守一条契约：**动手前先读项目的持久 context 层，产出的持久结论写回去**。成员：`ctx-research`（可用）、`ctx-grill`（设计中）。`to-ctx` 是家族共用的写入通道：家族 skill 以它收尾，单独用也行。

### 组合：管道写法

阶段型 skill 用 `|` 串联，从左到右读：`A | B` 表示「先跑 A，把结果喂给同一个 session 里的 B」。

```
/ctx-research <题目> | /to-ctx        # 先调研，再归档
/ctx-research <题目> | /handoff       # 先调研，再交接给下一个 agent
/multi-agent-driven <任务> | /to-ctx  # 先派发，再归档整合结果
```

这是 agent 解释的约定，不是 shell 解析；能成立是因为运行时就是模型。模式不参与管道，它是包在外面的：开着 `lowband`，整条链都在它之下运行。

### 双语策略

英文 `skills/` 是唯一事实源：模型和国际读者读它，且每个 skill 运行时都跟随用户语言输出，中文用户照样得到中文回复。`skills-zh/` 是给想读或想装中文指令的人准备的翻译版，改动后从 `skills/` 重新生成，冲突以英文为准。两边 skill 同名，装其一即可。

### ctx-grill 设计笔记（未定稿）

Matt 的 grill 是三件套：`grilling`（可复用追问引擎）、`grill-me`（通用入口，问完不留东西）、`grill-with-docs`（工程入口，边问边写 ADR 和领域模型）。分层的真实理由是「问完留下什么」，不是「带不带上下文」。

我的项目已有 `contexts/` 持久层，所以计划合成一个 `ctx-grill`：先读 ctx 再问（不问已回答的）、按「答案会不会改变方案方向」排优先级（Matt 版没有优先级，这是主要差异）、敲定的写回 contexts。实现前待想清楚的问题见英文 README。
