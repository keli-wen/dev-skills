---
name: to-ctx
description: Turn the current conversation's conclusions into a well-formed context document filed in the project's context system. Use for /to-ctx, "file this into contexts", "turn this conclusion into a context doc". Finds the placement rules (e.g. CONTEXT_MAP.md), writes in the project's house style, and reports the path.
metadata:
  short-description: File conclusions into the context system
---

# to-ctx

Take what this session has settled — a decision, a research result, a design, an investigation log — and turn it into a durable context file in the right place, so no future session has to rediscover it.

**Language**: context files are written in the project's documentation language (check neighboring files), which is not necessarily the conversation's language. Chat replies mirror the user.

## Steps

1. **Locate the context system**: find the project's durable layer and its placement rules — a map file (e.g. `contexts/CONTEXT_MAP.md`), a docs/ADR convention, or directory READMEs. If the project has its own context-management skill, defer to its rules and use this skill only as the entry point. If no context system exists, propose ONE location to the user before creating anything.
2. **Select what is durable**: keep decisions and their reasons, verified facts with sources, discovered constraints, and open questions. Drop process noise — exploration dead ends, tool logs, interim misunderstandings. If part of the content is already persisted (an issue, PR, or another context doc), reference it; never duplicate it.
3. **Match the house style**: read one or two neighboring context files first, then mirror their structure, headings, naming and dating conventions.
4. **Place and write** the file per the rules; run the map file's placement check before writing, not after.
5. **Report**: the chat gets a one-line summary, the file path, and where it sits in the map. If the map file itself must register the new doc, update it in the same change.

## Rules

- One fact, one home: never create a second source of truth for something already documented — update or reference the existing doc instead.
- The repo's own placement rules always win over this skill's defaults.
- Do not commit or push; filing the doc is the deliverable, version control stays with the user's workflow.
