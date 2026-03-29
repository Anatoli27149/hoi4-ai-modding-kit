# HOI4 AI Modding Kit 中文说明

## 这是什么

这是一个把 `Skill + MCP + CLI + 文档` 打包在一起的 HOI4 AI 模组开发仓库。

它解决的不是“AI 会不会写一点 HOI4 代码”，而是下面这些更实际的问题：

- 如何先识别真正的模组根目录
- 如何在改完 focus、event、decision 之后顺手查 ID 冲突
- 如何检查缺失 localisation
- 如何把 `error.log` 里的重复报错先归类，再决定先修什么
- 如何让 AI 遵守一个稳定的工作流程，而不是每次随意发挥

## 仓库里有什么

- `skills/hoi4-modding/`
  面向 Codex 的 Skill，负责告诉 AI 应该怎样完成 HOI4 模组任务。
- `src/hoi4_ai_modding/`
  Python 包，既可以当命令行工具用，也可以作为 MCP 服务使用。
- `docs/`
  项目说明、安装文档、语法速查表。
- `tools/install_codex_integration.ps1`
  Windows 下把 Skill 安装到 Codex 目录的便捷脚本。

## 最适合谁

- 想用 AI 辅助做 HOI4 模组的人
- 已经会写一点模组，但总漏 localisation、namespace、配套文件的人
- 想把自己的 HOI4 开发流程沉淀成可复用工具链的人

## 推荐使用方式

1. 在 VS Code 安装 `CWTools`
2. 用本仓库的 CLI 或 MCP 先检查模组结构
3. 再让 AI 去做具体功能
4. 每次改完都跑一次 ID 和 localisation 审计
5. 出问题时先看 `error.log` 汇总，而不是直接猜

## 最常用命令

```powershell
python -m pip install -e .
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding inventory-ids "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding audit-localisation "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding summarize-log "C:\Users\<you>\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
```

## 关于“完整语法”

本仓库提供的是高频、实战向速查，而不是替代游戏本体自带文档。

如果你要查当前游戏版本最完整的 trigger / effect 列表，优先看游戏安装目录里的：

- `documentation/triggers_documentation.html`
- `documentation/effects_documentation.html`

因为百科页面和社区资料可能会滞后于你当前版本。
