import sys as sys
import os

### INCLUDE LOCAL PACKAGE DIRECTORIES
cwd = os.getcwd()
print('Current working directory: ', cwd)

drawing_subdirectory = os.path.join(cwd, 'drawing')
memory_diagrams_subdirectory = os.path.join(cwd, 'memory_diagrams')

# Should be refactored soon into a single function call
sys.path.append(drawing_subdirectory)
sys.path.append(memory_diagrams_subdirectory)

#import timelapse as timelapse
#import sparse as sparse
#import memory_diagrams.array as array
#import memory_diagrams.hybrid as hybrid

import drawing as drawing
import numpy as np
import math as math

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

diagram_width = 10.
diagram_height = 4.

_drawing = drawing.Drawing(diagram_width = diagram_width, diagram_height = diagram_height, show_axes = True, horizontal_elements = 1, vertical_elements = 1, lower_padding = 1.0, show_axes_numbers = False)

axes = _drawing.Get_Axes()
fig = _drawing.Get_Figure()


y_offset = _drawing.Get_Y_Offset()
x_offset = 0.1


linewidth = 1.5

H1 = 0.5
L = (H1 / 2.) * math.tan(math.radians(30))

H2 = 0.25
OFFSET_2 = (H1 - H2) / 2.

H3 = 1.0
OFFSET_3 = (H1 - H3) / 2.

H4 = 0.5
OFFSET_4 = (H1 - H4) / 2.
        

# Triangle 1
v0x = 0.0
v0y = 0.0

v1x = L
v1y = H1 / 2.

v2x = 0.0
v2y = H1


vertices = np.array([(v0x, v0y), (v1x, v1y), (v2x, v2y), (v0x, v0y)])
codes = np.array([1, 2, 2, 2])
_path = path.Path(vertices, codes)

path_patch = patches.PathPatch(_path, linewidth=linewidth, facecolor = 'lightblue', fill=True, antialiased=True)
axes.add_patch(path_patch)


# Triangle 2

v0x = 0.0
v0y = OFFSET_2

v1x = L
v1y = H2/2. + OFFSET_2

v2x = 0.0
v2y = H2 + OFFSET_2

vertices = np.array([(v0x, v0y), (v1x, v1y), (v2x, v2y), (v0x, v0y)])
codes = np.array([1, 2, 2, 2])
_path = path.Path(vertices, codes)

path_patch = patches.PathPatch(_path, linewidth=linewidth, facecolor = 'lightgreen', fill=True, antialiased=True)
axes.add_patch(path_patch)

# Triangle 3

v0x = 0.0
v0y = OFFSET_3

v1x = L
v1y = H3/2. + OFFSET_3

v2x = 0.0
v2y = H3 + OFFSET_3

vertices = np.array([(v0x, v0y), (v1x, v1y), (v2x, v2y), (v0x, v0y)])
codes = np.array([1, 2, 2, 2])
_path = path.Path(vertices, codes)

path_patch = patches.PathPatch(_path, linewidth=linewidth, facecolor = 'tomato', fill=True, antialiased=True)
#axes.add_patch(path_patch)

# Triangle 4

v0x = 0.0
v0y = OFFSET_4

v1x = L
v1y = H4/2. + OFFSET_4

v2x = 0.0
v2y = H4 + OFFSET_4

vertices = np.array([(v0x, v0y), (v1x, v1y), (v2x, v2y), (v0x, v0y)])
codes = np.array([1, 2, 2, 2])
_path = path.Path(vertices, codes)

path_patch = patches.PathPatch(_path, linewidth=linewidth, facecolor = 'indigo', fill=True, antialiased=True)
#axes.add_patch(path_patch)


# Horizontal bar 1

# 
H_BAR1 = H1 / 2. + 0.08


L = (H1 / 2.) * math.tan(math.radians(30))
L_BAR1 = (H1 / 4.) / math.tan(math.radians(30))
x_offset = L - L_BAR1

vertices = np.array([(x_offset, H_BAR1), (x_offset + 5., H_BAR1)])
codes = np.array([1, 2])
_path = path.Path(vertices, codes)

path_patch = patches.PathPatch(_path, linewidth=linewidth, fill=True, antialiased=True)
axes.add_patch(path_patch)

# Horizontal bar 2

# 
H_BAR2 = H1 / 2. - 0.08


L = (H1 / 2.) * math.tan(math.radians(30))
L_BAR1 = (H1 / 4.) / math.tan(math.radians(30))
x_offset = L - L_BAR1

vertices = np.array([(x_offset, H_BAR2), (x_offset + 5., H_BAR2)])
codes = np.array([1, 2])
_path = path.Path(vertices, codes)

path_patch = patches.PathPatch(_path, linewidth=linewidth, fill=True, antialiased=True)
axes.add_patch(path_patch)


#x_coordinate_text = 1.0
#y_coordinate_text = H1 / 2. + H1 / 3.
#text = 'KeyVector'
#axes.text(x_coordinate_text, y_coordinate_text, str(text), ha='center', va='center', fontweight='bold')

# Plot adjustment (axes)
axes_width = L + 5. - L_BAR1
axes_height = H1
        
axes_aspect_ratio = axes_width / axes_height

axes.set_xlim(0, axes_width)
axes.set_ylim(0, axes_height)

# Width-based major axis
if axes_aspect_ratio > 1.0:
    diagram_height = diagram_width / axes_aspect_ratio
# Height-based major axis
else:
    diagram_width = diagram_height * axes_aspect_ratio
        
fig.set_figwidth(diagram_width)
fig.set_figheight(diagram_height)


_drawing.Save('banner.png')
_drawing.Show()
