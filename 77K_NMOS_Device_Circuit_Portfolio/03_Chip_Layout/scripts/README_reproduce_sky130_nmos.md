# SKY130 NMOS four-pad layout: reproducible build

The script `build_full_sky130_nmos_4pad.py` combines the NMOS core generator from the original `build_sky130_nmos_lvt_draft.py` with the subsequent four-pad floorplan, Metal1–Metal5 connectivity, and port-label steps.

## Prerequisites

- KLayout 0.30.x with its built-in Python `pya` module, as already installed on the user's Mac.
- Efabless SKY130 technology and its DRC/LVS rules for **verification** (not required to write GDS).
- SKY130 reference pad GDS at `~/Desktop/sky130_pad_refs/sky130_ef_io__bare_pad.gds`, cell `sky130_ef_io__bare_pad`.

## Run on the Mac

1. Put `build_full_sky130_nmos_4pad.py` in the `03_Chip_Layout/scripts/` folder.
2. Open KLayout, **Macros → Macro Development → Python**. Create/open a Python macro and paste in the content of `build_full_sky130_nmos_4pad.py`.
3. Save and click the green **Run** arrow. Or (if your KLayout path is `/Applications/klayout.app/Contents/MacOS/klayout`) run:

   ```bash
   "/Applications/klayout.app/Contents/MacOS/klayout" -b -r \
   "$HOME/Desktop/77K_NMOS_Device_Circuit_Portfolio/03_Chip_Layout/scripts/build_full_sky130_nmos_4pad.py"
   ```

4. A new `03_Chip_Layout/reproduced_run_N/` directory will be created. Existing files are **never overwritten**.
5. Open `NMOS_4PAD_PINLABELED_REPRODUCED.gds`, select cell `NMOS_4PAD_FLOORPLAN`, run the installed SKY130 **DRC** rules and **LVS** with the generated SPICE reference; ensure **Scale** is off and **Top Level Pins** is on, as for the previous successful project verification.

## Generated deliverables

- `NMOS_LVT_W1p6_L0p15_REPRODUCED.gds`
- `NMOS_4PAD_FLOORPLAN_REPRODUCED.gds`
- `NMOS_4PAD_CONNECTED_REPRODUCED.gds`
- `NMOS_4PAD_PINLABELED_REPRODUCED.gds`
- `NMOS_4PAD_reference_REPRODUCED.spice`
- `NMOS_4PAD_pinmap_REPRODUCED.csv`
- `BUILD_PROVENANCE.txt`

## What the build verifies and does not verify

- The build checks four independent conductive paths from NMOS Metal1 to pad Metal5 through via overlaps, and the bounding dimensions 545.4 × 555.4 µm, when used with the same pad GDS.
- These are **geometric checks only**, not replacements for DRC/LVS.
- The reference pad and conceptual PCB bonding arrangement have not been qualified for fabrication/assembly. The drawn-layout bounding box is **not** a final die outline.
- The historical verification results are stored separately: do not claim a new reproduced GDS passed DRC/LVS until it has been checked.

## Provenance

The NMOS drawing coordinates come from the user's earlier `build_sky130_nmos_lvt_draft.py` (kept unchanged in this archive), not an inferred reconstruction. Pad placement and metal interconnect steps reproduce the documented KLayout macros in the conversation. The bare pad GDS is an **external SKY130 design dependency** and must be preserved with proper attribution and licensing.
