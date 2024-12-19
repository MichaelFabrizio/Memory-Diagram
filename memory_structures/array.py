import numpy as np
import math as math

import drawing.drawing as drawing

# A sequence of N array elements
# The Add(key) function allows unsorted adding of integers
#
# The Draw() function handles all the calculations for element distances and geometry
# Which easily allows a user to generate arrays within the main.py script
class Array:
    def __init__(self, capacity, drawing_class = None):
        self.cap = capacity
        self.len = 1
        self.D = np.zeros(capacity, int) # D is renamable to 'Keys', this is the array we are adding to.
        
        if drawing_class == None:
            self.drawing = drawing.Drawing(diagram_width = 11., diagram_height = 4., show_axes = True, horizontal_elements = self.cap, vertical_elements = 1, lower_padding = 1.0, show_axes_numbers = True)
            print('Implicit drawing')
        else:
            self.drawing = drawing_class
            print('Supplied drawing')


    # Add new unsorted integers to the array structure. Does not check for duplicate keys, although it should.
    def Add(self, key):
        # These bounds checks ensure the key is on a defined number line. Ex: Represent [0, cap) keys,
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

            self.drawing.Draw_Square_With_Text(value, i, 0.0, dcolor)
        
        self.drawing.Save(name = 'Simple_Array.png')
        self.drawing.Show()

    def Save(self, name = 'array.png'):
        self.drawing.Save(name)

    def Get_Drawing(self):
        return self.drawing
