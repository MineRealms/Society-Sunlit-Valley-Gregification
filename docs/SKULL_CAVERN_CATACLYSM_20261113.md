# Skull Cavern: Cataclysm Spawn Integration

## Scope

Only the eight inhabited `society` cavern biome monster pools change.
The `cavern_top` entry pool stays empty. Existing InControl timers, distances,
height multipliers and count checks remain in effect.

## Relative Frequency

For original monster weight W and new Cataclysm weight C:

```text
C = round(W / 2)
P(Cataclysm) = C / (W + C) ~= 1/3
C / W ~= 1/2
```

The requested frequency is relative to ordinary monsters, not half of all
monsters. These are selection weights, not a guarantee of successful spawns.
Original pool entries and their relative weights are preserved.

| Biome | Added mob weights | Original W | Added C |
|---|---|---:|---:|
| skull_caves | the_watcher 100, endermaptera 121 | 441 | 221 |
| lush_caverns | endermaptera 210 | 420 | 210 |
| frozen_caves | draugr 100, royal_draugr 44, elite_draugr 16 | 320 | 160 |
| frozen_maelstrom | draugr 100, royal_draugr 60, elite_draugr 25 | 370 | 185 |
| desert_caves | koboleton 145 | 290 | 145 |
| desert_fault | koboleton 233 | 465 | 233 |
| blackstone_caves | the_watcher 180, ignited_berserker 45 | 450 | 225 |
| umbra_barrens | endermaptera 158 | 315 | 158 |

## Installed-Version Behavior

- Checked against Cataclysm 2.39 and InControl 9.4.1.
- No bosses, minibosses, pets, or aquatic mobs enter the land pool.
- Vanilla group settings are 1-2, or 1 for ignited_berserker. InControl ignores
  biome group sizes and uses its existing 2-3 target for successful spawns.
- InControl's existing persecond 0.15 checks are shared by all entries. This
  change does not create another timer or an additional mob-spawning task.
- Existing maxthis checks remain per EntityType and dimension, not an aggregate
  Cataclysm cap. Adding species does not establish a strict total-entity ceiling.
- Koboleton requires sky visibility for vanilla natural spawning; the installed
  InControl path can generate it underground while retaining instance checks.
- Ignited berserkers keep the mod's native Ignis-defeat gate and spawn roll.
  Their successful frequency is lower than their pool weight until allowed.
- Existing depth multipliers and Champions may further strengthen these mobs.

## Deployment

The live pack, pack/dev/overrides and pack/release/overrides contain identical
copies of the eight edited biome JSON files.

Biome world-generation registries are constructed when the server starts.
Uploading these files stages the update; ordinary /reload does not rebuild
those registries. Use the next agreed server restart for activation. Existing
chunks use the updated biome spawn tables after that restart; no terrain reset
is necessary.

Validation should check JSON, installed entity IDs, weight ratios, and runtime
biome codec decoding. No gameplay rate benchmark is claimed.

## Verification Record

- Local JSON and relative-weight checks passed for all eight biomes.
- All 24 JSON copies have matching SHA-256 across live/dev/release profiles.
- Eight server files were backed up, uploaded through Rosetta, and read back
  with matching SHA-256 on 2026-11-13.
- The running server decoded all eight pools with its MobSpawnSettings codec
  and confirmed all seven added EntityTypes are registered (13 ms validation).
- No entities were spawned, chunks edited, or server restart performed.
- The update is staged for the next agreed server restart; live spawning has
  not been observed with the new tables yet.

Remote-file backup:

```text
H:/MinecraftMods/skull-cavern-cataclysm-20261113/server-backups/20261113-061211-241515
```
