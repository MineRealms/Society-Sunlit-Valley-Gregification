"""Repair obsolete MVS override connectors and audit effective template pools.

Requires nbtlib (tested with 2.0.4). Run from any directory:
    python config/tools/repair_mvs_jigsaws.py --write
    python config/tools/repair_mvs_jigsaws.py --check

Only the documented cells below are eligible for repair. Their saved final_state
is placed directly, so no missing pool is introduced to hide the warning.
"""

import argparse
import copy
import gzip
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

import nbtlib


TARGETS = {
    "houses/large_warped_tower": {
        (14, 43, 10): (
            "mvs:houses/large_warped_tower/side_pool",
            "minecraft:warped_trapdoor[half=top]",
        ),
    },
    "other_decoration/wheat_grain_bin": {
        (0, 1, 2): ("mvs:farm/side_pool", "minecraft:structure_void"),
    },
    "other_decoration/wooden_wheat_farm": {
        (0, 1, 2): ("mvs:farm/side_pool", "minecraft:structure_void"),
        (8, 1, 0): ("mvs:farm/side_pool", "minecraft:structure_void"),
    },
}
FINAL_STATES = {
    "minecraft:structure_void": {"Name": nbtlib.String("minecraft:structure_void")},
    "minecraft:warped_trapdoor[half=top]": {
        "Name": nbtlib.String("minecraft:warped_trapdoor"),
        "Properties": nbtlib.Compound({"half": nbtlib.String("top")}),
    },
}
OVERRIDES = (Path("."), Path("pack/dev/overrides"), Path("pack/release/overrides"))


def parse_nbt(raw):
    if raw.startswith(b"\x1f\x8b"):
        raw = gzip.decompress(raw)
    return nbtlib.File.parse(io.BytesIO(raw))


def encode_nbt(nbt):
    stream = io.BytesIO()
    nbt.write(stream)
    return gzip.compress(stream.getvalue(), mtime=0)


def jigsaws(nbt):
    palettes = [nbt["palette"]] if "palette" in nbt else nbt["palettes"]
    states = {
        index
        for palette in palettes
        for index, state in enumerate(palette)
        if state["Name"] == "minecraft:jigsaw"
    }
    return [
        block for block in nbt.get("blocks", [])
        if int(block["state"]) in states
        or block.get("nbt", {}).get("id") == "minecraft:jigsaw"
    ]


def repair(raw, structure):
    before = parse_nbt(raw)
    after = copy.deepcopy(before)
    palette = after["palette"]
    by_position = {tuple(map(int, block["pos"])): block for block in after["blocks"]}
    changed = []
    for position, (obsolete_pool, final_state) in TARGETS[structure].items():
        block = by_position[position]
        replacement = nbtlib.Compound(copy.deepcopy(FINAL_STATES[final_state]))
        if palette[int(block["state"])] == replacement and "nbt" not in block:
            continue
        payload = block.get("nbt", {})
        if (palette[int(block["state"])]["Name"] != "minecraft:jigsaw"
                or payload.get("id") != "minecraft:jigsaw"
                or payload.get("pool") != obsolete_pool
                or payload.get("final_state") != final_state):
            raise ValueError(f"Unexpected connector at {structure} {position}")
        state = next((i for i, entry in enumerate(palette) if entry == replacement), None)
        if state is None:
            state = len(palette)
            palette.append(replacement)
        block["state"] = nbtlib.Int(state)
        del block["nbt"]
        changed.append(position)

    # Compare every unaffected tag, cell and palette entry, including loot/entities.
    restored = copy.deepcopy(after)
    before_blocks = {tuple(map(int, b["pos"])): b for b in before["blocks"]}
    for index, block in enumerate(restored["blocks"]):
        position = tuple(map(int, block["pos"]))
        if position in changed:
            restored["blocks"][index] = copy.deepcopy(before_blocks[position])
    del restored["palette"][len(before["palette"]):]
    if restored != before:
        raise AssertionError(f"Unrelated NBT changed: {structure}")
    if not changed:
        return raw, []
    encoded = encode_nbt(after)
    if parse_nbt(encoded) != after:
        raise AssertionError(f"NBT serialization changed data: {structure}")
    return encoded, changed


def jar_resources(path, namespace):
    pools = {}
    structures = {}
    with zipfile.ZipFile(path) as archive:
        pool_prefix = f"data/{namespace}/worldgen/template_pool/"
        structure_prefix = f"data/{namespace}/structures/"
        for name in archive.namelist():
            if name.startswith(pool_prefix) and name.endswith(".json"):
                key = namespace + ":" + name[len(pool_prefix):-5]
                pools[key] = json.loads(archive.read(name))
            elif namespace == "mvs" and name.startswith(structure_prefix) and name.endswith(".nbt"):
                key = name[len(structure_prefix):-4]
                structures[key] = jigsaws(parse_nbt(archive.read(name)))
    return pools, structures


def audit(root, upstream_pools, upstream_structures):
    pools = dict(upstream_pools)
    structures = dict(upstream_structures)
    for path in (root / "kubejs/data").glob("*/worldgen/template_pool/**/*.json"):
        relative = path.relative_to(root / "kubejs/data")
        key = relative.parts[0] + ":" + Path(*relative.parts[3:]).with_suffix("").as_posix()
        pools[key] = json.loads(path.read_text(encoding="utf-8"))
    structure_root = root / "kubejs/data/mvs/structures"
    overrides = list(structure_root.rglob("*.nbt"))
    for path in overrides:
        key = path.relative_to(structure_root).with_suffix("").as_posix()
        structures[key] = jigsaws(parse_nbt(path.read_bytes()))
    failures = []
    references = Counter()
    for name, blocks in structures.items():
        for block in blocks:
            pool = str(block.get("nbt", {}).get("pool", ""))
            references[pool] += 1
            if pool != "minecraft:empty" and (pool not in pools or not pools[pool].get("elements")):
                failures.append((name, tuple(map(int, block["pos"])), pool))
    print(f"AUDIT {root}: {len(overrides)} overrides, {len(structures)} effective structures, "
          f"{sum(references.values())} connectors, {len(references)} pool IDs")
    for name, position, pool in failures:
        print(f"  INVALID mvs:{name} {position}: {pool}")
    return len(failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="repair the documented cells")
    mode.add_argument("--check", action="store_true", help="read-only audit (default)")
    args = parser.parse_args()
    root = args.root.resolve()
    jars = list((root / "mods").glob("MoogsVoyagerStructures-*.jar"))
    if len(jars) != 1:
        raise ValueError(f"Expected exactly one MVS jar, found {jars}")
    vanilla = root / (root.name + ".jar")
    if not vanilla.is_file():
        raise ValueError(f"Vanilla resource jar missing: {vanilla}")
    pools, structures = jar_resources(jars[0], "mvs")
    vanilla_pools, _ = jar_resources(vanilla, "minecraft")
    pools.update(vanilla_pools)
    print(f"RESOURCES {jars[0].name}: {len(structures)} structures; "
          f"{len(pools)} MVS + vanilla pools")
    planned = []
    for structure in TARGETS:
        relative = Path("kubejs/data/mvs/structures") / (structure + ".nbt")
        raw = (root / relative).read_bytes()
        for mirror in OVERRIDES:
            path = root / mirror / relative
            if path.read_bytes() != raw:
                raise ValueError(f"Mirror has independent changes: {path}")
        updated, positions = repair(raw, structure)
        repeated, repeated_changes = repair(updated, structure)
        if repeated != updated or repeated_changes:
            raise AssertionError(f"Repair is not idempotent: {structure}")
        for mirror in OVERRIDES:
            path = root / mirror / relative
            planned.append((path, updated, positions))
            for position in positions:
                print(f"{'REPAIR' if args.write else 'PENDING'} {path.relative_to(root)} {position}")
    if args.write:
        for path, updated, positions in planned:
            if positions:
                path.write_bytes(updated)
                if path.read_bytes() != updated:
                    raise AssertionError(f"Write verification failed: {path}")
    pending = 0 if args.write else sum(len(positions) for _, _, positions in planned)
    for structure in TARGETS:
        relative = Path("kubejs/data/mvs/structures") / (structure + ".nbt")
        digests = {
            hashlib.sha256((root / mirror / relative).read_bytes()).hexdigest()
            for mirror in OVERRIDES
        }
        if len(digests) != 1:
            raise AssertionError(f"Mirror mismatch after repair: {structure}")
        print(f"SHA256 {relative.as_posix()} {next(iter(digests))}")
    failures = sum(audit(root / mirror, pools, structures) for mirror in OVERRIDES)
    print(f"RESULT pending_cells={pending} invalid_connectors={failures}; "
          "preservation, serialization and idempotence checks passed")
    return 1 if pending or failures else 0


if __name__ == "__main__":
    sys.exit(main())
