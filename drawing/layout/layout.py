#import matplotlib.patches as patches
#import matplotlib.path as path
import numpy as np
import math as math

class Layout:
    def __init__(self, axes_width, axes_height):
        self.axes_width = axes_width
        self.axes_height = axes_height

        # store the number of elements in some structure
        # Currently a list, which is sufficient for <1000 elements
        # Will need some other memory type if >1000 required
        self.element_list = np.array([], dtype=(np.int16, np.int16)
        self.column_list = np.array([], dtype=np.int16, np.int16)

    def Update_Axes(self, axes_width, axes_height):
        self.axes_width = axes_width
        self.axes_height = axes_height
