#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce the user's NMOS core -> four-pad SKY130 layout pipeline.

KLayout 0.30.x Python (pya) script.  All coordinates are in micrometres.

Only external layout dependency:
  ~/Desktop/sky130_pad_refs/sky130_ef_io__bare_pad.gds

Outputs are written to a new numbered run directory under:
  ~/Desktop/77K_NMOS_Device_Circuit_Portfolio/03_Chip_Layout/reproduced_run_N/

IMPORTANT:
- This reconstructs the exact *draft geometry* recorded in the user's original
  build_sky130_nmos_lvt_draft.py and later four-pad assembly scripts.
- Geometric continuity tests are NOT DRC, LVS, EM, IR-drop, ESD, or bondability proof.
- Re-run SKY130 DRC/LVS on the output using the actual PDK rule deck.
- The stand-alone bare_pad cell is an external reference, not a custom qualified I/O.
"""

from pathlib import Path
import csv
import hashlib
import pya

HOME = Path.home()
DESKTOP = HOME / "Desktop"
PORTFOLIO = DESKTOP / "77K_NMOS_Device_Circuit_Portfolio" / "03_Chip_Layout"
PAD_GDS = DESKTOP / "sky130_pad_refs" / "sky130_ef_io__bare_pad.gds"
DBU_UM = 0.001
TOP_NAME = "NMOS_4PAD_FLOORPLAN"
CORE_NAME = "NMOS_LVT_DRAFT"
PAD_NAME = "sky130_ef_io__bare_pad"
PORTS = {
    "G": ((0.0, 100.0), (0.0, 240.0), "VIN", 2),
    "S": ((-100.0, 0.0), (-240.0, 0.0), "GND", 3),
    "D": ((100.0, 0.0), (240.0, 0.0), "VOUT", 1),
    "B": ((0.0, -100.0), (0.0, -240.0), "GND", 4),
}


def out_folder():
    PORTFOLIO.mkdir(parents=True, exist_ok=True)
    num = 1
    while (PORTFOLIO / ("reproduced_run_" + str(num))).exists():
        num += 1
    folder = PORTFOLIO / ("reproduced_run_" + str(num))
    folder.mkdir(parents=True)
    return folder


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_core():
    # The primitives below match the previously saved original NMOS generator.
    ly = pya.Layout()
    ly.dbu = DBU_UM
    core = ly.create_cell(CORE_NAME)

    def unit(v):
        return int(round(v / ly.dbu))

    def rect(layer, dtype, x1, y1, x2, y2):
        li = ly.layer(pya.LayerInfo(layer, dtype))
        core.shapes(li).insert(pya.Box(unit(x1), unit(y1), unit(x2), unit(y2)))

    def text(name, x, y):
        li = ly.layer(pya.LayerInfo(68, 5))
        core.shapes(li).insert(pya.Text(name, pya.Trans(unit(x), unit(y))))

    # Device active area, 0.15-um channel length, 1.60-um effective width.
    rect(65, 20, -0.50, -0.80, 0.50, 0.80)   # diffusion
    rect(66, 20, -0.075, -1.05, 0.075, 1.05)  # poly
    rect(93, 44, -0.625, -0.925, 0.625, 0.925)  # nsdm
    rect(125, 44, -0.70, -1.10, 0.70, 1.10)  # LVT marker

    # Gate landing: poly -> licon -> local interconnect -> mcon -> M1.
    rect(66, 20, -0.175, 1.03, 0.175, 1.45)
    rect(95, 20, -0.195, 1.055, 0.195, 1.445)
    rect(66, 44, -0.085, 1.155, 0.085, 1.325)
    rect(67, 20, -0.175, 1.065, 0.175, 1.415)
    rect(67, 44, -0.085, 1.155, 0.085, 1.325)
    rect(68, 20, -0.175, 1.065, 0.175, 1.415)

    # Source/drain contact rows on each side of the gate.
    for x in (-0.30, 0.30):
        rect(67, 20, x - 0.175, -0.725, x + 0.175, 0.725)
        rect(68, 20, x - 0.175, -0.725, x + 0.175, 0.725)
        for y in (-0.51, -0.17, 0.17, 0.51):
            rect(66, 44, x - 0.085, y - 0.085, x + 0.085, y + 0.085)
        for y in (-0.54, -0.18, 0.18, 0.54):
            rect(67, 44, x - 0.085, y - 0.085, x + 0.085, y + 0.085)

    # Body tap below device.
    rect(65, 44, -0.25, -2.25, 0.25, -1.75)
    rect(94, 44, -0.375, -2.375, 0.375, -1.625)
    rect(66, 44, -0.085, -2.085, 0.085, -1.915)
    rect(67, 20, -0.175, -2.175, 0.175, -1.825)
    rect(67, 44, -0.085, -2.085, 0.085, -1.915)
    rect(68, 20, -0.175, -2.175, 0.175, -1.825)

    # The four original large M1 landing squares and their access traces.
    # These are NOT final bond pads.
    rect(68, 20, -0.10, 1.24, 0.10, 71.00)  # G
    rect(68, 20, -71.00, -0.10, -0.30, 0.10)  # S
    rect(68, 20, 0.30, -0.10, 71.00, 0.10)  # D
    rect(68, 20, -0.10, -71.00, 0.10, -2.00)  # B
    rect(68, 20, -30.00, 70.00, 30.00, 130.00)
    rect(68, 20, -130.00, -30.00, -70.00, 30.00)
    rect(68, 20, 70.00, -30.00, 130.00, 30.00)
    rect(68, 20, -30.00, -130.00, 30.00, -70.00)
    text("G", -2.584, 100.789)
    text("S", -105.895, -2.695)
    text("D", 100.506, -4.850)
    text("B", -4.581, -109.397)
    return ly, core


def box_square(x, y, width, dbu):
    h = width / 2.0
    return pya.Box(round((x - h) / dbu), round((y - h) / dbu),
                   round((x + h) / dbu), round((y + h) / dbu))


def box_route(x1, y1, x2, y2, width, dbu):
    h = width / 2.0
    return pya.Box(round((min(x1, x2) - h) / dbu),
                   round((min(y1, y2) - h) / dbu),
                   round((max(x1, x2) + h) / dbu),
                   round((max(y1, y2) + h) / dbu))


def add_pads_and_floorplan(ly, core):
    # Read the reference bare_pad GDS into the same layout (exactly as in
    # the earlier successful KLayout floorplan macro).
    ly.read(str(PAD_GDS))
    pad = ly.cell(PAD_NAME)
    if pad is None:
        raise RuntimeError("Reference pad cell not found: " + PAD_NAME)
    top = ly.create_cell(TOP_NAME)
    if top is None:
        raise RuntimeError("Unable to create top cell")
    top.insert(pya.CellInstArray(core.cell_index(), pya.Trans(pya.Point(0, 0))))
    pad_center = pad.bbox().center()
    dbu = ly.dbu
    for port, (_, target, _, _) in PORTS.items():
        x, y = target
        tx = round(x / dbu) - pad_center.x
        ty = round(y / dbu) - pad_center.y
        top.insert(pya.CellInstArray(
            pad.cell_index(), pya.Trans(pya.Point(tx, ty))
        ))
        print("Placed", port, "pad at", target, "um")
    return top


def add_metal_and_vias(ly, top):
    m2, m3, m4 = [ly.layer(n, 20) for n in (69, 70, 71)]
    v1, v2, v3 = [ly.layer(n, 44) for n in (68, 69, 70)]
    for port, (src, dst, _, _) in PORTS.items():
        x, y = src
        ex, ey = dst
        top.shapes(m2).insert(box_square(x, y, 4.0, ly.dbu))
        top.shapes(m3).insert(box_square(x, y, 4.0, ly.dbu))
        top.shapes(v1).insert(box_square(x, y, 0.15, ly.dbu))
        top.shapes(v2).insert(box_square(x, y, 0.20, ly.dbu))
        top.shapes(v3).insert(box_square(x, y, 0.20, ly.dbu))
        top.shapes(m4).insert(box_route(x, y, ex, ey, 4.0, ly.dbu))
        print("Routed", port, "M1->M4", src, "to", dst)


def add_m5_labels(ly, top):
    idx = ly.find_layer(72, 20)
    if idx is None or idx < 0:
        raise RuntimeError("Reference pad lacks Metal5 (72/20)")
    m5 = pya.Region(top.begin_shapes_rec(idx))
    m5.merge()
    layer = ly.layer(72, 5)
    for port, (_, (x, y), _, _) in PORTS.items():
        ix = round(x / ly.dbu)
        iy = round(y / ly.dbu)
        probe = pya.Region(pya.Box(ix - 100, iy - 100, ix + 100, iy + 100))
        if (m5 & probe).area() <= 0:
            raise RuntimeError(port + " metal5 missing under label")
        top.shapes(layer).insert(pya.Text(port, pya.Trans(ix, iy)))


def geometric_check(ly, top):
    """Basic check of the same cross-layer connectivity the user ran before.

    Does NOT inspect actual transistor device extraction; it is not DRC/LVS.
    """
    metal_components = []
    for met in range(68, 73):
        idx = ly.find_layer(met, 20)
        reg = pya.Region(top.begin_shapes_rec(idx))
        reg.merge()
        comps = []
        for polygon in reg.each():
            piece = pya.Region()
            piece.insert(polygon)
            comps.append(piece)
        metal_components.append(comps)
        print("Metal", met - 67, "independent regions:", len(comps))
        if len(comps) != 4:
            raise RuntimeError("Expected four metal regions on layer " + str(met))

    parent = {(level, i): (level, i)
              for level, comps in enumerate(metal_components)
              for i in range(len(comps))}

    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        parent[root(a)] = root(b)

    # A via connects adjacent metal layers when its area overlaps both.
    for level, met in enumerate(range(68, 72)):
        idx = ly.find_layer(met, 44)
        via_region = pya.Region(top.begin_shapes_rec(idx))
        count = 0
        for polygon in via_region.each():
            via = pya.Region()
            via.insert(polygon)
            low = [i for i, p in enumerate(metal_components[level])
                   if (via & p).area() > 0]
            high = [i for i, p in enumerate(metal_components[level + 1])
                    if (via & p).area() > 0]
            if not low or not high:
                raise RuntimeError("Disconnected via on layer " + str(met))
            for i in low:
                for j in high:
                    union((level, i), (level + 1, j))
            count += 1
        print("Via", level + 1, "geometrically connected:", count)

    def locate(level, x, y):
        # Tiny 0.2x0.2 um square overlapping the expected conductor.
        s = box_square(x, y, 0.2, ly.dbu)
        probe = pya.Region(s)
        hits = [(level, i) for i, r in enumerate(metal_components[level])
                if (probe & r).area() > 0]
        if len(hits) != 1:
            raise RuntimeError("Expected one conductor at: " + str((level, x, y)))
        return hits[0]

    roots = set()
    for port, (src, dst, _, _) in PORTS.items():
        a = locate(0, *src)
        b = locate(4, *dst)
        if root(a) != root(b):
            raise RuntimeError(port + ": M1 -> M5 path is OPEN")
        roots.add(root(a))
        print(port, "M1-to-M5 connection PASS")
    if len(roots) != 4:
        raise RuntimeError("Some external ports are shorted")
    print("Geometric connectivity: PASS (four isolated routes)")


def write_pinmap(folder):
    path = folder / "NMOS_4PAD_pinmap_REPRODUCED.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Port", "PCB_net", "X_um", "Y_um",
                    "Metal5_width_um", "Metal5_height_um"])
        for port, (_, (x, y), net, _) in PORTS.items():
            w.writerow([port, net, x, y, 65.4, 75.4])
    return path


def main():
    if not PAD_GDS.is_file():
        raise FileNotFoundError(
            "Required reference pad GDS missing: " + str(PAD_GDS) +
            "\nKeep the downloaded file in Desktop/sky130_pad_refs/"
        )

    folder = out_folder()  # Different run folder; never overwrite originals.
    ly, core = make_core()
    if abs(ly.dbu - DBU_UM) > 1e-9:
        raise RuntimeError("Unexpected layout database unit")

    core_path = folder / "NMOS_LVT_W1p6_L0p15_REPRODUCED.gds"
    ly.write(str(core_path))
    print("Core saved:", core_path)

    top = add_pads_and_floorplan(ly, core)
    floorplan_path = folder / "NMOS_4PAD_FLOORPLAN_REPRODUCED.gds"
    ly.write(str(floorplan_path))
    print("Floorplan saved:", floorplan_path)

    add_metal_and_vias(ly, top)
    connected_path = folder / "NMOS_4PAD_CONNECTED_REPRODUCED.gds"
    ly.write(str(connected_path))
    print("Connected layout saved:", connected_path)

    add_m5_labels(ly, top)
    geometric_check(ly, top)
    final_path = folder / "NMOS_4PAD_PINLABELED_REPRODUCED.gds"
    ly.write(str(final_path))
    print("Final labelled layout saved:", final_path)

    b = top.bbox()
    width, height = b.width() * ly.dbu, b.height() * ly.dbu
    print("Final drawing bbox:", width, "x", height, "um")
    if abs(width - 545.4) > 0.01 or abs(height - 555.4) > 0.01:
        raise RuntimeError("Final footprint size differs from prior result")

    # Reference netlist for the top-level circuit: M1 is the LVS device.
    (folder / "NMOS_4PAD_reference_REPRODUCED.spice").write_text(
        "* NMOS four-pad top-level LVS reference\n"
        ".subckt NMOS_4PAD_FLOORPLAN D G S B\n"
        "M1 D G S B sky130_fd_pr__nfet_01v8_lvt w=1.60u l=0.15u\n"
        ".ends NMOS_4PAD_FLOORPLAN\n.end\n",
        encoding="utf-8"
    )
    pinmap = write_pinmap(folder)
    (folder / "BUILD_PROVENANCE.txt").write_text(
        "SKY130 NMOS four-pad design reproduction\n"
        "Core geometry reference: build_sky130_nmos_lvt_draft.py "
        "(previously provided by user)\n"
        "Reference pad: " + str(PAD_GDS) + "\n"
        "Reference pad SHA256: " + sha256(PAD_GDS) + "\n"
        "KLayout DBU (um): " + str(ly.dbu) + "\n"
        "Cell: " + TOP_NAME + "\n"
        "Final drawing bbox (um): " + str(width) + " x " + str(height) + "\n"
        "Status: geometric connectivity pass; full DRC/LVS must be rerun.\n"
        "No claim of tapeout readiness, ESD protection, or bondability.\n",
        encoding="utf-8"
    )
    print("Pin map saved:", pinmap)
    print("OUTPUT DIRECTORY:", folder)
    print("NEXT: select top cell", TOP_NAME,
          "and rerun SKY130 full DRC and LVS (Scale OFF; Top-Level Pins ON).")


if __name__ == "__main__":
    main()
