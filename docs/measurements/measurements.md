# Pump measurement sheet

Numbered dimensions of the `Pump` reference model in `cad/TPU_Pump_Holder.FCStd`, to check against the real Rotek WPDC-06.7L pump.
The live sheet with input fields is at https://claude.ai/artifact/8BBLBfdxXsbRfHfFudTgku; values typed there are saved and read back to correct the model.

## How to measure

- **Heights:** stand the pump on a flat table with the mounting face down and measure from the table with the depth rod.
- **Lengths along the pump:** from the tip of the inlet barb.
- **Priority A** rows shape the holder (plate, slots, outer size, outlet, cable); **B** rows refine the shape.
- **Tolerance:** ±0.10 mm for A, ±0.20 mm for B. Rows marked *check* disagree with the drawing or with an earlier reading.

## A — Mounting face (seen from the wall side, inlet to the left)

![View A](view_A.svg)

| ID | Prio | Dimension | How | Model | Drawing | Earlier source |
|---|---|---|---|---|---|---|
| A1 | A | Plate width, across the slotted edges | Outside jaws | 45 | 45 | caliper 44.93 |
| A2 | A | Plate length along the pump axis | Outside jaws | 32 | 32 | caliper 32.03 |
| A3 | A | Slot pitch along the axis, centre to centre | Inside jaws across the outer walls of two slots on one edge, minus A5 | 20 | 20 | caliper 23.36 − 3.24 |
| A4 | A | Slot depth: side edge to the inner end of the slot | Depth rod from the side edge | 6.65 | 6.65 | caliper 6.30 and 6.59, disagree — *check* |
| A5 | A | Slot width at the entry, at the plate edge | Inside jaws | 3.3 | 3.3 | caliper 3.37 and 3.39 — *check* |
| A6 | A | Slot width in the hook | Inside jaws | 3.3 | 3.3 | caliper 3.24, place unsure — *check* |
| A7 | A | Slot length along the axis, hook included | Inside jaws | 5.46 | 5.2 | caliper 5.46 |
| A8 | A | Motor-end edge of the plate to the nearest slot wall | Depth rod from the plate end | 4.35 | 3.35 | photo; drawing says 3.35 — *check* |
| A9 | A | Inlet-end edge of the plate to the nearest slot wall | Depth rod from the plate end | 4.35 | 5.35 | photo; drawing says 5.35 — *check* |
| A10 | B | Frame at the inlet end, edge to the first pocket | Depth rod | 1.2 | — | photo |
| A11 | B | Pocket length along the axis, three inlet-side rows | Inside jaws | 6.3 | — | photo |
| A12 | B | Rib between two pockets | Outside jaws | 1.8 | — | photo |
| A13 | B | Pocket length, motor-end row | Inside jaws | 4.9 | — | photo |
| A14 | B | Frame at the motor end, edge to the last pocket | Depth rod | 1.6 | — | photo |
| A15 | B | Centre pocket width | Inside jaws | 10.2 | — | photo |
| A16 | B | Width of the pockets next to the centre ones | Inside jaws | 4 | — | photo |
| A17 | B | Outer pocket width, towards the slotted edge | Inside jaws | 8.4 | — | photo |
| A18 | B | Frame along the slotted edge | Depth rod | 1.4 | — | photo |
| A19 | B | Outer pocket, inlet side: length of the part beside the hook | Inside jaws | 3.99 | — | photo |
| A20 | B | Outer pocket, motor side: length of the part beside the hook | Inside jaws | 2.99 | — | photo |
| A21 | A | Depth of the four centre pockets | Depth rod | 2.5 | — | caliper 2.5 |
| A22 | A | Depth of the other pockets | Depth rod | 1.5 | — | caliper 1.5 |

## B — Side (mounting face on the table, outlet up)

![View B](view_B.svg)

| ID | Prio | Dimension | How | Model | Drawing | Earlier source |
|---|---|---|---|---|---|---|
| B1 | A | Overall length: inlet tip to the motor end face, grommet excluded | Outside jaws | 75 | 75 | drawing |
| B2 | A | Inlet tip to the inlet-end edge of the plate | Depth rod or outside jaws | 33 | 32 | photo; drawing says 32 — *check* |
| B3 | A | Motor-end edge of the plate to the motor end face | Depth rod from the plate end | 10 | 11 | caliper 10.22, unsure what it spanned — *check* |
| B4 | B | Inlet tip to the screw heads | Depth rod or outside jaws | 14.3 | — | guess |
| B5 | B | Inlet tip to the face of the Ø32 cover | Depth rod or outside jaws | 15 | — | guess |
| B6 | B | Head length: ear-lug face to the joint with the motor | Outside jaws | 15.5 | 15.5 | drawing |
| B7 | B | Inlet barb length (the Ø14.4 part) | Outside jaws | 4 | 4 | drawing |
| B8 | B | Neck length (the Ø13.4 part) | Outside jaws | 7 | 7 | drawing |
| B9 | B | Neck diameter | Outside jaws | 13.4 | 13.4 | drawing |
| B10 | A | Table to the top of the motor (gives the axis height) | From the table, depth rod | 39.63 | — | not measured — *check* |
| B11 | A | Table to the top of the highest ear lug | From the table, depth rod | 42 | — | not measured |
| B12 | A | Table to the outlet tip | From the table, depth rod | 52 | 52 | drawing |
| B13 | B | Inlet tip to the outlet axis | Outside jaws to the near side of the outlet, plus half of C13 | 16.5 | 16.5 | drawing |
| B14 | B | Outlet barb length (the Ø8 part) | Outside jaws | 5 | 5 | drawing |
| B15 | B | Step at the motor end: shoulder to the end face | Depth rod | 2.4 | — | guess |
| B16 | B | Grommet height above the motor end face | Depth rod | 1.5 | — | guess |

## C — Inlet end

![View C](view_C.svg)

| ID | Prio | Dimension | How | Model | Drawing | Earlier source |
|---|---|---|---|---|---|---|
| C1 | A | Head diameter | Outside jaws | 40.3 | 40 | caliper 40.29 |
| C2 | B | Diameter of the raised Ø32 cover | Outside jaws | 31.99 | 32 | caliper 31.99 |
| C3 | B | Diameter of the boss around the inlet | Outside jaws | 23 | 23 | drawing |
| C4 | B | Inlet barb diameter | Outside jaws | 14.4 | 14.4 | drawing |
| C5 | A | Across two opposite ear lugs, outer edges | Outside jaws | 49.1 | 49.1 | drawing |
| C6 | B | Ear lug width | Outside jaws | 6.7 | 6.7 | drawing |
| C7 | A | Table to the top of the lower screw head, side away from the outlet | From the table, depth rod | 11.62 | — | not measured (checks the 35° ear angle) |
| C8 | A | Table to the top of the lower screw head, outlet side | From the table, depth rod | 6.42 | — | not measured (checks the 35° ear angle) |
| C9 | B | Partition width | Outside jaws | 2.17 | — | caliper 2.17 |
| C10 | B | Partition height above the recessed segments | Depth rod | 1.5 | — | caliper 1.5 |
| C11 | A | Far side of the outlet tube to the opposite side of the head | Outside jaws | 31.65 | — | not measured (gives the outlet offset) — *check* |
| C12 | B | Outlet barb diameter | Outside jaws | 8 | 8 | drawing |
| C13 | B | Outlet tube diameter below the barb | Outside jaws | 7 | 7 | drawing |
| C14 | B | Screw head diameter | Outside jaws | 5 | — | guess |
| C15 | B | Screw head height above the ear lug | Depth rod | 2.2 | — | guess |

## D — Motor end

![View D](view_D.svg)

| ID | Prio | Dimension | How | Model | Drawing | Earlier source |
|---|---|---|---|---|---|---|
| D1 | A | Motor diameter | Outside jaws | 36.7 | — | caliper 36.72 |
| D2 | B | Diameter of the motor end face (inside the step) | Outside jaws | 33.6 | — | photo |
| D3 | A | Motor side (outlet side) to the centre of the wire hole | Depth rod or outside jaws | 9.05 | — | photo |
| D4 | B | Grommet length | Outside jaws | 16.4 | — | photo |
| D5 | B | Grommet width | Outside jaws | 8.8 | — | photo |
| D6 | A | Table to the centre of the wire hole | From the table, depth rod | 21.28 | — | photo |
| D7 | A | Plate thickness at the edge | Outside jaws | 3 | 3.5 | caliper 2.98 |
| D8 | B | Width of the web between the plate and the motor | Outside jaws | 13 | — | guess |
