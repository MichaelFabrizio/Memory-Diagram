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

        theta_0 = self.curve.Get_Theta_0() # In radians
        theta_f = self.curve.Get_Theta_F() # In radians
        
        # These coordinates are needed to place the arrowhead
        x0 = self.curve.Get_X0()
        y0 = self.curve.Get_Y0()
        
        xf = self.curve.Get_XF()
        yf = self.curve.Get_YF()

        if self.arrowstyle == '<->':
            self.first_triangle = triangles.EquilateralTriangle(x0, y0, self.arrowhead_sidelength, theta_0)
            self.second_triangle = triangles.EquilateralTriangle(xf, yf, self.arrowhead_sidelength, theta_f)
        if self.arrowstyle == '<-':
            self.first_triangle = triangles.EquilateralTriangle(x0, y0, self.arrowhead_sidelength, theta_0)
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
    def __init__(self, x0, y0, xf, yf, curve_strength = 0.8, arrowstyle = '<->'):
        control_point_1x = x0
        control_point_1y = y0 + (yf - y0) * curve_strength
        control_point_2x = xf
        control_point_2y = y0 + (yf - y0) * (1.0 - curve_strength)
        
        if (yf - y0) >= 0.0:
            theta_f = math.radians(90.0)
        else:
            theta_f = math.radians(-90.0)

        theta_0 = theta_f + math.radians(180)

        bezier = curves.Bezier(x0, y0, xf, yf, control_point_1x, control_point_1y, control_point_2x, control_point_2y, theta_0 = theta_0, theta_f = theta_f)
        super().__init__(x0, y0, xf, yf, bezier, arrowstyle = arrowstyle)

    def Draw(self, ax):
        super().Draw(ax)

class ReconnectingArrow(ArrowBase):
    def __init__(self, x0, y0, stride, theta = 0.0, height = 1.0, arrowstyle = '<->'):
        xf = x0 - stride * math.sin(theta)
        yf = y0 + stride * math.cos(theta)
        control_point_1x = x0 - height * math.cos(theta)
        control_point_1y = y0 - height * math.sin(theta)
        control_point_2x = x0 - height * math.cos(theta) - stride * math.sin(theta)
        control_point_2y = y0 - height * math.sin(theta) + stride * math.cos(theta)
        
        bezier = curves.Bezier(x0, y0, xf, yf, control_point_1x, control_point_1y, control_point_2x, control_point_2y, theta_0 = theta, theta_f = theta)
        super().__init__(x0, y0, xf, yf, bezier, arrowstyle = arrowstyle)

    def Draw(self, ax):
        super().Draw(ax)

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
