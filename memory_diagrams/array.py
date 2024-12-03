
import numpy as np
import math as math

import drawing as drawing

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

    def Draw(self):

        _drawing = drawing.Drawing(diagram_width = 11., diagram_height = 4., show_axes = True, horizontal_elements = self.cap, vertical_elements = 1, lower_padding = 1.0, show_axes_numbers = True)

        underline_bar_height = 1.0
        stride = 2.0

        _drawing.Scale_Axes_Height_By_Value(underline_bar_height)

        for i, value in enumerate(self.D):

            filled_color = 'darkseagreen'
            index_color = 'cadetblue'

            dcolor = 'white'

            if i == 0:
                dcolor = filled_color
            elif value != 0:
                dcolor = filled_color
            else:
                dcolor = 'white'

            _drawing.Draw_Square_With_Text(value, i, dcolor)
        
        # TODO: Test, Fix, Remove
        _drawing.Draw_Underline_Bar_Floating(1.0, 0.5, stride, underline_bar_height)

        #_drawing.Save(name = 'Simple_Array.png')
        _drawing.Show()


    def Save(self, name = 'array.png'):
        _drawing.Save(name)
