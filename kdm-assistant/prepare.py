"""Prepare local source assets from the existing page map and rendered scans."""
from pathlib import Path
import json
import re
import shutil
from records import RECORDS

ROOT = Path(__file__).resolve().parent

def prepare():
    data = ROOT / 'data'
    pages = data / 'pages'
    pages.mkdir(parents=True, exist_ok=True)
    map_path = ROOT.parent / 'KDM_Rules_Focused_Page_Map.md'
    mapping = [(int(a), int(b), None if c == 'Unnumbered' else int(c)) for a, b, c in re.findall(r'^\| (\d+) \| (\d+) \| (\d+|Unnumbered) \|', map_path.read_text(encoding='utf-8'), re.M)]
    if len(mapping) != 138:
        raise ValueError('Expected 138 retained source pages')
    by_source = {r['original']: r for r in RECORDS}
    manifest = []
    for revised, original, printed in mapping:
        source = ROOT.parent.parent / 'work' / 'pdf-triage' / f'page-{original:03}.jpg'
        target = pages / f'{revised}.jpg'
        if not target.exists():
            shutil.copy2(source, target)
        record = by_source.get(original)
        manifest.append({'revised': revised, 'original': original, 'printed': printed, 'edition': '1.5', 'title': record['title'] if record else 'Table of contents' if revised == 1 else 'Strain System' if revised == 2 else f'Book page {printed}', 'reviewed': bool(record), 'record_id': record['id'] if record else None})
    (data / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    retained_by_original = {p['original']: p for p in manifest}
    all_pages = []
    for original in range(1, 240):
        retained = retained_by_original.get(original)
        all_pages.append({'original': original, 'keep': bool(retained), 'revised': retained['revised'] if retained else None, 'printed': retained['printed'] if retained else None, 'status': 'reviewed record' if retained and retained['reviewed'] else 'retained image; extraction pending' if retained else 'excluded in approved triage'})
    (data / 'source-manifest.json').write_text(json.dumps(all_pages, indent=2), encoding='utf-8')
    print(f'Prepared {len(manifest)} page images and {len(RECORDS)} reviewed records.')

if __name__ == '__main__':
    prepare()
