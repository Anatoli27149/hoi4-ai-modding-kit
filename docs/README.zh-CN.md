# HOI4 AI Modding Kit 中文说明

## 一句话先说清

如果你想用 AI 做 HOI4 模组，但又不想每次都被 `localisation`、`namespace`、`scope` 这种细节绊住，这个仓库就是干这个的。

它不是只放 prompt，也不是只放 MCP，而是把下面三样东西放到了一起：

- `Skill`
  约束 AI 怎么做 HOI4 任务
- `MCP / CLI`
  负责查结构、查日志、做机械检查
- `文档`
  让中文使用者能快速看懂怎么装、怎么用、该先看什么

---

## 最适合什么人

- 想用 AI 辅助开发 HOI4 模组的中文用户
- 已经会写一些 `focus`、`event`、`decision`，但老是漏本地化、scope 或配套文件的人
- 想把 `AI + MCP + Skill` 真正用到具体项目里的人
- 想把自己的 HOI4 开发流程沉淀成一套长期能用的工具链的人

不太适合：

- 只想临时问 AI 一两个语法问题，不想搭本地工具链
- 完全不打算碰 Python、VS Code、本地文件工作流

---

## 仓库里最值得先看的东西

### `skills/hoi4-modding/`

这是 Codex 用的 skill，主要干的是把 AI 的做事方式收住，比如：

- 先看相邻文件
- 先确认 mod 根目录
- 改动按“内容包”走，不只改单个文件
- 改完后检查 ID 和 localisation

### `src/hoi4_ai_modding/`

这是 Python 包，既能当命令行工具用，也能当 MCP 用。

你可以用它来：

- 查模组根目录
- 看模组结构
- 盘点 ID 和 namespace
- 找缺失 localisation
- 汇总 `error.log`

### `docs/`

放项目文档，包括：

- 安装说明
- 项目规范
- HOI4 语法速查
- 国家 / 州 / 地图 / 工厂公式
- 网站首页

---

## 更稳一点的用法

1. 先用工具确认 mod 根目录
2. 再看项目现有结构和命名风格
3. 再让 AI 去写或改内容
4. 改完以后跑审计
5. 如果报错，再回头看 `error.log`

比起一上来就让 AI “给我写一条完整事件链”，这样会稳很多。

---

## 关于“完整语法”

这个仓库提供的是高频、实战向、适合配合 AI 使用的东西。

如果你要查当前游戏版本最完整的 trigger / effect 列表，还是优先看游戏安装目录里的：

- `documentation/triggers_documentation.html`
- `documentation/effects_documentation.html`

原因很简单：这两份文件跟你本机版本最接近，通常比社区零散资料更靠谱。

---

## 第一次看这个仓库，建议按这个顺序读

1. 先看仓库首页 `README.md`
2. 再看 [网站首页](./index.html)
3. 再看 [安装说明](./setup.md)
4. 再看 [语法速查](./syntax-quick-reference.md)
5. 如果你要让 AI 直接接手国家、州、地图和工厂分配，接着看 [国家与州公式](./hoi4-country-state-formulas.md)
6. 真正上手时再看 [项目规范](./project-spec.md)

---

## 一句话总结

这个仓库不是替你把模组全做完，而是让你在做 HOI4 模组时，AI 没那么容易掉链子。
