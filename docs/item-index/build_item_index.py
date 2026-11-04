"""Build the pack-wide item/block/fluid/entity name + description index (zh_cn / en_us).

Static sources, in Minecraft override order (later wins):
  1. every top-level mods/*.jar (not *.bak) and their META-INF/jarjar/*.jar
  2. enabled resource packs from options.txt (resourcePacks order)
  3. kubejs/assets/*/lang (KubeJS resource pack, loaded on top)
Optional runtime source: runtime_names.json (Rosetta dump of serialized hover-name components from a test
server). It resolves names GT builds at runtime (material dusts/plates/fluids) that have no per-item lang key.

Usage:  python -I docs/item-index/build_item_index.py
Outputs next to this script: item_index.csv (UTF-8 BOM, opens in Excel), magic_index.csv, lang_conflicts.csv
"""
from pathlib import Path
import csv
import io
import json
import re
import sys
import zipfile

HERE = Path(__file__).resolve().parent
PACK = HERE.parent.parent
LANGS = ('en_us', 'zh_cn')
MAGIC_NS = {'thaumcraft', 'forbidden_magic', 'taintedmagic', 'tainted_magic', 'thaumictinkerer', 'thaumic_tinkerer',
            'thaumicbases', 'thaumic_bases', 'warptheory', 'warp_theory', 'isorropia', 'pollution', 'thaumadds',
            'thaumicenergistics', 'thaumic_energistics', 'astralsorcery', 'applied_astralsorcery', 'botania',
            'me_thaumaturgy', 'mett', 'thaumcraft_client_tweaks'}
DESC_WORDS = ('tooltip', 'desc', 'lore', 'info', 'hint', 'jei', 'usage', 'flavor')

lang = {code: {} for code in LANGS}
origin = {}
conflicts = []


def load_lang_bytes(data, label, code):
    try:
        table = json.loads(data.decode('utf-8-sig'))
    except Exception:
        return
    if not isinstance(table, dict):
        return
    target = lang[code]
    for key, value in table.items():
        if not isinstance(value, str):
            continue
        if code == 'zh_cn' and key in target and target[key] != value:
            conflicts.append((key, origin.get(('zh', key), ''), label))
        target[key] = value
        origin[('zh' if code == 'zh_cn' else 'en', key)] = label


LANG_RE = re.compile(r'^assets/([^/]+)/lang/(en_us|zh_cn)\.json$', re.I)


def scan_zip(zf, label):
    names = zf.namelist()
    for name in names:
        match = LANG_RE.match(name)
        if match:
            load_lang_bytes(zf.read(name), label, match.group(2).lower())
    for name in names:
        if name.startswith('META-INF/jarjar/') and name.endswith('.jar'):
            try:
                with zipfile.ZipFile(io.BytesIO(zf.read(name))) as inner:
                    scan_zip(inner, label + '!' + name.rsplit('/', 1)[-1])
            except zipfile.BadZipFile:
                pass


mods = sorted((PACK / 'mods').glob('*.jar'))
for jar in mods:
    try:
        with zipfile.ZipFile(jar) as zf:
            scan_zip(zf, jar.name)
    except zipfile.BadZipFile:
        print('skip bad jar', jar.name, file=sys.stderr)

options = PACK / 'options.txt'
if options.exists():
    match = re.search(r'^resourcePacks:(\[.*\])$', options.read_text(encoding='utf-8', errors='replace'), re.M)
    for entry in (json.loads(match.group(1)) if match else []):
        if entry.startswith('file/'):
            pack = PACK / 'resourcepacks' / entry[5:]
            if pack.is_file() and zipfile.is_zipfile(pack):
                with zipfile.ZipFile(pack) as zf:
                    scan_zip(zf, 'resourcepack:' + pack.name)

for f in sorted((PACK / 'kubejs' / 'assets').glob('*/lang/*.json')):
    if f.stem.lower() in LANGS:
        load_lang_bytes(f.read_bytes(), 'kubejs:' + f.parent.parent.name, f.stem.lower())

# Entries: one per registry name that has a direct lang key.
KIND_RE = re.compile(r'^(item|block|fluid|fluid_type|entity)\.([a-z0-9_-]+)\.([a-z0-9_/-]+)$')
entries = {}
for key in set(lang['en_us']) | set(lang['zh_cn']):
    match = KIND_RE.match(key)
    if not match:
        continue
    kind, ns, path = match.groups()
    kind = 'fluid' if kind == 'fluid_type' else kind
    rid = ns + ':' + path
    entries.setdefault((kind, rid), {'kind': kind, 'id': rid, 'ns': ns, 'path': path, 'key': key})


def render(comp, code, depth=0):
    """Render a serialized Minecraft text component with one language table."""
    if depth > 8:
        return ''
    if isinstance(comp, str):
        return comp
    if isinstance(comp, list):
        return ''.join(render(c, code, depth + 1) for c in comp)
    if not isinstance(comp, dict):
        return ''
    text = ''
    if 'translate' in comp:
        key = comp['translate']
        pattern = lang[code].get(key) or lang['en_us'].get(key) or comp.get('fallback') or key
        args = [render(a, code, depth + 1) for a in comp.get('with', [])]
        counter = iter(range(len(args)))

        def substitute(m):
            if m.group(0) == '%%':
                return '%'
            index = int(m.group(1)) - 1 if m.group(1) else next(counter, None)
            return args[index] if index is not None and 0 <= index < len(args) else ''
        text = re.sub(r'%(?:(\d+)\$)?[sd%]', substitute, pattern)
    elif 'text' in comp:
        text = comp['text']
    for extra in comp.get('extra', []):
        text += render(extra, code, depth + 1)
    return text


runtime = HERE / 'runtime_names.json'
if runtime.exists():
    for row in json.loads(runtime.read_text(encoding='utf-8')).get('entries', []):
        kind, rid = row['kind'], row['id']
        ns, path = rid.split(':', 1)
        entry = entries.setdefault((kind, rid), {'kind': kind, 'id': rid, 'ns': ns, 'path': path, 'key': row.get('key', '')})
        entry['runtime'] = True
        comp = json.loads(row['name']) if isinstance(row.get('name'), str) else row.get('name')
        if comp is not None:
            entry['rt_en'] = render(comp, 'en_us')
            entry['rt_zh'] = render(comp, 'zh_cn')
        if row.get('tooltip'):
            entry['rt_tip'] = row['tooltip']

# Description keys indexed by every dot/colon/slash token so lookup per item stays cheap.
desc_keys = {}
for key in set(lang['en_us']) | set(lang['zh_cn']):
    low = key.lower()
    if any(word in low for word in DESC_WORDS):
        for token in set(re.split(r'[.:/]', low)):
            if token:
                desc_keys.setdefault(token, []).append(key)


def descriptions(entry):
    base, path, ns = entry.get('key', ''), entry['path'], entry['ns']
    found = set()
    for key in desc_keys.get(path, []):
        if (base and key.startswith(base + '.')) or (ns in key and ('.' + path + '.' in '.' + key + '.')):
            found.add(key)
    found = sorted(found)[:6]
    zh = ' | '.join(lang['zh_cn'][k] for k in found if lang['zh_cn'].get(k))
    en = ' | '.join(lang['en_us'][k] for k in found if lang['en_us'].get(k))
    return zh, en


def clean(text):
    return re.sub(r'§.', '', text or '').replace('\n', ' ').strip()


rows = []
for (kind, rid), entry in sorted(entries.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    key = entry.get('key', '')
    zh_desc, en_desc = descriptions(entry)
    if entry.get('rt_tip') and not en_desc:
        en_desc = entry['rt_tip']
    rows.append({
        'namespace': entry['ns'], 'id': rid, 'kind': kind,
        'zh_cn': clean(lang['zh_cn'].get(key) or entry.get('rt_zh', '')),
        'en_us': clean(lang['en_us'].get(key) or entry.get('rt_en', '')),
        'zh_desc': clean(zh_desc), 'en_desc': clean(en_desc), 'lang_key': key,
        'in_test_registry': 'yes' if entry.get('runtime') else '',
        'source': origin.get(('en', key)) or origin.get(('zh', key)) or 'runtime'})

FIELDS = ['namespace', 'id', 'kind', 'zh_cn', 'en_us', 'zh_desc', 'en_desc', 'lang_key', 'in_test_registry', 'source']


def write(name, data):
    with open(HERE / name, 'w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(data)


write('item_index.csv', rows)
write('magic_index.csv', [r for r in rows if r['namespace'] in MAGIC_NS])
with open(HERE / 'lang_conflicts.csv', 'w', encoding='utf-8-sig', newline='') as handle:
    writer = csv.writer(handle)
    writer.writerow(['key', 'earlier_source', 'overridden_by'])
    writer.writerows(conflicts)

kinds = {}
for r in rows:
    kinds[r['kind']] = kinds.get(r['kind'], 0) + 1
print('jars', len(mods), 'rows', len(rows), kinds,
      'magic', sum(1 for r in rows if r['namespace'] in MAGIC_NS),
      'with_zh', sum(1 for r in rows if r['zh_cn']),
      'with_desc', sum(1 for r in rows if r['zh_desc'] or r['en_desc']),
      'runtime', sum(1 for r in rows if r['in_test_registry']))
