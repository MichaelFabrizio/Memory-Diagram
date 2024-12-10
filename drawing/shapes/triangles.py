import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

class TriangleBase:
    def __init__(self, x0, y0, x1, y1, x2, y2, color):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.linewidth = '-' # needs parametrize

    def Draw(self, ax):
        vertices = np.array([(self.x0, self.y0), (self.x1, self.y1), (self.x2, self.y2), (self.x0, self.y0)])
        
        codes = np.array([1, 2, 2, 2])
        _path = path.Path(vertices, codes)

        # Create arrowhead patch
        path_patch = patches.PathPatch(_path, linewidth=1.0, facecolor = self.color, antialiased=True)
        ax.add_patch(path_patch)

class EquilateralTriangle(TriangleBase):
    # This constructor function will calculate the cartesian coordinates from polar
    def __init__(self, ax, xi, yi, sidelength, theta, color): 

        radius = sidelength * math.cos(math.radians(30))

        # Convert polar into cartesian here
        # Base class triangle is all cartesian to allow other triangle types
        # 
        # Diagram in progress 

        x0 = xi + (sidelength / 2.) * math.sin(theta)
        y0 = yi - (sidelength / 2.) * math.cos(theta)

        x1 = xi + radius * math.cos(theta)
        y1 = yi + radius * math.sin(theta)
        
        x2 = xi - (sidelength / 2.) * math.cos(math.pi/2. - theta) # Can be simplified?
        y2 = yi + (sidelength / 2.) * math.sin(math.pi/2. - theta) # Can be simplified?

        super().__init__(x0, y0, x1, y1, x2, y2, color)
    
    def Draw(self, ax):
        super().Draw(ax)



    # It would be helpful to have a constructor overload like in other languages
    # Not sure what level of support python has for parameter overloads, feedback welcome
    # 
    # def __init__(self, x0, y0, x1, y1, x2, y2):

