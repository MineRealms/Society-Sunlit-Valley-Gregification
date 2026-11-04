# KubeJS 结构与约定

> 适用：MC 1.20.1 / KubeJS 6（build.16，测试端 build.26）+ Rhino 2001.2.x

## 1. 目录职责

| 目录 | 生命周期 | 用途 |
|---|---|---|
| `kubejs/startup_scripts/` | 启动时一次 | 注册/修改物品、机器、全局变量（`global.*`） |
| `kubejs/server_scripts/` | 进入世界 / `/reload` | 配方、标签、进服/玩家事件、任务联动、HUD 面板声明 |
| `kubejs/client_scripts/` | 客户端启动 / 资源重载 | tooltip、客户端事件、JEI 辅助 |
| `kubejs/data/<ns>/...` | 数据包加载（`/reload`） | 配方 JSON、标签、`data/society/recipes/**` |
| `kubejs/assets/<ns>/...` | 资源包 | 语言/贴图 |
| `kubejs/config/` | — | KubeJS 自身配置 |
| `kubejs/space/` | — | 空间站截图等资源 |

约定：
- 每个脚本至少一行 `console.info("[模块] xxx.js loaded")`，方便在日志里确认加载。
- 大功能按目录分：`gt/`、`tc/`、`me/`、`gtmfo/`、`thaumadds/`、`isorropia/`、`technom/`、`npcs/`、`playerEvents/`、`recipes/`、`tags/`、`customMachines/`。
- 跨脚本的共享状态放 `startup_scripts` 的 `global.*`，并在 `ServerEvents.loaded` 前初始化。

## 2. 常改的位置

| 需求 | 文件 |
|---|---|
| 星辉祭坛合成（星光水晶瓶等） | `kubejs/data/society/recipes/altar/*.json` + `server_scripts/me/meRecipes.js` |
| GT 配方锁（LV 电路等） | `server_scripts/gt/*.js`、`recipes/*.js` |
| GTMFO 营养标签/数值 | `server_scripts/gtmfo/gtmfoNutrients.js` |
| 中州联动 | `server_scripts/me/meRecipes.js`、`meTags.js`、`meCooking.js` |
| tooltip | `client_scripts/tooltips/*.js` |
| HUD 面板 | `server_scripts/sunlitHud.js` |

## 3. 已知坑（务必先看）

| 症状 | 原因 / 处理 |
|---|---|
| `player.level() is not a function` | `player.level` 是属性，用 `player.level` 不是方法 |
| `redeclaration of var x` | Rhino 对同名 `var/const` 敏感；事件回调里换名或提到顶层 |
| 配方加进去了但 JEI 看不到 | 数据驱动模组（如 AS 祭坛）有槽位/结构限制：看服务端 `Parsing error loading recipe`，按报错改 `pattern`（AS 发现祭坛只允许内圈 3×3） |
| 品质标签无效 | `quality_food:quality_blocks` 是 **block tag**（`TagKey<Block>`），必须放在 `ServerEvents.tags("block")`；放进 item 事件不会生效 |
| `/reload` 后配方没变 | 只有 `ServerEvents.recipes` 会重跑；数据包 JSON 也会重载；客户端 JEI 需要重连/重载资源 |
| `EUt()` 返回对象 | GT 机器 API 的 JS 包装问题，按实际 jar 版本核对；标签/配方优先用 JSON 形式 |
| `gt_demo_sim_v6.js#15` 加载失败 | 那是 Node 测试脚本，不要放进 `kubejs/server_scripts/` |

## 4. HUD（Sunlit HUD 模组）

面板在服务端脚本声明，模组同步到客户端渲染：

```js
SunlitHud.panels([{
  id: 'sunlit_status', anchor: 'top_left', x: 4, y: 4, width: 104, scale: 1.0,
  avoidAllMusic: true,
  rows: [
    { type: 'text', source: 'day', color: '#FFD37F' },
    { type: 'text', source: 'season', label: '季节', color: '#8FD9FF' },
    { type: 'bar', source: 'nutrient.dairy', label: '乳', barMax: 30, color: '#9BD47A' },
    { type: 'text', source: 'warp.total', label: '扭曲', hideBelow: 1, color: '#C77DFF' },
    { type: 'text', source: 'light', label: '光照', hideAbove: 7, color: '#FFE066' },
    { type: 'text', source: 'pollution', label: '污染', hideBelow: 1, color: '#B8B8B8' }
  ]
}])
```

- 数据源：`day`、`season`、`nutrient.{dairy,fruit,grain,protein,vegetable}`、`warp.{permanent,sticky,temporary,total}`、`light`、`pollution`、`xyz`
- 行选项：`hideBelow`/`hideAbove`（条件显示）、`barMax`、`label`、`color`（`#RRGGBB`）
- 服务端查询：`SunlitHud.snapshot(player)`、`SunlitHud.season(level)`、`SunlitHud.clear()`、`SunlitHud.json()`
- 面板改动只需 `/reload`；模组本体改动要重启游戏
- 模组缺失时脚本用 `typeof SunlitHud !== 'undefined'` 保护

## 5. 调试

- 服务端脚本日志：`logs/kubejs/server.log`
- 客户端脚本日志：`logs/kubejs/client.log`
- 游戏日志：`logs/latest.log`（配方解析错误、模组异常都在这里）
- 配方是否真的存在：写临时脚本在 `ServerEvents.tick` 里 `server.getRecipeManager().getAllRecipesFor(RecipeType)` 打印数量，验证后删除
