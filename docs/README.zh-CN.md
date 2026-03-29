# HOI4 AI Modding Kit 中文说明

## 项目定位

这个项目的目标很明确：

让 AI 在 HOI4 模组开发里变得更稳、更像一个真正能协作的开发助手。

它不是单纯的提示词仓库，也不是只提供一个 MCP 服务，而是把三层东西组合起来：

- `Skill`
  规定 AI 在 HOI4 模组任务里应该怎样工作
- `MCP / CLI`
  提供本地结构检查和日志分析能力
- `文档`
  帮助中文使用者快速理解项目、安装方式和工作流

## 为什么要做这个项目

HOI4 模组开发里最烦人的问题，往往不是语法本身，而是这些细节：

- 改了 focus 但没补 `_desc`
- 事件 namespace 写乱了
- decision 和 localisation 没配套
- 逻辑块看着像对的，但 scope 不对
- 日志报错太多，不知道先修哪一类

AI 很容易在这些地方“看起来会写，实际不稳定”。

所以这个项目的思路不是“让 AI 写得更多”，而是：

- 让编辑器帮你校验
- 让 skill 约束 AI 工作方式
- 让本地工具补上结构化检查

## 这套仓库最适合的场景

- 做 focus、event、decision、idea 这类常规模组内容
- 想让 AI 改完以后顺手检查缺失本地化
- 想快速定位 `error.log` 里最值得先处理的问题
- 想把自己的 HOI4 开发工作流沉淀成工具链

## 仓库里最重要的内容

### `skills/hoi4-modding/`

这是 Codex 用的 skill，负责约束 AI 的行为，比如：

- 先看相邻文件
- 先确认 mod 根目录
- 改动按“内容包”走，不只改单个文件
- 改完后检查 ID 和 localisation

### `src/hoi4_ai_modding/`

这是 Python 包，提供命令行和 MCP 能力。

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

## 建议的使用顺序

1. 先用工具确认 mod 根目录
2. 再看项目现有结构和命名风格
3. 再让 AI 去写或改内容
4. 改完以后跑审计
5. 如果报错，再回头看 `error.log`

这比直接上来让 AI “给我写一个事件链”要稳得多。

## 关于完整语法

这个仓库提供的是“高频、实战向、适合 AI 协作”的内容。

如果你要查当前游戏版本最完整的 trigger / effect 列表，还是优先看游戏安装目录里的：

- `documentation/triggers_documentation.html`
- `documentation/effects_documentation.html`

因为这两份文件最接近你当前安装版本，可靠性比很多社区资料更高。

## 适合中文使用者的阅读顺序

推荐按这个顺序看：

1. 先看仓库首页 `README.md`
2. 再看 [安装说明](./setup.md)
3. 再看 [语法速查](./syntax-quick-reference.md)
4. 真正上手时再看 [项目规范](./project-spec.md)

## 一句话总结

这个项目不是想“替你写完 HOI4 模组”，而是帮你把 AI 变成一个更靠谱的 HOI4 模组协作工具。
