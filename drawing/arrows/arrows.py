import matplotlib.patches as patches
import matplotlib.path as path
import math as math
import numpy as np

import drawing.curves.curves as curves
import drawing.shapes.triangles as triangles

class ArrowBase:
    def __init__(self, x0, y0, xf, yf, curve, arrowstyle = '<->'):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf
        self.curve = curve
        self.arrowstyle = arrowstyle
        self.arrowhead_sidelength = 0.2 # Default for now
        self.arrowhead_height = self.arrowhead_sidelength * math.cos(math.radians(30.0))

        if self.arrowstyle == '<->':
            self.curve.Shorten(self.arrowhead_height, self.arrowhead_height)
        if self.arrowstyle == '<-':
            self.curve.Shorten(self.arrowhead_height, 0.0)
        if self.arrowstyle == '->':
            self.curve.Shorten(0.0, self.arrowhead_height)

        theta_f = self.curve.Get_Theta() # In radians
        
        x0 = self.curve.Get_X0()
        y0 = self.curve.Get_Y0()
        
        xf = self.curve.Get_XF()
        yf = self.curve.Get_YF()

        if self.arrowstyle == '<->':
            self.first_triangle = triangles.EquilateralTriangle(x0, y0, self.arrowhead_sidelength, math.radians(180) + theta_f)
            self.second_triangle = triangles.EquilateralTriangle(xf, yf, self.arrowhead_sidelength, theta_f)
        if self.arrowstyle == '<-':
            self.first_triangle = triangles.EquilateralTriangle(x0, y0, self.arrowhead_sidelength, math.radians(180) + theta_f)
        if self.arrowstyle == '->':
            self.second_triangle = triangles.EquilateralTriangle(xf, yf, self.arrowhead_sidelength, theta_f)

    def Draw(self, ax):
        if self.arrowstyle == '<->':
            self.curve.Draw(ax)
            self.first_triangle.Draw(ax)
            self.second_triangle.Draw(ax)
        if self.arrowstyle == '<-':
            self.curve.Draw(ax)
            self.first_triangle.Draw(ax)
        if self.arrowstyle == '->':
            self.curve.Draw(ax)
            self.second_triangle.Draw(ax)

class Arrow(ArrowBase):
    def __init__(self, x0, y0, xf, yf, arrowstyle = '<->'):
        line = curves.Line(x0, y0, xf, yf)
        super().__init__(x0, y0, xf, yf, line, arrowstyle = arrowstyle)

    def Draw(self, ax):
        super().Draw(ax)

class DiagonalArrow(ArrowBase):
    def __init__(self, x0, y0, xf, yf, arrowstyle = '<->'):
        bezier = curves.Bezier(x0, y0, xf, yf)
        super().__init__(x0, y0, xf, yf, bezier, arrowstyle = arrowstyle)

    def Draw(self, ax):
        super().Draw(ax)


# Connect two array elements on the same vertical/horizontal line.
# The North, South, East, West directionality is only a workaround solution, ideally it would be defined with Polar Coordinates (r, theta)
# 
# The two control points would also be theta dependent, I'll try to get a diagram for that.
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

# This arrow is the elbow shape.
# This one is already defined against theta, so it's mostly complete?
# However a change of coordinate system might affect the trig calculations
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
