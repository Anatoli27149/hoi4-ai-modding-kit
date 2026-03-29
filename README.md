# HOI4 AI Modding Kit

> 一个面向《钢铁雄心4》模组开发的 AI 工具链仓库。  
> A practical toolkit for building Hearts of Iron IV mods with AI.

---

## 这是什么

`HOI4 AI Modding Kit` 不是单纯的“提示词集合”，也不是一个只会读文件的 MCP。

它是一套面向 HOI4 模组开发的完整工作流，目标是让 AI 在做模组时更像一个靠谱的协作者，而不是偶尔吐出几段看起来像脚本的文本。

这个仓库把三层能力放到了一起：

- `VS Code + CWTools`
  负责编辑器内的语法、作用域、引用和部分本地化校验
- `hoi4-modding Skill`
  负责约束 AI 的工作方式，让它按 HOI4 的真实结构来生成、修改、检查内容
- `本地 MCP / CLI`
  负责做模组根目录识别、ID 盘点、缺失本地化检查、`error.log` 汇总

如果你的目标是：

- 用 AI 辅助做 HOI4 模组
- 降低 namespace、localisation、ID 冲突、配套文件遗漏这类错误
- 把自己的 HOI4 开发流程沉淀成长期可复用工具链

那这个仓库就是为这个场景准备的。

---

## 适合谁

- 想用 AI 辅助开发 HOI4 模组的中文用户
- 已经会写一些 focus、event、decision，但总是漏本地化或作用域检查的人
- 想把“AI + MCP + Skill”真正用于具体项目，而不是停留在概念层的人
- 想把自己的 HOI4 工作流做成可分享、可维护仓库的人

不太适合：

- 只想随便试一个 prompt，不需要本地工具链的人
- 不打算使用 Python / VS Code / 本地文件工作流的人

---

## 你能用它做什么

这个项目当前最适合解决下面这些高频问题：

- 找出哪个目录才是真正的 HOI4 mod 根目录
- 快速盘点 focus、event、decision、scripted 内容中的 ID 和 namespace
- 检查缺失 localisation
- 汇总 `error.log` 中最有价值的报错类别
- 让 AI 在改动时遵守“完整内容包”思路，而不是只改一个孤立片段

例如：

- 做一条新的德国工业线 focus，并连带补齐 localisation
- 为某个国家添加事件链，并检查 namespace 是否冲突
- 排查“脚本看着没错但游戏里不生效”的问题
- 先读 `error.log`，再决定该先修缺 loc、未知 effect，还是 scope 问题

---

## 为什么这套方案适合 HOI4

HOI4 模组开发里最常见的问题，不是“AI 不会写几行语法”，而是：

- 改了 focus，忘了补 `_desc`
- 写了 event，没处理 namespace
- 改了 decision，没补对应 localisation
- 逻辑块能写出来，但 scope 不对
- 报错很多时，不知道应该先修哪一类

所以更有效的方案不是只加大模型，也不是只接更多工具，而是把三件事同时做好：

1. 编辑器实时校验
2. AI 工作流约束
3. 本地结构化检查

这个仓库就是围绕这三个层面设计的。

---

## 三分钟上手

### 1. 安装 Python 包

```powershell
python -m pip install -e .
```

### 2. 对模组目录做基础检查

```powershell
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding inventory-ids "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding audit-localisation "D:\Games\HOI4\mod\my_mod"
```

### 3. 汇总错误日志

```powershell
python -m hoi4_ai_modding summarize-log "C:\Users\<you>\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
```

### 4. 如果你使用 Codex

运行：

```powershell
.\tools\install_codex_integration.ps1
```

然后把 MCP 配置注册到 Codex：

```toml
[mcp_servers.hoi4-modding]
command = "python"
args = ["-m", "hoi4_ai_modding.mcp_server"]
```

### 5. 如果你使用 VS Code

安装 `CWTools`：

```powershell
code --install-extension tboby.cwtools-vscode
```

---

## 推荐工作流

实际使用时，最稳的顺序通常是：

1. 先识别 mod 根目录
2. 先盘点结构和现有命名规则
3. 再让 AI 生成或修改内容
4. 改完以后立即跑 ID 审计和 localisation 审计
5. 出问题时先汇总 `error.log`
6. 再回去修逻辑、作用域或缺失资源

一句话概括：

`先看结构 -> 再改内容 -> 再做审计 -> 最后按日志修错`

---

## 仓库结构

```text
docs/                     项目文档、安装说明、语法速查
skills/hoi4-modding/      Codex Skill
src/hoi4_ai_modding/      Python 包，提供 CLI 和 MCP
tools/                    安装到 Codex 的便捷脚本
```

核心目录说明：

- `skills/hoi4-modding/`
  定义 AI 在 HOI4 任务里的工作方式
- `src/hoi4_ai_modding/core.py`
  放核心检测逻辑
- `src/hoi4_ai_modding/mcp_server.py`
  把本地检测能力包装成 MCP
- `docs/syntax-quick-reference.md`
  放实战向 HOI4 语法速查

---

## 常用命令

### 查找可能的模组根目录

```powershell
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
```

### 查看模组结构摘要

```powershell
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
```

### 盘点 ID / namespace

```powershell
python -m hoi4_ai_modding inventory-ids "D:\Games\HOI4\mod\my_mod"
```

### 检查缺失 localisation

```powershell
python -m hoi4_ai_modding audit-localisation "D:\Games\HOI4\mod\my_mod"
```

### 汇总 error.log

```powershell
python -m hoi4_ai_modding summarize-log "C:\Users\<you>\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
```

### 启动 MCP 服务

```powershell
python -m hoi4_ai_modding serve-mcp
```

---

## 和游戏原版文档的关系

这个仓库不是为了替代 HOI4 自带 documentation 文件。

如果你要查“当前游戏版本最完整的 trigger / effect 列表”，优先看游戏安装目录里的：

- `...\Hearts of Iron IV\documentation\triggers_documentation.html`
- `...\Hearts of Iron IV\documentation\effects_documentation.html`

本仓库更偏向：

- 高频实战语法
- 开发流程约束
- 项目结构检查
- AI 协作规范

也就是说，它解决的是“怎么更稳地做模组”，不是单纯提供一份 token 大字典。

---

## 文档导航

- [安装说明](./docs/setup.md)
- [项目规范](./docs/project-spec.md)
- [HOI4 语法速查](./docs/syntax-quick-reference.md)
- [中文说明页](./docs/README.zh-CN.md)

---

## 当前状态

项目目前是一个轻量但实用的起步版本，重点放在：

- 把 AI 协作流程做稳
- 把最有价值的本地检查能力做出来
- 让中文使用者可以快速看懂并开始使用

后续如果继续扩展，比较值得做的方向包括：

- 更强的 HOI4 内容类型识别
- 更细的资源引用检查
- 更完整的中文文档和示例模组
- 面向具体玩法类型的 skill 子模块

---

## English summary

This repository bundles a Codex skill, a local MCP server, and CLI tools for practical AI-assisted Hearts of Iron IV modding. It is designed to help users inspect mod structure, audit IDs and localisation, summarize `error.log`, and keep AI output aligned with real HOI4 project structure.
