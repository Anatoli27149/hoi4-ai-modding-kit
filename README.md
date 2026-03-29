# HOI4 AI Modding Kit

> 给做《钢铁雄心4》模组的人准备的一套 AI 工具链。  
> A practical toolkit for building Hearts of Iron IV mods with AI.

---

## 这仓库是干嘛的

这个仓库是我把一套比较顺手的 HOI4 AI 开发流程整理出来后的结果。

它不是单独的 prompt 仓库，也不是只放一个 MCP 服务，而是把平时真会用到的几样东西放到一起：

- `VS Code + CWTools`
  编辑器里先把语法、作用域、引用这类基础问题拦下来
- `hoi4-modding Skill`
  让 AI 按 HOI4 模组的真实结构去干活，不要东改一点西补一点
- `本地 MCP / CLI`
  用来查 mod 根目录、盘点 ID、找缺失本地化、汇总 `error.log`

如果你平时会遇到这些情况：

- AI 能写点脚本，但经常漏 localisation
- event 能跑起来，但 namespace 和配套文件容易乱
- 改完东西以后，不知道先查哪里最值
- 想把自己常用的 HOI4 工作流固定下来

那这仓库应该能帮上忙。

---

## 适合什么人用

- 想用 AI 辅助开发 HOI4 模组的中文用户
- 已经会写一些 focus、event、decision，但老是漏本地化、scope 或配套文件的人
- 想把 `AI + MCP + Skill` 真正用到具体项目里的人
- 想把自己那套 HOI4 开发流程做成一个可维护仓库的人

不太适合：

- 只想临时问 AI 一两个问题，不想搭本地工具链的人
- 完全不打算碰 Python、VS Code、本地文件工作流的人

---

## 你能用它做什么

当前这套东西最适合处理下面这些高频问题：

- 找出哪个目录才是真正的 HOI4 mod 根目录
- 快速盘点 focus、event、decision、scripted 内容中的 ID 和 namespace
- 检查缺失 localisation
- 汇总 `error.log` 中最有价值的报错类别
- 让 AI 在改动时遵守“完整内容包”思路，而不是只改一个孤立片段
- 把“创建国家、创建州、分配工厂、生成州预览图”这类大块任务拆成稳定流程

例如：

- 做一条新的德国工业线 focus，并连带补齐 localisation
- 为某个国家添加事件链，并检查 namespace 是否冲突
- 排查“脚本看着没错但游戏里不生效”的问题
- 先读 `error.log`，再决定该先修缺 loc、未知 effect，还是 scope 问题

---

## 为什么是这套组合

HOI4 模组里最烦的通常不是“不会写”，而是“看着像写对了，其实还差半截”。

最常见的坑基本就是这些：

- 改了 focus，忘了补 `_desc`
- 写了 event，没处理 namespace
- 改了 decision，没补对应 localisation
- 逻辑块能写出来，但 scope 不对
- 报错很多时，不知道应该先修哪一类

所以我最后收敛出来的做法不是“换更强的模型”，也不是“疯狂接工具”，而是把三件事一起做好：

1. 编辑器实时校验
2. AI 工作流约束
3. 本地结构化检查

这个仓库基本就是围着这三件事搭的。

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

先运行：

```powershell
.\tools\install_codex_integration.ps1
```

然后把这个 MCP 配置加到 Codex：

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

## 我更推荐的使用顺序

直接说人话版就是：

1. 先识别 mod 根目录
2. 先盘点结构和现有命名规则
3. 再让 AI 生成或修改内容
4. 改完以后立即跑 ID 审计和 localisation 审计
5. 出问题时先汇总 `error.log`
6. 再回去修逻辑、作用域或缺失资源

别一上来就让 AI “给我写一整套事件链”。  
先让它看清楚你这个 mod 的结构，再动手，成功率会高很多。

---

## 仓库结构

```text
docs/                     项目文档、安装说明、语法速查、任务公式
skills/hoi4-modding/      Codex Skill
src/hoi4_ai_modding/      Python 包，提供 CLI 和 MCP
tools/                    安装到 Codex 的便捷脚本
```

平时最常看的几个地方：

- `skills/hoi4-modding/`
  Skill 本体，决定 AI 应该怎么做 HOI4 相关任务
- `src/hoi4_ai_modding/core.py`
  核心检测逻辑都在这
- `src/hoi4_ai_modding/mcp_server.py`
  MCP 入口
- `docs/syntax-quick-reference.md`
  常用语法速查
- `docs/hoi4-country-state-formulas.md`
  国家、州、地图和建筑分配的细化公式
- `docs/index.html`
  可直接拿去做 GitHub Pages 首页的中文落地页

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

## 和游戏自带 documentation 的关系

这个仓库不是拿来替代 HOI4 原版文档的。

如果你要查“当前游戏版本最完整的 trigger / effect 列表”，优先看游戏安装目录里的：

- `...\Hearts of Iron IV\documentation\triggers_documentation.html`
- `...\Hearts of Iron IV\documentation\effects_documentation.html`

这个仓库更偏向做这些事：

- 高频实战语法
- 开发流程约束
- 项目结构检查
- AI 协作规范

说白了，它解决的是“怎么更稳地做模组”，不是给你扔一大份 token 清单。

---

## 文档导航

- [安装说明](./docs/setup.md)
- [项目规范](./docs/project-spec.md)
- [HOI4 语法速查](./docs/syntax-quick-reference.md)
- [国家 / 州 / 地图 / 工厂公式](./docs/hoi4-country-state-formulas.md)
- [网站首页](./docs/index.html)
- [中文说明页](./docs/README.zh-CN.md)

---

## 现在做到哪了

当前版本还是偏轻量，但已经够拿来真正干活了，重点放在：

- 把 AI 协作流程做稳
- 把最有价值的本地检查能力做出来
- 让中文使用者可以快速看懂并开始使用
- 把国家、州、地图和建筑这类高频重活补成可复用的公式文档

后面如果继续往下做，比较值得补的方向有：

- 更强的 HOI4 内容类型识别
- 更细的资源引用检查
- 更完整的中文文档和示例模组
- 面向具体玩法类型的 skill 子模块

---

## English summary

This repository bundles a Codex skill, a local MCP server, and CLI tools for practical AI-assisted Hearts of Iron IV modding. It is designed to help users inspect mod structure, audit IDs and localisation, summarize `error.log`, and keep AI output aligned with real HOI4 project structure.
