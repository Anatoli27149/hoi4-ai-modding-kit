# HOI4 AI Modding Kit

A shareable project for building Hearts of Iron IV mods with AI in a disciplined way.

## 中文简介

这是一个面向《钢铁雄心4》模组开发的 AI 工作流仓库，目标不是“随便生成一点脚本”，而是把真正能长期使用的三层工具链放在一起：

- `VS Code + CWTools` 负责编辑器内的语法、作用域和引用校验
- `hoi4-modding` Skill 负责约束 AI 的工作方式，让它按完整内容包来改，而不是只吐零碎片段
- 本地 `MCP / CLI` 负责做模组根目录识别、ID 盘点、缺失本地化检查和 `error.log` 汇总

如果你的目标是“用 AI 更稳定地做 HOI4 模组”，而不是只试一两个 prompt，这个仓库就是给这个场景准备的。

This repository packages three layers together:

- A Codex skill for HOI4-focused planning, generation, review, and debugging.
- A lightweight local MCP server for mod-root discovery, ID inventory, localisation audits, and error-log summaries.
- Project docs and CLI tools so the workflow is usable even outside Codex.

## Why this exists

For HOI4 modding, the highest-value AI setup is usually not "just use a model" and not "just use an MCP."
The practical stack is:

- `VS Code + CWTools` for editor-time syntax and scope validation.
- A focused `hoi4-modding` skill for consistent generation and review behavior.
- A small local MCP/CLI layer for structure checks, localisation coverage, and log-driven debugging.

That is the stack this repository implements.

## Repository layout

```text
docs/                     Project docs, setup, syntax reference, and workflow spec
skills/hoi4-modding/      Codex skill bundle
src/hoi4_ai_modding/      Python package for MCP and CLI tooling
tools/                    Convenience installer scripts
```

## Quick start

1. Install the package in editable mode:

```powershell
python -m pip install -e .
```

2. Use the CLI against a mod:

```powershell
hoi4-find-mod-roots "D:\Games\HOI4\mod"
hoi4-inspect-mod "D:\Games\HOI4\mod\my_mod"
hoi4-inventory-ids "D:\Games\HOI4\mod\my_mod"
hoi4-audit-localisation "D:\Games\HOI4\mod\my_mod"
hoi4-summarize-log "C:\Users\<you>\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
```

If the installed script directory is not on `PATH`, use the module entry instead:

```powershell
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
```

3. If you use Codex, install the skill and MCP integration:

```powershell
.\tools\install_codex_integration.ps1
```

4. In VS Code, install `tboby.cwtools-vscode`.

## 中文快速开始

1. 安装 Python 包：

```powershell
python -m pip install -e .
```

2. 对模组目录做结构检查：

```powershell
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding inventory-ids "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding audit-localisation "D:\Games\HOI4\mod\my_mod"
```

3. 如果你在用 Codex，把 `skills/hoi4-modding/` 安装进本地技能目录，并注册 MCP。

4. 在 VS Code 里安装 `CWTools`，让编辑器即时提示脚本问题。

## Codex MCP config

Add this server block to your Codex config if the installer did not do it for you:

```toml
[mcp_servers.hoi4-modding]
command = "python"
args = ["-m", "hoi4_ai_modding.mcp_server"]
```

## Recommended workflow

1. Use the skill to inspect the mod before editing.
2. Generate or revise content in full bundles, not isolated snippets.
3. Run ID inventory and localisation audit after every meaningful change.
4. Use `error.log` summaries to drive debugging instead of guessing.
5. Let CWTools catch syntax and scope issues while editing.

## Docs

- [Setup](./docs/setup.md)
- [Project Spec](./docs/project-spec.md)
- [Syntax Quick Reference](./docs/syntax-quick-reference.md)
- [中文说明](./docs/README.zh-CN.md)

## Status

This project is intentionally lightweight. It does not try to replace CWTools or the game's own documentation pages. It aims to make AI-assisted HOI4 modding more reliable and repeatable.
