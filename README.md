# Keli's Agent Skills

个人 agent skills 仓库，组织方式参考 [mattpocock/skills](https://github.com/mattpocock/skills)。核心主题：**低认知带宽下的人机协作**。agent 的工作能力不降级，但呈现方式、提问方式和决策方式要对齐我当下的状态。

## 安装

```bash
npx skills@latest add keli-wen/skills
```

Claude Code 里用 `/lowband` 调用，Codex 里用 `$lowband`。

## Skills

| Skill | 状态 | 一句话 |
|---|---|---|
| `lowband` | ✅ 可用 | 低带宽协作模式：脑力不足时 agent 只给驾驶舱信息，决策做成带推荐项的选择题 |
| `handoff` | 🚧 规划中 | 最小充分交接：把当前任务打包给下一个 agent / session |
| `multi-agent-driven` | 🚧 规划中 | 按任务类型把当前任务拆给多个 subagent，用 handoff 做派发契约 |
| `ctx-research` | 🚧 规划中 | 基于项目 contexts 和我的需求做多智能体深度研究 |
| `grill-with-ctx` | 🚧 规划中 | 带上下文、按优先级的追问：先读 ctx 再问，只问 ctx 答不了的，重要的先问 |

## 设计约定

### lowband 是横切模式，不是普通 skill

lowband 开启后是常驻协议。因为它和其他 skill 的指令同时在上下文里，其他 skill 可以声明一段「lowband 适配」，在低带宽下改变自己的行为：

- `grill-with-ctx`：只问高优先级问题，其余自己 assume，并把假设显式记下来
- `ctx-research`：跳过中间确认，直接跑完给结论（研究是只读的，跳过确认不越权）

硬边界：**lowband 降低打扰，不扩大授权**。删除、发布、部署、对外发送这类动作，任何模式下都要用户拍板。

### grill-with-ctx 设计笔记

Matt 仓库里的 grill 是三件套，不是两层：`grilling` 是可复用的追问引擎（model-invoked），`grill-me` 是通用入口（问任何话题，问完不留东西），`grill-with-docs` 是工程特化入口（边问边把敲定的结论写进 `CONTEXT.md` 和 ADR）。分层的真实理由是：入口决定「问完之后留下什么」。

我的项目已经有自己的持久层（`contexts/` 体系），所以两个入口可以合成一个 `grill-with-ctx`：

1. **先读再问**：追问前先读相关 contexts，凡是 contexts 已经回答的不问
2. **priority-aware**：问题按「答案会不会改变方案方向」排序，重要的先问；边际价值明显下降就停，不追求穷尽（Matt 的版本没有做优先级，这是主要差异点）
3. **写回**：问出来的决策落回 contexts，下次不再问
4. **lowband 适配**：只问 P0，P1 以下自己 assume 并输出假设清单

### 组合规则（借自 Matt）

用户调用的 skill 可以调 model-invoked 的 skill；反向和平级互调都不允许，避免循环。依赖方向：`ctx-research` → `multi-agent-driven` → `handoff`。
