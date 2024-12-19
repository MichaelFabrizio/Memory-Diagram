import numpy as np
import math as math    

import drawing as drawing

# The Sparse class refers to the sparse set datastructure, which is well researched in the Entity-Component-System community.
# It is a structure of two arrays: one sparse array of data, one dense array of data.
#
# I have chosen a different nomenclature to define these arrays (for my work):
# 
# Array S: Sparse -> Indices
# Array D: Dense -> Keys
#
# Although, these arrays are merged under the keyvector setup into a single array, Indices.
# This nomenclature work will be defined in the discussion threads
class Sparse:
    def __init__(self, capacity):
        self.cap = capacity
        self.len = 1

        self.S = np.zeros(capacity, int)
        self.D = np.zeros(capacity, int)


    # There is an error in the logic here, will have to revisit
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
        _drawing = drawing.Drawing(diagram_width = 11., diagram_height = 4., show_axes = True, horizontal_elements = self.cap, vertical_elements = 2, lower_padding = 1.0, show_axes_numbers = True)


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

            _drawing.Draw_Square_With_Text(value, i, 0.0, dcolor)

        _drawing.Step_Array_Down(2.0)

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


        _drawing.Save(name = 'Sparse_Set.png')
        _drawing.Show()
