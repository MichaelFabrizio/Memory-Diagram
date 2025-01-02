import sys as sys
import os
from pathlib import Path

import numpy as np

script_dir = Path(os.path.abspath(__file__)).parent.absolute()
base_dir = script_dir.parent.absolute().parent.absolute()

sys.path.append(str(base_dir))

import drawing.drawing as drawing
import memory_structures.array as array

_drawing = drawing.Drawing(diagram_width = 11., diagram_height = 4., show_axes = True, horizontal_elements = 10, vertical_elements = 1, lower_padding = 0.1, upper_padding = 2.0, left_padding = 0.1, right_padding = 0.1, show_axes_numbers = False)

_array = array.Array(10, _drawing)
_array.Add(1)
_array.Add(2)
_array.Add(3)
_array.Add(4)
_array.Add(5)
_array.Add(6)
_array.Add(7)


_array.Draw()

_drawing.Draw_Centered_X_Anchored(5)
_drawing.Draw_Reconnecting_Arrow_Anchored(5, 7, arrowstyle = '<-')

_array.Save('remove_key.png')
_array.Show()
