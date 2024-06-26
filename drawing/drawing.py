import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

import arrows.arrows as arrows

class Drawing:
    def __init__(self, diagram_width = 20.0, diagram_height = 4.0, show_axes = False):
        self.offset = 0.0

        self.fig, self.ax = plt.subplots(figsize=(diagram_width, diagram_height))
        self.ax.set_aspect('equal')

        if show_axes:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        else:
            self.ax.axis('off')



    def Draw_Vertical_Arrow(self, x0, y0, xf, yf, color, arrow_side_length = 0.2, dashed = False):
        arrow = arrows.VerticalArrow(x0, self.offset + y0, xf, self.offset + yf, linestyle = '-')
        arrow.Draw(self.ax)

    def Draw_Diagonal_Arrow(self, x0, y0, xf, yf, interior_padding, color, arrow_side_length = 0.2, dashed = False):
        arrow = arrows.DiagonalArrow(x0, self.offset + y0, xf, self.offset + yf, linestyle = '-')
        arrow.Draw(self.ax)

    def Draw_Reconnecting_Arrow(self, x_offset, y_offset, stride, cardinality = 'north', height = 1.0, linestyle = '-', arrowstyle = '<->'):
        arrow = arrows.ReconnectingArrow(x_offset, self.offset + y_offset, stride, cardinality, height = 1.0, linestyle = '-', arrowstyle = '<->')
        arrow.Draw(self.ax)

    def Draw_Corner_Arrow(self, x, y, radius, theta):
        arrow = arrows.CornerArrow(x, self.offset + y, radius, theta)
        arrow.Draw(self.ax)

    def Draw_Centered_X(self, x_center, y_center, length, color='red', inner_length = 0.2):
        half_length = length/2.
        length_diff = half_length - inner_length

        # V1 & V11 are defined relative to V0
        v0x = x_center + inner_length
        v0y = y_center
        v1x = v0x + length_diff
        v1y = v0y + length_diff
        v11x = v0x + length_diff
        v11y = v0y - length_diff

        # V2 & V4 are defined relative to V3
        v3x = x_center
        v3y = y_center + inner_length
        v2x = v3x + length_diff
        v2y = v3y + length_diff
        v4x = v3x - length_diff
        v4y = v3y + length_diff

        # V5 & V7 are defined relative to V6
        v6x = x_center - inner_length
        v6y = y_center
        v5x = v6x - length_diff
        v5y = v6y + length_diff
        v7x = v6x - length_diff
        v7y = v6y - length_diff

        # V8 & V10 are defined relative to V9
        v9x = x_center
        v9y = y_center - inner_length
        v8x = v9x - length_diff
        v8y = v9y - length_diff
        v10x = v9x + length_diff
        v10y = v9y - length_diff
        
        # Define line segments in MatPlotLib
        vertices = np.array([(v0x, v0y), (v1x, v1y), (v2x, v2y), (v3x, v3y), (v4x, v4y), (v5x, v5y),
                             (v6x, v6y), (v7x, v7y), (v8x, v8y), (v9x, v9y), (v10x, v10y), (v11x, v11y), (v0x, v0y)])
        codes = np.array([1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        _path = path.Path(vertices, codes)

        path_patch = patches.PathPatch(_path, linewidth=1.5, facecolor = color, fill=True, antialiased=True)
        self.ax.add_patch(path_patch)

    def Draw_Square_With_Text(self, text, x0, y0, length, color):
        rect = patches.Rectangle((x0, self.offset + y0), length, length, facecolor=color, edgecolor='black', linewidth=1.5)
        self.ax.add_patch(rect)
        self.ax.text(x0 + length/2., self.offset + y0 + length/2., str(text), ha='center', va='center', fontweight='bold')
        
    def Draw_Array(self, array, x0, y0, padding, length, color):
        for i, value in enumerate(array):
            rect = patches.Rectangle((x0 + i * (length + padding), self.offset + y0), length, length, facecolor=color, edgecolor='black', linewidth=1.5)
            self.ax.add_patch(rect)
            self.ax.text(x0 + length/2. + i * (length + padding), self.offset + y0 + length/2., str(value), ha='center', va='center', fontweight='bold')

    def Step_Array_Down(self, offset_amount=0.0):
        self.offset = self.offset - offset_amount

    def Set_Axes_Size(self, axes_width, axes_height):
        self.ax.set_xlim(0, axes_width)
        self.ax.set_ylim(0, axes_height)

    def Show(self):
        plt.show()

    def Save(self, name = 'data_structure.png'):
        plt.savefig(name, bbox_inches='tight', pad_inches=0.1)
