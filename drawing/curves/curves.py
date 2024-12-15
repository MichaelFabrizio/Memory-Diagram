import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

class Curve:
    def __init__(self, x0, y0, xf, yf, theta):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf
        self.theta = theta
    
    def Get_X0(self):
        return self.x0
    
    def Get_XF(self):
        return self.xf
    
    def Get_Y0(self):
        return self.y0

    def Get_YF(self):
        return self.yf

    def Get_Theta(self):
        return self.theta
    

class Line(Curve):
    def __init__(self, x0, y0, xf, yf):
        # Divide by zero condition
        if abs(xf - x0) < 0.01:
            theta = math.radians(90.0)

        # Auto calculate theta for a default line
        elif (xf - x0) > 0.0:
            # Relative to postive x-axis
            theta = math.atan((yf - y0) / (xf - x0))
        else:
            # Relative to negative x-axis, needs 180 degree offset
            theta = math.radians(180.0) + math.atan((yf - y0) / (xf - x0))
        
        super().__init__(x0, y0, xf, yf, theta)
    
    def Shorten(self, initial, final):
        self.x0 = self.x0 + initial * math.cos(self.theta)
        self.y0 = self.y0 + initial * math.sin(self.theta)

        self.xf = self.xf - final * math.cos(self.theta)
        self.yf = self.yf - final * math.sin(self.theta)

    def Draw(self, ax):
        vertices = np.array([(self.x0, self.y0),                    # Start coordinate
                             (self.xf, self.yf)])                   # End coordinate

        codes = np.array([1, 2])
        _path = path.Path(vertices, codes)
        
        path_patch = patches.PathPatch(_path, linewidth=1.8, fill=False, antialiased=True, linestyle = '-')
        ax.add_patch(path_patch)


class Bezier(Curve):
    def __init__(self, x0, y0, xf, yf, curve_strength = 0.8):
        if (yf - y0) >= 0.0:
            theta = math.radians(90.0)
        else:
            theta = math.radians(-90.0)

        super().__init__(x0, y0, xf, yf, theta)

        self.control_point_1x = x0
        self.control_point_1y = y0 + (yf - y0) * curve_strength
        self.control_point_2x = xf
        self.control_point_2y = y0 + (yf - y0) * (1.0 - curve_strength)
        
    
    def Shorten(self, initial, final):
        self.x0 = self.x0 + initial * math.cos(self.theta)
        self.y0 = self.y0 + initial * math.sin(self.theta)

        self.xf = self.xf - final * math.cos(self.theta)
        self.yf = self.yf - final * math.sin(self.theta)
        # TODO: Add control point adjustments

    def Draw(self, ax):
        vertices = np.array([(self.x0, self.y0),                                # Start coordinate
                             (self.control_point_1x, self.control_point_1y),    # First control point
                             (self.control_point_2x, self.control_point_2y),    # Second control point
                             (self.xf, self.yf)])                               # End coordinate

        codes = np.array([1, 4, 4, 4])
        _path = path.Path(vertices, codes)
        
        path_patch = patches.PathPatch(_path, linewidth=1.8, fill=False, antialiased=True, linestyle = '-')
        ax.add_patch(path_patch)
