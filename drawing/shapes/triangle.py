import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

class TriangleBase:
    def __init__(self, x0, y0, x1, y1, x2, y2, color, arrowhead_size = 0.2):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.arrowhead_size = arrowhead_size
        self.linewidth = '-' # needs parametrize

    def Draw(self, ax):
        vertices = np.array([(x0, y0), (x1, y1), (x2, y2), (x0, y0)])
        
        codes = np.array([1, 2, 2, 2, 2])
        _path = path.Path(vertices, codes)

        # Create arrowhead patch
        path_patch = patches.PathPatch(_path, linewidth=self.linewidth, facecolor = self.color, antialiased=True)
        ax.add_patch(path_patch)

class EquilateralTriangle(TriangleBase):
    # This constructor function will calculate the cartesian coordinates from polar
    def __init__(self, ax, x0, y0, theta, color, arrowhead_size = 0.2): 
        arrowhead_length = math.cos(math.radians(30)) * arrowhead_size

        xf = x0 + arrowhead_length * math.cos(theta)
        yf = y0 + arrowhead_length * math.sin(theta)

#        super().__init__()
        
    def Draw(self, ax):
        super().Draw(ax)



    # It would be helpful to have a constructor overload like in other languages
    # Not sure what level of support python has for parameter overloads, feedback welcome
    # 
    # def __init__(self, x0, y0, x1, y1, x2, y2):

