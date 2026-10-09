#!/usr/bin/env python3
"""Linear first-pass vibration estimate for the four straight TPU columns.

All material properties below are scenarios, not measured AzureFilm 95A values.
The pump, columns and base are represented by one rigid mass and linear springs.
"""

from math import pi, sqrt

MASS_KG = 0.280  # user measurement with working hoses
POST_COUNT = 4
POST_LENGTH_MM = 7.2  # capsule overall length along X
POST_WIDTH_MM = 6.0  # capsule width along Y
POST_HEIGHT_MM = 12.0
DAMPING_RATIO = 0.15  # illustrative, not measured


def capsule_section(length_mm: float, width_mm: float) -> tuple[float, float, float]:
    """Return area, Ixx and Iyy in mm^2 and mm^4 for a horizontal capsule."""
    radius = width_mm / 2
    straight = length_mm - width_mm
    area = 2 * radius * straight + pi * radius**2
    ixx = straight * (2 * radius) ** 3 / 12 + pi * radius**4 / 4
    iyy = (
        (2 * radius) * straight**3 / 12
        + pi * radius**4 / 4
        + 4 * straight * radius**3 / 3
        + pi * radius**2 * straight**2 / 4
    )
    return area, ixx, iyy


def natural_hz(stiffness_n_per_mm: float) -> float:
    return sqrt(stiffness_n_per_mm * 1000 / MASS_KG) / (2 * pi)


def force_transmissibility(exciting_hz: float, natural_frequency_hz: float) -> float:
    ratio = exciting_hz / natural_frequency_hz
    damping_term = 2 * DAMPING_RATIO * ratio
    return sqrt((1 + damping_term**2) / ((1 - ratio**2) ** 2 + damping_term**2))


def main() -> None:
    area, ixx, iyy = capsule_section(POST_LENGTH_MM, POST_WIDTH_MM)
    print(f"m={MASS_KG:.3f} kg, 4 capsule posts {POST_LENGTH_MM:g} x {POST_WIDTH_MM:g} x {POST_HEIGHT_MM:g} mm")
    print(f"area/post={area:.3f} mm^2, Ixx={ixx:.3f} mm^4, Iyy={iyy:.3f} mm^4")
    print(f"illustrative damping ratio={DAMPING_RATIO:g}; E is an assumed dynamic modulus")
    print("E MPa | kz N/mm | fn,z Hz | dry sag mm | T(50 Hz) | T(100 Hz) | T(200 Hz)")
    for young_mpa in (5, 15, 30, 60):
        kz = POST_COUNT * young_mpa * area / POST_HEIGHT_MM
        fn_z = natural_hz(kz)
        sag = MASS_KG * 9.81 / kz
        print(
            f"{young_mpa:5g} | {kz:8.1f} | {fn_z:7.1f} | {sag:10.4f} |"
            f" {force_transmissibility(50, fn_z):8.2f} |"
            f" {force_transmissibility(100, fn_z):9.2f} |"
            f" {force_transmissibility(200, fn_z):9.2f}"
        )
    young_mpa = 15
    for direction, inertia in (("X", iyy), ("Y", ixx)):
        k_cantilever = POST_COUNT * 3 * young_mpa * inertia / POST_HEIGHT_MM**3
        print(
            f"lateral {direction}, E=15 MPa: fn={natural_hz(k_cantilever):.1f} Hz "
            f"(free tip rotation) to {natural_hz(4*k_cantilever):.1f} Hz "
            "(fixed-guided tip)"
        )


if __name__ == "__main__":
    main()
