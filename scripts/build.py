#!/usr/bin/env python3
"""Rebuild TPU_Pump_Holder from scratch in the running FreeCAD: the pump reference body and the
experimental TPU four-post stand. Every step is one fdmkit run() batch sent over XML-RPC; it stops at the first ERR.

  python3 scripts/build.py          closes the document and rebuilds everything
  python3 scripts/build.py 12       resumes from step 12 (document left open)

Pump (body "Body", label Rotek_WPDC-06.7L-10M-24-VP): origin at the slot pattern centre on the
mounting face, X along the pump axis (inlet towards -X), Z into the pump. Native symmetry: one
slot corner + MultiTransform, +Y pockets + Mirrored, one ear and one face partition + PolarPattern.

Holder (body "Holder"): a TPU 95A floor with two countersunk M4 holes and four vertical
columns. Their top shoulders support the pump plate 4 mm above the floor; elongated heads
snap into its hook slots. The Holder tree contains the floor Pad, bottom Chamfer, four-corner Fillet,
one complete post (column Pad plus snap-head AdditiveLoft), its MultiTransform, and the M4 holes.
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
    ('cone_start', 12, 'Inlet tip to start of the short conical transition (user measurement)'),
    ('neck_len', 'cone_start - in_len', 'Straight inlet neck length, derived from cone_start minus inlet barb length'),
    ('cone_len', 0.5, 'Axial length of the short taper from the inlet neck to the cylindrical boss'),
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
    ('out_x', 15.75, 'Inlet tip to outlet axis; established position, independent of inlet cone'),
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
    ('pin_d', 3.2, 'Snap boss stem width across the 3.5-wide hook slot'),
    ('pin_hd', 4.2, 'Snap boss head width across the hook slot: flexes through it, then holds the plate'),
    ('pin_cyl', 0.3, 'Snap boss head: straight part'),
    ('pin_lead', 2.0, 'Snap boss head: lead-in ramp height'),
    ('pin_tip', 1.9, 'Snap boss tip width across the hook slot'),
    ('b_ch', 0.4, 'Bed chamfer height (elephant foot)'),
    ('b_cha', 40, 'Bed chamfer angle from vertical, deg'),
    ('floor_corner_r', 1.1, 'Native Fillet radius at all four floor corners'),
    ('post_h', 4, 'Air gap from the fixed floor to the pump plate; height of four support columns'),
    ('post_l', 7.2, 'Support column footprint length along the pump axis'),
    ('post_w', 6.0, 'Support column footprint width across the slot'),
    ('post_head_pre', 0.3, 'Snap-head ramp starts below the plate top to lightly preload the slot edges'),
    (None, 'M4 MOUNTING', None),
    ('m4_clear', 4.5, 'Through clearance diameter for two M4 mounting screws'),
    ('m4_sink_d', 9.6, 'Top countersink diameter for ISO 14581 M4 flat heads'),
    ('m4_sink_a', 90, 'Countersink included angle, deg'),
    ('m4_rim', 6, 'Material from each floor end to the countersink rim'),
    (None, 'HOLDER DERIVED', None),
    ('wy', 'fl_w/2 + clr', 'Side wall inner face |Y|'),
    ('wy2', 'wy + w_t', 'Side wall outer face |Y|'),
    ('hx0', 'x_fs - clr - w_t', 'Holder start X (inlet end)'),
    ('hx1', 'x_fe + clr + w_t', 'Holder end X (motor end)'),
    ('floor_x0', 'x_tip + head_x0', 'Inlet-side floor edge, aligned with the pump head face; gives an orientation cue'),
    ('m4_x_in', 'floor_x0 + m4_sink_d/2 + m4_rim', 'Inlet-side M4 centre X'),
    ('m4_x_out', 'hx1 - m4_sink_d/2 - m4_rim', 'Motor-side M4 centre X'),
    ('z_bb', '-f_t', 'Z of the bed face'),
    ('lip_z0', 'fl_t - lip_pre - clr/tan(lip_a)', 'Z where the lip underside meets the wall'),
    ('lip_zt', 'lip_z0 + lip_o/tan(lip_a)', 'Z of the lip tip, bottom'),
    ('pin_x', 'hole_dx/2 - (hook_l - hole_d)/2', 'Snap boss X: centre of the hook slot'),
    ('pin_h1', '(pin_hd - pin_d)/2/tan(lip_a)', 'Snap boss head: height of the widening part'),
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


STEPS = [
    # fresh document (fdmkit new: params sheet + body "Body")
    f'new({DOC!r}); import FreeCAD as App; App.ActiveDocument.saveAs({FCSTD!r})',
    params_batch(),
    # ================= pump
    # plate, web, motor, end step, head
    "sk('s_plate','XY'); rect('s_plate','fl_len','fl_w','x_fs + fl_len/2',0); pad('s_plate','fl_t','plate'); "
    "sk('s_web','XY'); rect('s_web','fl_len','web_w','x_fs + fl_len/2',0); pad('s_web','fl_t + web_h','web'); "
    "sk('s_motor','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_motor').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x1'); App.ActiveDocument.recompute(); circ('s_motor','p_d',0,'ax_h'); pad('s_motor','p_len - head_x1 - cap_len','motor'); "
    "sk('s_end','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_end').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.p_len - params.cap_len'); App.ActiveDocument.recompute(); circ('s_end','cap_d',0,'ax_h'); pad('s_end','cap_len','motor_end'); "
    "sk('s_head','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_head').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x0'); App.ActiveDocument.recompute(); circ('s_head','head_d',0,'ax_h'); pad('s_head','head_x1 - head_x0','head')",
    # pump axis datum line
    helpers("Body") + '''ln = b.newObject("PartDesign::Line", "pump_axis")
ln.AttachmentSupport = [(org("X_Axis"), "")]
ln.MapMode = "ObjectX"
ln.setExpression(".AttachmentOffset.Base.y", "params.ax_h")
d.recompute()
ln.Visibility = False
"pump_axis: base " + str(tuple(round(c, 3) for c in ln.Placement.Base)) + " dir " + str(tuple(round(c, 3) for c in ln.Placement.Rotation.multVec(App.Vector(0, 0, 1))))''',
    # one ear: lug, screw head, partition to the lug (ear B, at 90 - ear_a from +Y)
    "sk('s_ear','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_ear').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x0'); App.ActiveDocument.recompute(); circ('s_ear','2*ear_r','ear_lk/2*sin(ear_a)','ax_h + ear_lk/2*cos(ear_a)'); pad('s_ear','head_x1 - head_x0','ear_lug'); "
    "sk('s_screw','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_screw').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x0'); App.ActiveDocument.recompute(); circ('s_screw','scr_d','ear_lk/2*sin(ear_a)','ax_h + ear_lk/2*cos(ear_a)'); pad('s_screw','scr_h','ear_screw',reverse=True); "
    "sk('s_ear_rib','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_ear_rib').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x0'); App.ActiveDocument.recompute(); " + ring_poly('s_ear_rib', '(90 - ear_a)', 'cov_d/2 - 0.5', 'ear_lk/2') + "; pad('s_ear_rib','rib_h','ear_rib',reverse=True)",
    # four ears by polar pattern around the pump axis
    helpers("Body") + '''pp = d.addObject("PartDesign::PolarPattern", "ears")
pp.Originals = [d.ear_lug, d.ear_screw, d.ear_rib]
b.addObject(pp)
pp.Axis = (d.pump_axis, [""])
pp.Angle = 360
pp.Occurrences = 4
done(pp, [d.ear_rib, d.ear_screw, d.ear_lug])''',
    # raised cover and one face partition
    "sk('s_cover','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_cover').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x0 - params.cov_t'); App.ActiveDocument.recompute(); circ('s_cover','cov_d',0,'ax_h'); pad('s_cover','cov_t','cover'); "
    "sk('s_face_rib','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_face_rib').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.head_x0'); App.ActiveDocument.recompute(); " + ring_poly('s_face_rib', 'rib_a', 'cov_d/2 - 0.5', 'head_d/2') + "; pad('s_face_rib','rib_h','face_rib',reverse=True)",
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
    # cylindrical boss starts after the short cone; the neck's internal core connects it
    "sk('s_boss','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_boss').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.in_len + params.neck_len + params.cone_len'); App.ActiveDocument.recompute(); circ('s_boss','boss_d',0,'ax_h'); pad('s_boss','head_x0 - cov_t - in_len - neck_len - cone_len','boss'); "
    "sk('s_neck','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_neck').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.in_len'); App.ActiveDocument.recompute(); circ('s_neck','neck_d',0,'ax_h'); pad('s_neck','neck_len + cone_len','neck'); "
    "sk('s_inlet','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_inlet').setExpression('.AttachmentOffset.Base.z','params.x_tip'); App.ActiveDocument.recompute(); circ('s_inlet','in_d',0,'ax_h'); pad('s_inlet','in_len','inlet')",
    # outlet and grommet
    "sk('s_outlet_tube','XY'); import FreeCAD as App; App.ActiveDocument.getObject('s_outlet_tube').setExpression('.AttachmentOffset.Base.z','params.ax_h'); App.ActiveDocument.recompute(); circ('s_outlet_tube','out_d2','x_tip + out_x','out_y'); pad('s_outlet_tube','out_reach - out_len - ax_h','outlet_tube'); "
    "sk('s_outlet_barb','XY'); import FreeCAD as App; App.ActiveDocument.getObject('s_outlet_barb').setExpression('.AttachmentOffset.Base.z','params.out_reach - params.out_len'); App.ActiveDocument.recompute(); circ('s_outlet_barb','out_d','x_tip + out_x','out_y'); pad('s_outlet_barb','out_len','outlet_barb'); "
    "sk('s_grommet','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_grommet').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.p_len'); App.ActiveDocument.recompute(); slot('s_grommet','grm_l','grm_w','grm_y','ax_h + grm_z',90); pad('s_grommet','grm_t','grommet')",
    # one slot corner (+X, +Y): entry open to the edge and hook towards the middle
    ""
    "sk('s_slot_entry','XY'); import FreeCAD as App; App.ActiveDocument.getObject('s_slot_entry').setExpression('.AttachmentOffset.Base.z','params.fl_t'); App.ActiveDocument.recompute(); slot('s_slot_entry','fl_w/2 + slot_ov - hole_dy/2 + hole_d','hole_d','hole_dx/2','(hole_dy/2 + fl_w/2 + slot_ov)/2',90); pocket('s_slot_entry','through','slot_entry'); "
    "sk('s_slot_hook','XY'); import FreeCAD as App; App.ActiveDocument.getObject('s_slot_hook').setExpression('.AttachmentOffset.Base.z','params.fl_t'); App.ActiveDocument.recompute(); slot('s_slot_hook','hook_l','hook_w','hole_dx/2 - (hook_l - hole_d)/2','hole_dy/2'); pocket('s_slot_hook','through','slot_hook')",
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
    # 0.5 mm axial cone on the inlet face, added around the neck's internal core
    "sk('s_boss_cone','YZ'); import FreeCAD as App; App.ActiveDocument.getObject('s_boss_cone').setExpression('.AttachmentOffset.Base.z','params.x_tip + params.cone_start'); App.ActiveDocument.recompute(); circ('s_boss_cone','neck_d',0,'ax_h'); "
    + helpers('Body') + '''f = b.newObject("PartDesign::Pad", "boss_cone")
f.Profile = d.s_boss_cone
f.setExpression("Length", "params.cone_len")
f.setExpression("TaperAngle", "atan((params.boss_d - params.neck_d)/(2*params.cone_len))")
done(f, [d.pockets_side_mirror])''',
    # pump finish: label, colour
    helpers("Body") + '''b.Label = "Rotek_WPDC-06.7L-10M-24-VP"
d.Comment = "ROTEK Food Grade Mini Centrifugal Pump with Brushless DC Motor, housing A01VP, 24 VDC, 6.7 L/min or 10 mWs. Model WPDC-06.7L-10M-24-VP (PUM409)."
b.ViewObject.ShapeColor = (0.51, 0.74, 0.96)
d.save()
bb = b.Shape.BoundBox
f"pump x {bb.XMin:.2f}..{bb.XMax:.2f} y {bb.YMin:.2f}..{bb.YMax:.2f} z {bb.ZMin:.2f}..{bb.ZMax:.2f} V {b.Shape.Volume:.1f} valid {b.Shape.isValid()}"''',
    # ================= holder
    '''import FreeCAD as App, FreeCADGui as Gui
d = App.ActiveDocument
b = d.addObject("PartDesign::Body", "Holder")
b.ViewObject.ShapeColor = (0.98, 0.64, 0.51)
Gui.getDocument(d.Name).ActiveView.setActiveObject("pdbody", b)
d.recompute()
"Holder: OK"''',
    # floor reaches the pump head face at floor_x0
    "plane('hl_bed','XY','z_bb'); sk('s_h_foot','hl_bed'); "
    "rect('s_h_foot','hx1 - floor_x0','2*wy2','(floor_x0 + hx1)/2',0); pad('s_h_foot','f_t','h_foot')",
    # Native chamfer along all four edges of the glued face.
    '''import FreeCAD as App
d = App.ActiveDocument
h = d.h_foot
z = float(d.params.get("z_bb"))
edges = ["Edge" + str(i) for i, e in enumerate(h.Shape.Edges, 1)
         if abs(e.BoundBox.ZMin - z) < 1e-5 and abs(e.BoundBox.ZMax - z) < 1e-5]
assert len(edges) == 4, edges
f = d.Holder.newObject("PartDesign::Chamfer", "bed_chamfer")
f.Base = (h, edges)
f.ChamferType = "Two distances"
f.setExpression("Size", "params.b_ch")
f.setExpression("Size2", "params.b_ch * tan(params.b_cha)")
f.Label = "Chamfer on glued face"
d.recompute()
assert f.Shape.isValid() and len(f.Shape.Solids) == 1
h.Visibility = False
f.Visibility = True
f"Bed chamfer: V {f.Shape.Volume:.1f}"''',
    # standard PartDesign Fillet on all four vertical floor corner edges
    '''import FreeCAD as App
d = App.ActiveDocument
p = d.params
h = d.bed_chamfer
y0 = float(p.get("wy2"))
x0 = float(p.get("floor_x0"))
x1 = float(p.get("hx1"))
z = float(p.get("z_bb")) + float(p.get("b_ch"))
edges = []
for i, edge in enumerate(h.Shape.Edges, 1):
    bb = edge.BoundBox
    if (any(abs(bb.XMin - x) < 1e-5 and abs(bb.XMax - x) < 1e-5 for x in (x0, x1))
            and abs(abs(bb.YMin) - y0) < 1e-5 and abs(bb.YMax - bb.YMin) < 1e-5
            and abs(bb.ZMin - z) < 1e-5 and abs(bb.ZMax) < 1e-5):
        edges.append("Edge" + str(i))
assert len(edges) == 4, edges
f = d.Holder.newObject("PartDesign::Fillet", "floor_corner_fillet")
f.Base = (h, edges)
f.setExpression("Radius", "params.floor_corner_r")
f.Label = "All four floor corners R1.1"
d.Holder.Tip = f
d.recompute()
assert f.Shape.isValid() and len(f.Shape.Solids) == 1
f.ViewObject.ShapeColor = d.Holder.ViewObject.ShapeColor
f.ViewObject.LineColor = d.Holder.ViewObject.LineColor
h.Visibility = False
f.Visibility = True
f"Four corner fillets: R {f.Radius}, V {f.Shape.Volume:.1f}"''',
    # Build one complete oval column before making the four-position pattern.
    "sk('s_post_one','XY'); slot('s_post_one','post_l','post_w','pin_x','-hole_dy/2',0); "
    "pad('s_post_one','post_h','post_one')",
    # The lofted head belongs to this first column. Its shoulder bears on the plate.
    '''import FreeCAD as App
sections = (
    ("base", "pin_d", "post_h"),
    ("shaft", "pin_d", "post_h + fl_t - post_head_pre"),
    ("head", "pin_hd", "post_h + fl_t + pin_h1 - post_head_pre"),
    ("crown", "pin_hd", "post_h + fl_t + pin_h1 + pin_cyl - post_head_pre"),
    ("tip", "pin_tip", "post_h + fl_t + pin_h1 + pin_cyl + pin_lead - post_head_pre"),
)
for tag, width, z in sections:
    name = "s_post_boss_" + tag
    sk(name, "XY")
    slot(name, "hook_l - 2*clr", width, "pin_x", "-hole_dy/2", 0)
    App.ActiveDocument.getObject(name).setExpression(".AttachmentOffset.Base.z", "params." + z.replace(" + ", " + params.").replace(" - ", " - params."))
App.ActiveDocument.recompute()
assert all(App.ActiveDocument.getObject("s_post_boss_" + tag).FullyConstrained for tag, _, _ in sections)
"Five loft sketches on XY with independent Z offsets"''',
    helpers('Holder') + '''lo = d.addObject("PartDesign::AdditiveLoft", "post_boss_one")
lo.Profile = (d.s_post_boss_base, [""])
lo.Sections = [(d.s_post_boss_shaft, [""]), (d.s_post_boss_head, [""]),
               (d.s_post_boss_crown, [""]), (d.s_post_boss_tip, [""])]
lo.Ruled = True
lo.Label = "Snap head on first column"
b.addObject(lo)
b.Tip = lo
done(lo, [d.post_one])''',
    mirror_multi('Holder', 'post_complete_four', ['post_one', 'post_boss_one'], ['post_boss_one']),
    # two through M4 holes on the floor centreline; 90 deg countersinks face the pump
    '''import FreeCAD as App, FreeCADGui as Gui, Part, Sketcher
d = App.ActiveDocument
Gui.getDocument(d.Name).ActiveView.setActiveObject("pdbody", d.Holder)
sk("s_h_mount", "XY")
circ("s_h_mount", "m4_clear", "m4_x_in", 0)
s = d.getObject("s_h_mount")
p = d.getObject("params")
g = s.addGeometry(Part.Circle(App.Vector(float(p.get("m4_x_out")), 0, 0), App.Vector(0, 0, 1), float(p.get("m4_clear"))/2))
s.addConstraint(Sketcher.Constraint("Equal", 0, g))
s.addConstraint(Sketcher.Constraint("PointOnObject", g, 3, -1))
i = s.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, g, 3, float(p.get("m4_x_out"))))
s.renameConstraint(i, "mount_x_out")
s.setExpression("Constraints.mount_x_out", "params.m4_x_out")
d.recompute()
assert s.FullyConstrained and not s.ConflictingConstraints and not s.RedundantConstraints
hole("s_h_mount", "m4_clear", "through", "h_mount")
h = d.getObject("h_mount")
h.HoleCutType = "Countersink"
h.setExpression("HoleCutDiameter", "params.m4_sink_d")
h.setExpression("HoleCutCountersinkAngle", "params.m4_sink_a")
h.DrillPoint = "Flat"
h.Label = "M4 mounting holes and countersinks"
h.ViewObject.ShapeColor = d.Holder.ViewObject.ShapeColor
h.ViewObject.LineColor = d.Holder.ViewObject.LineColor
d.recompute()
assert h.BaseFeature == d.post_complete_four and d.Holder.Tip == h
assert h.Shape.isValid() and len(h.Shape.Solids) == 1
f"M4 mount: DoF {s.DoF}, V {h.Shape.Volume:.1f}"''',
    '''import FreeCAD as App
d = App.ActiveDocument
d.Body.setExpression("Placement.Base.z", "params.post_h")
d.recompute()
assert abs(d.Body.Placement.Base.z - float(d.params.get("post_h"))) < 1e-6
assert d.Holder.Tip == d.h_mount
assert d.Body.Shape.isValid() and d.Holder.Shape.isValid()
"Pump raised onto four columns"''',
    # holder finish
    helpers("Holder") + '''import FreeCADGui as Gui
b.Label = "Holder"
d.floor_corner_fillet.Label = "All four floor corners R1.1"
d.h_mount.Label = "Two M4 holes with countersinks"
d.post_one.Label = "First support column"
d.post_boss_one.Label = "Snap head on first column"
d.post_complete_four.Label = "Four complete support posts"
for o in b.Group:
    o.Visibility = False
d.h_mount.Visibility = True
for o in d.Objects:
    if o.TypeId in ("PartDesign::Plane", "PartDesign::Line", "Sketcher::SketchObject"):
        o.Visibility = False
d.Body.Visibility = True
b.Visibility = True
d.recompute()
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
d.save()
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
