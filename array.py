
import numpy as np
import math as math

import Drawing.drawing as drawing

class Array:
    def __init__(self, capacity):
        self.cap = capacity
        self.len = 1
        self.D = np.zeros(capacity, int)

# "PUBLIC" API FUNCTIONS

    def Add(self, key):
        if key <= 0:
            raise AssertionError("key <= 0")
        if key >= self.cap:
            raise AssertionError("key >= cap")

        else:
            self.D[self.len] = key
            self.len += 1

    def Debug_Info(self):
        print("Length: ", self.len)
        print("Dense Set: ", self.D)

array = Array(10)
array.Add(1)
array.Add(2)
array.Add(6)
array.Add(4)
array.Add(5)

length = 1.0
x_padding = 0.1
y_padding = 0.1 # Should also be renamed to y_padding (to match x_padding)

# Adjust plot settings
axes_width = array.cap * (length + x_padding) + x_padding 
axes_height = 2.0 * y_padding + length
x0 = x_padding
y0 = y_padding

_drawing = drawing.Drawing(diagram_width = 8., diagram_height = 4., show_axes = True)
_drawing.Set_Axes_Size(axes_width, axes_height)

for i, value in enumerate(array.D):

    filled_color = 'darkseagreen'
    index_color = 'cadetblue'

    dcolor = 'white'

    if i == 0:
        dcolor = filled_color
    elif value != 0:
        dcolor = filled_color
    else:
        dcolor = 'white'

    _drawing.Draw_Square_With_Text(value, x0 + i * (length + x_padding), y0, length, dcolor)

_drawing.Save(name = 'Simple_Array.png')
_drawing.Show()

