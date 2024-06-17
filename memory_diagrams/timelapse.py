import numpy as np
import math as math

import drawing as drawing

class Timelapse:
    def __init__(self, capacity, totalsteps):
        self.cap = capacity
        self.len = 0
        self.S = np.zeros(capacity, int)
        self.totalsteps = totalsteps
        self.stepsize = 3.0

        self.drawing = drawing.Drawing(diagram_width = 8., diagram_height = 4., show_axes=True)
        
        ## Temporarily here, but this code can be merged with Draw() call code
        #  Need to declare these as member variables
        length = 1.0
        x_padding = 0.1
        y_padding = 0.1

        # (X,Y) Drawing start coordinates
        x0 = x_padding
        y0 = y_padding

        # Adjust plot settings
        axes_width = self.cap * (length + x_padding) + x_padding 
        axes_height = 2.0 * y_padding + length + (self.totalsteps - 1) * self.stepsize

        self.drawing.Set_Axes_Size(axes_width, axes_height)

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

    def Clear(self):
        for i, element in enumerate(self.S):
            self.S[i] = 0

    def Debug_Info(self):
        print("Length: ", self.len)
        print("Sparse Set: ", self.S)

    def Draw(self):
        length = 1.0
        x_padding = 0.1
        y_padding = 0.1

        # (X,Y) Drawing start coordinates
        x0 = x_padding
        y0 = y_padding + (self.totalsteps - 1) * self.stepsize

        # Draw rectangles for Hybrid Set S
        for i, value in enumerate(self.S):

            filled_color = 'darkseagreen'
            index_color = 'cadetblue'

            color = 'white'

            if i == 0:
                color = 'darkseagreen'
            elif i <= (self.len):
                if self.S[i] == 0:
                    color = 'white'
                elif self.S[i] == i:
                    color = 'darkseagreen'
                else:
                    color = 'cadetblue'

            if i > self.len:
                if self.S[i] == 0:
                    color = 'white'
                else:
                    color = 'cadetblue'

            self.drawing.Draw_Square_With_Text(value, x0 + i * (length + x_padding), y0, length, color)

        self.drawing.Step_Array_Down(self.stepsize)
        self.Clear()

    def DrawInput(self, key):
        length = 1.0
        x_padding = 0.1
        y_padding = 0.1

        x0 = x_padding
        y0 = y_padding + (self.totalsteps - 1) * self.stepsize

        x_key = x0 + key * (length + x_padding)

        x_arrow = x_key + length/2.
        y_arrow_f = y0 + length - self.stepsize

        self.drawing.Draw_Square_With_Text(key, x_key, y0, length, 'darkseagreen')

        self.drawing.Draw_Vertical_Arrow(   x_arrow, y0, x_arrow, y_arrow_f,
                                            theta_0 = math.radians(90.0), theta_f = math.radians(-90.0),
                                            color = 'darkseagreen', arrowstyle = '->')

        self.drawing.Step_Array_Down(self.stepsize)
        self.Clear()


    def Save(self):
        self.drawing.Save(name = 'Hybrid_Set.png')

    def Show(self):
        self.drawing.Show()


