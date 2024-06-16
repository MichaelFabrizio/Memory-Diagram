import numpy as np
import math as math    

import drawing as drawing

class Sparse:
    def __init__(self, capacity):
        self.cap = capacity
        self.len = 1
        self.S = np.zeros(capacity, int)
        self.D = np.zeros(capacity, int)

# "PUBLIC" API FUNCTIONS

    def Add(self, key):
        if key <= 0:
            raise AssertionError("key <= 0")
        if key >= self.cap:
            raise AssertionError("key >= cap")

        if self.S[key] != 0:
            print("Duplicate add attempt")
            return
        else:
            self.D[self.len] = key
            self.S[key] = self.len
            self.len += 1

    def Debug_Info(self):
        print("Length: ", self.len)
        print("Sparse Set: ", self.S)
        print("Dense Set: ", self.D)

    def Draw(self):
        length = 1.0
        x_padding = 0.1
        y_padding = 0.1

        # Distance between top and bottom arrays
        array_separation = 2.0 * length

        # (X,Y) Drawing start coordinates
        x0 = x_padding
        y0 = y_padding + length + array_separation
        y0S = y_padding

        # Adjust plot settings
        axes_width = self.cap * (length + x_padding) + x_padding 
        axes_height = array_separation + 2.0 * length + 2.0 * y_padding

        _drawing = drawing.Drawing(diagram_width = 8., diagram_height = 4., show_axes=True)
        _drawing.Set_Axes_Size(axes_width, axes_height)

        # Draw rectangles for Sparse Set S
        for i, value in enumerate(self.S):
            sx_center = x0 + length/2. + i * (length + x_padding)
            sy_top = y0S + length

            dx_center = x0 + length/2. + value * (length + x_padding)
            dy_bottom = y0

            filled_color = 'darkseagreen'
            index_color = 'cadetblue'

            color = 'white'

            if i == 0:
                color = filled_color
            elif value != 0:
                if value == i:
                    color = filled_color
                    _drawing.Draw_Vertical_Arrow(sx_center, sy_top, sx_center, dy_bottom, color)
                else:
                    color = index_color
                    _drawing.Draw_Diagonal_Arrow(sx_center, sy_top, dx_center, dy_bottom, 1.2, color, dashed=True)
            else:
                color = 'white'

            _drawing.Draw_Square_With_Text(value, x0 + i * (length + x_padding), y0S, length, color)

        # Draw rectangles for Dense Set D
        for i, value in enumerate(self.D):

            filled_color = 'darkseagreen'
            index_color = 'cadetblue'

            dcolor = 'white'
            delement = self.D[i]

            if delement != 0:
                if self.S[delement] == delement:
                    dcolor = filled_color
                else:
                    dcolor = index_color
            else:
                dcolor = 'white'

            _drawing.Draw_Square_With_Text(value, x0 + i * (length + x_padding), y0, length, dcolor)

        _drawing.Save(name = 'Sparse_Set.png')
        _drawing.Show()
