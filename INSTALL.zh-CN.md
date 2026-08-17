# 安装 Dev Agent Skills

[English version](./INSTALL.md)

Dev Agent Skills 提供两个刻意分开维护的语言包：

| 语言包 | 来源 | 适合谁 |
|---|---|---|
| 中文版 | `skills-zh/` | 平时主要用中文与 agent 协作，并需要中文专属 `readout` 规则的用户 |
| 英文版 | `skills/` | 平时主要用英文与 agent 协作的用户 |

两个版本使用相同的 skill 名称。请选择一个版本安装，不要同时安装。

## 安装为普通 skills

这种方式适用于 `skills` CLI 支持的各种 agent。安装后没有 plugin 命名空间，直接使用 `readout`、`handoff` 等名称。

### 安装到当前项目

安装中文版：

```bash
npx skills@latest add https://github.com/keli-wen/dev-skills/tree/master/skills-zh
```

安装英文版：

```bash
npx skills@latest add keli-wen/dev-skills
```

### 全局安装

加上 `-g`，可以让所选语言包在所有项目中可用：

```bash
# 中文版
npx skills@latest add https://github.com/keli-wen/dev-skills/tree/master/skills-zh -g

# 英文版
npx skills@latest add keli-wen/dev-skills -g
```

如果只想安装给某个 agent，可以使用 `-a`，例如 `-a codex` 或 `-a claude-code`。

## 安装为 plugin

Plugin 会把整套 skills 放在 `devai` 命名空间下。例如，`handoff` 会显示为 `devai:handoff`。

### 英文 plugin

目前已经发布的 `dev-skills` marketplace 安装的是英文版。

Codex：

```bash
codex plugin marketplace add keli-wen/dev-skills
codex plugin add devai@dev-skills
```

Claude Code：

```bash
claude plugin marketplace add keli-wen/dev-skills
claude plugin install devai@dev-skills
```

这些都是普通终端命令，不必先进入 Codex 或 Claude Code 的交互会话。

### 中文 plugin

中文 plugin 从同一个仓库的 `zh` 分支发布。它的 marketplace 名为 `dev-skills-zh`，plugin 名仍然是 `devai`。

```bash
# Codex
codex plugin marketplace add keli-wen/dev-skills --ref zh
codex plugin add devai@dev-skills-zh

# Claude Code
claude plugin marketplace add keli-wen/dev-skills@zh
claude plugin install devai@dev-skills-zh
```

## 切换语言

中英文版本刻意复用相同的 skill 与 plugin 名称。切换语言前，应先移除已经安装的版本，避免两个定义争用同一个名称。

语言后缀属于发行源，不属于 plugin 身份：

- 英文版：`devai@dev-skills`
- 中文版，从 `zh` 分支发布：`devai@dev-skills-zh`

两种 plugin 发行版最终都使用 `devai` 命名空间。
