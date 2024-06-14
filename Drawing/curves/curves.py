import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

class Curve:
    def __init__(self, x0, y0, xf, yf, theta_0, theta_f, linestyle='-'):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf
        
        self.theta_0 = theta_0
        self.theta_f = theta_f

        self.linestyle = linestyle

    def Get_Angle():
        theta = 90.0

        if abs(xf - x0) < 1e-2:
            if yf >= 0.0:
                return math.radians(90.0)
            if yf < 0.0:
                return math.radians(-90.0)
        elif (xf - x0) > 0.0:
            return math.atan((yf-y0)/(xf-x0))
        elif (xf - x0) < 0.0:
            return math.atan((yf-y0)/(xf-x0)) + math.pi() / 2.0

class Bezier(Curve):
    def __init__(self, x0, y0, xf, yf, 
                 control_point_1x, control_point_1y, control_point_2x, control_point_2y,
                 theta_0 = 0.0, theta_f = 0.0,
                 linestyle = '-'):
        super().__init__(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle)

        # Eventually turn these into __init__ parameters
        self.orientation = math.radians(90) # Does nothing right now
        self.curve_strength = 1.0

        self.control_point_1x = control_point_1x
        self.control_point_1y = control_point_1y
        self.control_point_2x = control_point_2x
        self.control_point_2y = control_point_2y


    def Shorten(self, initial, final):
        dx_0 = initial * math.cos(self.theta_0)
        dy_0 = initial * math.sin(self.theta_0)
        
        dx_f = final * math.cos(self.theta_f)
        dy_f = final * math.sin(self.theta_f)

        self.control_point_1x = self.control_point_1x + dx_0
        self.control_point_1y = self.control_point_1y + dy_0
        self.control_point_2x = self.control_point_2x + dx_f
        self.control_point_2y = self.control_point_2y + dy_f

        self.x0 = self.x0 + dx_0
        self.y0 = self.y0 + dy_0
        self.xf = self.xf + dx_f
        self.yf = self.yf + dy_f

    def Draw(self, ax):
        vertices = np.array([(self.x0, self.y0),                                # Start coordinate
                             (self.control_point_1x, self.control_point_1y),    # First control point
                             (self.control_point_2x, self.control_point_2y),    # Second control point
                             (self.xf, self.yf)])                               # End coordinate

        codes = np.array([1, 4, 4, 4])
        _path = path.Path(vertices, codes)
        
        # Increased linewidth to 1.8 for these arrow paths because it looks better
        path_patch = patches.PathPatch(_path, linewidth=1.8, fill=False, antialiased=True, linestyle = self.linestyle)
        ax.add_patch(path_patch)

class Line(Curve):
    def __init__(self, x0, y0, xf, yf, 
                 theta_0 = 0.0, theta_f = 0.0, linestyle = '-'):
        super().__init__(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle)

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
