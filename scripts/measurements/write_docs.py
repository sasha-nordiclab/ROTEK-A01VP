"""Writes docs/measurements/: the four view SVGs and measurements.md (model vs the last readings).

Run after build_page.py. Readings come from docs/measurements/readings.json, a snapshot of the
live sheet's `meas` collection.
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'measurements'))
ROWS = json.load(open(os.path.join(HERE, 'rows.json')))
RD = json.load(open(os.path.join(DOCS, 'readings.json')))
MEAS = RD['values']

for v in 'ABCD':
    shutil.copy(os.path.join(HERE, f'view_{v}.svg'), DOCS)

TITLES = {
    'A': 'A — Mounting face (seen from the wall side, inlet to the left)',
    'B': 'B — Side (mounting face on the table, outlet up)',
    'C': 'C — Inlet end',
    'D': 'D — Motor end',
}


def num(v):
    return '—' if v is None else f'{v:g}'


out = [
    '# Pump measurement sheet',
    '',
    'Numbered dimensions of the `Pump` reference model in `cad/TPU_Pump_Holder.FCStd`, checked against the real Rotek WPDC-06.7L pump.',
    'The live sheet with input fields is at https://claude.ai/artifact/8BBLBfdxXsbRfHfFudTgku; values typed there are saved and read back to correct the model.',
    f'Readings below: round {RD["round"]}, {RD["date"]}.',
    '',
    '## How to measure',
    '',
    '- **Heights:** stand the pump on a flat table with the mounting face down and measure from the table with the depth rod, or with outside jaws from the plate frame.',
    '- **Lengths along the pump:** from the tip of the inlet barb.',
    '- **Priority A** rows shape the holder (plate, slots, outer size, outlet, cable); **B** rows refine the shape.',
    '- **Tolerance:** ±0.10 mm for A, ±0.20 mm for B. Δ is the reading minus the model; ✗ marks a Δ past tolerance. Rows marked *check* are to measure next.',
]
for v in 'ABCD':
    out += ['', f'## {TITLES[v]}', '', f'![View {v}](view_{v}.svg)', '',
            '| ID | Prio | Dimension | How | Model | Drawing | Reading | Δ | Source |',
            '|---|---|---|---|---|---|---|---|---|']
    for r in ROWS:
        if r['view'] != v:
            continue
        m = MEAS.get(r['id'])
        if m is None:
            d = ''
        else:
            dv = m - r['model']
            tol = 0.1 if r['prio'] == 'A' else 0.2
            d = f'{dv:+.2f}' + (' ✗' if abs(dv) > tol + 1e-9 else '')
        src = r['source'] + (' — *check*' if r['check'] else '')
        out.append(f"| {r['id']} | {r['prio']} | {r['label']} | {r['how']} | {num(r['model'])} | {num(r['drawing'])} | {num(m)} | {d} | {src} |")
open(os.path.join(DOCS, 'measurements.md'), 'w').write('\n'.join(out) + '\n')
print('measurements.md:', len(ROWS), 'rows,', len(MEAS), 'readings')
