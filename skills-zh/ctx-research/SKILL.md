---
name: ctx-research
description: 基于项目持久 context 体系的深度调研。触发语：「ctx research」「基于 context 调研 X」「结合我们的 contexts 做深度研究」。先读已有 contexts，把问题磨到真正的知识缺口上，再多智能体展开调研，关键论断做对抗验证，结论写回去。
metadata:
  short-description: 以 context 为地基的深度调研
---

# ctx-research

从「项目已经知道什么」出发的调研，以「项目知道得更多」收尾。它和通用 deep research 的差别有两处：搜索之前先用已有 contexts 把问题磨尖，验证过的发现要写回 context 体系。

**语言**：跟随用户的语言。

## 步骤

1. **落地**：找到项目的持久 context 层（比如带地图文件的 `contexts/` 树，或 docs/ADR 体系）。读与问题相关的条目，把读到的分成三类：已回答的（不再调研）、假设过但没验证的、真正开放的。
2. **磨题**：把调研问题重述为「用户需要的」减去「contexts 已有的」的差值。只有差值本身模糊时才和用户确认范围，否则直接推进。
3. **展开**（用 `multi-agent-driven` 的模式）：不同角度的并行调研者——官方文档、社区与先例、论文、真实代码。每人返回可引用的原始发现，带来源名和 URL 或路径。
4. **验证**：会驱动决策的论断都过一遍对抗检查：由独立的一步尝试反驳它或证明它过时。关键论断标注 confirmed / plausible / refuted。
5. **综合**：一份报告——先答案，再证据，最后开放问题。引用的事实和你自己的判断分开呈现。
6. **写回**：持久的部分交给 `to-ctx`，按项目规则放进 context 体系。聊天里给摘要加文件路径。

## 规则

- contexts 已回答的永不重复调研；引用那个 context 文件即可。
- 验证力度跟决策影响成正比，不跟论断有多有趣成正比。
- 依赖方向：可以用 `multi-agent-driven`、`to-ctx` 和 `handoff`；永不调用面向用户的 skill。
