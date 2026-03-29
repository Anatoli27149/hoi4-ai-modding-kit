# 国家、州、地图与建筑公式

任务只要碰到下面任意一种，就先读这份参考：

- 新建国家 tag
- 写 `history/countries/`
- 写 `history/states/`
- 分州、改州、改建筑数量
- 生成州块预览图
- 准备修改 `provinces.bmp`、`definition.csv`、`buildings.txt`

## 资料读取顺序

1. 先读游戏自带 `documentation/effects_documentation.*`
2. 再读 `documentation/triggers_documentation.*`
3. 再读原版对应目录里的同类文件
4. 再读本模组邻近文件
5. 最后才自己补结构

不要凭空发明国家 tag、州 ID、角色 token、OOB 名字、州类别和建筑上限。

## 国家 bundle

创建国家时，默认输出整包，不要只给一个 `history/countries/*.txt` 片段。

最少要检查这些文件：

- `common/country_tags/*.txt`
- `common/countries/*.txt`
- `history/countries/*.txt`
- `localisation/*/*.yml`
- `gfx/flags/`

最小输出模板：

```txt
TAG = "countries/Country Name.txt"
```

```txt
graphical_culture = eastern_european_gfx
graphical_culture_2d = eastern_european_2d
color = { 120 40 40 }
```

```txt
capital = 610
set_research_slots = 3
set_convoys = 10
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
set_stability = 0.35
set_war_support = 0.15
```

硬规则：

- `capital` 是州 ID。
- `set_popularities` 总和必须等于 `100`。
- 如果项目已用 `common/characters/`，优先 `recruit_character`。
- 如引用 `set_oob`、`set_air_oob`、`set_naval_oob`，必须确认 OOB 存在。
- 国家本地化至少补齐 `TAG`、`TAG_DEF`、`TAG_ADJ` 和意识形态变体。

## 州 bundle

创建或改写州时，至少要联动：

- `history/states/*.txt`
- `localisation/*/state_names*.yml`

最小州模板：

```txt
state = {
    id = 610
    name = "STATE_610"
    manpower = 850000
    state_category = town

    history = {
        owner = TAG
        controller = TAG
        add_core_of = TAG
        victory_points = { 12345 10 }
        buildings = {
            infrastructure = 3
            industrial_complex = 2
            arms_factory = 1
            12345 = {
                naval_base = 3
            }
        }
    }

    provinces = { 12340 12341 12342 12345 }
    local_supplies = 2.0
}
```

硬规则：

- `name = "STATE_<id>"` 是本地化 key。
- `province_id` 只能属于一个州。
- `naval_base`、`bunker`、`coastal_bunker`、`supply_node` 属于省级建筑。
- `dockyard`、`naval_base`、`coastal_bunker` 只允许在沿海合法位置出现。

## 州类别和共享槽

先算共享槽，再写工厂数量。

共享槽常见消耗方：

- `industrial_complex`
- `arms_factory`
- `dockyard`
- `synthetic_refinery`
- `fuel_silo`
- `rocket_site`
- `nuclear_reactor`

原版基础槽常用值：

- `pastoral = 1`
- `rural = 2`
- `town = 4`
- `large_town = 5`
- `city = 6`
- `large_city = 8`
- `metropolis = 10`
- `megalopolis = 12`

如果共享建筑超槽：

1. 先考虑更合理的 `state_category`
2. 还不够，再考虑运行时 `add_extra_state_shared_building_slots`
3. `add_extra_state_shared_building_slots` 是运行时 effect，不是静态州文件字段
4. 不要在静态州文件里假装它已经扩槽

## 地图和州预览图

默认先做预览图和冲突检查，再改底层地图。

只要用户没有明确要求“新增省份”或“改省份边界”，就：

- 不改 `provinces.bmp`
- 不改 `definition.csv`
- 不改 `adjacencies.csv`
- 只重组现有 `province_ids`

进入地图底层修改时，再联动：

- `map/provinces.bmp`
- `map/definition.csv`
- `map/adjacencies.csv`
- `history/states/*.txt`
- 必要时 `map/buildings.txt`
- 必要时 `strategic regions`

注意：

- `history/states/*.txt` 决定建筑数量和开局状态。
- `map/buildings.txt` 更像地图上建筑模型摆位。

## 交付前校验

每次结束前至少确认：

- 国家 tag 已注册
- 国家、州、本地化文件成套存在
- `STATE_<id>` 本地化存在
- `set_popularities` 合法
- `capital` 有效
- `province_id` 没有重复归州
- 沿海建筑没有放错
- 共享建筑没有超槽
- 角色、OOB、ideas、focus、events 的引用没悬空
