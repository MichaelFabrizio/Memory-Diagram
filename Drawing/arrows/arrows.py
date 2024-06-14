import matplotlib.patches as patches
import matplotlib.path as path
import math as math
import curves.curves as curves
import numpy as np

class ArrowBase:
    def __init__(self, x0, y0, xf, yf, color = 'white', arrowhead_size = 0.2, linestyle = '-', arrowstyle = '<->'):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf
        self.color = color
        self.arrowhead_size = arrowhead_size
        self.arrowstyle = arrowstyle
        self.linestyle = linestyle
    
    def __Draw_Triangle_Arrowhead(self, ax, x0, y0, xf, yf, color, side_length = 0.2):
        dy = yf - y0
        dx = xf - x0
        theta = 0.0

        # Prevent division by dy=0 errors
        if dy == 0:
            if dx < 0:
                theta = math.radians(90)
            if dx > 0:
                theta = math.radians(-90)
        else:
            theta = math.atan(dx/dy)

        # Calculate arrowhead vertices using trig
        vertices = np.array([(x0, y0),                                                                                  # v0
                             (x0 + side_length/2. * math.cos(theta), y0 - side_length/2. * math.sin(theta)),            # v1
                             (xf, yf), (x0 - side_length/2. * math.cos(theta), y0 + side_length/2. * math.sin(theta)),  # v2
                             (x0, y0)])                                                                                 # v3

        # MatPlotLib "Path codes" to define straight lines
        codes = np.array([1, 2, 2, 2, 2])
        _path = path.Path(vertices, codes)

        # Create arrowhead patch
        path_patch = patches.PathPatch(_path, linewidth=1.5, facecolor = color, antialiased=True)
        ax.add_patch(path_patch)

    # PARAMETERS:
    # ax - A matplotlib ax which is passed by the Drawing class.
    # arrowbody - The curve or line of the arrow. Type arrowbody requires a method Shorten(initial_amount, final_amount, theta_0, theta_f). Theta in radians.
    def Draw(self, ax, arrowbody, arrowstyle):
        # Height delta of a single arrowhead
        arrowhead_dy = math.cos(math.radians(30)) * self.arrowhead_size
        top_arrow_y0 = self.yf - arrowhead_dy
        bot_arrow_y0 = self.y0 + arrowhead_dy

        if arrowstyle == '<->':
            arrowbody.Shorten(arrowhead_dy, arrowhead_dy)
            self.__Draw_Triangle_Arrowhead(ax, self.xf, top_arrow_y0, self.xf, self.yf, self.color, arrowhead_dy)
            self.__Draw_Triangle_Arrowhead(ax, self.x0, bot_arrow_y0, self.x0, self.y0, self.color, arrowhead_dy)
        if arrowstyle == '<-':
            arrowbody.Shorten(arrowhead_dy, 0)
            self.__Draw_Triangle_Arrowhead(ax, self.x0, bot_arrow_y0, self.x0, self.y0, self.color, arrowhead_dy)
        if arrowstyle == '->':
            arrowbody.Shorten(0, arrowhead_dy)
            self.__Draw_Triangle_Arrowhead(ax, self.xf, top_arrow_y0, self.xf, self.yf, self.color, arrowhead_dy)

class DiagonalArrow(ArrowBase):
    def __init__(self, x0, y0, xf, yf, color = 'white', arrowhead_size = 0.2, linestyle = '-', arrowstyle = '<->'):
        super().__init__(x0, y0, xf, yf, linestyle = linestyle, arrowstyle = arrowstyle)

        # Calculate control points
        control_point_1x = x0;
        control_point_1y = y0 + 1.0; # Curve-strength = 1.0
        control_point_2x = xf;
        control_point_2y = yf - 1.0;

        # Class defined final direction vectors
        theta_0 = math.radians(90.0)
        theta_f = math.radians(-90.0)

        # Generate cubic bezier's shape in constructor
        self.cubic_bezier = curves.Bezier(x0, y0, xf, yf, 
                                          control_point_1x, control_point_1y, control_point_2x, control_point_2y,
                                          theta_0, theta_f,
                                          linestyle = linestyle)

    def Draw(self, ax):
        super().Draw(ax, self.cubic_bezier, self.arrowstyle)
        self.cubic_bezier.Draw(ax)

class VerticalArrow(ArrowBase):
    def __init__(self, x0, y0, xf, yf, color = 'white', arrowhead_size = 0.2, linestyle = '-', arrowstyle = '<->'):
        super().__init__(x0, y0, xf, yf, linestyle = linestyle, arrowstyle = arrowstyle)

        # Class defined final direction vectors
        theta_0 = math.radians(90.0)
        theta_f = math.radians(-90.0)
        
        self.line = curves.Line(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle)
    def Draw(self, ax):
        super().Draw(ax, self.line, self.arrowstyle)
        self.line.Draw(ax)

class ReconnectingArrow(ArrowBase):
    def __init__(self, axes_offset, cardinality = 'north', height = 1.0, linestyle = '-', arrowstyle = '<->'):
        if cardinality == 'north':
            pass
        if cardinality == 'south':
            pass
        if cardinality == 'east':
            pass
        if cardinality == 'west':
            pass
        
        super().__init__(x0, y0, xf, yf, linestyle = linestyle, arrowstyle = arrowstyle)
        self.cubic_bezier = curves.Bezier(x0, y0, xf, yf, linestyle = linestyle)

    def Draw(self, ax):
        super().Draw(ax, self.cubic_bezier, self.arrowstyle)
        self.cubic_bezier.Draw(ax)
