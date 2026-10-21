# Install Rondo

[中文版](./INSTALL.zh-CN.md)

Everything below installs `skills/`, the English pack. `skills-zh/` is its Chinese mirror, kept for reading rather than as a separate release; see [Reading the skills in Chinese](#reading-the-skills-in-chinese).

## Install as ordinary skills

This route works across agents supported by the `skills` CLI. Skills are installed without a plugin namespace, so you invoke `readout`, `handoff`, and the other skills by their own names.

### Project install

Install into the current project:

```bash
npx skills@latest add keli-wen/rondo
```

### Global install

Add `-g` to make the skills available across projects:

```bash
npx skills@latest add keli-wen/rondo -g
```

The installer can target a specific agent with `-a`, for example `-a codex`, `-a claude-code`, or `-a gemini-cli`.

## Install as a plugin

Plugin installation keeps the skills together under the `rondo` namespace. For example, `/long-horizon` becomes `/rondo:long-horizon` and `/handoff` becomes `/rondo:handoff`.

Codex:

```bash
codex plugin marketplace add keli-wen/rondo
codex plugin add rondo@rondo
```

Claude Code:

```bash
claude plugin marketplace add keli-wen/rondo
claude plugin install rondo@rondo
```

These are terminal commands. You do not need to start an interactive Codex or Claude Code session first.

## Migrating from devai

Rondo replaces the `devai` plugin namespace and the `dev-skills` marketplace name. It is a new plugin identity, so an existing installation does not automatically become `rondo@rondo`. Skill names and behavior stay the same; update saved plugin invocations such as `/devai:long-horizon` to `/rondo:long-horizon`.

To migrate, replace the old plugin and marketplace with the new ones. These examples use the default user scope; for a Claude Code project or local installation, add the matching `--scope project` or `--scope local` to both plugin commands.

Codex:

```bash
codex plugin remove devai@dev-skills
codex plugin marketplace remove dev-skills
codex plugin marketplace add keli-wen/rondo
codex plugin add rondo@rondo
```

Claude Code:

```bash
claude plugin uninstall devai@dev-skills
claude plugin marketplace remove dev-skills
claude plugin marketplace add keli-wen/rondo
claude plugin install rondo@rondo
```

If you installed ordinary skills with `npx skills`, keep using `/long-horizon`, `/handoff`, and the other unnamespaced names. Use `keli-wen/rondo` for future installs; the skill directories keep their existing names.

For command details, see the [Codex plugin reference](https://learn.chatgpt.com/docs/developer-commands#codex-plugin), [Codex marketplace guide](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli), and [Claude Code plugin reference](https://code.claude.com/docs/en/plugins/cli-reference).

## Reading the skills in Chinese

`skills-zh/` holds a Chinese mirror of every skill under the same names. It exists so Chinese-speaking users can read what each rule actually says; the agent itself does not need it. The English pack already mirrors the user's language when it replies, and it carries the Chinese-specific writing rules in `skills/readout/references/chinese.md`.

The mirror follows `skills/` and has no install path of its own. Nothing stops you from installing it, but the skill names collide with the English pack, so remove one before adding the other.
