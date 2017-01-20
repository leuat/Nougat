from ovito.vis import *
from ovito.io import import_file
import ovito.vis
import sys
import math

data = sys.argv[1]
size = int(sys.argv[2])
image = sys.argv[3]

columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z"]
node = import_file(data, multiple_frames=False, columns=columns)

# Disable simulation box
cell = node.source.cell
cell.display.enabled = False   
node.compute()

vp = Viewport()
z = 0.7
vp.type = Viewport.Type.PERSPECTIVE
vp.camera_pos = (360, -160, 214)
vp.camera_dir = (-0.68, 0.62, -0.38)
vp.fov = math.radians(38.0)
node.add_to_scene()

settings = RenderSettings(
    filename = image,
    size = (size, size),
    renderer = TachyonRenderer()
)
vp.render(settings)
