# HOI4 国家、州、地图与建筑公式

这篇文档不是“再给一份泛 prompt”，而是把 HOI4 里最容易写散、写漏、写错的国家包、州包、地图包和建筑分配拆成一套能直接交给 AI 的工作公式。

如果你是想让 AI 直接接手大部分开发任务，先看这里，再去补具体玩法内容，会比直接一句“帮我做个国家”稳很多。

## 资料优先级

做这类任务时，资料源的优先级建议固定成这样：

1. 游戏安装目录自带的 `documentation/`
2. 原版对应目录里的实际样板文件
3. Parawikis 的流程类页面
4. 你自己的模组现有命名和目录结构

真正的全量 trigger / effect / modifier，不要靠记忆硬背，优先查：

- `<HOI4 install>/documentation/effects_documentation.html`
- `<HOI4 install>/documentation/triggers_documentation.html`
- `<HOI4 install>/documentation/modifiers_documentation.html`

## 做成 skill，至少拆成 6 个模块

1. `country-bundle`
   负责创建国家 tag、颜色、名字、旗帜、基础文件。
2. `country-history-preset`
   负责开局政治、科技、科研槽、运输船、角色、OOB、民族精神。
3. `state-bundle`
   负责州文件、州名、人口、资源、建筑、核心和宣称。
4. `state-economy-balance`
   负责州类别、共享建筑槽、工厂数量和建筑上限。
5. `state-map-overlay`
   负责根据州块规划生成预览图，先校验再改图。
6. `validator`
   负责查 tag、查本地化、查省份冲突、查建筑非法、查槽位超限。

## 1. 创建国家公式

### 推荐输入结构

```yaml
task: create_country_bundle
mod_root: <mod root>
tag: NCH
country_file_name: North China.txt
display_name:
  simp_chinese: 北华
  english: North China
adj:
  simp_chinese: 北华
  english: North Chinese
ideology_names:
  fascism: 北华国
  democratic: 北华共和国
  neutrality: 北华王国
  communism: 北华人民共和国
color: { 120 40 40 }
color_ui: { 180 90 90 }
graphical_culture: eastern_european_gfx
graphical_culture_2d: eastern_european_2d
capital_state_id: 610
starting_states: [610, 611, 612]
core_states: [610, 611, 612]
claimed_states: []
need_flags: true
need_characters: true
```

### 必须一次性生成的文件

- `common/country_tags/<mod>_countries.txt`
- `common/countries/<CountryFileName>.txt`
- `history/countries/<TAG> - <CountryName>.txt`
- `localisation/simp_chinese/<mod>_countries_l_simp_chinese.yml`
- `localisation/english/<mod>_countries_l_english.yml`
- `gfx/flags/<TAG>.tga`
- `gfx/flags/medium/<TAG>.tga`
- `gfx/flags/small/<TAG>.tga`
- 如果角色独立维护，再生成 `common/characters/<TAG>.txt`

### 国家注册公式

```txt
NCH = "countries/North China.txt"
```

### 国家基础文件公式

路径：`common/countries/North China.txt`

```txt
graphical_culture = eastern_european_gfx
graphical_culture_2d = eastern_european_2d

color = { 120 40 40 }
```

说明：

- 这里负责地图色和图形文化。
- 开局政治、科技、角色、OOB 不写在这里，放到 `history/countries/`。

### 国家本地化公式

```yml
l_simp_chinese:
 NCH_fascism:0 "北华国"
 NCH_fascism_DEF:0 "北华国"
 NCH_democratic:0 "北华共和国"
 NCH_democratic_DEF:0 "北华共和国"
 NCH_neutrality:0 "北华王国"
 NCH_neutrality_DEF:0 "北华王国"
 NCH_communism:0 "北华人民共和国"
 NCH_communism_DEF:0 "北华人民共和国"
 NCH_fascism_ADJ:0 "北华"
 NCH_democratic_ADJ:0 "北华"
 NCH_neutrality_ADJ:0 "北华"
 NCH_communism_ADJ:0 "北华"
 NCH:0 "北华"
 NCH_DEF:0 "北华"
 NCH_ADJ:0 "北华"
```

旗帜最少要有主旗，稳一点的话四种意识形态旗一起准备：

- `NCH.tga`
- `NCH_fascism.tga`
- `NCH_democratic.tga`
- `NCH_neutrality.tga`
- `NCH_communism.tga`

## 2. 国家预设公式

路径：`history/countries/<TAG> - <CountryName>.txt`

```txt
capital = 610

set_research_slots = 3
set_convoys = 10

set_technology = {
    infantry_weapons = 1
    tech_support = 1
    gw_artillery = 1
}

set_oob = "NCH_1936"
set_air_oob = "NCH_1936_air"

add_ideas = {
    NCH_foundation_spirit
}

recruit_character = NCH_founder
recruit_character = NCH_chief_of_army

set_politics = {
    ruling_party = neutrality
    last_election = "1936.1.1"
    election_frequency = 48
    elections_allowed = no
}

set_popularities = {
    fascism = 10
    democratic = 20
    neutrality = 65
    communism = 5
}

set_war_support = 0.15
set_stability = 0.35

set_country_flag = NCH_created
```

### 这里最容易写错的点

- `capital` 填州 ID，不是省份 ID。
- `set_popularities` 四项加起来必须正好等于 `100`。
- `set_oob`、`set_air_oob`、`set_naval_oob` 引用的文件必须真的存在。
- 如果角色已经写进 `common/characters/`，优先 `recruit_character`，不要重复造人。

### 临时造国家领导人公式

如果你只是快速起一个测试国家，可以直接用：

```txt
create_country_leader = {
    name = "NCH_leader_name"
    desc = "NCH_leader_desc"
    picture = "Portrait_NCH_leader.dds"
    expire = "1965.1.1"
    ideology = despotism
    traits = {
        popular_figurehead
    }
}
```

但正式项目更建议用 `common/characters/<TAG>.txt` + `recruit_character`。

## 3. 州 / 区块公式

路径：`history/states/<id>-<name>.txt`

```txt
state = {
    id = 610
    name = "STATE_610"
    manpower = 850000

    resources = {
        steel = 8
        aluminium = 2
    }

    state_category = town

    history = {
        owner = NCH
        controller = NCH

        add_core_of = NCH
        add_claim_by = CHI

        victory_points = {
            12345 10
            12346 5
        }

        buildings = {
            infrastructure = 3
            industrial_complex = 2
            arms_factory = 1
            air_base = 2
            anti_air_building = 1

            12345 = {
                naval_base = 3
                bunker = 2
            }
        }

        1939.1.1 = {
            buildings = {
                industrial_complex = 3
                arms_factory = 2
            }
        }
    }

    provinces = {
        12340 12341 12342 12343 12344 12345 12346
    }

    local_supplies = 2.0
}
```

### 字段作用

- `id`
  州 ID，必须唯一。
- `name = "STATE_610"`
  这是本地化 key，不是显示文本。
- `manpower`
  州人口池。
- `resources`
  州资源。
- `state_category`
  州类别，直接影响基础共享建筑槽。
- `owner`
  法理拥有者。
- `controller`
  实际控制者。
- `add_core_of`
  核心州归属。
- `add_claim_by`
  宣称。
- `victory_points`
  `省份ID 分值`。
- `buildings`
  州级和省级建筑都写在这里。
- `provinces`
  州包含的全部省份 ID。

### 州名本地化公式

```yml
l_simp_chinese:
 STATE_610:0 "北平"
```

## 4. 州类别、工厂数量和建筑上限公式

### 原版州类别基础共享槽

| 州类别 | 基础共享槽 |
| --- | ---: |
| `wasteland` | 0 |
| `enclave` | 0 |
| `tiny_island` | 0 |
| `pastoral` | 1 |
| `small_island` | 1 |
| `rural` | 2 |
| `large_island` | 3 |
| `town` | 4 |
| `large_town` | 5 |
| `city` | 6 |
| `large_city` | 8 |
| `metropolis` | 10 |
| `megalopolis` | 12 |

### 原版常用建筑上限

| 建筑 | 主要上限 | 备注 |
| --- | --- | --- |
| `infrastructure` | `state_max = 5` | 州级 |
| `arms_factory` | `state_max = 20` | 吃共享槽 |
| `industrial_complex` | `state_max = 20` | 吃共享槽 |
| `dockyard` | `state_max = 20` | 吃共享槽，必须沿海 |
| `air_base` | `state_max = 10` | 州级 |
| `anti_air_building` | `state_max = 5` | 州级 |
| `radar_station` | `state_max = 6` | 州级 |
| `synthetic_refinery` | `state_max = 3` | 吃共享槽 |
| `fuel_silo` | 受共享槽约束 | 州级 |
| `rocket_site` | `state_max = 3` | 吃共享槽 |
| `nuclear_reactor` | `state_max = 1` | 吃共享槽 |
| `naval_base` | `province_max = 10` | 省级，必须海岸省 |
| `bunker` | `province_max = 10` | 省级 |
| `coastal_bunker` | `province_max = 10` | 省级，必须海岸省 |
| `supply_node` | `province_max = 1` | 省级 |
| `rail_way` | `province_max = 1` | 省级 |

### 工厂数量公式

```txt
shared_slots_needed =
industrial_complex +
arms_factory +
dockyard +
synthetic_refinery +
fuel_silo +
rocket_site +
nuclear_reactor +
other_shared_slot_buildings

base_shared_slots = slots_from_state_category(state_category)
```

### 分配规则

1. `shared_slots_needed <= base_shared_slots`
   直接写进州文件。
2. `shared_slots_needed > base_shared_slots`
   先考虑上调 `state_category`。
3. 还是不够
   再考虑事件、决议或脚本里用 `add_extra_state_shared_building_slots`。
   这个是运行时 effect，不是 `history/states/` 里的静态字段。
4. `dockyard`、`naval_base`、`coastal_bunker`
   必须先校验沿海。
5. `naval_base`、`bunker`、`coastal_bunker`、`supply_node`
   要挂到具体省份块，不要写成州级建筑。

### 实战分配建议

- `pastoral` / `rural`
  共享建筑尽量控制在 `0-2`，别硬塞一堆工厂。
- `town` / `large_town`
  适合 `1-3` 民工或军工。
- `city` / `large_city`
  适合首都州、副工业州，能给更多民工、防空、空军基地。
- `metropolis` / `megalopolis`
  适合超级首都或工业核心，不要滥用。

## 5. 根据区块生成州预览图公式

如果你只是重新分配现有省份到不同州，完全可以先生成一张预览图，不急着动地图底层文件。

### 推荐输入

```yaml
task: generate_state_overlay
definition_csv: <mod root>/map/definition.csv
provinces_bmp: <mod root>/map/provinces.bmp
state_plan:
  - state_id: 610
    color: "#8B2E2E"
    label: 北平州
    province_ids: [12340, 12341, 12342, 12343]
    capital_province: 12345
  - state_id: 611
    color: "#2E5A8B"
    label: 天津州
    province_ids: [12350, 12351, 12352]
    capital_province: 12353
output:
  overlay_png: docs/generated/state_overlay.png
  legend_csv: docs/generated/state_overlay_legend.csv
  conflict_report: docs/generated/state_conflicts.txt
```

### 输出规则

1. 读 `definition.csv`，建立 `province_id -> RGB` 映射。
2. 读 `provinces.bmp`，按 RGB 抠出每个省份区域。
3. 按州规划统一上色，输出预览图。
4. 生成冲突报告：
   - 一个省份被两个州同时引用
   - 引用了不存在的省份
   - 海洋省份被塞进陆地州
   - 有省份没被任何州引用

## 6. 什么时候必须改底图

下面两种事，不能只改 `history/states/`：

1. 你要新增省份
2. 你要改省份边界

这时才进入地图底层流程：

1. 改 `map/provinces.bmp`
2. 改 `map/definition.csv`
3. 必要时改 `map/adjacencies.csv`
4. 重排 `history/states/*.txt` 的 `provinces = {}`
5. 必要时补 `strategic regions`
6. 如果你还要地图上的建筑摆件位置正确，再改 `map/buildings.txt` 或用 Nudger 摆位

要记住：

- `history/states/*.txt`
  决定开局有几座建筑。
- `map/buildings.txt`
  更像建筑模型摆位，不是建筑数量总表。

## 7. 最终校验公式

每次生成完，都要跑一遍下面这套检查：

- `TAG` 是否注册到了 `common/country_tags/`
- `common/countries/<name>.txt` 是否存在
- `history/countries/<TAG> - <name>.txt` 是否存在
- 国家本地化是否补齐 `TAG / TAG_DEF / TAG_ADJ / ideology variants`
- 旗帜是否存在
- `set_popularities` 总和是否等于 `100`
- `capital` 指向的州是否存在
- `recruit_character` 引用的 token 是否有定义
- `set_oob` / `set_air_oob` / `set_naval_oob` 引用的文件是否存在
- 每个州文件是否包含 `id / name / state_category / history / provinces`
- 每个 `province_id` 是否只属于一个州
- `dockyard`、`naval_base`、`coastal_bunker` 是否只出现在沿海合法位置
- 共享建筑总量是否超过州类别槽位
- `STATE_<id>` 本地化是否补齐

## 8. 可以直接交给 AI 的句法公式

```txt
你是 HOI4 模组工程代理，不是聊天助手。

收到“创建国家 / 创建州 / 生成州地图 / 分配工厂数量”类任务时，必须按下面流程执行：

1. 先查游戏自带 documentation，再查原版同类文件。
2. 国家任务按 country bundle 输出，不得只给 history/countries 单文件。
3. 州任务按 state bundle 输出，不得只给一个 provinces 列表。
4. 建筑任务先计算共享槽，再决定 state_category 和建筑数量。
5. 地图任务默认只重排现有 province_ids；只有用户明确要求新增省份时，才允许修改 provinces.bmp 和 definition.csv。
6. 每次输出都必须附带校验报告，包括 ID 冲突、省份冲突、本地化缺失、建筑非法和槽位超限。
```

## 参考入口

- Parawikis: [State modding](https://hoi4.parawikis.com/wiki/State_modding)
- Parawikis: [Building modding](https://hoi4.parawikis.com/zh-hans/Building_modding)
- Parawikis: [Nudger](https://hoi4.parawikis.com/zh-tw/Nudger)
- 游戏自带文档：`documentation/effects_documentation.*`
- 游戏自带文档：`documentation/triggers_documentation.*`
- 原版样板：`common/country_tags/`、`common/countries/`、`history/countries/`、`history/states/`
