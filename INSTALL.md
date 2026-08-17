# Install Dev Agent Skills

[中文版](./INSTALL.zh-CN.md)

Dev Agent Skills ships two deliberately separate language packs:

| Pack | Source | Best for |
|---|---|---|
| English | `skills/` | Users who normally work with their agent in English |
| Chinese | `skills-zh/` | Users who normally work with their agent in Chinese, including the Chinese-specific `readout` rules |

Both packs use the same skill names. Install one pack, not both.

## Install as ordinary skills

This route works across agents supported by the `skills` CLI. Skills are installed without a plugin namespace, so you invoke `readout`, `handoff`, and the other skills by their own names.

### Project install

Install the English pack into the current project:

```bash
npx skills@latest add keli-wen/dev-skills
```

Install the Chinese pack into the current project:

```bash
npx skills@latest add https://github.com/keli-wen/dev-skills/tree/master/skills-zh
```

### Global install

Add `-g` to make the selected pack available across projects:

```bash
# English
npx skills@latest add keli-wen/dev-skills -g

# Chinese
npx skills@latest add https://github.com/keli-wen/dev-skills/tree/master/skills-zh -g
```

The installer can target a specific agent with `-a`, for example `-a codex` or `-a claude-code`.

## Install as a plugin

Plugin installation keeps the skills together under the `devai` namespace. For example, `handoff` appears as `devai:handoff`.

### English plugin

The English plugin is available today from the `dev-skills` marketplace.

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

### Chinese plugin

The Chinese plugin is published from the `zh` branch of the same repository. Its marketplace is named `dev-skills-zh`, while the plugin remains `devai`.

```bash
# Codex
codex plugin marketplace add keli-wen/dev-skills --ref zh
codex plugin add devai@dev-skills-zh

# Claude Code
claude plugin marketplace add keli-wen/dev-skills@zh
claude plugin install devai@dev-skills-zh
```

## Switching languages

The English and Chinese packs intentionally reuse the same skill and plugin names. Remove the installed pack before installing the other language so two definitions do not compete for the same name.

The language suffix belongs to the distribution source, not the plugin identity:

- English: `devai@dev-skills`
- Chinese, published from the `zh` branch: `devai@dev-skills-zh`

Both plugin distributions expose the `devai` namespace.
