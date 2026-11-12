#!/usr/bin/env python3
"""Apply personal market rewards without reformatting existing FTBQ chapters.

The game normalizes chapter formatting when saving. This patch generator uses
the existing SNBT parser and token offsets to retain those bytes and all IDs.
Run after the full chapter generators; --check validates without writing.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_astral_sorcery_chapter as astral
import build_thaumic_industry_chapter as thaumic
import build_tinkers_chapter as tinkers

TOOLS = Path(__file__).resolve().parent
QUESTS = TOOLS.parent / 'quests'
MAP = TOOLS / 'market_theme_unlock_ids.json'
SALT = 'sunlitmarket-theme-unlocks-v1'


class SpannedSnbtParser(astral.SnbtParser):
    def __init__(self, text):
        super().__init__(text)
        self.offsets = [m.span() for m in self.token.finditer(text)
                        if not m.group().isspace() and not m.group().startswith(('#', '//', '/*'))]
        self.spans = {}

    def value(self):
        start = self.i
        value = super().value()
        if isinstance(value, (dict, list)):
            self.spans[id(value)] = (self.offsets[start][0], self.offsets[self.i - 1][1])
        return value


def command_reward(reward_id, unlock, title):
    return dict(id=reward_id, type='command',
                command='execute as {p} run sunlitmarket unlock ' + unlock,
                title=title, elevate_perms=True, silent=True,
                team_reward=False, auto='no_toast')


def edit_quest(raw, quest_id, reward=None, description=None, append_description=None):
    text = raw.decode('utf-8')
    parser = SpannedSnbtParser(text)
    before = parser.parse()
    matches = [q for q in before['quests'] if q['id'] == quest_id]
    if len(matches) != 1:
        raise ValueError('Milestone quest missing or repeated: ' + quest_id)
    quest = matches[0]
    expected = copy.deepcopy(before)
    target = next(q for q in expected['quests'] if q['id'] == quest_id)
    edits = []
    if reward:
        current = [r for r in quest.get('rewards', ()) if r['id'] == reward['id']]
        if current and current != [reward]:
            raise ValueError('Existing market reward differs: ' + reward['id'])
        if not current:
            if any(r.get('command') == reward['command'] for r in quest.get('rewards', ())):
                raise ValueError('Unlock already uses a different reward ID: ' + quest_id)
            target.setdefault('rewards', []).append(reward)
            rendered = astral.dump(reward, 4)
            if 'rewards' in quest:
                _, end = parser.spans[id(quest['rewards'])]
                insert = (',' if quest['rewards'] else '') + '\n\t\t\t\t' + rendered + '\n\t\t\t'
                edits.append((end - 1, end - 1, insert))
            else:
                _, end = parser.spans[id(quest)]
                line = text.rfind('\n', 0, end - 1) + 1
                edits.append((line, line, '\t\t\trewards: [\n\t\t\t\t' + rendered + '\n\t\t\t]\n'))
    if append_description and append_description not in quest.get('description', ()):
        description = list(quest.get('description', ())) + [append_description]
    if description is not None and quest.get('description') != description:
        if 'description' not in quest:
            raise ValueError('Expected existing description: ' + quest_id)
        start, end = parser.spans[id(quest['description'])]
        edits.append((start, end, astral.dump(description, 3)))
        target['description'] = description
    for start, end, value in sorted(edits, reverse=True):
        text = text[:start] + value + text[end:]
    if astral.SnbtParser(text).parse() != expected:
        raise ValueError('Lossless patch changed unrelated quest data: ' + quest_id)
    return text.encode('utf-8')


def native_maps():
    result = {}
    t = json.loads(tinkers.MAP.read_text(encoding='utf-8'))
    t['ids'] = dict(sorted(tinkers.allocate().items()))
    result[tinkers.MAP] = t
    a = json.loads(astral.MAP.read_text(encoding='utf-8'))
    external, _, _, _ = astral.scan()
    a['ids'] = dict(sorted(astral.allocate(a, astral.keys_for(astral.content()), external).items()))
    result[astral.MAP] = a
    h = json.loads(thaumic.MAP.read_text(encoding='utf-8'))
    h['ids'] = dict(sorted(thaumic.allocate(thaumic.get_keys(), thaumic.external_ids()).items()))
    result[thaumic.MAP] = h
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    maps = native_maps()
    old = json.loads(MAP.read_text(encoding='utf-8')) if MAP.exists() else {}
    if old and (old.get('schema') != 1 or old.get('salt') != SALT):
        raise ValueError('Market theme ID map owner changed')
    own_key = 'reward/botania/terrasteel/unlock/theme.botania.adept'
    own_id = '%016X' % (int.from_bytes(hashlib.sha256((SALT + ':' + own_key).encode()).digest()[:8], 'big') & 0x7FFFFFFFFFFFFFFF)
    if old.get('ids', {}).get(own_key, own_id) != own_id:
        raise ValueError('Botania reward ID drift')
    specs = []
    for module, key, title, note in (
            (tinkers, 'advanced', '解锁匠魂高阶材料贸易', '完成后解锁匠魂主题商人的高阶材料报价；声望和每日库存限制仍然生效。'),
            (astral, 'metal', '解锁星辉金属贸易', '完成后解锁星辉主题商人的星辉锭报价；声望和每日库存限制仍然生效。'),
            (thaumic, 'template_2', '解锁神秘虚空金属贸易', '完成后解锁神秘主题商人的虚空锭报价；先取得虚空金属并完成本模板，不会在神秘锭入门阶段提前开放。')):
        unlock = module.THEME_UNLOCKS[key]
        ids = maps[module.MAP]['ids']
        specs.append(dict(chapter=module.OUTPUT.name, quest=ids['quest/' + key],
                          reward=command_reward(ids['reward/' + key + '/unlock/' + unlock], unlock, title),
                          unlock=unlock, description=note))
    specs.append(dict(chapter='botania.snbt', quest='46F86152B5B36A3B',
                      reward=command_reward(own_id, 'theme.botania.adept', '解锁植物魔法高阶材料贸易'),
                      unlock='theme.botania.adept',
                      description='取得泰拉钢后解锁植物魔法主题商人的高阶材料报价；声望和每日库存限制仍然生效。'))
    output = {}
    for spec in specs:
        path = QUESTS / 'chapters' / spec['chapter']
        raw = path.read_bytes()
        output[path] = edit_quest(raw, spec['quest'], spec['reward'], append_description=spec['description'])
        if edit_quest(output[path], spec['quest'], spec['reward'], append_description=spec['description']) != output[path]:
            raise ValueError('Patch is not idempotent: ' + spec['chapter'])
    # Updating the digest adopts the current game-normalized file; no layout,
    # item-stack serialization, quest/task ID, or other chapter field is changed.
    for path, doc in maps.items():
        chapter = {'tinkers_ids.json': tinkers.OUTPUT, 'astral_sorcery_ids.json': astral.OUTPUT,
                   'thaumic_industry_ids.json': thaumic.OUTPUT}[path.name]
        if 'output_sha256' in doc:
            doc['output_sha256'] = hashlib.sha256(output[chapter]).hexdigest()
        original = json.loads(path.read_text(encoding='utf-8'))
        if any(doc['ids'].get(k) != v for k, v in original['ids'].items()):
            raise ValueError('Existing semantic ID changed: ' + path.name)
        output[path] = (json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    registry = dict(schema=1, salt=SALT, ids={own_key: own_id},
                    milestones=[{k: s[k] for k in ('chapter', 'quest', 'unlock')} | {'reward': s['reward']['id']} for s in specs])
    output[MAP] = (json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    counts = {}
    for path in sorted(QUESTS.rglob('*.snbt')):
        doc = astral.SnbtParser(output.get(path, path.read_bytes()).decode('utf-8-sig')).parse()
        for node in astral.walk(doc):
            value = node.get('id')
            if isinstance(value, str) and astral.valid_id(value):
                counts[value] = counts.get(value, 0) + 1
    for spec in specs:
        if counts.get(spec['reward']['id']) != 1:
            raise ValueError('Market reward ID collision: ' + spec['reward']['id'])
    changed = [str(p.relative_to(TOOLS.parent)) for p, b in output.items() if not p.exists() or p.read_bytes() != b]
    if args.check:
        missing = [str(p) for p, b in output.items() if not p.exists() or p.read_bytes() != b]
        if missing:
            raise ValueError('Run generation after review: ' + ', '.join(missing))
    else:
        for path, data in output.items():
            if not path.exists() or path.read_bytes() != data:
                path.write_bytes(data)
    print(json.dumps(dict(mode='check' if args.check else 'write', milestones=registry['milestones'],
                          unique_definitions=len(counts), idempotent=True, changed=changed), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
