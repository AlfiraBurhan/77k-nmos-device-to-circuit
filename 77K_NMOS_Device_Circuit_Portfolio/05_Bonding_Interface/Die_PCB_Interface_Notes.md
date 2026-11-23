# Die-to-PCB Bonding Interface Notes

## 1. Scope and status

This document describes the **conceptual** bond-wire interface between the
KLayout SKY130 LVT NMOS layout and the KiCad PCB footprint `SKY130_NMOS_DIE_BOND_V2`.

**Not fabrication or packaging verified.** No wire-bond assembly, die singulation,
electrical measurement of this fabricated layout, or PCB manufacturing has been performed.

## 2. Source artifacts

- `NMOS_4PAD_PINLABELED_DRAFT.gds` / independently reproduced counterpart
  `NMOS_4PAD_PINLABELED_REPRODUCED.gds`
- `NMOS_4PAD_pinmap.csv` (die coordinates)
- `Die_to_PCB_Bonding_Map.csv` (port-to-pad mapping and planar distances)
- KiCad schematic, PCB, and custom footprint `SKY130_NMOS_DIE_BOND_V2`

The diagram `Bonding_Assembly_Diagram.png` is a **conceptual top view**, not
an exported KiCad assembly drawing or a photomicrograph.

## 3. Coordinate convention

- All coordinates in the table below are relative to the Q1 footprint/die
  center (not the global KiCad board origin).
- KLayout uses +Y upward. The KiCad top-view drawing convention in this
  project uses +Y downward. The die's Y coordinates were therefore negated.
- This mapping assumes **zero rotation and no mirror operation** when placing
  the die. A physical flip, rotation, or different assembly orientation
  requires recomputation.

## 4. Bonding map

| Die port | KiCad PCB pad | Net | Die position, KiCad frame (mm) | PCB pad center (mm) | Planar center distance (mm) |
|---|---:|---|---|---|---:|
| D | 1 | VOUT | (+0.240, 0.000) | (+1.500, 0.000) | 1.260 |
| G | 2 | VIN | (0.000, -0.240) | (0.000, -1.500) | 1.260 |
| S | 3 | GND | (-0.240, 0.000) | (-1.500, 0.000) | 1.260 |
| B | 4 | GND | (0.000, +0.240) | (0.000, +1.500) | 1.260 |

On the PCB, S and B both use GND. Their on-die pads remain distinct;
their physical bond wires are separate.

## 5. Physical dimensions

| Feature | Value | Status |
|---|---|---|
| Drawn GDS geometry bounding box | 545.4 × 555.4 μm | Measured from GDS; **not** a cut-die size |
| Metal5 pad size | 65.4 × 75.4 μm each | Measured from GDS |
| Pad-opening size | 60 × 70 μm each | Measured from reference pad layout |
| Bond-pad centers in KLayout | D(+240,0), G(0,+240), S(-240,0), B(0,-240) μm | From GDS |
| KiCad F.Fab die outline | 1.0 × 1.0 mm | **Conceptual**, not manufacturing-defined |
| KiCad PCB pad size | 1.0 × 1.0 mm | Footprint planning value; assembly unverified |
| Die-to-PCB pad center spacing | 1.26 mm in plane | Computed; **not** actual wire length |

The center-to-center planar spacing is `|1.500 − 0.240| = 1.260 mm`
for each cardinal-direction connection. A real bond wire uses a three-dimensional
loop and its length depends on landing locations and loop height, so 1.260 mm
is not a wire-length specification.

## 6. Electrical and verification status

- Metal1-to-Metal5 geometrical connectivity: 4/4 paths reported PASS in the
  user's KLayout inspection script.
- The source layout and its reproduced version were subsequently reported
  to pass their relevant LVS/DRC runs; retain the actual logs, input filenames,
  rule configurations, and screenshot evidence alongside the GDS files.
- KiCad PCB verification: reported DRC violations 0, unconnected items 0,
  schematic-consistency errors 0, with 5 tests ignored.

These checks are **not** equivalent to qualified packaging, wire-bond
process verification, or fabricated-chip characterization.

## 7. Open manufacturing/assembly constraints

Before using this design for fabrication or bonding, obtain:
1. Foundry/multi-project-wafer requirements for chip outline, seal ring,
   scribe/kerf and bond-pad placement.
2. Confirmation that the selected SKY130 bare-pad cell and passivation
   structure are acceptable for the intended assembly process.
3. Assembly-house requirements for pad material/metallization, minimum
   bond-pad dimensions, PCB bond-finger metallization/surface finish, wire
   type and diameter, capillary access, loop height, clearance and maximum span.
4. ESD/protection and handling plan appropriate to the intended measurement setup.
5. Verification of pin orientation against the actual mounted die, and
   a die-attach/encapsulation or handling plan as needed.

## 8. Evidence and reference files to preserve

- Final input GDS and reference SPICE netlist
- GDS DRC results including activated rule groups and version
- LVS cross-reference result, extracted netlist, and `.lvsdb`
- KiCad PCB files, footprint library and DRC report
- `NMOS_4PAD_pinmap.csv` and `Die_to_PCB_Bonding_Map.csv`

