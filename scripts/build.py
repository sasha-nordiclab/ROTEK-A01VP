#!/usr/bin/env python3
"""Rebuild TPU_Pump_Holder from scratch in the running FreeCAD: the pump reference body and the
TPU sock holder. Every step is one fdmkit run() batch sent over XML-RPC; it stops at the first ERR.

  python3 scripts/build.py          closes the document and rebuilds everything
  python3 scripts/build.py 12       resumes from step 12 (document left open)

Pump (body "Body", label Rotek_WPDC-06.7L-10M-24-VP): origin at the slot pattern centre on the
mounting face, X along the pump axis (inlet towards -X), Z into the pump. Native symmetry: one
slot corner + MultiTransform, +Y pockets + Mirrored, one ear and one face partition + PolarPattern.

Holder (body "Holder"): a TPU 95A sock under the mounting face, printed flat on its glued floor
with no bridges (vertical walls, 40 deg undersides only): side walls with preloaded lips, keys in
the slot entries, snap pins with a widening head in the hook ends, corner stops.
"""
import os
import sys
import xmlrpc.client

URL = os.environ.get('FREECAD_RPC', 'http://127.0.0.1:9875')
MOD = os.path.expanduser('~/Library/Application Support/FreeCAD/v26-3/Mod/fdmkit')
HERE = os.path.dirname(os.path.abspath(__file__))
FCSTD = os.path.normpath(os.path.join(HERE, '..', 'cad', 'TPU_Pump_Holder.FCStd'))
DOC = 'TPU_Pump_Holder'

# (name, value or formula, description); None as name starts a group header
PARAMS = [
    # ---------------- pump
    (None, 'MOTOR AND HEAD', None),
    ('ax_h', 21.28, 'Pump axis height above the mounting face (drawing ear geometry; not measured yet, row B10)'),
    ('p_len', 74.5, 'Inlet tip to the motor end face, grommet excluded (caliper 74.5; drawing 75)'),
    ('p_d', 36.7, 'Motor diameter (caliper 36.72)'),
    ('head_d', 40.3, 'Pump head diameter (caliper 40.29)'),
    ('head_x0', 15.0, 'Inlet tip to the ear-lug face of the head (caliper 15.0; photo IMG_7253 15.0)'),
    ('head_len', 16.4, 'Head length, ear-lug face to the joint with the motor (photo IMG_7253 16.4; drawing 15.5; caliper 14.0 disagrees)'),
    ('head_x1', 'head_x0 + head_len', 'Inlet tip to the joint between head and motor'),
    ('cap_d', 33.2, 'Motor end face diameter inside the end step (caliper)'),
    ('cap_len', 2.0, 'Length of the step at the motor end (caliper)'),
    (None, 'EARS', None),
    ('ear_lk', 42.4, 'Bolt circle of the four head screws (drawing)'),
    ('ear_r', 3.35, 'Ear lug radius (drawing R3.35; caliper 6.8 wide)'),
    ('ear_span', 40.75, 'Mounting face to the far edge of the highest ear lug (caliper 40.75; drawing 42)'),
    ('ear_a', 'acos((ear_span - ax_h - ear_r) / (ear_lk / 2)) / 1deg', 'Ear angle from the vertical, deg, from ear_span and ax_h (drawing says 35)'),
    ('scr_d', 5, 'Screw head diameter (photo estimate)'),
    ('scr_h', 2.2, 'Screw head height above the ear lug (estimate; caliper 2.0, within tolerance)'),
    (None, 'INLET', None),
    ('in_d', 14.4, 'Inlet barb diameter (drawing)'),
    ('in_len', 4, 'Inlet barb length (drawing)'),
    ('neck_d', 13.4, 'Inlet neck diameter (drawing)'),
    ('neck_len', 8.2, 'Inlet neck length (caliper 8.2; drawing 7)'),
    (None, 'INLET FACE', None),
    ('cov_d', 31.99, 'Raised cover on the inlet face (caliper)'),
    ('rib_t', 2.17, 'Partition width on the inlet face (caliper)'),
    ('rib_h', 1.5, 'Partition height = depth of the recessed segments and ear-lug faces (caliper)'),
    ('rib_a', 12, 'Angle of the first face partition from the +Y axis, deg (photo)'),
    (None, 'OUTLET', None),
    ('out_d', 8, 'Outlet barb diameter (drawing)'),
    ('out_len', 5, 'Outlet barb length (drawing)'),
    ('out_d2', 7, 'Outlet tube diameter below the barb (drawing)'),
    ('out_reach', 51.4, 'Mounting face to the outlet tip (caliper 51.4; drawing 52)'),
    ('out_gap', 0.05, 'Outlet tube front set back from the boss face plane: coplanar faces break the boolean (construction)'),
    ('out_x', 'in_len + neck_len + out_d2/2 + out_gap', 'Inlet tip to the outlet axis: tube tangent to the boss (mini flange), front at the boss face'),
    ('out_y', -7.35, 'Outlet axis offset from the pump axis along Y (caliper 31.0 across tube and head, minus head_d/2 and out_d2/2; drawing 8)'),
    (None, 'CABLE GROMMET', None),
    ('grm_y', -9.3, 'Wire hole offset from the pump axis along Y, at axis height (photo)'),
    ('grm_z', -3.8, 'Grommet centre below the wire hole (photo)'),
    ('grm_w', 9.5, 'Grommet width (caliper)'),
    ('grm_l', 15, 'Grommet length, figure-8 of two discs (caliper)'),
    ('grm_t', 1.5, 'Grommet height above the motor end face (estimate)'),
    (None, 'MOUNT PLATE', None),
    ('fl_w', 45, 'Plate width across the slotted edges (caliper 44.93)'),
    ('fl_len', 32, 'Plate length along the pump axis (caliper 32.03)'),
    ('fl_t', 3.0, 'Plate thickness at the edge (caliper 2.98, 3.0)'),
    ('fl_off', 1.0, 'Plate centre offset from the slot pattern towards the inlet (drawing 3.35 / 5.35; caliper 3.45 / 5.5)'),
    ('web_w', 13, 'Web between plate and motor (drawing estimate)'),
    ('web_h', 1.5, 'Web height above the plate back (estimate)'),
    (None, 'SLOTS', None),
    ('hole_x0', 39, 'Inlet tip to the inlet-side slot centre (drawing)'),
    ('hole_dx', 20, 'Slot pitch along the axis (drawing, caliper 23.36 - 3.24)'),
    ('hole_dy', 35, 'Slot pitch across the plate (drawing)'),
    ('hole_d', 3.3, 'Slot width at the entry (drawing; caliper 3.37 to 3.40)'),
    ('hook_w', 3.5, 'Slot width in the hook (caliper)'),
    ('hook_l', 5.46, 'Slot length along the axis, hook included (caliper)'),
    ('slot_ov', 2, 'Cutter overshoot past the plate edge (construction)'),
    (None, 'POCKETS', None),
    ('pk_d', 1.5, 'Depth of the side and outer pockets (caliper)'),
    ('pk_dc', 2.5, 'Depth of the centre pockets (caliper)'),
    ('rib', 1.8, 'Rib between pockets (photo)'),
    ('frame', 1.4, 'Frame along the slotted edges (photo; caliper 1.5, within tolerance)'),
    ('pk_fi', 1.5, 'Frame at the inlet end (caliper)'),
    ('pk_fm', 1.6, 'Frame at the motor end (photo; caliper 1.5, within tolerance)'),
    ('pk_h', 6.3, 'Pocket length along the axis, three inlet-side rows (photo)'),
    ('pk_c3w', 10.2, 'Centre pocket width (photo)'),
    ('pk_c2w', 4.3, 'Side pocket width (caliper)'),
    (None, 'DERIVED', None),
    ('x_tip', '-(hole_x0 + hole_dx/2)', 'X of the inlet tip; origin is the slot pattern centre'),
    ('fl_x0', 'hole_x0 + hole_dx/2 - fl_len/2 - fl_off', 'Inlet tip to the inlet-end edge of the plate'),
    ('x_fs', 'x_tip + fl_x0', 'X of the inlet-end plate edge'),
    ('x_fe', 'x_tip + fl_x0 + fl_len', 'X of the motor-end plate edge'),
    ('cov_t', 'rib_h', 'Cover height above the recessed face = partition height'),
    ('boss_d', 'out_d2 - 2*out_y', 'Boss (mini flange) around the inlet, tangent to the outlet tube (photo 22.3; drawing 23)'),
    ('pk_c2a', 'pk_c3w/2 + rib', 'Side pockets, inner Y'),
    ('pk_c2b', 'pk_c2a + pk_c2w', 'Side pockets, outer Y'),
    ('pk_c1a', 'pk_c2b + rib', 'Outer pockets, inner Y'),
    ('pk_c1b', 'fl_w/2 - frame', 'Outer pockets, outer Y'),
    ('pk_hx', 'hole_dx/2 + hole_d/2 - hook_l - rib', 'Outer pockets stop this far from X 0 beside the hooks'),
    ('pk_hy', 'hole_dy/2 - hook_w/2 - rib', 'Outer pockets reach this Y beside the hooks'),
    ('pk_ra0', 'x_fs + pk_fi', 'Row A (inlet end) start X'),
    ('pk_ra1', 'pk_ra0 + pk_h', 'Row A end X'),
    ('pk_rb0', 'pk_ra1 + rib', 'Row B start X'),
    ('pk_rb1', 'pk_rb0 + pk_h', 'Row B end X'),
    ('pk_rc0', 'pk_rb1 + rib', 'Row C start X'),
    ('pk_rc1', 'pk_rc0 + pk_h', 'Row C end X'),
    ('pk_rd0', 'pk_rc1 + rib', 'Row D (motor end) start X'),
    ('pk_rd1', 'x_fe - pk_fm', 'Row D end X'),
    # ---------------- holder (TPU sock)
    (None, 'HOLDER', None),
    ('clr', 0.1, 'Wall to plate edge clearance, per side'),
    ('lip_pre', 0.1, 'Lip preload: interference with the plate back at its edge, holds the pump down without rattle'),
    ('f_t', 5, 'Floor thickness under the pump plate, glued face down'),
    ('w_t', 1.8, 'Side wall thickness'),
    ('lip_o', 1.0, 'Lip overlap onto the plate back'),
    ('lip_a', 40, 'Lip and pin head underside angle from vertical, deg (print limit 40)'),
    ('lip_tip', 0.5, 'Vertical face at the lip tip'),
    ('lip_r', 35, 'Lip entry ramp angle from horizontal, deg'),
    ('key_w', 3.0, 'Key width along X (slot entry 3.3)'),
    ('key_d', 2.0, 'Key depth into the slot entry from the plate edge'),
    ('key_h', 2.8, 'Key height (plate 3.0 thick)'),
    ('ret_y0', 19.6, 'Corner stops start at this |Y|: clear of the motor (R 18.36) and the lower ears (19.5)'),
    ('pin_d', 3.2, 'Snap pin shaft diameter (slot hook 3.5 wide)'),
    ('pin_hd', 4.2, 'Snap pin head diameter: squeezes through the 3.5 hook, then holds the plate'),
    ('pin_cyl', 0.3, 'Snap pin head: straight part'),
    ('pin_lead', 2.0, 'Snap pin head: lead-in cone height'),
    ('pin_tip', 1.9, 'Snap pin tip diameter'),
    ('b_ch', 0.4, 'Bed chamfer height (elephant foot)'),
    ('b_cha', 40, 'Bed chamfer angle from vertical, deg'),
    (None, 'HOLDER DERIVED', None),
    ('wy', 'fl_w/2 + clr', 'Side wall inner face |Y|'),
    ('wy2', 'wy + w_t', 'Side wall outer face |Y|'),
    ('hx0', 'x_fs - clr - w_t', 'Holder start X (inlet end)'),
    ('hx1', 'x_fe + clr + w_t', 'Holder end X (motor end)'),
    ('z_bb', '-f_t', 'Z of the bed face'),
    ('lip_z0', 'fl_t - lip_pre - clr/tan(lip_a)', 'Z where the lip underside meets the wall'),
    ('lip_zt', 'lip_z0 + lip_o/tan(lip_a)', 'Z of the lip tip, bottom'),
    ('pin_x', 'hole_dx/2 + hole_d/2 - hook_l + hook_w/2', 'Snap pin X: inner end of the slot hook'),
    ('pin_h1', '(pin_hd - pin_d)/2/tan(lip_a)', 'Snap pin head: height of the widening part'),
]


def params_batch():
    """All cells at once and one recompute (P() per param recomputes the whole model each time).
    Values go in as formulas: the en_DK locale misreads plain decimals."""
    lines = ['import FreeCAD as App', 's = App.ActiveDocument.getObject("params")']
    for r, (name, val, desc) in enumerate(PARAMS, 1):
        if name is None:
            lines.append(f's.set("A{r}", {val!r}); s.setStyle("A{r}", "bold")')
        else:
            lines.append(f's.set("A{r}", {name!r}); s.set("B{r}", {"=" + str(val)!r}); s.setAlias("B{r}", {name!r}); s.set("C{r}", {desc!r})')
    lines += ['s.setColumnWidth("A", 110); s.setColumnWidth("C", 560)', 'App.ActiveDocument.recompute()',
              "P('ax_h', 'ear_a', 'x_fs', 'x_fe', 'boss_d', 'out_x', 'wy', 'lip_z0', 'lip_zt', 'pin_x', 'pin_h1')"]
    return '\n'.join(lines)


def ring_poly(sk, t, r1, r2, w='rib_t'):
    """Radial bar in a YZ sketch around the pump axis: angle t from +Y, radii r1..r2, width w."""
    pts = [(f'({r1})*cos({t}) + {w}/2*sin({t})', f'ax_h + ({r1})*sin({t}) - {w}/2*cos({t})'),
           (f'({r2})*cos({t}) + {w}/2*sin({t})', f'ax_h + ({r2})*sin({t}) - {w}/2*cos({t})'),
           (f'({r2})*cos({t}) - {w}/2*sin({t})', f'ax_h + ({r2})*sin({t}) + {w}/2*cos({t})'),
           (f'({r1})*cos({t}) - {w}/2*sin({t})', f'ax_h + ({r1})*sin({t}) + {w}/2*cos({t})')]
    return f'poly({sk!r}, {pts!r})'



ROWS = [('pk_ra0', 'pk_ra1'), ('pk_rb0', 'pk_rb1'), ('pk_rc0', 'pk_rc1'), ('pk_rd0', 'pk_rd1')]


def helpers(body):
    """Python prelude for steps that add transforms: done() checks tip chain, validity, one solid."""
    return f'''import FreeCAD as App
d = App.ActiveDocument
b = d.getObject({body!r})
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
    return f"{{f.Name}}: OK V {{f.Shape.Volume:.1f}}"
'''


def mirror_multi(body, name, originals, prev):
    """Originals mirrored across YZ and XZ (MultiTransform of two Mirrored)."""
    return helpers(body) + f'''mt = d.addObject("PartDesign::MultiTransform", {name!r})
mt.Originals = [{', '.join('d.' + o for o in originals)}]
b.addObject(mt)
m1 = d.addObject("PartDesign::Mirrored", {name + '_mirror_x'!r}); m1.MirrorPlane = (org("YZ_Plane"), [""])
m2 = d.addObject("PartDesign::Mirrored", {name + '_mirror_y'!r}); m2.MirrorPlane = (org("XZ_Plane"), [""])
mt.Transformations = [m1, m2]
m1.Visibility = m2.Visibility = False
done(mt, [{', '.join('d.' + o for o in prev)}])'''


def mirror_xz(body, name, originals, prev):
    return helpers(body) + f'''mi = d.addObject("PartDesign::Mirrored", {name!r})
mi.Originals = [{', '.join('d.' + o for o in originals)}]
b.addObject(mi)
mi.MirrorPlane = (org("XZ_Plane"), [""])
done(mi, [{', '.join('d.' + o for o in prev)}])'''


# holder +Y side wall with the lip, YZ section (sketch x = Y, sketch y = Z); starts inside the floor
WALL = [('wy', '-f_t/2'), ('wy2', '-f_t/2'), ('wy2', 'lip_zt + lip_tip + (w_t + lip_o)*tan(lip_r)'),
        ('wy - lip_o', 'lip_zt + lip_tip'), ('wy - lip_o', 'lip_zt'), ('wy', 'lip_z0')]
# snap pin half profile, sketch x = radius from the pin axis, sketch y = Z (revolved about V_Axis)
PIN = [('0', '0'), ('pin_d/2', '0'), ('pin_d/2', 'fl_t'), ('pin_hd/2', 'fl_t + pin_h1'),
       ('pin_hd/2', 'fl_t + pin_h1 + pin_cyl'), ('pin_tip/2', 'fl_t + pin_h1 + pin_cyl + pin_lead'),
       ('0', 'fl_t + pin_h1 + pin_cyl + pin_lead')]

STEPS = [
    # fresh document (fdmkit new: params sheet + body "Body")
    f'new({DOC!r}); import FreeCAD as App; App.ActiveDocument.saveAs({FCSTD!r})',
    params_batch(),
    # ================= pump
    # plate, web, motor, end step, head
    "sk('s_plate','XY'); rect('s_plate','fl_len','fl_w','x_fs + fl_len/2',0); pad('s_plate','fl_t','plate'); "
    "sk('s_web','XY'); rect('s_web','fl_len','web_w','x_fs + fl_len/2',0); pad('s_web','fl_t + web_h','web'); "
    "plane('pl_motor','YZ','x_tip + head_x1'); sk('s_motor','pl_motor'); circ('s_motor','p_d',0,'ax_h'); pad('s_motor','p_len - head_x1 - cap_len','motor'); "
    "plane('pl_end','YZ','x_tip + p_len - cap_len'); sk('s_end','pl_end'); circ('s_end','cap_d',0,'ax_h'); pad('s_end','cap_len','motor_end'); "
    "plane('pl_head','YZ','x_tip + head_x0'); sk('s_head','pl_head'); circ('s_head','head_d',0,'ax_h'); pad('s_head','head_x1 - head_x0','head')",
    # pump axis datum line
    helpers("Body") + '''ln = b.newObject("PartDesign::Line", "pump_axis")
ln.AttachmentSupport = [(org("X_Axis"), "")]
ln.MapMode = "ObjectX"
ln.setExpression(".AttachmentOffset.Base.y", "params.ax_h")
d.recompute()
ln.Visibility = False
"pump_axis: base " + str(tuple(round(c, 3) for c in ln.Placement.Base)) + " dir " + str(tuple(round(c, 3) for c in ln.Placement.Rotation.multVec(App.Vector(0, 0, 1))))''',
    # one ear: lug, screw head, partition to the lug (ear B, at 90 - ear_a from +Y)
    "sk('s_ear','pl_head'); circ('s_ear','2*ear_r','ear_lk/2*sin(ear_a)','ax_h + ear_lk/2*cos(ear_a)'); pad('s_ear','head_x1 - head_x0','ear_lug'); "
    "sk('s_screw','pl_head'); circ('s_screw','scr_d','ear_lk/2*sin(ear_a)','ax_h + ear_lk/2*cos(ear_a)'); pad('s_screw','scr_h','ear_screw',reverse=True); "
    "sk('s_ear_rib','pl_head'); " + ring_poly('s_ear_rib', '(90 - ear_a)', 'cov_d/2 - 0.5', 'ear_lk/2') + "; pad('s_ear_rib','rib_h','ear_rib',reverse=True)",
    # four ears by polar pattern around the pump axis
    helpers("Body") + '''pp = d.addObject("PartDesign::PolarPattern", "ears")
pp.Originals = [d.ear_lug, d.ear_screw, d.ear_rib]
b.addObject(pp)
pp.Axis = (d.pump_axis, [""])
pp.Angle = 360
pp.Occurrences = 4
done(pp, [d.ear_rib, d.ear_screw, d.ear_lug])''',
    # raised cover and one face partition
    "plane('pl_cover','YZ','x_tip + head_x0 - cov_t'); sk('s_cover','pl_cover'); circ('s_cover','cov_d',0,'ax_h'); pad('s_cover','cov_t','cover'); "
    "sk('s_face_rib','pl_head'); " + ring_poly('s_face_rib', 'rib_a', 'cov_d/2 - 0.5', 'head_d/2') + "; pad('s_face_rib','rib_h','face_rib',reverse=True)",
    # four face partitions, the one under the outlet (rib_a + 90) suppressed
    helpers("Body") + '''import math
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
    # inlet boss (mini flange, straight step from the neck, no cone), neck, barb
    "plane('pl_boss','YZ','x_tip + in_len + neck_len'); sk('s_boss','pl_boss'); circ('s_boss','boss_d',0,'ax_h'); pad('s_boss','head_x0 - cov_t - in_len - neck_len','boss'); "
    "plane('pl_neck','YZ','x_tip + in_len'); sk('s_neck','pl_neck'); circ('s_neck','neck_d',0,'ax_h'); pad('s_neck','neck_len','neck'); "
    "plane('pl_inlet','YZ','x_tip'); sk('s_inlet','pl_inlet'); circ('s_inlet','in_d',0,'ax_h'); pad('s_inlet','in_len','inlet')",
    # outlet and grommet
    "plane('pl_axis','XY','ax_h'); sk('s_outlet_tube','pl_axis'); circ('s_outlet_tube','out_d2','x_tip + out_x','out_y'); pad('s_outlet_tube','out_reach - out_len - ax_h','outlet_tube'); "
    "plane('pl_barb','XY','out_reach - out_len'); sk('s_outlet_barb','pl_barb'); circ('s_outlet_barb','out_d','x_tip + out_x','out_y'); pad('s_outlet_barb','out_len','outlet_barb'); "
    "plane('pl_motor_face','YZ','x_tip + p_len'); sk('s_grommet','pl_motor_face'); slot('s_grommet','grm_l','grm_w','grm_y','ax_h + grm_z',90); pad('s_grommet','grm_t','grommet')",
    # one slot corner (+X, +Y): entry open to the edge and hook towards the middle
    "plane('pl_plate_back','XY','fl_t'); "
    "sk('s_slot_entry','pl_plate_back'); slot('s_slot_entry','fl_w/2 + slot_ov - hole_dy/2 + hole_d','hole_d','hole_dx/2','(hole_dy/2 + fl_w/2 + slot_ov)/2',90); pocket('s_slot_entry','through','slot_entry'); "
    "sk('s_slot_hook','pl_plate_back'); slot('s_slot_hook','hook_l','hook_w','hole_dx/2 - (hook_l - hole_d)/2','hole_dy/2'); pocket('s_slot_hook','through','slot_hook')",
    # four slots by mirroring the corner across YZ and XZ
    helpers("Body") + '''mt = d.addObject("PartDesign::MultiTransform", "slots")
mt.Originals = [d.slot_entry, d.slot_hook]
b.addObject(mt)
m1 = d.addObject("PartDesign::Mirrored", "slots_mirror_x"); m1.MirrorPlane = (org("YZ_Plane"), [""])
m2 = d.addObject("PartDesign::Mirrored", "slots_mirror_y"); m2.MirrorPlane = (org("XZ_Plane"), [""])
mt.Transformations = [m1, m2]
m1.Visibility = m2.Visibility = False
done(mt, [d.slot_hook, d.slot_entry])''',
    # centre pockets (symmetric about Y 0), pk_dc deep
    "sk('s_pockets_mid','XY'); "
    + '; '.join(f"rect('s_pockets_mid','{b1} - {a}','pk_c3w','({a} + {b1})/2',0)" for a, b1 in ROWS)
    + "; pocket('s_pockets_mid','pk_dc','pockets_mid',reverse=True)",
    # side and outer pockets on +Y, pk_d deep (outer ones are L-shaped around the slot hooks)
    "sk('s_pockets_side','XY'); "
    + '; '.join(f"rect('s_pockets_side','{b1} - {a}','pk_c2w','({a} + {b1})/2','(pk_c2a + pk_c2b)/2')" for a, b1 in ROWS) + '; '
    + "poly('s_pockets_side',[('pk_rb1','pk_c1a'),('pk_rb1','pk_c1b'),('-pk_hx','pk_c1b'),('-pk_hx','pk_hy'),('pk_rb0','pk_hy'),('pk_rb0','pk_c1a')]); "
    + "poly('s_pockets_side',[('pk_rc0','pk_c1a'),('pk_rc0','pk_c1b'),('pk_hx','pk_c1b'),('pk_hx','pk_hy'),('pk_rc1','pk_hy'),('pk_rc1','pk_c1a')]); "
    + "pocket('s_pockets_side','pk_d','pockets_side',reverse=True)",
    # mirror the side pockets to -Y
    helpers("Body") + '''mi = d.addObject("PartDesign::Mirrored", "pockets_side_mirror")
mi.Originals = [d.pockets_side]
b.addObject(mi)
mi.MirrorPlane = (org("XZ_Plane"), [""])
done(mi, [d.pockets_side])''',
    # pump finish: label, colour
    helpers("Body") + '''b.Label = "Rotek_WPDC-06.7L-10M-24-VP"
d.Comment = "ROTEK Food Grade Mini Centrifugal Pump with Brushless DC Motor, housing A01VP, 24 VDC, 6.7 L/min or 10 mWs. Model WPDC-06.7L-10M-24-VP (PUM409)."
b.ViewObject.ShapeColor = (0.72, 0.80, 0.92)
d.save()
bb = b.Shape.BoundBox
f"pump x {bb.XMin:.2f}..{bb.XMax:.2f} y {bb.YMin:.2f}..{bb.YMax:.2f} z {bb.ZMin:.2f}..{bb.ZMax:.2f} V {b.Shape.Volume:.1f} valid {b.Shape.isValid()}"''',
    # ================= holder
    '''import FreeCAD as App, FreeCADGui as Gui
d = App.ActiveDocument
b = d.addObject("PartDesign::Body", "Holder")
b.ViewObject.ShapeColor = (0.99, 0.80, 0.62)
Gui.getDocument(d.Name).ActiveView.setActiveObject("pdbody", b)
d.recompute()
"Holder: OK"''',
    # floor; the first b_ch is padded with a taper (positive grows outwards) for the bed chamfer
    "plane('hl_bed','XY','z_bb'); sk('s_h_foot','hl_bed'); "
    "rect('s_h_foot','hx1 - hx0 - 2*b_ch*tan(b_cha)','2*wy2 - 2*b_ch*tan(b_cha)','(hx0 + hx1)/2',0); pad('s_h_foot','b_ch','h_foot'); "
    "import FreeCAD; FreeCAD.ActiveDocument.getObject('h_foot').setExpression('TaperAngle', 'params.b_cha'); FreeCAD.ActiveDocument.recompute(); "
    "plane('hl_floor','XY','z_bb + b_ch'); sk('s_h_floor','hl_floor'); rect('s_h_floor','hx1 - hx0','2*wy2','(hx0 + hx1)/2',0); pad('s_h_floor','f_t - b_ch','h_floor')",
    # +Y side wall with the lip; corner stops at both plate ends up to the lip tip
    f"plane('hl_wall','YZ','hx0'); sk('s_h_wall','hl_wall'); poly('s_h_wall', {WALL!r}); pad('s_h_wall','hx1 - hx0','h_wall'); "
    "sk('s_h_stop','XY'); "
    "rect('s_h_stop','w_t','wy - ret_y0 + w_t/2','hx0 + w_t/2','(ret_y0 + wy + w_t/2)/2'); "
    "rect('s_h_stop','w_t','wy - ret_y0 + w_t/2','hx1 - w_t/2','(ret_y0 + wy + w_t/2)/2'); "
    "pad('s_h_stop','lip_zt','h_stop')",
    mirror_xz('Holder', 'h_side', ['h_wall', 'h_stop'], ['h_stop', 'h_wall']),
    # one key into the slot entry (+X +Y) and one snap pin in the hook end, revolved on a datum
    # plane through the pin axis
    "sk('s_h_key','XY'); rect('s_h_key','key_w','key_d + clr + w_t/2','hole_dx/2','fl_w/2 - key_d + (key_d + clr + w_t/2)/2'); pad('s_h_key','key_h','h_key'); "
    "plane('hl_pin','XZ','hole_dy/2'); import FreeCAD; pl = FreeCAD.ActiveDocument.getObject('hl_pin'); pl.setExpression('.AttachmentOffset.Base.x', 'params.pin_x'); FreeCAD.ActiveDocument.recompute(); "
    f"sk('s_h_pin','hl_pin'); poly('s_h_pin', {PIN!r}); revolve('s_h_pin', 360, 'V_Axis', 'h_pin'); "
    "bb = FreeCAD.ActiveDocument.getObject('h_pin').AddSubShape.BoundBox; tuple(round(v, 2) for v in (bb.Center.x, bb.Center.y, bb.ZMin, bb.ZMax, bb.XLength))",
    mirror_multi('Holder', 'h_keys_pins', ['h_key', 'h_pin'], ['h_pin', 'h_key']),
    # holder finish
    helpers("Holder") + '''b.Label = "Holder"
for o in d.Objects:
    if o.TypeId in ("PartDesign::Plane", "PartDesign::Line", "Sketcher::SketchObject"):
        o.Visibility = False
d.recompute(); d.save()
bb = b.Shape.BoundBox
f"holder x {bb.XMin:.2f}..{bb.XMax:.2f} y {bb.YMin:.2f}..{bb.YMax:.2f} z {bb.ZMin:.2f}..{bb.ZMax:.2f} V {b.Shape.Volume:.1f} valid {b.Shape.isValid()}"''',
]


def rpc(code, timeout=300):
    r = xmlrpc.client.ServerProxy(URL, allow_none=True).execute_code(code, timeout)
    msg = r.get('message') or r.get('error') or str(r)
    return r.get('success'), msg.split('Output: ', 1)[-1].strip()


def run(expr):
    head = f'import sys\nsys.path.count({MOD!r}) or sys.path.insert(0, {MOD!r})\nimport fdmkit\n'
    ok, out = rpc(head + f'print(fdmkit.run({expr!r}))')
    return out if ok else 'RPC ERR ' + out


if __name__ == '__main__':
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if start == 0:
        ok, out = rpc(f'import FreeCAD as App\nif {DOC!r} in App.listDocuments(): App.closeDocument({DOC!r})\nprint(list(App.listDocuments()))')
        print('close:', out)
    for i, expr in enumerate(STEPS[start:], start):
        out = run(expr)
        print(f'[{i}]', out[-600:])
        if 'ERR' in out:
            sys.exit(f'stopped at step {i}')
