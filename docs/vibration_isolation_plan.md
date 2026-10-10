# Pump vibration isolation plan

Status: **rejected** in favour of the four-post stand (see [four_post_vibration.md](four_post_vibration.md)). Kept for reference. It was a concept for discussion; the model was not changed for it. The sizes of the compliant elements and their effectiveness were never confirmed by calculation or test.

## What transmits vibration now

- The pump mounting plate (X −17…15, width 45 mm) rests on the solid 5 mm floor of the holder.
- The side walls have only 0.1 mm side clearance; the lips have 0.1 mm interference. The keys and catches that hold the plate are joined to the same floor.
- Two M4 screws fix this pad to the bath. One screw sits under the mounting plate area (X = +6.1 mm), the other in front of it (X = −23.2 mm).
- Removing material only under the plate would therefore leave a parallel vibration path through the walls, lips and catches.

## Proposed layout

Split the part functionally into a fixed base with the M4 screws and the glued face, and an inner pump cradle. The cradle carries a few small supports under the plate, the existing keys and the catches. Leave a gap along its sides to the fixed base; the only intended load path between them is four symmetric compliant TPU bridges. The screws and their heads must not touch the cradle. The two rounded front corners and the orientation cue of the long pad are kept.

For a first prototype a single printed part with bridges is preferable, if the outer outline may grow a little: the side wall already takes almost all the width margin, and at the rear end only 1.9 mm remain to the edge. A fully floating cradle will probably not fit the current outline. If the outline cannot grow, first test a modest relief under the plate with flexible local catches; it will not give full isolation. The alternative is a separate cradle with replaceable elastic connectors. Do not move the holes or the outer outline without agreement.

## Design steps

1. In CAD, mark the fixed zones around both M4 screws, the glued face, the plate outline and the working zones of the keys/catches. Check the room for a gap within the current 50.9 × 48.8 mm outline, especially at the rear end, where only 1.9 mm remain from the plate to the edge.
2. Unload the plate's bearing area: keep small support pads on the cradle and leave a gap under the rest of the plate. Place the supports so that the pump does not rock and does not rest on a screw head.
3. Separate the side retaining elements from the fixed part. Connect them to the base only through the four compliant bridges. Add travel stops with clearance for installation or a tug on a hose; in normal operation the stops do not touch the cradle.
4. Start with a gap of about 1–2 mm between the moving cradle and the fixed base and check it in all three directions. This is a starting range for a mock-up, not a calculated result. Choose bridge thickness, length and shape from the load and a test print, keeping the minimum printable walls.
5. Keep the standard M4 installation and the ability to remove the pump. Check that the screw heads are recessed and do not form a rigid bridge to the cradle, and that the bridges are not under large constant tension or bending after snapping in.
6. Print a comparison sample and test it in the working position under water: bath noise/vibration with the current holder and with the new version, visible cradle travel, settling over time, behaviour at start-up and under hose tension. Water and hoses can also carry vibration around the mount.

## Data needed before tuning stiffness

- The real mass of the pump with connected hoses and the direction of its load in the working position; under water the weight drops because of buoyancy.
- Rotation speed / main vibration frequencies at nominal supply (or a vibration recording on the housing and the bath).
- The allowed growth of the holder outline and height, and the desired travel margin when snapping in.

Principle: isolation depends on the ratio of the excitation frequency to the natural frequency of the system and on the stiffness/load of the supports. A smaller contact area alone does not guarantee improvement, and supports that are too stiff can transmit almost all of the vibration. See the [Sorbothane guide to choosing isolators](https://www.sorbothane.com/technical-data/articles/how-to-select-a-standard-sorbothane-isolator/) and the [engineering design guide](https://www.sorbothane.com/wp-content/uploads/Sorbothane-EDG.pdf). These sources describe the principle; their numeric material properties must not be applied to printed TPU 95A.
