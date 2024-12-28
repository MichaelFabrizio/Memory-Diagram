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

x_center = 2.0
y_center = 2.0
arrow_length = 2.0

for i in np.linspace(0, 9, 10):
    theta = i * math.radians(180.) / 10.
    x0 = x_center - arrow_length * math.cos(theta)
    y0 = y_center - arrow_length * math.sin(theta)
    xf = x_center + arrow_length * math.cos(theta)
    yf = y_center + arrow_length * math.sin(theta)
    _drawing.Draw_Arrow(x0, y0, xf, yf, arrowstyle = '<->')

_drawing.Save('test_basic_arrow.png')
_drawing.Show()
