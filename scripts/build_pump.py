#!/usr/bin/env python3
"""Rebuild the Pump reference body from scratch in the running FreeCAD.

Every step is an fdmkit run() batch sent over XML-RPC; the run stops at the first ERR.
Symmetry is native PartDesign: one slot corner + MultiTransform (two mirrors), the
+Y pockets + Mirrored, one ear (lug, screw head, partition) + PolarPattern x4 around
the pump axis, one face partition + PolarPattern x4 with the one under the outlet
suppressed.

  python3 scripts/build_pump.py            closes TPU_Pump_Holder and rebuilds it
"""
import os
import sys
import xmlrpc.client

URL = os.environ.get('FREECAD_RPC', 'http://127.0.0.1:9875')
MOD = os.path.expanduser('~/Library/Application Support/FreeCAD/v26-3/Mod/fdmkit')
HERE = os.path.dirname(os.path.abspath(__file__))
FCSTD = os.path.normpath(os.path.join(HERE, '..', 'cad', 'TPU_Pump_Holder.FCStd'))
DOC = 'TPU_Pump_Holder'

# ------------------------------------------------------------------ params
# (name, value or formula, description); None as name starts a group header
PARAMS = [
    (None, 'MOTOR AND HEAD', None),
    ('p_len', 75, 'Inlet tip to the motor end face, grommet excluded (drawing)'),
    ('p_d', 36.7, 'Motor diameter (caliper 36.72)'),
    ('head_d', 40.3, 'Pump head diameter (caliper 40.29)'),
    ('head_x0', 16.5, 'Inlet tip to the ear-lug face of the head (drawing 22 - 5.5)'),
    ('head_x1', 32, 'Inlet tip to the joint between head and motor (drawing 22 + 10)'),
    ('cap_d', 33.6, 'Motor end face diameter inside the end step (photo)'),
    ('cap_len', 2.4, 'Length of the step at the motor end (estimate)'),
    (None, 'EARS', None),
    ('ear_lk', 42.4, 'Bolt circle of the four head screws (drawing)'),
    ('ear_r', 3.35, 'Ear lug radius (drawing R3.35)'),
    ('ear_a', 35, 'Ear angle from the vertical, deg (drawing)'),
    ('ear_span', 42, 'Mounting face to the far edge of the farthest ear lug (drawing)'),
    ('scr_d', 5, 'Screw head diameter (photo estimate)'),
    ('scr_h', 2.2, 'Screw head height above the ear lug (estimate)'),
    (None, 'INLET', None),
    ('in_d', 14.4, 'Inlet barb diameter (drawing)'),
    ('in_len', 4, 'Inlet barb length (drawing)'),
    ('neck_d', 13.4, 'Inlet neck diameter (drawing)'),
    ('neck_len', 7, 'Inlet neck length (drawing)'),
    ('boss_d', 23, 'Boss around the inlet (drawing)'),
    ('cone_len', 2.5, 'Cone from the neck to the boss (drawing estimate)'),
    (None, 'INLET FACE', None),
    ('cov_d', 31.99, 'Raised cover on the inlet face (caliper)'),
    ('rib_t', 2.17, 'Partition width on the inlet face (caliper)'),
    ('rib_h', 1.5, 'Partition height = depth of the recessed segments and ear-lug faces (caliper)'),
    ('rib_a', 12, 'Angle of the first face partition from the +Y axis, deg (photo)'),
    (None, 'OUTLET', None),
    ('out_d', 8, 'Outlet barb diameter (drawing)'),
    ('out_len', 5, 'Outlet barb length (drawing)'),
    ('out_d2', 7, 'Outlet tube diameter below the barb (drawing)'),
    ('out_reach', 52, 'Mounting face to the outlet tip (drawing)'),
    ('out_x', 16.5, 'Inlet tip to the outlet axis (drawing 22 - 5.5)'),
    ('out_y', -8, 'Outlet axis offset from the pump axis along Y (drawing and photos)'),
    (None, 'CABLE GROMMET', None),
    ('grm_y', -9.3, 'Wire hole offset from the pump axis along Y, at axis height (photo)'),
    ('grm_z', -3.8, 'Grommet centre below the wire hole (photo)'),
    ('grm_w', 8.8, 'Grommet width (photo)'),
    ('grm_l', 16.4, 'Grommet length, figure-8 of two discs (photo)'),
    ('grm_t', 1.5, 'Grommet height above the motor end face (estimate)'),
    (None, 'MOUNT PLATE', None),
    ('fl_w', 45, 'Plate width across the slotted edges (caliper 44.93)'),
    ('fl_len', 32, 'Plate length along the pump axis (caliper 32.03)'),
    ('fl_t', 3.0, 'Plate thickness at the edge (caliper 2.98)'),
    ('web_w', 13, 'Web between plate and motor (drawing estimate)'),
    ('web_h', 1.5, 'Web height above the plate back (estimate)'),
    (None, 'SLOTS', None),
    ('hole_x0', 39, 'Inlet tip to the inlet-side slot centre (drawing)'),
    ('hole_dx', 20, 'Slot pitch along the axis (drawing, caliper 23.36 - 3.24)'),
    ('hole_dy', 35, 'Slot pitch across the plate (drawing)'),
    ('hole_d', 3.3, 'Slot width (drawing; caliper 3.24 to 3.39)'),
    ('hook_l', 5.46, 'Slot length along the axis, hook included (caliper)'),
    ('slot_ov', 2, 'Cutter overshoot past the plate edge (construction)'),
    (None, 'POCKETS', None),
    ('pk_d', 1.5, 'Depth of the side and outer pockets (caliper)'),
    ('pk_dc', 2.5, 'Depth of the centre pockets (caliper)'),
    ('rib', 1.8, 'Rib between pockets (photo)'),
    ('frame', 1.4, 'Frame along the slotted edges (photo)'),
    ('pk_fi', 1.2, 'Frame at the inlet end (photo)'),
    ('pk_fm', 1.6, 'Frame at the motor end (photo)'),
    ('pk_h', 6.3, 'Pocket length along the axis, three inlet-side rows (photo)'),
    ('pk_c3w', 10.2, 'Centre pocket width (photo)'),
    ('pk_c2w', 4.0, 'Side pocket width (photo)'),
    ('pk_fr', 2.2, 'Radius of the outer pockets around the slot hooks (photo)'),
    ('pk_r', 0.8, 'Corner radius of the rectangular pockets (photo)'),
    (None, 'DERIVED', None),
    ('ax_h', 'ear_span - ear_lk/2*cos(ear_a) - ear_r', 'Pump axis height above the mounting face'),
    ('x_tip', '-(hole_x0 + hole_dx/2)', 'X of the inlet tip; origin is the slot pattern centre'),
    ('fl_x0', 'hole_x0 + hole_dx/2 - fl_len/2', 'Inlet tip to the plate (plate symmetric about the slots)'),
    ('x_fs', 'x_tip + fl_x0', 'X of the inlet-end plate edge'),
    ('x_fe', 'x_tip + fl_x0 + fl_len', 'X of the motor-end plate edge'),
    ('cov_t', 'rib_h', 'Cover height above the recessed face = partition height'),
    ('pk_c2a', 'pk_c3w/2 + rib', 'Side pockets, inner Y'),
    ('pk_c2b', 'pk_c2a + pk_c2w', 'Side pockets, outer Y'),
    ('pk_c1a', 'pk_c2b + rib', 'Outer pockets, inner Y'),
    ('pk_c1b', 'fl_w/2 - frame', 'Outer pockets, outer Y'),
    ('pk_hx', 'hole_dx/2 + hole_d/2 - hook_l - rib', 'Outer pockets stop this far from X 0 beside the hooks'),
    ('pk_hy', 'hole_dy/2 - hole_d/2 - rib', 'Outer pockets reach this Y beside the hooks'),
    ('pk_ra0', 'x_fs + pk_fi', 'Row A (inlet end) start X'),
    ('pk_ra1', 'pk_ra0 + pk_h', 'Row A end X'),
    ('pk_rb0', 'pk_ra1 + rib', 'Row B start X'),
    ('pk_rb1', 'pk_rb0 + pk_h', 'Row B end X'),
    ('pk_rc0', 'pk_rb1 + rib', 'Row C start X'),
    ('pk_rc1', 'pk_rc0 + pk_h', 'Row C end X'),
    ('pk_rd0', 'pk_rc1 + rib', 'Row D (motor end) start X'),
    ('pk_rd1', 'x_fe - pk_fm', 'Row D end X'),
]


def params_batch():
    lines = ['import FreeCAD as App, FreeCADGui as Gui',
             's = App.ActiveDocument.getObject("params")',
             'nxt = lambda: 1 + max([int("".join(ch for ch in c if ch.isdigit())) for c in s.getUsedCells()] or [0])']
    for name, val, desc in PARAMS:
        if name is None:
            lines.append(f'r = nxt(); s.set(f"A{{r}}", {val!r}); s.setStyle(f"A{{r}}", "bold")')
            continue
        arg = repr(val) if isinstance(val, str) else repr(float(val) if isinstance(val, float) else val)
        lines.append(f'P({name}={arg})')
        lines.append(f'r = int(s.getCellFromAlias({name!r})[1:]); s.set(f"C{{r}}", {desc!r})')
    lines.append('s.setColumnWidth("A", 110); s.setColumnWidth("C", 520)')
    lines.append('App.ActiveDocument.recompute()')
    lines.append("P('ax_h', 'x_fs', 'x_fe', 'pk_rd0', 'pk_hx', 'pk_hy')")
    return '\n'.join(lines)


def ring_poly(sk, t, r1, r2, w='rib_t'):
    """Radial bar in a YZ sketch around the pump axis: angle t from +Y, radii r1..r2, width w."""
    pts = [(f'({r1})*cos({t}) + {w}/2*sin({t})', f'ax_h + ({r1})*sin({t}) - {w}/2*cos({t})'),
           (f'({r2})*cos({t}) + {w}/2*sin({t})', f'ax_h + ({r2})*sin({t}) - {w}/2*cos({t})'),
           (f'({r2})*cos({t}) - {w}/2*sin({t})', f'ax_h + ({r2})*sin({t}) + {w}/2*cos({t})'),
           (f'({r1})*cos({t}) - {w}/2*sin({t})', f'ax_h + ({r1})*sin({t}) + {w}/2*cos({t})')]
    return f'poly({sk!r}, {pts!r})'


def rect_fillets(sk, x0, x1, y0, y1):
    return '; '.join(f'fil({sk!r}, ({x!r}, {y!r}), "pk_r")' for x in (x0, x1) for y in (y0, y1))


ROWS = [('pk_ra0', 'pk_ra1'), ('pk_rb0', 'pk_rb1'), ('pk_rc0', 'pk_rc1'), ('pk_rd0', 'pk_rd1')]

HELPERS = '''import FreeCAD as App
d = App.ActiveDocument
b = d.getObject("Body")
org = lambda role: [f for f in b.Origin.OriginFeatures if f.Role == role][0]
def done(f, prev):
    d.recompute()
    assert b.Tip == f, ("tip", b.Tip.Name)
    assert f.BaseFeature == prev[0], ("base", f.BaseFeature.Name if f.BaseFeature else None)
    bad = [o.Name for o in d.Objects if "Invalid" in o.State or "Error" in o.State]
    assert not bad, bad
    assert f.Shape.isValid() and len(f.Shape.Solids) == 1, (f.Name, len(f.Shape.Solids))
    for o in prev: o.Visibility = False
    f.Visibility = True
    return f"{f.Name}: OK V {f.Shape.Volume:.1f}"
'''

BATCHES = [
    # 0: fresh document
    f'new({DOC!r}); import FreeCAD as App; App.ActiveDocument.saveAs({FCSTD!r})',
    # 1: params with groups and descriptions
    params_batch(),
    # 2: plate, web, motor, end step, head
    "sk('s_plate','XY'); rect('s_plate','fl_len','fl_w','x_fs + fl_len/2',0); pad('s_plate','fl_t','plate'); "
    "sk('s_web','XY'); rect('s_web','fl_len','web_w','x_fs + fl_len/2',0); pad('s_web','fl_t + web_h','web'); "
    "plane('pl_motor','YZ','x_tip + head_x1'); sk('s_motor','pl_motor'); circ('s_motor','p_d',0,'ax_h'); pad('s_motor','p_len - head_x1 - cap_len','motor'); "
    "plane('pl_end','YZ','x_tip + p_len - cap_len'); sk('s_end','pl_end'); circ('s_end','cap_d',0,'ax_h'); pad('s_end','cap_len','motor_end'); "
    "plane('pl_head','YZ','x_tip + head_x0'); sk('s_head','pl_head'); circ('s_head','head_d',0,'ax_h'); pad('s_head','head_x1 - head_x0','head')",
    # 3: pump axis datum line
    HELPERS + '''ln = b.newObject("PartDesign::Line", "pump_axis")
ln.AttachmentSupport = [(org("X_Axis"), "")]
ln.MapMode = "ObjectX"
ln.setExpression(".AttachmentOffset.Base.y", "params.ax_h")
d.recompute()
ln.Visibility = False
"pump_axis: base " + str(tuple(round(c, 3) for c in ln.Placement.Base)) + " dir " + str(tuple(round(c, 3) for c in ln.Placement.Rotation.multVec(App.Vector(0, 0, 1))))''',
    # 4: one ear: lug, screw head, partition to the lug (ear B, at 90 - ear_a from +Y)
    "sk('s_ear','pl_head'); circ('s_ear','2*ear_r','ear_lk/2*sin(ear_a)','ax_h + ear_lk/2*cos(ear_a)'); pad('s_ear','head_x1 - head_x0','ear_lug'); "
    "sk('s_screw','pl_head'); circ('s_screw','scr_d','ear_lk/2*sin(ear_a)','ax_h + ear_lk/2*cos(ear_a)'); pad('s_screw','scr_h','ear_screw',reverse=True); "
    "sk('s_ear_rib','pl_head'); " + ring_poly('s_ear_rib', '(90 - ear_a)', 'cov_d/2 - 0.5', 'ear_lk/2') + "; pad('s_ear_rib','rib_h','ear_rib',reverse=True)",
    # 5: four ears by polar pattern around the pump axis
    HELPERS + '''pp = d.addObject("PartDesign::PolarPattern", "ears")
pp.Originals = [d.ear_lug, d.ear_screw, d.ear_rib]
b.addObject(pp)
pp.Axis = (d.pump_axis, [""])
pp.Angle = 360
pp.Occurrences = 4
done(pp, [d.ear_rib, d.ear_screw, d.ear_lug])''',
    # 6: raised cover and one face partition
    "plane('pl_cover','YZ','x_tip + head_x0 - cov_t'); sk('s_cover','pl_cover'); circ('s_cover','cov_d',0,'ax_h'); pad('s_cover','cov_t','cover'); "
    "sk('s_face_rib','pl_head'); " + ring_poly('s_face_rib', 'rib_a', 'cov_d/2 - 0.5', 'head_d/2') + "; pad('s_face_rib','rib_h','face_rib',reverse=True)",
    # 7: four face partitions, the one under the outlet (rib_a + 90) suppressed
    HELPERS + '''import math
pp = d.addObject("PartDesign::PolarPattern", "face_ribs")
pp.Originals = [d.face_rib]
b.addObject(pp)
pp.Axis = (d.pump_axis, [""])
pp.Angle = 360
pp.Occurrences = 4
d.recompute()
P = d.getObject("params")
ax, x0, rt, rh, ra = (float(getattr(P.get(n), "Value", P.get(n))) for n in ("ax_h", "x_tip", "head_x0", "rib_h", "rib_a"))
def has(deg):
    t = math.radians(deg); r = 17.9
    return pp.Shape.isInside(App.Vector(x0 + rt - rh / 2, r * math.cos(t), ax + r * math.sin(t)), 0.01, True)
before = [has(ra + k * 90) for k in range(4)]
pp.SuppressedIndices = [1]
d.recompute()
after = [has(ra + k * 90) for k in range(4)]
f"{done(pp, [d.face_rib])} present at rib_a+k*90 before {before} after {after}"''',
    # 8: inlet boss, cone (taper by expression), neck, barb
    "plane('pl_boss','YZ','x_tip + in_len + neck_len + cone_len'); sk('s_boss','pl_boss'); circ('s_boss','boss_d',0,'ax_h'); pad('s_boss','head_x0 - cov_t - in_len - neck_len - cone_len','boss'); "
    "plane('pl_cone','YZ','x_tip + in_len + neck_len'); sk('s_cone','pl_cone'); circ('s_cone','neck_d',0,'ax_h'); pad('s_cone','cone_len','cone'); "
    "import FreeCAD; c = FreeCAD.ActiveDocument.getObject('cone'); c.setExpression('TaperAngle', 'atan((params.boss_d - params.neck_d) / 2 / params.cone_len)'); FreeCAD.ActiveDocument.recompute(); "
    "plane('pl_neck','YZ','x_tip + in_len'); sk('s_neck','pl_neck'); circ('s_neck','neck_d',0,'ax_h'); pad('s_neck','neck_len','neck'); "
    "plane('pl_inlet','YZ','x_tip'); sk('s_inlet','pl_inlet'); circ('s_inlet','in_d',0,'ax_h'); pad('s_inlet','in_len','inlet'); "
    "(round(c.TaperAngle.Value, 2), c.Shape.isValid())",
    # 9: outlet and grommet
    "plane('pl_axis','XY','ax_h'); sk('s_outlet_tube','pl_axis'); circ('s_outlet_tube','out_d2','x_tip + out_x','out_y'); pad('s_outlet_tube','out_reach - out_len - ax_h','outlet_tube'); "
    "plane('pl_barb','XY','out_reach - out_len'); sk('s_outlet_barb','pl_barb'); circ('s_outlet_barb','out_d','x_tip + out_x','out_y'); pad('s_outlet_barb','out_len','outlet_barb'); "
    "plane('pl_motor_face','YZ','x_tip + p_len'); sk('s_grommet','pl_motor_face'); slot('s_grommet','grm_l','grm_w','grm_y','ax_h + grm_z',90); pad('s_grommet','grm_t','grommet')",
    # 10: one slot corner (+X, +Y): entry open to the edge and hook towards the middle
    "plane('pl_plate_back','XY','fl_t'); "
    "sk('s_slot_entry','pl_plate_back'); slot('s_slot_entry','fl_w/2 + slot_ov - hole_dy/2 + hole_d','hole_d','hole_dx/2','(hole_dy/2 + fl_w/2 + slot_ov)/2',90); pocket('s_slot_entry','through','slot_entry'); "
    "sk('s_slot_hook','pl_plate_back'); slot('s_slot_hook','hook_l','hole_d','hole_dx/2 - (hook_l - hole_d)/2','hole_dy/2'); pocket('s_slot_hook','through','slot_hook')",
    # 11: four slots by mirroring the corner across YZ and XZ
    HELPERS + '''mt = d.addObject("PartDesign::MultiTransform", "slots")
mt.Originals = [d.slot_entry, d.slot_hook]
b.addObject(mt)
m1 = d.addObject("PartDesign::Mirrored", "slots_mirror_x"); m1.MirrorPlane = (org("YZ_Plane"), [""])
m2 = d.addObject("PartDesign::Mirrored", "slots_mirror_y"); m2.MirrorPlane = (org("XZ_Plane"), [""])
mt.Transformations = [m1, m2]
m1.Visibility = m2.Visibility = False
done(mt, [d.slot_hook, d.slot_entry])''',
    # 12: centre pockets (symmetric about Y 0), 2.5 deep, rounded corners
    "sk('s_pockets_mid','XY'); "
    + '; '.join(f"rect('s_pockets_mid','{b1} - {a}','pk_c3w','({a} + {b1})/2',0)" for a, b1 in ROWS) + '; '
    + '; '.join(rect_fillets('s_pockets_mid', a, b1, 'pk_c3w/2', '-pk_c3w/2') for a, b1 in ROWS)
    + "; pocket('s_pockets_mid','pk_dc','pockets_mid',reverse=True)",
    # 13: side and outer pockets on +Y, 1.5 deep
    "sk('s_pockets_side','XY'); "
    + '; '.join(f"rect('s_pockets_side','{b1} - {a}','pk_c2w','({a} + {b1})/2','(pk_c2a + pk_c2b)/2')" for a, b1 in ROWS) + '; '
    + '; '.join(rect_fillets('s_pockets_side', a, b1, 'pk_c2a', 'pk_c2b') for a, b1 in ROWS) + '; '
    + "poly('s_pockets_side',[('pk_rb1','pk_c1a'),('pk_rb1','pk_c1b'),('-pk_hx','pk_c1b'),('-pk_hx','pk_hy'),('pk_rb0','pk_hy'),('pk_rb0','pk_c1a')]); "
    + "fil('s_pockets_side',('-pk_hx','pk_hy'),'pk_fr'); "
    + '; '.join(f"fil('s_pockets_side',({x!r},{y!r}),'pk_r')" for x, y in (('pk_rb1', 'pk_c1a'), ('pk_rb1', 'pk_c1b'), ('-pk_hx', 'pk_c1b'), ('pk_rb0', 'pk_c1a'))) + '; '
    + "poly('s_pockets_side',[('pk_rc0','pk_c1a'),('pk_rc0','pk_c1b'),('pk_hx','pk_c1b'),('pk_hx','pk_hy'),('pk_rc1','pk_hy'),('pk_rc1','pk_c1a')]); "
    + "fil('s_pockets_side',('pk_hx','pk_hy'),'pk_fr'); "
    + '; '.join(f"fil('s_pockets_side',({x!r},{y!r}),'pk_r')" for x, y in (('pk_rc0', 'pk_c1a'), ('pk_rc0', 'pk_c1b'), ('pk_hx', 'pk_c1b'), ('pk_rc1', 'pk_c1a'))) + '; '
    + "pocket('s_pockets_side','pk_d','pockets_side',reverse=True)",
    # 14: mirror the side pockets to -Y
    HELPERS + '''mi = d.addObject("PartDesign::Mirrored", "pockets_side_mirror")
mi.Originals = [d.pockets_side]
b.addObject(mi)
mi.MirrorPlane = (org("XZ_Plane"), [""])
done(mi, [d.pockets_side])''',
    # 15: finish: label, colour, hide datums, save, check
    HELPERS + '''b.Label = "Pump"
b.ViewObject.ShapeColor = (0.72, 0.80, 0.92)
for o in d.Objects:
    if o.TypeId in ("PartDesign::Plane", "PartDesign::Line") or o.TypeId == "Sketcher::SketchObject":
        o.Visibility = False
d.recompute(); d.save()
bb = b.Shape.BoundBox
f"x {bb.XMin:.2f}..{bb.XMax:.2f} y {bb.YMin:.2f}..{bb.YMax:.2f} z {bb.ZMin:.2f}..{bb.ZMax:.2f} V {b.Shape.Volume:.1f} solids {len(b.Shape.Solids)} valid {b.Shape.isValid()}"''',
]


def rpc(code):
    r = xmlrpc.client.ServerProxy(URL, allow_none=True).execute_code(code, 180)
    msg = r.get('message') or r.get('error') or str(r)
    return r.get('success'), msg.split('Output: ', 1)[-1].strip()


def run(expr):
    head = (f'import sys\nsys.path.count({MOD!r}) or sys.path.insert(0, {MOD!r})\nimport fdmkit\n')
    ok, out = rpc(head + f'print(fdmkit.run({expr!r}))')
    return out if ok else 'RPC ERR ' + out


if __name__ == '__main__':
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if start == 0:
        ok, out = rpc(f'import FreeCAD as App\nif {DOC!r} in App.listDocuments(): App.closeDocument({DOC!r})\nprint(list(App.listDocuments()))')
        print('close:', out)
    for i, expr in enumerate(BATCHES[start:], start):
        out = run(expr)
        print(f'[{i}]', out[-1500:])
        if 'ERR' in out:
            sys.exit(f'stopped at batch {i}')
