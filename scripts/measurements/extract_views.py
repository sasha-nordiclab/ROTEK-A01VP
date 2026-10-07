# Run inside FreeCAD (fdmkit run): projects body Pump into 4 views with hidden-line
# removal and dumps polylines (in screen mm, y down) plus all params to views.json.
import json
import FreeCAD as App
import TechDraw

OUT = '/Users/acidetch/SynologyDrive/3dprojects/FreeCad/TPU_Pump_Holder/scripts/measurements/views.json'
V = App.Vector
d = App.getDocument('TPU_Pump_Holder')
shape = d.getObject('Body').Shape
sheet = d.getObject('params')

# projected (X, Y) -> screen (sx, sy), y down; checked with a test box
VIEWS = {
    'A': ((0, 0, -1), lambda X, Y: (-X, Y)),   # mounting face, seen from the wall side
    'B': ((0, -1, 0), lambda X, Y: (Y, X)),    # side, outlet up, plate down
    'C': ((-1, 0, 0), lambda X, Y: (Y, X)),    # inlet end
    'D': ((1, 0, 0), lambda X, Y: (-Y, -X)),   # motor end
}
KINDS = {0: 'hard', 1: 'smooth', 3: 'outline'}


def polylines(comp, f):
    out = []
    if comp is None or comp.isNull():
        return out
    for e in comp.Edges:
        try:
            pts = e.discretize(Deflection=0.02)
        except Exception:
            continue
        out.append([[round(c, 2) for c in f(p.x, p.y)] for p in pts])
    return out


res = {'views': {}, 'params': {}}
for name, (dirv, f) in VIEWS.items():
    parts = TechDraw.projectEx(shape, V(*dirv))
    res['views'][name] = {k: polylines(parts[i], f) for i, k in KINDS.items()}

for c in sheet.getUsedCells():
    a = sheet.getAlias(c)
    if a:
        v = sheet.get(a)
        res['params'][a] = float(getattr(v, 'Value', v))

with open(OUT, 'w') as fh:
    json.dump(res, fh)
summary = {n: {k: len(v) for k, v in vv.items()} for n, vv in res['views'].items()}
