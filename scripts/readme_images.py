"""Export the README images from the open TPU_Pump_Holder document.

Standard View3D.saveImage of the live view, white background. The camera is
centred on the projected shape and scaled to fill the frame, because fitAll
frames the bounding sphere and leaves the model off-centre. Run in FreeCAD:
exec(open('scripts/readme_images.py').read(), {})
"""
import FreeCAD as App, FreeCADGui as Gui
import os
OUT = os.path.join(os.path.dirname(App.ActiveDocument.FileName), '..', 'docs', 'img') + os.sep
W, H, FILL = 1600, 1250, 0.88
d = App.ActiveDocument
v = Gui.ActiveDocument.ActiveView
vw = v.getViewer()
pump, holder = d.getObject('Body'), d.getObject('Holder')

def frame(bodies):
    cam = v.getCameraNode()
    rot = App.Rotation(*cam.orientation.getValue().getValue())
    right, up = rot.multVec(App.Vector(1, 0, 0)), rot.multVec(App.Vector(0, 1, 0))
    pts = [p for b in bodies for p in b.Shape.tessellate(0.2)[0]]
    xs = [p.dot(right) for p in pts]; ys = [p.dot(up) for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    pos = App.Vector(*cam.position.getValue().getValue())
    pos = pos + right * (cx - pos.dot(right)) + up * (cy - pos.dot(up))
    cam.position.setValue(pos.x, pos.y, pos.z)
    cam.height.setValue(max(bh, bw * H / W) / FILL)

def shot(name, bodies, turn):
    for b in (pump, holder):
        b.Visibility = b in bodies
    v.viewIsometric()
    if turn:
        v.setCameraOrientation(App.Rotation(App.Vector(0, 0, 1), -90).multiply(v.getCameraOrientation()))
    v.fitAll()
    frame(bodies)
    v.saveImage(OUT + name, W, H, 'White')

nc = vw.isEnabledNaviCube()
vw.setEnabledNaviCube(False)
try:
    for n, bs in (('assembly', [pump, holder]), ('pump', [pump]), ('holder', [holder])):
        shot(n + '_1.png', bs, False)
        shot(n + '_2.png', bs, True)
finally:
    pump.Visibility = holder.Visibility = True
    vw.setEnabledNaviCube(nc)
    v.viewIsometric(); v.fitAll()
