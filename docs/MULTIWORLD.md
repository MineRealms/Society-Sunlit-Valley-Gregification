# Multiworld（多世界）接入说明

> 状态：**已接入**。jar 为自打补丁版，来源 Modrinth `multiworld` 1.10-forge + 本地 ASM 修复。

## 1. 为什么不是原版 jar

包里跑的是 **Mohist + Sinytra Connector**。Multiworld 的官方 1.20.1 Forge 构建
（Modrinth version id `ct6IgvWn`，文件名 `Multiworld-Forge-1.20.1.jar`）
**在 Connector 下必定启动崩溃**，症状是：

```
java.lang.NoClassDefFoundError: net.minecraft.server.MinecraftServer
  at xyz.nucleoid.fantasy.mixin.MinecraftServerAccess ...
```

看着像「服务器 jar 坏了」或「mod 不支持 1.20.1」，其实两者都不是。真正原因：

- `xyz.nucleoid.fantasy.mixin.MixinMinecraftServer` 里有一个
  `@Redirect(method = "createWorlds", at = @At(INVOKE, target = "Ljava/util/Map;put(...)"))`
  的 `onLoadWorld` 处理器，**没有写 ordinal**。
- Connector 会把 `MinecraftServer` 重新改写一遍，这个 redirect 匹配不上，
  Mixin 抛 `MixinTransformerError`，而它发生在 `MinecraftServer` 的**类初始化**阶段，
  于是后续任何引用都变成 `NoClassDefFoundError`。

上游作者已合入 PR #171「Remove redirect for sinytra compatibility」（2026-03-18），
但**至今没有发新版本**，Modrinth 上所有版本都带这个 redirect。

## 2. 我们做的补丁

只做一件事：用 ASM 把 `MixinMinecraftServer` 里的 `onLoadWorld` 方法整段删掉
（连带它的 `@Redirect` 注解），其余字节原样保留。

重打包时**必须**恢复原 manifest：

```
Manifest-Version: 1.0
MixinConfigs: dim.mixins.json,fantasy.mixins.json
```

否则 Mixin 会静默不生效（不报错，但 `/mw` 一用就 NPE）。

产物：`mods/Multiworld-Forge-1.20.1-1.10-sinytra.jar`
sha256 `9a50f4230a3c01848d783fa1eba6c010cda13411325851a4d634ab661d556f97`

## 3. 为什么不去构建上游源码

上游仓库 `settings.gradle` 里 `include 'Multiworld-Forge-1.20.1'` 是**注释掉的**，
CI 也从不构建 Forge 模块。强行打开会连续撞：

1. shadow 7.1.1 与 Gradle 9 不兼容（`Could not get unknown property 'convention'`）
2. architectury-plugin 3.4 缺 `net.fabricmc.loom.configuration.ide.RunConfig`
3. `archivesBaseName` 在 Gradle 9 被移除
4. loom 在 root / subproject 各有一份 classloader → `LoomGradleExtension` ClassCastException
5. 最后卡在 `Multiworld-Common` 的 `mappings-yay-identifier.jar` 分层映射上

**Forge 模块是死代码**，不是我们环境的问题。

## 4. 命令

| 命令 | 说明 |
|---|---|
| `/mw create <名字> [NORMAL|FLAT|NETHER|END] [-g=] [-s=]` | 新建世界 |
| `/mw tp <玩家> <世界>` | 传送 |
| `/mw spawn` / `/mw setspawn` | 出生点 |
| `/mw delete <世界>` | 删除 |
| `/mw list` | 列出 |
| `/mw time` / `/mw difficulty` / `/mw gamerule` | 世界属性 |

权限节点：`multiworld.tp`、`multiworld.create` 等（走 luckperms / CyberPermissions）。

## 5. 已知限制

- 依赖 `architectury`（包里已有 9.2.14-forge，满足 `[6.3.49,)`）。
- 上游 issue #172 提到**从源码构建的 HEAD** 在 `/mw create` 时需要 MixinExtras；1.10 版本不需要。
- 1.10 版本不包含 1.11–1.14 的天气/传送门修复（那些主要是 1.21 线的改动）。
- 与 Bukkit 侧 Multiverse 不要同时装，两套都会接管世界列表。

## 6. 验证清单

1. 客户端启动到主菜单，日志里没有 `MixinTransformerError` / `NoClassDefFoundError: net.minecraft.server.MinecraftServer`。
2. 进服后 `/mw list` 有输出。
3. `/mw create test FLAT` 成功，`/mw tp <自己> test` 能过去。
4. `/mw delete test` 能删干净。
