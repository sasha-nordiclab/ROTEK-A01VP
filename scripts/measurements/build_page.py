"""Builds the measurement page (HTML) and per-view SVGs from views.json.

Screen coords are mm with y down. Model -> screen per view:
  A (mounting face, from the wall side): (x, y) -> (x, y)
  B (side, outlet up):                    (x, z) -> (x, -z)
  C (inlet end):                          (y, z) -> (-y, -z)
  D (motor end):                          (y, z) -> (y, -z)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'views.json')))
p = R['params']

ax = p['ax_h']
xt = p['x_tip']
xfs, xfe = p['x_fs'], p['x_fe']
pw = p['fl_w'] / 2
hx0, hx1 = xt + p['head_x0'], xt + p['head_x1']
xend = xt + p['p_len']
xcap0 = xend - p['cap_len']
Rm, Rh, Rc, Rcap = p['p_d'] / 2, p['head_d'] / 2, p['cov_d'] / 2, p['cap_d'] / 2
Rlk, er = p['ear_lk'] / 2, p['ear_r']
ea = math.radians(p['ear_a'])
hs = p['hole_dx'] / 2          # slot centre |x|
hy = p['hole_dy'] / 2          # slot centre |y|
sw = p['hole_d'] / 2           # slot half width
x_wall = hs + sw               # slot outer wall |x|
x_hook = x_wall - p['hook_l']  # hook end |x|
y_in = hy - p['hook_w'] / 2    # slot inner end |y| (hook bottom)
x_out = xt + p['out_x']
y_out = p['out_y']
z_out_tip = p['out_reach']
z_barb0 = z_out_tip - p['out_len']
rb, rd = p['out_d'] / 2, p['out_d2'] / 2
x_cov = hx0 - p['cov_t']
x_scr = hx0 - p['scr_h']
# ears in the YZ plane: (y, z) of each lug centre
EAR = {
    'A': (-Rlk * math.cos(ea), ax + Rlk * math.sin(ea)),
    'B': (Rlk * math.sin(ea), ax + Rlk * math.cos(ea)),
    'C': (Rlk * math.cos(ea), ax - Rlk * math.sin(ea)),
    'D': (-Rlk * math.sin(ea), ax - Rlk * math.cos(ea)),
}
gy, gz = p['grm_y'], ax             # wire hole
g_half_w = p['grm_w'] / 2
g_z0 = ax + p['grm_z'] - p['grm_l'] / 2
g_z1 = ax + p['grm_z'] + p['grm_l'] / 2

# pocket grid
ra0, ra1, rb0, rb1 = p['pk_ra0'], p['pk_ra1'], p['pk_rb0'], p['pk_rb1']
rc0, rc1, rd0, rd1 = p['pk_rc0'], p['pk_rc1'], p['pk_rd0'], p['pk_rd1']
c3 = p['pk_c3w'] / 2
c2a, c2b, c1a, c1b = p['pk_c2a'], p['pk_c2b'], p['pk_c1a'], p['pk_c1b']
phx = p['pk_hx']


def r2(v):
    return round(v + 0.0, 2)


# ------------------------------------------------------------------ rows
# id, view, label, how, prio, model, drawing, source, check
ROWS = []


def row(i, label, how, prio, model, drawing=None, source='', check=False):
    ROWS.append(dict(id=i, view=i[0], label=label, how=how, prio=prio, model=r2(model),
                     drawing=drawing, source=source, check=check))


OJ, IJ, DR, TB = 'Outside jaws', 'Inside jaws', 'Depth rod', 'From the table'
row('A1', 'Plate width, across the slotted edges', OJ, 'A', p['fl_w'], 45, 'caliper 44.93, 45.0')
row('A2', 'Plate length along the pump axis', OJ, 'A', p['fl_len'], 32, 'caliper 32.03, 32.0')
row('A3', 'Slot pitch along the axis, centre to centre', IJ + ' across the outer walls of two slots on one edge, minus A5', 'A', p['hole_dx'], 20, 'caliper 20.0')
row('A4', 'Slot depth: side edge to the inner end of the slot', DR + ' from the side edge', 'A', p['fl_w'] / 2 - y_in, 6.65, 'caliper 6.85 (earlier 6.30, 6.59)')
row('A5', 'Slot width at the entry, at the plate edge', IJ, 'A', p['hole_d'], 3.3, 'caliper 3.37, 3.39, 3.40')
row('A6', 'Slot width in the hook', IJ, 'A', p['hook_w'], 3.3, 'caliper 3.5')
row('A7', 'Slot length along the axis, hook included', IJ, 'A', p['hook_l'], 5.2, 'caliper 5.46')
row('A8', 'Motor-end edge of the plate to the nearest slot wall', DR + ' from the plate end', 'A', xfe - x_wall, 3.35, 'caliper 3.45')
row('A9', 'Inlet-end edge of the plate to the nearest slot wall', DR + ' from the plate end', 'A', -x_wall - xfs, 5.35, 'caliper 5.5; A8 + A9 + the slots run 0.25 over A2')
row('A10', 'Frame at the inlet end, edge to the first pocket', DR, 'B', p['pk_fi'], None, 'caliper 1.5')
row('A11', 'Pocket length along the axis, three inlet-side rows', IJ, 'B', p['pk_h'], None, 'photo', True)
row('A12', 'Rib between two pockets', OJ, 'B', p['rib'], None, 'photo', True)
row('A13', 'Pocket length, motor-end row', IJ, 'B', rd1 - rd0, None, 'caliper 4.5')
row('A14', 'Frame at the motor end, edge to the last pocket', DR, 'B', p['pk_fm'], None, 'caliper 1.5')
row('A15', 'Centre pocket width', IJ, 'B', p['pk_c3w'], None, 'photo')
row('A16', 'Width of the pockets next to the centre ones', IJ, 'B', p['pk_c2w'], None, 'caliper 4.3')
row('A17', 'Outer pocket width, towards the slotted edge', IJ, 'B', c1b - c1a, None, 'photo')
row('A18', 'Frame along the slotted edge', DR, 'B', p['frame'], None, 'caliper 1.5')
row('A19', 'Outer pocket, inlet side: length of the part beside the hook', IJ, 'B', rb1 + phx, None, 'photo', True)
row('A20', 'Outer pocket, motor side: length of the part beside the hook', IJ, 'B', phx - rc0, None, 'caliper 4.0, off by 0.3 after the plate shift', True)
row('A21', 'Depth of the four centre pockets', DR, 'A', p['pk_dc'], None, 'caliper 2.5')
row('A22', 'Depth of the other pockets', DR, 'A', p['pk_d'], None, 'caliper 1.5')

row('B1', 'Overall length: inlet tip to the motor end face, grommet excluded', OJ, 'A', p['p_len'], 75, 'caliper 74.5')
row('B2', 'Inlet tip to the inlet-end edge of the plate', DR + ' or outside jaws', 'A', xfs - xt, 32, 'caliper 31.5; B2 + A2 + B3 is 1.0 short of B1', True)
row('B3', 'Motor-end edge of the plate to the motor end face', DR + ' from the plate end', 'A', xend - xfe, 11, 'caliper 10.0 and 10.22; see B2', True)
row('B4', 'Inlet tip to the ear-lug face, under the screw heads', DR + ' or outside jaws', 'B', hx0 - xt, None, 'caliper 15.0; photo IMG_7253 15.0')
row('B5', 'Inlet tip to the face of the Ø32 cover', DR + ' or outside jaws', 'B', x_cov - xt, None, 'guess', True)
row('B6', 'Head length: ear-lug face to the joint with the motor', OJ, 'B', hx1 - hx0, 15.5, 'photo 16.4; caliper 14.0 disagrees', True)
row('B7', 'Inlet barb length (the Ø14.4 part)', OJ, 'B', p['in_len'], 4, 'caliper 4.0')
row('B8', 'Neck length (the Ø13.4 part)', OJ, 'B', p['neck_len'], 7, 'caliper 8.2')
row('B9', 'Neck diameter', OJ, 'B', p['neck_d'], 13.4, 'caliper 13.5')
row('B10', 'Mounting face to the top of the motor (gives the axis height)', OJ + ' from the plate frame over the motor', 'A', ax + Rm, None, 'not measured', True)
row('B11', 'Table to the top of the highest ear lug', TB + ', depth rod', 'A', EAR['B'][1] + er, None, 'caliper 40.75; drawing 42')
row('B12', 'Table to the outlet tip', TB + ', depth rod', 'A', z_out_tip, 52, 'caliper 51.4')
row('B13', 'Inlet tip to the outlet axis', OJ + ' to the near side of the outlet, plus half of C13', 'B', p['out_x'], 16.5, 'tube tangent to the boss, front flush with the boss face', True)
row('B14', 'Outlet barb length (the Ø8 part)', OJ, 'B', p['out_len'], 5, 'caliper 5.0')
row('B15', 'Step at the motor end: shoulder to the end face', DR, 'B', p['cap_len'], None, 'caliper 2.0')
row('B16', 'Grommet height above the motor end face', DR, 'B', p['grm_t'], None, 'guess')
row('B17', 'Inlet tip to the motor-end edge of the plate', OJ + ', jaws from the mounting-face side', 'A', xfe - xt, 64, 'new: cross-checks B2', True)
row('B18', 'Inlet-end edge of the plate to the motor end face', OJ + ', jaws from the mounting-face side', 'A', xend - xfs, 43, 'new: cross-checks B3', True)

row('C1', 'Head diameter', OJ, 'A', p['head_d'], 40, 'caliper 40.29')
row('C2', 'Diameter of the raised Ø32 cover', OJ, 'B', p['cov_d'], 32, 'caliper 31.99')
row('C3', 'Diameter of the boss (mini flange) around the inlet', OJ, 'B', p['boss_d'], 23, 'photo 22.3; model keeps it tangent to the outlet tube', True)
row('C4', 'Inlet barb diameter', OJ, 'B', p['in_d'], 14.4, 'drawing')
row('C5', 'Across two opposite ear lugs, outer edges', OJ, 'A', 2 * Rlk + 2 * er, 49.1, 'caliper 49.0')
row('C6', 'Ear lug width', OJ, 'B', 2 * er, 6.7, 'caliper 6.8')
row('C7', 'Table to the top of the lower screw head, side away from the outlet', TB + ', depth rod', 'A', EAR['C'][1] + p['scr_d'] / 2, None, 'not measured (checks the ear angle)', True)
row('C8', 'Table to the top of the lower screw head, outlet side', TB + ', depth rod', 'A', EAR['D'][1] + p['scr_d'] / 2, None, 'not measured (checks the ear angle)', True)
row('C9', 'Partition width', OJ, 'B', p['rib_t'], None, 'caliper 2.17')
row('C10', 'Partition height above the recessed segments', DR, 'B', p['rib_h'], None, 'caliper 1.5')
row('C11', 'Far side of the outlet tube to the opposite side of the head', OJ, 'A', Rh - y_out + rd, None, 'caliper 31.0')
row('C12', 'Outlet barb diameter', OJ, 'B', p['out_d'], 8, 'caliper 8.0')
row('C13', 'Outlet tube diameter below the barb', OJ, 'B', p['out_d2'], 7, 'caliper 6.9')
row('C14', 'Screw head diameter', OJ, 'B', p['scr_d'], None, 'caliper 5.0')
row('C15', 'Screw head height above the ear lug', DR, 'B', p['scr_h'], None, 'caliper 2.0')

row('D1', 'Motor diameter', OJ, 'A', p['p_d'], None, 'caliper 36.72')
row('D2', 'Diameter of the motor end face (inside the step)', OJ, 'B', p['cap_d'], None, 'caliper 33.2')
row('D3', 'Motor side (outlet side) to the centre of the wire hole', DR + ' or outside jaws', 'A', Rm + gy, None, 'photo', True)
row('D4', 'Grommet length', OJ, 'B', p['grm_l'], None, 'caliper 15.0')
row('D5', 'Grommet width', OJ, 'B', p['grm_w'], None, 'caliper 9.5')
row('D6', 'Table to the centre of the wire hole', TB + ', depth rod', 'A', gz, None, 'photo', True)
row('D7', 'Plate thickness at the edge', OJ, 'A', p['fl_t'], 3.5, 'caliper 2.98, 3.0')
row('D8', 'Width of the web between the plate and the motor', OJ, 'B', p['web_w'], None, 'guess')

# ------------------------------------------------------------------ overlay primitives
EXT_GAP, EXT_OVER, ARW, ARH, BUB = 0.7, 1.0, 1.3, 0.45, 1.9


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def arrow(tip, d):
    # filled triangle with its tip at `tip`, pointing along unit vector d
    bx, by = tip[0] - d[0] * ARW, tip[1] - d[1] * ARW
    nx, ny = -d[1] * ARH, d[0] * ARH
    return f'<path class="ah" d="M{f(tip[0])} {f(tip[1])}L{f(bx + nx)} {f(by + ny)}L{f(bx - nx)} {f(by - ny)}Z"/>'


def bubble(i, c, depth=False):
    cls = 'tag depth' if depth else 'tag'
    return (f'<g class="{cls}" data-id="{i}" tabindex="0" role="button" aria-label="Dimension {i}">'
            f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{BUB}"/>'
            f'<text x="{f(c[0])}" y="{f(c[1])}">{i}</text></g>')


def dimline(i, q1, q2, bub=None):
    """Dimension line q1-q2 with arrows; bubble at `bub` (leader if off the line) or at the middle."""
    dx, dy = q2[0] - q1[0], q2[1] - q1[1]
    L = math.hypot(dx, dy)
    u = (dx / L, dy / L)
    out = []
    if L >= 2 * ARW + 0.6:
        out.append(f'<line class="dl" x1="{f(q1[0])}" y1="{f(q1[1])}" x2="{f(q2[0])}" y2="{f(q2[1])}"/>')
        out.append(arrow(q1, (-u[0], -u[1])))
        out.append(arrow(q2, u))
    else:  # short: arrows outside, pointing inwards
        a = (q1[0] - u[0] * 3, q1[1] - u[1] * 3)
        b = (q2[0] + u[0] * 3, q2[1] + u[1] * 3)
        out.append(f'<line class="dl" x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}"/>')
        out.append(arrow(q1, u))
        out.append(arrow(q2, (-u[0], -u[1])))
    mid = ((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2)
    if bub is None:
        bub = mid
    else:
        out.append(f'<line class="ld" x1="{f(mid[0])}" y1="{f(mid[1])}" x2="{f(bub[0])}" y2="{f(bub[1])}"/>')
    return out, bub


def ext(a, b):
    return f'<line class="xl" x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}"/>'


def ext_to(pt, toward, gap=EXT_GAP, over=EXT_OVER):
    """Extension line from feature point `pt` to dimension point `toward`, gap at the part, overshoot."""
    dx, dy = toward[0] - pt[0], toward[1] - pt[1]
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return ''
    u = (dx / L, dy / L)
    return ext((pt[0] + u[0] * gap, pt[1] + u[1] * gap), (toward[0] + u[0] * over, toward[1] + u[1] * over))


def H(i, x1, x2, yl, y1=None, y2=None, bub=None):
    """Horizontal dimension between x1 and x2 at screen y = yl; extension lines from y1/y2."""
    out = []
    if y1 is not None:
        out.append(ext_to((x1, y1), (x1, yl)))
    if y2 is not None:
        out.append(ext_to((x2, y2), (x2, yl)))
    d, b = dimline(i, (x1, yl), (x2, yl), bub)
    return out + d + [bubble(i, b)]


def Vd(i, y1, y2, xl, x1=None, x2=None, bub=None):
    """Vertical dimension between screen y1 and y2 at x = xl; extension lines from x1/x2."""
    out = []
    if x1 is not None:
        out.append(ext_to((x1, y1), (xl, y1)))
    if x2 is not None:
        out.append(ext_to((x2, y2), (xl, y2)))
    d, b = dimline(i, (xl, y1), (xl, y2), bub)
    return out + d + [bubble(i, b)]


def Slant(i, p1, p2, off):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy)
    n = (-dy / L, dx / L)
    q1 = (p1[0] + n[0] * off, p1[1] + n[1] * off)
    q2 = (p2[0] + n[0] * off, p2[1] + n[1] * off)
    out = [ext_to(p1, q1), ext_to(p2, q2)]
    d, b = dimline(i, q1, q2)
    return out + d + [bubble(i, b)]


def Lead(i, pt, at, depth=False):
    return [f'<circle class="dot" cx="{f(pt[0])}" cy="{f(pt[1])}" r="0.35"/>',
            f'<line class="ld" x1="{f(pt[0])}" y1="{f(pt[1])}" x2="{f(at[0])}" y2="{f(at[1])}"/>',
            bubble(i, at, depth)]


def Tag(i, at, depth=True):
    return [bubble(i, at, depth)]


def on_circle(cx, cy, r, deg):
    # screen angle, counter-clockwise from +x with y up
    t = math.radians(deg)
    return (cx + r * math.cos(t), cy - r * math.sin(t))


# ------------------------------------------------------------------ per-view overlays
OV = {k: [] for k in 'ABCD'}

# A: mounting face (x, y)
A = OV['A']
A += H('A2', xfs, xfe, pw + 8, pw, pw)
A += Vd('A1', -pw, pw, xfs - 8, xfs, xfs)
A += H('A3', -hs, hs, -pw - 5.5, -hy, -hy)
A += Vd('A4', -pw, -y_in, -x_wall - 2.0, -hs, -hs)
A += Lead('A5', (x_wall - 0.9, -pw + 1.2), (pw - 1.5, -pw - 5.5))
A += Lead('A6', (x_hook + 1.2, -hy - 0.4), (3.0, -pw - 2.8))
A += H('A7', x_hook, x_wall, -hy + 4.2, -hy, -hy)
A += H('A8', x_wall, xfe, pw + 3.5, pw, pw)
A += H('A9', xfs, -x_wall, pw + 3.5, pw, pw)
A += H('A10', xfs, ra0, 0, bub=(xfs - 3.6, -3.4))
A += H('A11', ra0, ra1, 0)
A += H('A12', ra1, rb0, 0, bub=((ra1 + rb0) / 2, 8.6))
A += H('A13', rd0, rd1, 0)
A += H('A14', rd1, xfe, 0, bub=(xfe + 3.6, -3.4))
xc = (rb0 + rb1) / 2 + 0.6
A += Vd('A15', -c3, c3, xc)
A += Vd('A16', -c2b, -c2a, xc)
A += Vd('A17', -c1b, -c1a, xc)
A += Vd('A18', -pw, -c1b, xc, bub=(xc - 3.6, -pw - 2.8))
A += H('A19', -phx, rb1, 17.0)
A += H('A20', rc0, phx, 17.0)
A += Tag('A21', ((rc0 + rc1) / 2, 2.6))
A += Tag('A22', ((rc0 + rc1) / 2, (c2a + c2b) / 2))

# B: side (x, -z)
B = OV['B']
S = lambda x, z: (x, -z)
B += H('B1', xt, xend, 16, -(ax - p['in_d'] / 2), -(ax - Rcap))
B += H('B2', xt, xfs, 12, -(ax - p['in_d'] / 2), 0)
B += H('B5', xt, x_cov, 8, -(ax - p['in_d'] / 2), -(ax - Rc))
B += H('B4', xt, hx0, 4, -(ax - p['in_d'] / 2), -(EAR['D'][1] - er))
B += H('B6', hx0, hx1, 4, -(ax - Rh), -(ax - Rh))
B += H('B3', xfe, xend, 4, 0, -(ax - Rcap))
B += H('B17', xt, xfe, 20, -(ax - p['in_d'] / 2), 0)
B += H('B18', xfs, xend, 8, 0, -(ax - Rcap))
B += H('B7', xt, xt + p['in_len'], -(ax + p['in_d'] / 2 + 2.6), -(ax + p['in_d'] / 2), -(ax + p['in_d'] / 2))
B += H('B8', xt + p['in_len'], xt + p['in_len'] + p['neck_len'], -(ax + p['in_d'] / 2 + 2.6), None, -(ax + p['neck_d'] / 2))
B += Lead('B9', (xt + p['in_len'] + p['neck_len'] / 2, -(ax - p['neck_d'] / 2)), (xt + p['in_len'] + 0.5, -8.0))
B += Vd('B10', 0, -(ax + Rm), xend + 15, None, 5)
B += Vd('B11', 0, -(EAR['B'][1] + er), xend + 21, None, hx0 + 7)
B += Vd('B12', 0, -z_out_tip, xt - 6, None, x_out - rb)
B += H('B13', xt, x_out, -(z_out_tip + 4), -(ax + p['in_d'] / 2), -z_out_tip)
B += Vd('B14', -z_barb0, -z_out_tip, x_out + rb + 3, x_out + rb, x_out + rb)
B += H('B15', xcap0, xend, -(ax + Rm + 5.5), -(ax + Rm), -(ax + Rcap), bub=(xend + 5, -(ax + Rm + 9)))
B += H('B16', xend, xend + p['grm_t'], -(g_z1 + 2.8), -g_z1, -g_z1, bub=(xend + 6.5, -(g_z1 + 6)))

# C: inlet end (-y, -z)
C = OV['C']
Sc = lambda y, z: (-y, -z)
C += H('C11', -Rh, -y_out + rd, -(z_barb0 - 0.5) - 1.5, -ax, -(z_barb0 - 2))
pA, pC = Sc(*EAR['A']), Sc(*EAR['C'])
uu = ((pA[0] - pC[0]) / (2 * Rlk), (pA[1] - pC[1]) / (2 * Rlk))
C += Slant('C5', (pC[0] - uu[0] * er, pC[1] - uu[1] * er), (pA[0] + uu[0] * er, pA[1] + uu[1] * er), 5)
pB = Sc(*EAR['B'])
C += Lead('C6', (pB[0] - er * 0.85, pB[1] - er * 0.5), (-Rh - 6, -(EAR['B'][1] + 5)))
sC = Sc(*EAR['C'])
C += Vd('C7', 0, sC[1] - p['scr_d'] / 2, -Rh - 7, None, sC[0])
sD = Sc(*EAR['D'])
C += Vd('C8', 0, sD[1] - p['scr_d'] / 2, Rh + 7, None, sD[0])
C += Lead('C1', on_circle(0, -ax, Rh, 150), (-Rh - 9, -(ax + 12)))
C += Lead('C9', (-(Rc + 1.5) * math.cos(math.radians(p['rib_a'])), -(ax + (Rc + 1.5) * math.sin(math.radians(p['rib_a'])))), (-Rh - 9, -(ax + 6)))
C += Lead('C4', on_circle(0, -ax, p['in_d'] / 2, 195), (-Rh - 9, -ax))
C += Lead('C10', ((Rc + 1.5) * math.cos(math.radians(p['rib_a'])), -(ax - (Rc + 1.5) * math.sin(math.radians(p['rib_a'])))), (Rh + 9, -(ax - 3)))
C += Lead('C2', on_circle(0, -ax, Rc, 250), (-8, 5))
C += Lead('C3', on_circle(0, -ax, p['boss_d'] / 2, 292), (6, 5))
C += Lead('C12', (-y_out + rb, -(z_out_tip - 2)), (-y_out + rb + 7, -(z_out_tip + 1)))
C += Lead('C13', (-y_out + rd, -(z_barb0 - 4)), (-y_out + rd + 7.5, -(z_barb0 - 4)))
C += Lead('C14', (pB[0] + p['scr_d'] / 2, pB[1]), (-6, -(z_out_tip + 1)))
C += Lead('C15', (pA[0] + p['scr_d'] / 2 * 0.7, pA[1] - 1.0), (Rh + 9, -(EAR['A'][1] + 3)))

# D: motor end (y, -z)
D = OV['D']
Sd = lambda y, z: (y, -z)
C_motor = (0, -ax)
D += H('D3', -Rm, gy, -(ax + Rm + 4.5), -ax, -gz)
D += Vd('D4', -g_z0, -g_z1, gy + g_half_w + 2.6, gy + g_half_w, gy + g_half_w)
D += H('D5', gy - g_half_w, gy + g_half_w, -(g_z1 + 3), -(ax + p['grm_z']), -(ax + p['grm_z']))
D += Vd('D6', 0, -gz, -Rm - 9.5, None, gy)
D += Vd('D7', 0, -p['fl_t'], pw + 4, None, pw, bub=(pw + 8.5, -6.5))
D += Lead('D8', (p['web_w'] / 2 - 1, -(p['fl_t'] + 0.7)), (p['web_w'] / 2 + 4, 5.5))
D += Lead('D1', on_circle(0, -ax, Rm, 38), (Rm + 7, -(ax + Rm + 2)))
D += Lead('D2', on_circle(0, -ax, Rcap, 62), (Rm - 2, -(ax + Rm + 7.5)))

# ------------------------------------------------------------------ assemble SVGs
VB = {  # x0, y0, w, h in screen mm
    'A': (-31, -34, 62, 70),
    'B': (-58, -64, 113, 90),
    'C': (-33, -58, 66, 69),
    'D': (-33, -60, 66, 71),
}
GROUND = {'B': True, 'C': True, 'D': True}


def edges_svg(v):
    out = []
    for kind in ('hard', 'outline', 'smooth'):
        segs = []
        for pl in R['views'][v][kind]:
            if len(pl) < 2:
                continue
            segs.append('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pl))
        if segs:
            out.append(f'<path class="e {kind}" d="{"".join(segs)}"/>')
    return out


def ground_svg(v):
    x0, y0, w, h = VB[v]
    out = [f'<line class="gl" x1="{f(x0 + 1)}" y1="0" x2="{f(x0 + w - 1)}" y2="0"/>']
    x = x0 + 2
    while x < x0 + w - 2:
        out.append(f'<line class="gh" x1="{f(x)}" y1="0.3" x2="{f(x - 1.6)}" y2="1.9"/>')
        x += 2.2
    out.append(f'<text class="gt" x="{f(x0 + w - 2)}" y="4.6">TABLE</text>')
    return out


def build_svg(v):
    x0, y0, w, h = VB[v]
    parts = [f'<svg class="dwg" viewBox="{f(x0)} {f(y0)} {f(w)} {f(h)}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="View {v}">']
    if GROUND.get(v):
        parts += ground_svg(v)
    parts += edges_svg(v)
    parts.append('<g class="ov">')
    parts += [s for s in OV[v] if s]
    parts.append('</g></svg>')
    return ''.join(parts)


SVGS = {v: build_svg(v) for v in 'ABCD'}
for v, s in SVGS.items():
    with open(os.path.join(HERE, f'view_{v}.svg'), 'w') as fh:
        fh.write(s.replace('<svg ', '<svg style="background:#fff" ', 1).replace('class="dwg"', 'class="dwg" font-family="monospace"'))

# sanity: every row has a tag and no tag lacks a row
tags = {s.split('data-id="')[1].split('"')[0] for v in OV for s in OV[v] if 'data-id="' in s}
ids = {r['id'] for r in ROWS}
assert tags == ids, (sorted(ids - tags), sorted(tags - ids))

json.dump(ROWS, open(os.path.join(HERE, 'rows.json'), 'w'), indent=1)
tpl = open(os.path.join(HERE, 'page_template.html')).read()
page = (tpl.replace('/*ROWS*/[]', json.dumps(ROWS, separators=(',', ':')))
        .replace('<!--SVG_A-->', SVGS['A']).replace('<!--SVG_B-->', SVGS['B'])
        .replace('<!--SVG_C-->', SVGS['C']).replace('<!--SVG_D-->', SVGS['D']))
open(os.path.join(HERE, 'pump_measurements.html'), 'w').write(page)
print(len(ROWS), 'rows;', {v: len(s) for v, s in SVGS.items()}, 'page', len(page))
