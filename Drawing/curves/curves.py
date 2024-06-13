import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

class Curve:
    def __init__(self, x0, y0, xf, yf, linestyle='-'):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf

        self.linestyle = linestyle

class Bezier(Curve):
    def __init__(self, x0, y0, xf, yf, linestyle = '-'):
        super().__init__(x0, y0, xf, yf, linestyle = linestyle)

        # Eventually turn these into __init__ parameters
        self.orientation = math.radians(90) # Does nothing right now
        self.curve_strength = 1.0

        # Needs trig generalizing
        self.first_control_point = self.y0 + self.curve_strength
        self.second_control_point = self.yf - self.curve_strength

    def Shorten(self, initial, final):
        # Needs trig generalizing + additional checks (prevent initial/final > "effective curve length")
        self.y0 = self.y0 + initial
        self.yf = self.yf - final
        self.first_control_point = self.first_control_point + initial
        self.second_control_point = self.second_control_point - final

    def Draw(self, ax):
        vertices = np.array([(self.x0, self.y0),                    # Start coordinate
                             (self.x0, self.first_control_point),   # First control point
                             (self.xf, self.second_control_point),  # Second control point
                             (self.xf, self.yf)])                   # End coordinate

        codes = np.array([1, 4, 4, 4])
        _path = path.Path(vertices, codes)
        
        # Increased linewidth to 1.8 for these arrow paths because it looks better
        path_patch = patches.PathPatch(_path, linewidth=1.8, fill=False, antialiased=True, linestyle = self.linestyle)
        ax.add_patch(path_patch)

class Line(Curve):
    def __init__(self, x0, y0, xf, yf, linestyle = '-'):
        super().__init__(x0, y0, xf, yf, linestyle = linestyle)

    def Shorten(self, initial, final):
        self.y0 = self.y0 + initial
        self.yf = self.yf - final

    def Draw(self, ax):
        vertices = np.array([(self.x0, self.y0),                    # Start coordinate
                             (self.xf, self.yf)])                   # End coordinate

        codes = np.array([1, 2])
        _path = path.Path(vertices, codes)
        
        # Increased linewidth to 1.8 for these arrow paths because it looks better
        path_patch = patches.PathPatch(_path, linewidth=1.8, fill=False, antialiased=True, linestyle = self.linestyle)
        ax.add_patch(path_patch)
