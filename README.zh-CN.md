# Keli's Agent Skills（中文）

[English README](./README.md)

个人 agent skills 仓库，组织方式参考 [mattpocock/skills](https://github.com/mattpocock/skills)。核心主题：**低认知带宽下的人机协作**。agent 的工作能力不降级，但呈现方式、提问方式和决策路由要对齐人当下的状态。

## 安装

```bash
npx skills@latest add keli-wen/skills
```

Claude Code 里用 `/lowband` 调用，Codex 里用 `$lowband`，其余 skill 同理。

## Skills

| Skill | 状态 | 一句话 |
|---|---|---|
| `lowband` | ✅ 可用 | 低带宽模式：只给驾驶舱信息，决策做成带推荐项的二选一 |
| `handoff` | ✅ 可用 | 最小充分交接：把任务压缩到下一个 agent 能直接开工 |
| `multi-agent-driven` | ✅ 可用 | 按任务类型把当前任务派发给多个 subagent |
| `ctx-research` | ✅ 可用 | 基于项目 contexts 的深度研究，结论写回 context 体系 |
| `grill-with-ctx` | 🤔 设计中 | 带上下文、按优先级的追问，设计笔记见英文 README |

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
