# TPU pump holder — vibration-damping mount

A TPU holder for the Rotek WPDC-06.7L-10M-24-VP pump (PUM409) that damps the pump's vibration.

## Model

**Working model:** [TPU_Pump_Holder.FCStd](cad/TPU_Pump_Holder.FCStd).

- Body **Pump** is a reference model of the pump, built from the manufacturer's drawing, photos and caliper measurements. Every size is in the `params` spreadsheet.
- The holder comes next, as a separate body.

### Coordinates

- Origin: the centre of the four mount slots, on the mounting face of the plate (z = 0).
- X runs along the pump axis, with the inlet towards −X (inlet tip at x = −49).
- Z points from the mounting face into the pump. The pump axis is at `ax_h` = 21.28 mm.
- The holder goes below z = 0.

### Mount plate

- 45 × 32 × 3.0 mm, symmetric about the slots.
- Four L-shaped bayonet slots, 3.3 mm wide: the entry is open to the side edge, and a 5.46 mm hook turns towards the middle of the plate. Slot pitch 20 × 35 mm.
- Sixteen pockets on the mounting face: the centre column is 2.5 mm deep (a 13 mm web to the motor sits behind it), the rest are 1.5 mm deep.

### Not measured yet

- Mounting face to the far side of the motor (39.6 mm in the model). Until then `ax_h` comes from the drawing only.

## Folders

- `cad/` — FreeCAD model.
- `docs/` — notes and calculations.
- `exports/step/` — STEP files of the printed parts.
- `references/` — the manufacturer's drawing and measurement photos.
