# Four-post stand: preliminary vibration estimate

The model in `experiment/four-post-stand` holds the pump plate 4 mm above a glued floor on four straight TPU columns. This calculation checks the load path before printing. It is a linear, dry, one-mass estimate, not a measurement or FEM validation. The initial 12 mm prototype was shortened at the user's request.

## Inputs

| Quantity | Value | Status |
|---|---:|---|
| Pump plus working hoses | 0.280 kg | User measurement |
| Number of columns | 4 | CAD |
| Column capsule footprint | 7.2 × 6.0 mm | CAD, `post_l`, `post_w` |
| Free column height | 4.0 mm | CAD, `post_h` |
| Section area | 35.474 mm² each | Calculated from capsule |
| Dynamic Young modulus | 5, 15, 30, 60 MPa | Scenarios; **not** measured for this filament/print |
| Damping ratio | 0.15 | Scenario; **not** measured |

The [AzureFilm TPU 95A product page](https://azurefilm.com/product/tpu-flexible-95a-blue/) describes the material qualitatively but does not supply a dynamic modulus or damping curve for the printed part. Therefore the modulus and damping values above are a sensitivity sweep, not material specifications.

## Method

For a vertical force carried in compression by all four equal columns, `kz = 4 E A / h`. With mass `m`, `fn = sqrt(1000 kz / m)/(2π)` for `kz` in N/mm. Dry static deflection is `mg/kz`. The force transmissibility for a linear damped isolator is `T = sqrt((1 + (2ζr)²) / ((1-r²)² + (2ζr)²))`, with `r = f/fn`. Isolation (`T < 1`) begins only when `f > sqrt(2) fn`; see the [FIU/Rao vibration isolation handout](https://web.eng.fiu.edu/LEVY/images/EML3222/EML3222-Rao%20Handout.pdf).

| Assumed E | Vertical stiffness | Vertical fn | Dry sag | T at 50 Hz | T at 100 Hz | T at 200 Hz |
|---:|---:|---:|---:|---:|---:|---:|
| 5 MPa | 177.4 N/mm | 126.7 Hz | 0.0155 mm | 1.18 | 2.31 | 0.71 |
| 15 MPa | 532.1 N/mm | 219.4 Hz | 0.0052 mm | 1.05 | 1.26 | 3.22 |
| 30 MPa | 1064.2 N/mm | 310.3 Hz | 0.0026 mm | 1.03 | 1.11 | 1.65 |
| 60 MPa | 2128.5 N/mm | 438.8 Hz | 0.0013 mm | 1.01 | 1.05 | 1.26 |

`T > 1` means more force reaches the glued base than the motor's applied harmonic force at that frequency. At the mid-range example `E=15 MPa`, isolation begins above about 310 Hz. The four thick straight columns do not provide reliable low-frequency vertical isolation; their static compression is only about 0.005 mm in this example. Reaching `fn≈30 Hz` at the same area and modulus would require a column height around 214 mm, so tuning this concept by post height alone is impractical. At 100 Hz, the shorter posts reduce the calculated resonance amplification from 2.31 to 1.26, but at 200 Hz they increase it from 0.71 to 3.22. Neither result is an actual pump operating point.

For horizontal bending, the capsule has `Ixx=85.217 mm⁴` and `Iyy=117.860 mm⁴`. With `E=15 MPa`, a cantilever estimate gives first lateral frequencies of 173 Hz in X and 147 Hz in Y. If the pump plate fully constrains the column tips against rotation, they rise to about 346 and 295 Hz. The real assembly lies somewhere between those ideal boundary conditions and may rock. These lateral values are less certain than the axial values.

## Limits and next check

- The pump vibration frequency at operating voltage is unknown; do not label a particular table column as the actual operating point.
- Water, buoyancy, moving water in the pump, hoses, glue compliance, print direction and TPU viscoelasticity are omitted. Hoses can bypass the stand and carry vibration directly to the bath.
- The calculated vertical stiffness applies to compression into the post shoulders. Upward force is caught by the snap heads and has a different, nonlinear load path. `post_head_pre=0.3 mm` creates a small nominal head/plate interference in CAD (0.078 mm³ total over four heads), but real preload and snap force require a print test.
- Check the vibration frequency and acceleration on the pump and bath in water, and check whether the plate can slide along the slot entries without the old side keys.

Recompute the table with `python3 scripts/post_vibration_estimate.py`.
