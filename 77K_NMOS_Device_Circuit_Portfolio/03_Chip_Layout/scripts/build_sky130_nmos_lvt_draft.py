# KLayout 0.30.x Python Macro
# Generate a NEW provisional SKY130 nfet_01v8_lvt layout from the geometry
# of NMOS_final2.gds. Does not modify any open GDS.
# Units: micrometres, dbu = 0.001 um.
# This design MUST pass full SKY130 DRC and LVS before fabrication claims.
import os
import pya

out = pya.Layout()
out.dbu = 0.001
cell = out.create_cell("NMOS_LVT_DRAFT")

def grid(um):
    return int(round(um / out.dbu))

def rectangle(layer, datatype, x1, y1, x2, y2):
    li = out.layer(pya.LayerInfo(layer, datatype))
    cell.shapes(li).insert(pya.Box(grid(x1), grid(y1), grid(x2), grid(y2)))

def label(name, x, y):
    li = out.layer(pya.LayerInfo(68, 5))
    cell.shapes(li).insert(pya.Text(name, pya.Trans(grid(x), grid(y))))

# NMOS active region: L = 0.15 um (poly x width), W = 1.60 um (diff y height)
rectangle(65, 20, -0.50, -0.80, 0.50, 0.80)  # diff
rectangle(66, 20, -0.075, -1.05, 0.075, 1.05)  # poly gate
rectangle(93, 44, -0.625, -0.925, 0.625, 0.925)  # nsdm implant
rectangle(125, 44, -0.70, -1.10, 0.70, 1.10)  # low-Vt marker, provisional

# Gate contact above the transistor
rectangle(66, 20, -0.175, 1.03, 0.175, 1.45)  # poly landing
rectangle(95, 20, -0.195, 1.055, 0.195, 1.445)  # npc marker
rectangle(66, 44, -0.085, 1.155, 0.085, 1.325)  # licon
rectangle(67, 20, -0.175, 1.065, 0.175, 1.415)  # li1
rectangle(67, 44, -0.085, 1.155, 0.085, 1.325)  # mcon
rectangle(68, 20, -0.175, 1.065, 0.175, 1.415)  # met1

# Source and drain have 4 licon and 4 mcon per side.
# Rows are spread across 1.6 um effective device width.
for x in (-0.30, 0.30):
    rectangle(67, 20, x-0.175, -0.725, x+0.175, 0.725)  # li1 landing
    rectangle(68, 20, x-0.175, -0.725, x+0.175, 0.725)  # met1 landing
    for y in (-0.51, -0.17, 0.17, 0.51):
        rectangle(66, 44, x-0.085, y-0.085, x+0.085, y+0.085)  # licon
    for y in (-0.54, -0.18, 0.18, 0.54):
        rectangle(67, 44, x-0.085, y-0.085, x+0.085, y+0.085)  # mcon

# Body tap moved down so the longer gate and LVT implant remain separate.
rectangle(65, 44, -0.25, -2.25, 0.25, -1.75)  # tap
rectangle(94, 44, -0.375, -2.375, 0.375, -1.625)  # psdm
rectangle(66, 44, -0.085, -2.085, 0.085, -1.915)  # licon
rectangle(67, 20, -0.175, -2.175, 0.175, -1.825)  # li1
rectangle(67, 44, -0.085, -2.085, 0.085, -1.915)  # mcon
rectangle(68, 20, -0.175, -2.175, 0.175, -1.825)  # met1

# Four external Metal1 traces and large squares FROM THE USER'S ORIGINAL
# demonstration layout. These squares are NOT verified bondable die pads.
rectangle(68, 20, -0.10, 1.24, 0.10, 71.00)  # G trace
rectangle(68, 20, -71.00, -0.10, -0.30, 0.10)  # S trace
rectangle(68, 20, 0.30, -0.10, 71.00, 0.10)  # D trace
rectangle(68, 20, -0.10, -71.00, 0.10, -2.00)  # B trace
rectangle(68, 20, -30.00, 70.00, 30.00, 130.00)  # G square
rectangle(68, 20, -130.00, -30.00, -70.00, 30.00)  # S square
rectangle(68, 20, 70.00, -30.00, 130.00, 30.00)  # D square
rectangle(68, 20, -30.00, -130.00, 30.00, -70.00)  # B square
label("G", -2.584, 100.789)
label("S", -105.895, -2.695)
label("D", 100.506, -4.850)
label("B", -4.581, -109.397)

folder = os.path.join(os.path.expanduser("~"), "Desktop")
if not os.path.isdir(folder):
    folder = os.path.expanduser("~")
base = "NMOS_LVT_W1p6_L0p15_DRAFT"
filename = os.path.join(folder, base + ".gds")
number = 2
while os.path.exists(filename):
    filename = os.path.join(folder, base + "_" + str(number) + ".gds")
    number += 1
out.write(filename)
print("Created:", filename)
print("Target L=0.15 um, W=1.60 um, low-Vt drawing 125/44 included")
print("UNVERIFIED DRAFT: run SKY130 DRC and LVS; Metal1 squares are not actual bond pads")
