import matplotlib.patches as patches
import matplotlib.path as path
import math as math
import curves.curves as curves
import numpy as np

class ArrowBase:
    def __init__(self, x0, y0, xf, yf, theta_0 = 0.0, theta_f = 0.0, color = 'white', arrowhead_size = 0.2, linestyle = '-', arrowstyle = '<->'):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf
        self.theta_0 = theta_0
        self.theta_f = theta_f
        self.color = color
        self.arrowhead_size = arrowhead_size
        self.arrowstyle = arrowstyle
        self.linestyle = linestyle
    
    def __Draw_Triangle_Arrowhead(self, ax, x0, y0, theta, color, side_length = 0.2):
        arrowhead_length = math.cos(math.radians(30)) * self.arrowhead_size

        xf = x0 + arrowhead_length * math.cos(theta)
        yf = y0 + arrowhead_length * math.sin(theta)

        # Calculate arrowhead vertices using trig
        vertices = np.array([(x0, y0),                                                                                  # v0
                             (x0 + side_length/2. * math.sin(theta), y0 - side_length/2. * math.cos(theta)),            # v1
                             (xf, yf), (x0 - side_length/2. * math.sin(theta), y0 + side_length/2. * math.cos(theta)),  # v2
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
        arrowhead_length = math.cos(math.radians(30)) * self.arrowhead_size
        
        dx_0 = - arrowhead_length * math.cos(self.theta_0)
        dy_0 = - arrowhead_length * math.sin(self.theta_0)
        
        dx_f = - arrowhead_length * math.cos(self.theta_f)
        dy_f = - arrowhead_length * math.sin(self.theta_f)

        if arrowstyle == '<->':
            arrowbody.Shorten(arrowhead_length, arrowhead_length)
            self.__Draw_Triangle_Arrowhead(ax, self.xf + dx_f, self.yf + dy_f, self.theta_f, self.color, arrowhead_length)
            self.__Draw_Triangle_Arrowhead(ax, self.x0 + dx_0, self.y0 + dy_0, self.theta_0, self.color, arrowhead_length)
        if arrowstyle == '<-':
            arrowbody.Shorten(arrowhead_length, 0)
            self.__Draw_Triangle_Arrowhead(ax, self.x0 + dx_0, self.y0 + dy_0, self.theta_0, self.color, arrowhead_length)
        if arrowstyle == '->':
            arrowbody.Shorten(0, arrowhead_length)
            self.__Draw_Triangle_Arrowhead(ax, self.xf + dx_f, self.yf + dy_f, self.theta_f, self.color, arrowhead_length)

class DiagonalArrow(ArrowBase):
    def __init__(self, x0, y0, xf, yf, color = 'white', arrowhead_size = 0.2, linestyle = '-', arrowstyle = '<->'):

        # Class defined final direction vectors
        theta_0 = math.radians(-90.0)
        theta_f = math.radians(90.0)

        super().__init__(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle, arrowstyle = arrowstyle)

        # Calculate control points
        control_point_1x = x0;
        control_point_1y = y0 + 1.0; # Curve-strength = 1.0
        control_point_2x = xf;
        control_point_2y = yf - 1.0;

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
        # Class defined final direction vectors
        theta_0 = math.radians(-90.0)
        theta_f = math.radians(90.0)
        
        super().__init__(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle, arrowstyle = arrowstyle)

        
        self.line = curves.Line(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle)
    def Draw(self, ax):
        super().Draw(ax, self.line, self.arrowstyle)
        self.line.Draw(ax)

class ReconnectingArrow(ArrowBase):
    def __init__(self, x_offset, y_offset, stride, cardinality, height = 1.0, linestyle = '-', arrowstyle = '<->'):
        # Can be generalized for different angles to reduce code bloat
        if cardinality == 'north':
            theta_0 = math.radians(90.0)
            theta_f = math.radians(90.0)
            
            x0 = x_offset - stride / 2.0
            xf = x_offset + stride / 2.0
            y0 = y_offset
            yf = y_offset

            super().__init__(x0, y_offset, xf, y_offset,
                             theta_0, theta_f,
                             linestyle = linestyle, arrowstyle = arrowstyle)
        
            control_point_1x = x0
            control_point_1y = y_offset - 1.0
            control_point_2x = xf
            control_point_2y = y_offset - 1.0

        if cardinality == 'south':
            theta_0 = math.radians(-90.0)
            theta_f = math.radians(-90.0)
            
            x0 = x_offset - stride / 2.0
            xf = x_offset + stride / 2.0
            y0 = y_offset
            yf = y_offset

            super().__init__(x0, y_offset, xf, y_offset,
                             theta_0, theta_f,
                             linestyle = linestyle, arrowstyle = arrowstyle)
        
            control_point_1x = x0
            control_point_1y = y_offset + 1.0
            control_point_2x = xf
            control_point_2y = y_offset + 1.0
        if cardinality == 'east':
            theta_0 = math.radians(0.0)
            theta_f = math.radians(0.0)
            
            x0 = x_offset
            xf = x_offset
            y0 = y_offset - stride / 2.0
            yf = y_offset + stride / 2.0
            super().__init__(x_offset, y0, x_offset, yf,
                             theta_0, theta_f,
                             linestyle = linestyle, arrowstyle = arrowstyle)
        
            control_point_1x = x_offset - 1.0
            control_point_1y = y0
            control_point_2x = x_offset - 1.0
            control_point_2y = yf
        if cardinality == 'west':
            theta_0 = math.radians(180.0)
            theta_f = math.radians(180.0)
            
            x0 = x_offset
            xf = x_offset
            y0 = y_offset - stride / 2.0
            yf = y_offset + stride / 2.0
            super().__init__(x_offset, y0, x_offset, yf,
                             theta_0, theta_f,
                             linestyle = linestyle, arrowstyle = arrowstyle)
        
            control_point_1x = x_offset + 1.0
            control_point_1y = y0
            control_point_2x = x_offset + 1.0
            control_point_2y = yf
        
        # Generate cubic bezier's shape in constructor
        self.cubic_bezier = curves.Bezier(x0, y0, xf, yf, 
                                          control_point_1x, control_point_1y, control_point_2x, control_point_2y,
                                          theta_0, theta_f,
                                          linestyle = linestyle)

    def Draw(self, ax):
        super().Draw(ax, self.cubic_bezier, self.arrowstyle)
        self.cubic_bezier.Draw(ax)

class CornerArrow(ArrowBase):
    def __init__(self, x_offset, y_offset, radius, theta, linestyle = '-', arrowstyle = '<->'):
        dx0 = - radius * math.sin(theta)
        dy0 =   radius * math.cos(theta)
        dxf =   radius * math.cos(theta)
        dyf =   radius * math.sin(theta)

        x0 = x_offset + dx0
        y0 = y_offset + dy0
        xf = x_offset + dxf
        yf = y_offset + dyf

        theta_0 = theta + math.pi/2.
        theta_f = theta

        control_point_1x = x_offset + 0.2 * dx0
        control_point_1y = y_offset + 0.2 * dy0
        control_point_2x = x_offset + 0.2 * dxf
        control_point_2y = y_offset + 0.2 * dyf

        super().__init__(x0, y0, xf, yf, theta_0, theta_f, linestyle = linestyle, arrowstyle = arrowstyle)
        
        self.cubic_bezier = curves.Bezier(x0, y0, xf, yf, 
                                          control_point_1x, control_point_1y, control_point_2x, control_point_2y,
                                          theta_0, theta_f,
                                          linestyle = linestyle)
    
    def Draw(self, ax):
        super().Draw(ax, self.cubic_bezier, self.arrowstyle)
        self.cubic_bezier.Draw(ax)
