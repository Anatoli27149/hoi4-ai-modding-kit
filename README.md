# HOI4 AI Modding Kit

> 给做《钢铁雄心4》模组的人准备的一套 AI 工具链。  
> A practical toolkit for building Hearts of Iron IV mods with AI.

[网站首页](https://anatoli27149.github.io/hoi4-ai-modding-kit/) | [安装说明](./docs/setup.md) | [语法速查](./docs/syntax-quick-reference.md) | [国家 / 州 / 地图 / 工厂公式](./docs/hoi4-country-state-formulas.md)

---

## 先说人话

这个仓库不是“给 AI 几句 prompt 就开干”的那种东西。

它更像一套专门给 HOI4 模组准备的工作流：

- 用 `Skill` 约束 AI 怎么干活
- 用 `MCP / CLI` 处理查结构、查日志、查缺失这类机械活
- 用 `CWTools + 文档` 把语法、作用域、配套文件这些高频坑提前拦下来

如果你经常遇到下面这些情况，这仓库基本就是给你准备的：

- AI 能写一点，但老是漏 localisation
- event 能跑，结果 namespace、scope 或配套文件乱了
- 改完一堆内容，不知道先查哪里最值
- 想把自己那套 HOI4 开发流程沉淀下来，而不是每次都从头摸

---

## 30 秒判断适不适合你

### 适合

- 想用 AI 辅助做 HOI4 模组，而且不想每次都被低级错误绊住
- 已经会写一些 `focus`、`event`、`decision`，但总是漏本地化、scope 或配套文件
- 想把 `AI + MCP + Skill + 编辑器校验` 真正连成一套工作流
- 想做国家、州、地图、工厂分配这类更重的内容，而不是只写零碎脚本

### 不太适合

- 只想临时问 AI 一两个语法问题，不想搭本地工具链
- 完全不打算碰 Python、VS Code、本地文件工作流
- 想靠一个 prompt 直接包办所有复杂模组开发，不愿意做任何校验

---

## 这个仓库到底有什么

| 组件 | 在哪 | 干什么 |
| --- | --- | --- |
| `hoi4-modding Skill` | `skills/hoi4-modding/` | 规定 AI 做 HOI4 任务时该怎么读文件、怎么生成内容包、怎么做校验 |
| `MCP / CLI` | `src/hoi4_ai_modding/` | 查 mod 根目录、盘点 ID、找缺失 localisation、汇总 `error.log` |
| `中文文档` | `docs/` | 让中文使用者能快速看懂怎么装、怎么用、该按什么顺序做 |
| `GitHub Pages 首页` | `docs/index.html` | 给第一次进仓库的人一个更好读的入口 |
| `Codex 安装脚本` | `tools/install_codex_integration.ps1` | 快速把这套东西接到 Codex 里 |

---

## 它最适合解决什么问题

- 找出哪个目录才是真正的 HOI4 mod 根目录
- 快速盘点 `focus`、`event`、`decision`、`scripted_*` 里的 ID 和 namespace
- 检查缺失 localisation
- 汇总 `error.log` 里最值得先处理的问题
- 让 AI 按“完整内容包”去改文件，而不是只改一段孤立代码
- 把“创建国家、创建州、分配工厂、生成州预览图”这类重活拆成稳定流程

典型场景：

- 做一条新的德国工业线 `focus`，顺手把 localisation 补齐
- 给某个国家加一整条事件链，并检查 namespace 冲突
- 排查“脚本看着没错，但游戏里不生效”
- 在改国家、州和地图前，先按公式把结构理顺

---

## 为什么不是只靠 prompt

HOI4 模组最烦的往往不是“不会写”，而是“看着像写对了，其实还差半截”。

最常见的坑基本就是这些：

- 改了 `focus`，忘了补 `_desc`
- 写了 `event`，没处理 namespace
- 改了 `decision`，没补对应 localisation
- 逻辑块能写出来，但 scope 不对
- 报错一多，就不知道先修哪一类

所以这个仓库的核心思路不是“换更强的模型”，而是把三件事一起做好：

1. 编辑器实时校验
2. AI 工作流约束
3. 本地结构化检查

---

## 三分钟上手

### 1. 安装 Python 包

```powershell
python -m pip install -e .
```

### 2. 先对模组目录做基础检查

```powershell
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding inventory-ids "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding audit-localisation "D:\Games\HOI4\mod\my_mod"
```

### 3. 看错误日志

```powershell
python -m hoi4_ai_modding summarize-log "C:\Users\<you>\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
```

### 4. 如果你用 Codex

先运行：

```powershell
.\tools\install_codex_integration.ps1
```

再把 MCP 配到 Codex：

```toml
[mcp_servers.hoi4-modding]
command = "python"
args = ["-m", "hoi4_ai_modding.mcp_server"]
```

### 5. 如果你用 VS Code

安装 `CWTools`：

```powershell
code --install-extension tboby.cwtools-vscode
```

---

## 我更推荐的使用顺序

别一上来就让 AI “给我写一整套事件链”。

更稳的顺序一般是：

1. 先识别 mod 根目录
2. 先盘点项目结构和命名规则
3. 再让 AI 生成或修改内容
4. 改完立刻跑 ID 审计和 localisation 审计
5. 出问题时先汇总 `error.log`
6. 再回去修逻辑、作用域或缺失资源

这样做的好处很简单：先把低级错和结构问题拦掉，后面你和 AI 才有精力处理真正的玩法设计。

---

## 仓库结构

```text
docs/                     项目文档、网站页、语法速查、任务公式
skills/hoi4-modding/      Codex Skill
src/hoi4_ai_modding/      Python 包，提供 CLI 和 MCP
tools/                    安装到 Codex 的便捷脚本
```

第一次进来，最值得先看的几个地方：

- `skills/hoi4-modding/`
  Skill 本体，决定 AI 做 HOI4 任务时的做事方式
- `src/hoi4_ai_modding/core.py`
  核心检测逻辑
- `src/hoi4_ai_modding/mcp_server.py`
  MCP 入口
- `docs/syntax-quick-reference.md`
  常用语法速查
- `docs/hoi4-country-state-formulas.md`
  国家、州、地图和建筑分配的细化公式
- `docs/index.html`
  GitHub Pages 首页

---

## 文档导航

- [网站首页](https://anatoli27149.github.io/hoi4-ai-modding-kit/)
- [安装说明](./docs/setup.md)
- [项目规范](./docs/project-spec.md)
- [HOI4 语法速查](./docs/syntax-quick-reference.md)
- [国家 / 州 / 地图 / 工厂公式](./docs/hoi4-country-state-formulas.md)
- [中文说明页](./docs/README.zh-CN.md)

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

说白了，它解决的是“怎么更稳地做模组”，不是单纯给你堆一大份代码表。

---

## 现在做到哪了

当前版本还是偏轻量，但已经够拿来真正干活了。

现在的重点是：

- 把 AI 协作流程做稳
- 把最有价值的本地检查能力做出来
- 让中文使用者能快速看懂并开始使用
- 把国家、州、地图和建筑这类高频重活补成可复用公式

后面如果继续往下做，比较值得补的方向有：

- 更强的 HOI4 内容类型识别
- 更细的资源引用检查
- 更完整的中文文档和示例模组
- 面向具体玩法类型的 skill 子模块

---

## English Summary

This repository bundles a Codex skill, local MCP and CLI tooling, and Chinese-facing docs for practical AI-assisted Hearts of Iron IV modding. It focuses on structure inspection, ID and localisation audits, log summarization, and keeping AI output aligned with real HOI4 project structure.
