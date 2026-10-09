# Pump measurement sheet

Numbered dimensions of the `Pump` reference model in `cad/TPU_Pump_Holder.FCStd`, checked against the real Rotek WPDC-06.7L pump.
The live sheet with input fields is at https://claude.ai/artifact/8BBLBfdxXsbRfHfFudTgku; values typed there are saved and read back to correct the model.
Readings below: round 1, 2026-10-07.

## How to measure

- **Heights:** stand the pump on a flat table with the mounting face down and measure from the table with the depth rod, or with outside jaws from the plate frame.
- **Lengths along the pump:** from the tip of the inlet barb.
- **Priority A** rows shape the holder (plate, slots, outer size, outlet, cable); **B** rows refine the shape.
- **Tolerance:** ±0.10 mm for A, ±0.20 mm for B. Δ is the reading minus the model; ✗ marks a Δ past tolerance. Rows marked *check* are to measure next.

## A — Mounting face (seen from the wall side, inlet to the left)

![View A](view_A.svg)

| ID | Prio | Dimension | How | Model | Drawing | Reading | Δ | Source |
|---|---|---|---|---|---|---|---|---|
| A1 | A | Plate width, across the slotted edges | Outside jaws | 45 | 45 | 45 | +0.00 | caliper 44.93, 45.0 |
| A2 | A | Plate length along the pump axis | Outside jaws | 32 | 32 | 32 | +0.00 | caliper 32.03, 32.0 |
| A3 | A | Slot pitch along the axis, centre to centre | Inside jaws across the outer walls of two slots on one edge, minus A5 | 20 | 20 | 20 | +0.00 | caliper 20.0 |
| A4 | A | Slot depth: side edge to the inner end of the slot | Depth rod from the side edge | 6.75 | 6.65 | 6.85 | +0.10 | caliper 6.85 (earlier 6.30, 6.59) |
| A5 | A | Slot width at the entry, at the plate edge | Inside jaws | 3.3 | 3.3 | 3.4 | +0.10 | caliper 3.37, 3.39, 3.40 |
| A6 | A | Slot width in the hook | Inside jaws | 3.5 | 3.3 | 3.5 | +0.00 | caliper 3.5 |
| A7 | A | Slot length along the axis, hook included | Inside jaws | 5.46 | 5.2 | 5.46 | +0.00 | caliper 5.46 |
| A8 | A | Motor-end edge of the plate to the nearest slot wall | Depth rod from the plate end | 3.35 | 3.35 | 3.45 | +0.10 | caliper 3.45 |
| A9 | A | Inlet-end edge of the plate to the nearest slot wall | Depth rod from the plate end | 5.35 | 5.35 | 5.5 | +0.15 ✗ | caliper 5.5; A8 + A9 + the slots run 0.25 over A2 |
| A10 | B | Frame at the inlet end, edge to the first pocket | Depth rod | 1.5 | — | 1.5 | +0.00 | caliper 1.5 |
| A11 | B | Pocket length along the axis, three inlet-side rows | Inside jaws | 6.3 | — | — |  | photo — *check* |
| A12 | B | Rib between two pockets | Outside jaws | 1.8 | — | — |  | photo — *check* |
| A13 | B | Pocket length, motor-end row | Inside jaws | 4.6 | — | 4.5 | -0.10 | caliper 4.5 |
| A14 | B | Frame at the motor end, edge to the last pocket | Depth rod | 1.6 | — | 1.5 | -0.10 | caliper 1.5 |
| A15 | B | Centre pocket width | Inside jaws | 10.2 | — | — |  | photo |
| A16 | B | Width of the pockets next to the centre ones | Inside jaws | 4.3 | — | 4.3 | +0.00 | caliper 4.3 |
| A17 | B | Outer pocket width, towards the slotted edge | Inside jaws | 8.1 | — | — |  | photo |
| A18 | B | Frame along the slotted edge | Depth rod | 1.4 | — | 1.5 | +0.10 | caliper 1.5 |
| A19 | B | Outer pocket, inlet side: length of the part beside the hook | Inside jaws | 3.29 | — | — |  | photo — *check* |
| A20 | B | Outer pocket, motor side: length of the part beside the hook | Inside jaws | 3.69 | — | 4 | +0.31 ✗ | caliper 4.0, off by 0.3 after the plate shift — *check* |
| A21 | A | Depth of the four centre pockets | Depth rod | 2.5 | — | 2.5 | +0.00 | caliper 2.5 |
| A22 | A | Depth of the other pockets | Depth rod | 1.5 | — | 1.5 | +0.00 | caliper 1.5 |

## B — Side (mounting face on the table, outlet up)

![View B](view_B.svg)

| ID | Prio | Dimension | How | Model | Drawing | Reading | Δ | Source |
|---|---|---|---|---|---|---|---|---|
| B1 | A | Overall length: inlet tip to the motor end face, grommet excluded | Outside jaws | 74.5 | 75 | 74.5 | +0.00 | caliper 74.5 |
| B2 | A | Inlet tip to the inlet-end edge of the plate | Depth rod or outside jaws | 32 | 32 | 31.5 | -0.50 ✗ | caliper 31.5; B2 + A2 + B3 is 1.0 short of B1 — *check* |
| B3 | A | Motor-end edge of the plate to the motor end face | Depth rod from the plate end | 10.5 | 11 | 10 | -0.50 ✗ | caliper 10.0 and 10.22; see B2 — *check* |
| B4 | B | Inlet tip to the ear-lug face, under the screw heads | Depth rod or outside jaws | 15 | — | 15 | +0.00 | caliper 15.0; photo IMG_7253 15.0 |
| B5 | B | Inlet tip to the face of the Ø32 cover | Depth rod or outside jaws | 13.5 | — | — |  | guess — *check* |
| B6 | B | Head length: ear-lug face to the joint with the motor | Outside jaws | 16.4 | 15.5 | 14 | -2.40 ✗ | photo 16.4; caliper 14.0 disagrees — *check* |
| B7 | B | Inlet barb length (the Ø14.4 part) | Outside jaws | 4 | 4 | 4 | +0.00 | caliper 4.0 |
| B8 | B | Neck length (the Ø13.4 part) | Outside jaws | 8.2 | 7 | 8.2 | +0.00 | caliper 8.2 |
| B9 | B | Neck diameter | Outside jaws | 13.4 | 13.4 | 13.5 | +0.10 | caliper 13.5 |
| B10 | A | Mounting face to the top of the motor (gives the axis height) | Outside jaws from the plate frame over the motor | 39.63 | — | — |  | not measured — *check* |
| B11 | A | Table to the top of the highest ear lug | From the table, depth rod | 40.75 | — | 40.75 | +0.00 | caliper 40.75; drawing 42 |
| B12 | A | Table to the outlet tip | From the table, depth rod | 51.4 | 52 | 51.4 | +0.00 | caliper 51.4 |
| B13 | B | Inlet tip to the outlet axis | Outside jaws to the near side of the outlet, plus half of C13 | 15.75 | 16.5 | — |  | tube tangent to the boss, front flush with the boss face — *check* |
| B14 | B | Outlet barb length (the Ø8 part) | Outside jaws | 5 | 5 | 5 | +0.00 | caliper 5.0 |
| B15 | B | Step at the motor end: shoulder to the end face | Depth rod | 2 | — | 2 | +0.00 | caliper 2.0 |
| B16 | B | Grommet height above the motor end face | Depth rod | 1.5 | — | — |  | guess |
| B17 | A | Inlet tip to the motor-end edge of the plate | Outside jaws, jaws from the mounting-face side | 64 | 64 | — |  | new: cross-checks B2 — *check* |
| B18 | A | Inlet-end edge of the plate to the motor end face | Outside jaws, jaws from the mounting-face side | 42.5 | 43 | — |  | new: cross-checks B3 — *check* |

## C — Inlet end

![View C](view_C.svg)

| ID | Prio | Dimension | How | Model | Drawing | Reading | Δ | Source |
|---|---|---|---|---|---|---|---|---|
| C1 | A | Head diameter | Outside jaws | 40.3 | 40 | 40.29 | -0.01 | caliper 40.29 |
| C2 | B | Diameter of the raised Ø32 cover | Outside jaws | 31.99 | 32 | 31.99 | +0.00 | caliper 31.99 |
| C3 | B | Diameter of the boss (mini flange) around the inlet | Outside jaws | 21.7 | 23 | — |  | photo 22.3; model keeps it tangent to the outlet tube — *check* |
| C4 | B | Inlet barb diameter | Outside jaws | 14.4 | 14.4 | — |  | drawing |
| C5 | A | Across two opposite ear lugs, outer edges | Outside jaws | 49.1 | 49.1 | 49 | -0.10 | caliper 49.0 |
| C6 | B | Ear lug width | Outside jaws | 6.7 | 6.7 | 6.8 | +0.10 | caliper 6.8 |
| C7 | A | Table to the top of the lower screw head, side away from the outlet | From the table, depth rod | 10.01 | — | — |  | not measured (checks the ear angle) — *check* |
| C8 | A | Table to the top of the lower screw head, outlet side | From the table, depth rod | 7.66 | — | — |  | not measured (checks the ear angle) — *check* |
| C9 | B | Partition width | Outside jaws | 2.17 | — | 2.17 | +0.00 | caliper 2.17 |
| C10 | B | Partition height above the recessed segments | Depth rod | 1.5 | — | 1.5 | +0.00 | caliper 1.5 |
| C11 | A | Far side of the outlet tube to the opposite side of the head | Outside jaws | 31 | — | 31 | +0.00 | caliper 31.0 |
| C12 | B | Outlet barb diameter | Outside jaws | 8 | 8 | 8 | +0.00 | caliper 8.0 |
| C13 | B | Outlet tube diameter below the barb | Outside jaws | 7 | 7 | 6.9 | -0.10 | caliper 6.9 |
| C14 | B | Screw head diameter | Outside jaws | 5 | — | 5 | +0.00 | caliper 5.0 |
| C15 | B | Screw head height above the ear lug | Depth rod | 2.2 | — | 2 | -0.20 | caliper 2.0 |

## D — Motor end

![View D](view_D.svg)

| ID | Prio | Dimension | How | Model | Drawing | Reading | Δ | Source |
|---|---|---|---|---|---|---|---|---|
| D1 | A | Motor diameter | Outside jaws | 36.7 | — | 36.72 | +0.02 | caliper 36.72 |
| D2 | B | Diameter of the motor end face (inside the step) | Outside jaws | 33.2 | — | 33.2 | +0.00 | caliper 33.2 |
| D3 | A | Motor side (outlet side) to the centre of the wire hole | Depth rod or outside jaws | 9.05 | — | — |  | photo — *check* |
| D4 | B | Grommet length | Outside jaws | 15 | — | 15 | +0.00 | caliper 15.0 |
| D5 | B | Grommet width | Outside jaws | 9.5 | — | 9.5 | +0.00 | caliper 9.5 |
| D6 | A | Table to the centre of the wire hole | From the table, depth rod | 21.28 | — | — |  | photo — *check* |
| D7 | A | Plate thickness at the edge | Outside jaws | 3 | 3.5 | 3 | +0.00 | caliper 2.98, 3.0 |
| D8 | B | Width of the web between the plate and the motor | Outside jaws | 13 | — | — |  | guess |
