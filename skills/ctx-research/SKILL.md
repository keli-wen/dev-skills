---
name: ctx-research
description: Deep research grounded in the project's durable context system. Use for "ctx research", "基于 context 调研 X", "结合我们的 contexts 做深度研究". Reads existing contexts first, sharpens the question to the real knowledge gap, fans out multi-agent research, verifies key claims, and files results back.
metadata:
  short-description: Context-grounded deep research
---

# ctx-research

Research that starts from what the project already knows and ends with the project knowing more. It differs from generic deep research in two ways: the question is sharpened against existing contexts before any searching, and verified findings are written back into the context system.

**Language**: mirror the user's language.

## Steps

1. **Ground**: locate the project's durable context layer (e.g. a `contexts/` tree with a map file, or a docs/ADR system). Read the entries relevant to the question. Sort what you find into: already answered (do not re-research), assumed but unverified, genuinely open.
2. **Refine**: restate the research question as the delta between what the user needs and what contexts already hold. Confirm scope with the user only if the delta is ambiguous; otherwise proceed.
3. **Fan out** (using `multi-agent-driven` patterns): parallel researchers with distinct angles — official docs, community and prior art, papers, code in the wild. Each returns raw, citable findings with source name and URL or path.
4. **Verify**: every claim that will drive a decision gets an adversarial pass — a separate check that tries to refute it or show it is stale. Mark key claims confirmed / plausible / refuted.
5. **Synthesize**: one report — answer first, then evidence, then open questions. Keep cited facts and your own judgment visibly separate.
6. **File back**: hand the durable part to `to-ctx`, which places it in the project's context system per its rules. The chat gets the summary plus the file path.

## Rules

- Never re-research what contexts already answer; cite the context file instead.
- Verification effort scales with decision impact, not with how interesting a claim is.
- Dependency direction: may use `multi-agent-driven`, `to-ctx`, and `handoff`; never invokes user-facing skills.
