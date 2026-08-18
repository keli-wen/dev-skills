# readout: writing in Chinese

Read this when the reply is in Chinese. It continues the numbering in `SKILL.md`, and every rule there still applies. Each rule below names a defect that only exists in Chinese, which is why none of them has a counterpart in the main list.

11. **Keep the action in the verb, not in a noun.** Chinese does this with 进行 / 作出 / 实现 / 开展 plus an abstract noun. Write 「深入分析了性能瓶颈」, not 「对性能瓶颈进行了深入的分析」. Once the action moves into the object, the verb slot holds an empty shell: the reader steps over it, then has to go back and pick the action up.

12. **A four-character set phrase has to be replaceable by something concrete.** The phrases themselves are fine — 「一目了然」 costs the reader less than talking around it. What fails is stacking several in parallel so that rhythm stands in for content. 「全面梳理了相关代码，深入分析了潜在问题，系统性地完成了重构」 sounds thorough and leaves the reader unable to name one file you touched. Try replacing each phrase with a statement that can be checked; delete the ones that will not convert.

13. **Keep technical terms in the original, say everything else in Chinese.** In 「这个 feature 的 performance 有 regression」, all three English words have exact Chinese equivalents, and the reader pays once per switch. Keep the original only for terms with no settled Chinese translation, and put those in backticks — `prefix caching`.

14. **Don't queue modifiers in front of the noun.** A Chinese modifier can only sit before what it modifies, so an English chain of relative clauses carried over intact forces the reader to hold the whole string until the head noun finally arrives. 「一个由多位来自不同背景、经过反复讨论后被最终确定下来的方案」 unpacks into 「这个方案是几位背景不同的人反复讨论后定下来的」.

15. **Say it out loud — rule 10, in its Chinese form.** Chinese over-compression takes two fixed shapes: two-syllable words cut to one (「验证」 written as 「验」, 「复现」 as 「现」), and dropped structural particles (「塞得太满」 written as 「塞太满」). Modern Chinese leans on the second syllable to disambiguate, so a bare 「验」 could be 验证, 检验, or 经验, and the reader has to restore the full word before reading on. You saved two characters and cost them a step.

## Calibration

Same content, three registers. Only the third is a readout.

- ❌ **Packed**: 「已完成对重试机制的全面排查，定位到指数退避的实现在并发压力下未能遵守配置的上限，该问题表现为 #412 中反馈的间歇性超时，并提示修复位置应位于调度器而非客户端。」
- ❌ **Fragmented**: 「重试机制——已排查。退避：高负载下有问题。上限没生效。相关：#412。修复位置：调度器（大概）。」
- ✅ **Readout**: 「#412 里的重试 bug 是真的，问题在调度器，不在客户端。并发压力下，指数退避没有遵守你配置的上限，重试堆积起来，请求就超时了。我用 20 个并发请求复现了。单线程下会不会走到同一条路径，我还没验证。」
