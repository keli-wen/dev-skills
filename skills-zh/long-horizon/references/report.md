# 报告模板与数据契约

`report.html` 由 `assets/report-template.html` 生成。模板是固定的，一次运行只往里写数据。

## 三个块，三个负责方

| 块 | 谁写 | 什么时候 |
|---|---|---|
| `<script id="lh-icons">` | skill 本身 | 运行期间从不改 |
| `<script id="lh-labels">` | 编排者 | 开工时写一次 |
| `<script id="lh-data">` | 编排者 | 每翻一位、每个 session 结束时 |

- **开工时**：把模板复制成 `.long-horizon/<goal-slug>/report.html`。session 语言和模板语言不同时，把 `lh-labels` 重写一次：键不变，只翻译值，并设好 `lang`。`status.*` 要短（中文 6 个字以内，英文 16 个字母左右）：它放在固定大小的图节点里。然后用真实目标替换示例 `lh-data`，再检查版面（见下文）。
- **每次刷新**：只重写 `lh-data`，别的都不动。运行期间不改标记、样式、脚本和图标。看板缺什么，用 `custom_panels` 补；模板本身的改进回到 skill 里做。
- **单向生成**：`lh-data` 里的一切必须已经存在于状态文件（`goal.md`、`ledger.json`、`log.md`、`next.md`、`events.jsonl`）。报告是视图，不是事实源。

刷新脚本（把 `data.json` 写进数据块）：

```bash
python3 - .long-horizon/<goal-slug> <<'PY'
import json, re, sys, pathlib
ws = pathlib.Path(sys.argv[1]); html = (ws / "report.html").read_text()
data = json.dumps(json.loads((ws / "data.json").read_text()), ensure_ascii=False).replace("</", "<\\/")
html, n = re.subn(r'(<script id="lh-data" type="application/json">).*?(</script>)', lambda m: m.group(1) + data + m.group(2), html, flags=re.S)
assert n == 1; (ws / "report.html").write_text(html)
PY
```

## `lh-data` 结构

```jsonc
{
  "schema": "long-horizon/report@1",
  "goal": { "slug", "title", "statement", "phase": "draft|running|review|stopped", "sessions", "updated", "repo"?, "base"? },
  "groups": [ { "id", "label", "hint"?, "color"?, "icon"? } ],          // 泳道；icon 取值见下
  "done_when": [ { "id", "text", "check", "items": ["<台账 id>"], "passes"? } ],
  "non_goals": [ "..." ], "invariants": [ "..." ],
  "envelope": { "allowed": [ "..." ], "forbidden": [ "..." ] },
  "verification": { "orchestrator": "...", "verifier": "..." },
  "open_questions": [ { "id", "text", "recommend", "blocks": ["<台账 id>"], "asking"? } ],   // 只在 spec 阶段
  "ledger": [ {
    "id", "title", "desc", "verify", "passes", "evidence": [ "..." ], "deps": [ "..." ], "discovered-from",
    "group"?, "status"?: "in-flight|blocked|failed", "question"?, "attempts"?, "human"?, "issue"?, "pr"?, "est"?
  } ],
  "decisions": [ { "when", "text" } ],
  "log": [ { "when", "kind": "dispatch|verify|fail|blocked|session|spec", "text" } ],   // 新的在前，保持简短
  "theme": { "accent"? },
  "custom_panels": [ { "title", "kind": "kv|list|text", "items"?, "text"? } ]
}
```

- `ledger` 的行与 `ledger.json` 一一对应；可选字段也存在 `ledger.json` 里，报告才仍然只是视图。
- `status` 只用来表达 `passes` 表达不了的状态。只是在等依赖的条目不要写。
- 有 `question` 的条目表示需要人来决定，会出现在「需要你处理」里。
- `human: true` 表示人工步骤，比如「合并 PR #241」。依赖全部通过后它才算「需要你」，在那之前只是在等。

## 模板自己算的（不要写进数据）

可开始的条目（依赖全部通过）、关键路径（未完成条目上最长的链，按 `est` 加权，缺省为 1）、卡点（挡住最多未完成后继的未完成条目）、计数、完成条件进度、地平线刻度。

## 检查版面

`scripts/check-report.py` 用 headless Chrome 在 375px 和 1440px 下打开报告，逐个切换 tab、逐条打开详情抽屉，列出被截断的文案、折行的行、溢出盒子的内容和会横向滚动的页面。只需要 Chrome 或 Chromium（找不到时设 `CHROME` 指向它）。

- **开工时**，写完 `lh-labels` 后跑：`python3 -I scripts/check-report.py .long-horizon/<goal-slug>/report.html`。它点名的文案改短。
- **改模板之后、发布之前**跑：`python3 -I scripts/check-report.py --stress`。它用最坏情况填满模板的示例数据（一个条目带全部三个标签、很长的泳道名、ISO 时间、很长的标题、啰嗦的英文文案），必须全部通过。

在浏览器里打开 `report.html?lint`，页面顶部会显示同一份清单。

## 图标

`groups[].icon` 可选：`prep`、`visual`、`copy`、`engine`、`usage`、`wrap`。收件箱用 `spec`、`decide`、`act`、`retry`，品牌标志是 `horizon`。节点上的标签（瓶颈、人工、新发现）是图标，任何语言下宽度都一样；它们的名字在悬停提示、图例和详情抽屉里。图标是手绘蒙版：墨线跟随文字色，色块取泳道色或状态色，深浅主题都能用。
