# 安装 Dev Agent Skills

[English version](./INSTALL.md)

下面所有命令装的都是英文包 `skills/`。`skills-zh/` 是它的中文镜像，用来阅读，不作为单独的发行版，见[用中文读这些 skill](#用中文读这些-skill)。

## 安装为普通 skills

这种方式适用于 `skills` CLI 支持的各种 agent。安装后没有 plugin 命名空间，直接使用 `readout`、`handoff` 等名称。

### 安装到当前项目

```bash
npx skills@latest add keli-wen/dev-skills
```

### 全局安装

加上 `-g`，让这些 skill 在所有项目中可用：

```bash
npx skills@latest add keli-wen/dev-skills -g
```

如果只想安装给某个 agent，可以使用 `-a`，例如 `-a codex`、`-a claude-code` 或 `-a gemini-cli`。

## 安装为 plugin

Plugin 会把整套 skills 放在 `devai` 命名空间下。例如，`handoff` 会显示为 `devai:handoff`。

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

## 用中文读这些 skill

`skills-zh/` 里是每个 skill 的中文镜像，名称一一对应。它的用途是让中文用户读懂每条规则在讲什么；agent 本身并不需要它。英文包在回复时本来就跟随用户的语言，中文特有的写作规则也在英文包里，位置是 `skills/readout/references/chinese.md`。

镜像跟着 `skills/` 走，没有专属的安装路径。要装也拦不住，但它和英文包的 skill 重名，装另一个之前先把这一个移除。
