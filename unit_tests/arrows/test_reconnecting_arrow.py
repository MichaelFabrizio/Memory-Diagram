import sys as sys
import os
from pathlib import Path

import numpy as np
import math

script_dir = Path(os.path.abspath(__file__)).parent.absolute()
base_dir = script_dir.parent.absolute().parent.absolute()

sys.path.append(str(base_dir))

import drawing.drawing as drawing

# Manually set axes_auto to false
# And set the axes_width and axes_height parameters to be proportional to diagram_width + diagram_height
# Which creates a diagram without skew
_drawing = drawing.Drawing(diagram_width = 4., diagram_height = 4., show_axes = True, show_axes_numbers = True, axes_auto = False, axes_width = 4.0, axes_height = 4.0)

# PARAMETERS:
# x0 = 3.0, y0 = 1.0, stride = 2.0
_drawing.Draw_Reconnecting_Arrow(3.0, 1.0, 2.0, theta = math.pi / 4., arrowstyle = '<->')

_drawing.Save('test_reconnecting_arrow.png')
_drawing.Show()
