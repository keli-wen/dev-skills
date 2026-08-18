# Install Dev Agent Skills

[中文版](./INSTALL.zh-CN.md)

Everything below installs `skills/`, the English pack. `skills-zh/` is its Chinese mirror, kept for reading rather than as a separate release; see [Reading the skills in Chinese](#reading-the-skills-in-chinese).

## Install as ordinary skills

This route works across agents supported by the `skills` CLI. Skills are installed without a plugin namespace, so you invoke `readout`, `handoff`, and the other skills by their own names.

### Project install

Install into the current project:

```bash
npx skills@latest add keli-wen/dev-skills
```

### Global install

Add `-g` to make the skills available across projects:

```bash
npx skills@latest add keli-wen/dev-skills -g
```

The installer can target a specific agent with `-a`, for example `-a codex`, `-a claude-code`, or `-a gemini-cli`.

## Install as a plugin

Plugin installation keeps the skills together under the `devai` namespace. For example, `handoff` appears as `devai:handoff`.

Codex:

```bash
codex plugin marketplace add keli-wen/dev-skills
codex plugin add devai@dev-skills
```

Claude Code:

```bash
claude plugin marketplace add keli-wen/dev-skills
claude plugin install devai@dev-skills
```

These are terminal commands. You do not need to start an interactive Codex or Claude Code session first.

## Reading the skills in Chinese

`skills-zh/` holds a Chinese mirror of every skill under the same names. It exists so Chinese-speaking users can read what each rule actually says; the agent itself does not need it. The English pack already mirrors the user's language when it replies, and it carries the Chinese-specific writing rules in `skills/readout/references/chinese.md`.

The mirror follows `skills/` and has no install path of its own. Nothing stops you from installing it, but the skill names collide with the English pack, so remove one before adding the other.
