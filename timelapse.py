import numpy as np
import math as math

import Drawing.drawing as drawing

class Timelapse:
    def __init__(self, capacity):
        self.cap = capacity
        self.len = 0
        self.S = np.zeros(capacity, int)

# INTERNAL ALGORITHM IMPLEMENTATION:

    def __Checked_Less_Than_Place(self, key):
        Swap_Key = self.S[key]
        if Swap_Key < key:
            # Invalid branch
            raise AssertionError("Unknown_Less_Than_Place(): Error: Swap_Key < key")
        if Swap_Key == key:
            return                   # Key was found internally
        if Swap_Key > (self.len + 1):
            self.S[key] = key
            self.__Unchecked_Greater_Than_Place(Swap_Key)
        if Swap_Key == (self.len + 1): # Last possible branch, can be simplified to an else statement
            self.S[key] = key
            self.__Unchecked_Exact_Place(Swap_Key)

    def __Checked_Exact_Place(self, key):
        if self.S[key] != 0:
            return                   # Key was found internally
        else:
            self.S[key] = key
            self.len += 1

    def __Unchecked_Exact_Place(self, key):
        self.S[key] = key
        self.len += 1

    def __Unchecked_Greater_Than_Place(self, key):
        next_empty_pointer = self.S[self.len + 1]
        
        if next_empty_pointer != 0:
            self.S[next_empty_pointer] = key
            self.S[self.len + 1] = self.len + 1
            self.S[key] = next_empty_pointer
            self.len += 1

        else:
            self.S[self.len + 1] = key
            self.S[key] = self.len + 1
            self.len += 1


    def __Checked_Greater_Than_Place(self, key):
        if self.S[key] != 0:
            return                   # Key was found internally

        next_empty_pointer = self.S[self.len + 1]

        if next_empty_pointer != 0:
            self.S[next_empty_pointer] = key
            self.S[self.len + 1] = self.len + 1
            self.S[key] = next_empty_pointer
            self.len += 1

        else:
            self.S[self.len + 1] = key
            self.S[key] = self.len + 1
            self.len += 1

# "PUBLIC" API FUNCTIONS

    def Add(self, key):
        if key <= 0:
            raise AssertionError("key <= 0")
        if key >= self.cap:
            raise AssertionError("key >= cap")

        if key < (self.len + 1):
            self.__Checked_Less_Than_Place(key)
        
        if key == (self.len + 1):
            self.__Checked_Exact_Place(key)

        if key > (self.len + 1):
            self.__Checked_Greater_Than_Place(key)

    def Debug_Info(self):
        print("Length: ", self.len)
        print("Sparse Set: ", self.S)

timelapse = Timelapse(16)

length = 1.0
x_padding = 0.1
y_padding = 0.1

# (X,Y) Drawing start coordinates
x0 = x_padding
y0 = y_padding

# Adjust plot settings
axes_width = timelapse.cap * (length + x_padding) + x_padding 
axes_height = 2.0 * y_padding + length

_drawing = drawing.Drawing(diagram_width = 8., diagram_height = 4., show_axes=True)
_drawing.Set_Axes_Size(axes_width, axes_height)

# Draw rectangles for Hybrid Set S
for i, value in enumerate(timelapse.S):

    filled_color = 'darkseagreen'
    index_color = 'cadetblue'

    color = 'white'

    if i <= (timelapse.len + 1):
        if timelapse.S[i] == i:
            color = 'darkseagreen'
        else:
            color = 'cadetblue'

    if i > timelapse.len:
        if timelapse.S[i] == 0:
            color = 'white'
        else:
            color = 'cadetblue'

    _drawing.Draw_Square_With_Text(value, x0 + i * (length + x_padding), y0, length, color)

_drawing.Step_Array_Down(2.0)

for i, value in enumerate(timelapse.S):

    filled_color = 'darkseagreen'
    index_color = 'cadetblue'

    color = 'white'

    if i <= (timelapse.len + 1):
        if timelapse.S[i] == i:
            color = 'darkseagreen'
        else:
            color = 'cadetblue'

    if i > timelapse.len:
        if timelapse.S[i] == 0:
            color = 'white'
        else:
            color = 'cadetblue'

    _drawing.Draw_Square_With_Text(value, x0 + i * (length + x_padding), y0, length, color)

_drawing.Save(name = 'Hybrid_Set.png')
_drawing.Show()
