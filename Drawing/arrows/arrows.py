import matplotlib.patches as patches
import matplotlib.path as path
import math as math
import bezier.bezier as bezier
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

    # arrowbody - The curve or line of the arrow. Requires a method Shorten(initial_amount, final_amount)
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
            pass


class DiagonalArrow(ArrowBase):
    def __init__(self, x0, y0, xf, yf, color = 'white', arrowhead_size = 0.2, linestyle = '-', arrowstyle = '<->'):
        super().__init__(x0, y0, xf, yf, arrowstyle = arrowstyle)
        self.cubic_bezier = bezier.Bezier(x0, y0, xf, yf)

    def Draw(self, ax):
        super().Draw(ax, self.cubic_bezier, self.arrowstyle)
        self.cubic_bezier.Draw(ax)
