# 安装 Rondo

[English version](./INSTALL.md)

下面所有命令装的都是英文包 `skills/`。`skills-zh/` 是它的中文镜像，用来阅读，不作为单独的发行版，见[用中文读这些 skill](#用中文读这些-skill)。

## 安装为普通 skills

这种方式适用于 `skills` CLI 支持的各种 agent。安装后没有 plugin 命名空间，直接使用 `readout`、`handoff` 等名称。

### 安装到当前项目

```bash
npx skills@latest add keli-wen/rondo
```

### 全局安装

加上 `-g`，让这些 skill 在所有项目中可用：

```bash
npx skills@latest add keli-wen/rondo -g
```

如果只想安装给某个 agent，可以使用 `-a`，例如 `-a codex`、`-a claude-code` 或 `-a gemini-cli`。

## 安装为 plugin

Plugin 会把整套 skills 放在 `rondo` 命名空间下。例如，`/long-horizon` 变成 `/rondo:long-horizon`，`/handoff` 变成 `/rondo:handoff`。

Codex：

```bash
codex plugin marketplace add keli-wen/rondo
codex plugin add rondo@rondo
```

Claude Code：

```bash
claude plugin marketplace add keli-wen/rondo
claude plugin install rondo@rondo
```

这些都是普通终端命令，不必先进入 Codex 或 Claude Code 的交互会话。

## 从 devai 迁移

Rondo 替换了 `devai` 插件命名空间与 `dev-skills` marketplace 名称。这是新的插件身份，已有安装不会自动变成 `rondo@rondo`。Skill 名称与行为保持不变；请把保存的 `/devai:long-horizon` 等插件调用改成 `/rondo:long-horizon`。

迁移时，用新插件和 marketplace 替换旧安装。以下示例使用默认的 user scope；如果 Claude Code 原来装在 project 或 local scope，请在卸载和安装两个插件命令中都加上对应的 `--scope project` 或 `--scope local`。

Codex：

```bash
codex plugin remove devai@dev-skills
codex plugin marketplace remove dev-skills
codex plugin marketplace add keli-wen/rondo
codex plugin add rondo@rondo
```

Claude Code：

```bash
claude plugin uninstall devai@dev-skills
claude plugin marketplace remove dev-skills
claude plugin marketplace add keli-wen/rondo
claude plugin install rondo@rondo
```

通过 `npx skills` 安装普通 skill 的用户继续使用 `/long-horizon`、`/handoff` 等无命名空间的名称。后续安装改用 `keli-wen/rondo`；skill 目录名称不变。

命令细节见 [Codex 插件参考](https://learn.chatgpt.com/docs/developer-commands#codex-plugin)、[Codex marketplace 指南](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)与 [Claude Code 插件参考](https://code.claude.com/docs/en/plugins/cli-reference)。

## 用中文读这些 skill

`skills-zh/` 里是每个 skill 的中文镜像，名称一一对应。它的用途是让中文用户读懂每条规则在讲什么；agent 本身并不需要它。英文包在回复时本来就跟随用户的语言，中文特有的写作规则也在英文包里，位置是 `skills/readout/references/chinese.md`。

镜像跟着 `skills/` 走，没有专属的安装路径。要装也拦不住，但它和英文包的 skill 重名，装另一个之前先把这一个移除。
