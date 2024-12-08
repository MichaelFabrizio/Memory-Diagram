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
        # Bounds checks
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
        _drawing = drawing.Drawing(diagram_width = 11., diagram_height = 4., show_axes = True, horizontal_elements = self.cap, vertical_elements = 1, lower_padding = 1.0, show_axes_numbers = True)

#        underline_bar_height = 1.0
#        stride = 2.0

#        drawing.Scale_Axes_Height_By_Value(underline_bar_height)
        _drawing.Scale_Axes_Height_By_Value(1.1)

        for i, value in enumerate(self.S):
            filled_color = 'darkseagreen'
            index_color = 'cadetblue'

            dcolor = 'white'

            if i == 0:
                dcolor = filled_color
            elif value != 0:
                dcolor = filled_color
            else:
                dcolor = 'white'

            _drawing.Draw_Square_With_Text(value, i, 0.0, dcolor)
        
        #:_drawing.Draw_Underline_Bar_Anchored(1, 5, underline_bar_height, 0.2)
        #_drawing.Draw_Diagonal_Arrow(3.0, 1.0, 5.0, 2.0, 0.5, 'black')


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
            _drawing.Draw_Square_With_Text(value, i, 2.0, dcolor)
            #_drawing.Draw_Vertical_Arrow_Anchored(i, 0.0, 2.0, 'black')

        _drawing.Save(name = 'Sparse_Set.png')
        _drawing.Show()
