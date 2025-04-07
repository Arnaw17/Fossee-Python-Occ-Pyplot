from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax1
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

# ================================
# Parameters (mm)
# ================================
column_height = 6100
column_spacing = 450
ismb_width = 100
ismb_depth = 200
plate_thickness = 10
plate_width = 430
plate_height = 300
lace_width = 100
lace_thickness = 8
lace_pitch = 450

# ================================
# Geometry Creation
# ================================

def create_ismb_column(origin_x):
    """Creates one ISMB section as a box (simplified shape)"""
    p1 = gp_Pnt(origin_x, 0, 0)
    return BRepPrimAPI_MakeBox(p1, ismb_width, ismb_depth, column_height).Shape()

def create_end_plate(z_pos):
    """Creates top or bottom plate"""
    p = gp_Pnt(-plate_width/2 + ismb_width/2, -plate_height/2 + ismb_depth/2, z_pos)
    return BRepPrimAPI_MakeBox(p, plate_width, plate_height, plate_thickness).Shape()

def create_lace(x_start, x_end, z_start, z_end):
    """Creates a diagonal lace bar between two ISMBs"""
    length = ((x_end - x_start)**2 + (z_end - z_start)**2)**0.5
    lace = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), lace_thickness, lace_width, length).Shape()

    # Rotate and translate lace to fit between columns
    trsf = gp_Trsf()
    angle = gp_Dir(x_end - x_start, 0, z_end - z_start)
    axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))
    trsf.SetRotation(axis, angle.Angle(gp_Dir(0, 0, 1)))

    t = BRepBuilderAPI_Transform(lace, trsf)
    trsf_move = gp_Trsf()
    trsf_move.SetTranslation(gp_Pnt(0, 0, 0), gp_Pnt(x_start, 0, z_start))
    final = BRepBuilderAPI_Transform(t.Shape(), trsf_move)
    return final.Shape()

# ================================
# Main Assembly
# ================================
def build_column():
    shapes = []

    # Left and Right ISMBs
    shapes.append(create_ismb_column(0))
    shapes.append(create_ismb_column(column_spacing))

    # Top and Bottom Plates
    shapes.append(create_end_plate(0))
    shapes.append(create_end_plate(column_height - plate_thickness))

    # Lacing
    num_laces = int(column_height // lace_pitch)
    for i in range(num_laces):
        z1 = i * lace_pitch
        z2 = (i + 1) * lace_pitch
        # Diagonal lacing from left to right and vice versa
        shapes.append(create_lace(0, column_spacing, z1, z2))
        shapes.append(create_lace(column_spacing, 0, z1, z2))

    return shapes

# ================================
# Display
# ================================
if __name__ == "__main__":
    display, start_display, add_menu, add_function_to_menu = init_display()
    column_parts = build_column()
    for shape in column_parts:
        display.DisplayShape(shape, update=True)
    start_display()
