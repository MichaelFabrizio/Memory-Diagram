import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import math as math

import drawing.arrows.arrows as arrows
import drawing.shapes.triangles as triangles
import drawing.curves.curves as curves

class Drawing:
    def __init__(self, diagram_width = 20.0, diagram_height = 4.0, show_axes = False, show_axes_numbers = False,
                 left_padding = 0.1, right_padding = 0.1, lower_padding = 0.1, upper_padding = 0.1,
                 interior_x_padding = 0.1, interior_y_padding = 1.0,
                 horizontal_elements = 0, vertical_elements = 0,
                 element_width = 1.0, element_height = 1.0,
                 axes_auto = True, axes_width = 1.0, axes_height = 1.0):

        # The user may specify their print size, via diagram_width & diagram_height parameters
        # The diagram and axes calculations are done automatically,
        #
        # The computer prioritizes the mathematical requirement:
        # 
        # Aspect Ratio = axes_width / axes_height
        #
        # So the diagram may be scaled to match the aspect ratio. This is the default, I suppose it could be a setting/parameter.
        self.diagram_width = diagram_width
        self.diagram_height = diagram_height

        # The 'exterior paddings', which add layering around the 'functional diagram' itself.
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.lower_padding = lower_padding
        self.upper_padding = upper_padding

        # The 'interior paddings', which is the spacing between elements
        self.interior_x_padding = interior_x_padding
        self.interior_y_padding = interior_y_padding

        # The diagram is built as a table-like system:
        # IE: There are a set number of horizontal and vertical elements.
        # This allows us to calculate the required dimensions (axes_width, axes_height), below.
        self.horizontal_elements = horizontal_elements
        self.vertical_elements = vertical_elements

        # Each element is either a square or rectangle, with some spacing in-between.
        self.element_width = element_width
        self.element_height = element_height

        if axes_auto:
            # The actual plot dimensions required, ie: the XY coordinate ranges that all values are based on.
            self.axes_width = self.left_padding + self.right_padding + float(self.horizontal_elements) * (self.interior_x_padding + self.element_width) - self.interior_x_padding
            self.axes_height = self.lower_padding + self.upper_padding + float(self.vertical_elements) * (self.interior_y_padding + self.element_height) - self.interior_y_padding
        else:
            self.axes_width = axes_width
            self.axes_height = axes_height

        # These are the origin point coordinates that all drawing coordinates are based on.
        self.x_offset = self.left_padding
        self.y_offset = self.axes_height - self.upper_padding - self.element_height

        # BEGIN: diagram_width / diagram_height scaling logic
        #
        # LOGIC: Adjusts diagram_width and diagram_height to match the required
        # axes_aspect_ratio. Otherwise there will be skewed dimensions.
        #
        # ====================
        self.axes_aspect_ratio = self.axes_width / self.axes_height

        # Width-based major axis
        if self.axes_aspect_ratio > 1.0:
            self.diagram_height = self.diagram_width / self.axes_aspect_ratio
        # Height-based major axis
        else:
            self.diagram_width = self.diagram_height * self.axes_aspect_ratio
        # ====================
        # END: diagram_width / diagram_height scaling logic

        self.fig, self.ax = plt.subplots(figsize=(self.diagram_width, self.diagram_height))
        
        self.ax.set_xlim(0, self.axes_width)
        self.ax.set_ylim(0, self.axes_height)

        # The default values
        # self.layout = Layout(self.axes_width, self.axes_height)

        if show_axes:
            if show_axes_numbers:
                return
            else:
                # The graph square is included without numbers
                self.ax.set_xticks([])
                self.ax.set_yticks([])
        else:
            self.ax.axis('off')

    def Draw_Vertical_Arrow_Anchored(self, i, spacer, height, arrowstyle = '<->', position = 'below'):
        if position == 'below':
            x0 = self.x_offset + i * (self.element_width + self.interior_x_padding) + self.element_width / 2.
            y0 = self.y_offset - spacer - height
            yf = self.y_offset - spacer
            self.Draw_Arrow(x0, y0, x0, yf, arrowstyle = arrowstyle)

        if position == 'above':
            x0 = self.x_offset + i * (self.element_width + self.interior_x_padding) + self.element_width / 2.
            y0 = self.y_offset + self.element_height + spacer + height
            yf = self.y_offset + self.element_height + spacer
            self.Draw_Arrow(x0, y0, x0, yf, arrowstyle = arrowstyle)

    def Draw_Arrow(self, x0, y0, xf, yf, arrowstyle = '<->'):
        arrow = arrows.Arrow(x0, y0, xf, yf, arrowstyle = arrowstyle)
        arrow.Draw(self.ax)

    def Draw_Diagonal_Arrow_Anchored(self, i0, iF, y0, arrowstyle = '<->'):
        x0 = self.x_offset + i0 * (self.element_width + self.interior_x_padding) + self.element_width / 2.
        y0 = self.y_offset - self. element_height + y0
        
        xf = self.x_offset + iF * (self.element_width + self.interior_x_padding) + self.element_width / 2.
        yf = self.y_offset

        self.Draw_Diagonal_Arrow(x0, y0, xf, yf, arrowstyle = arrowstyle)

    def Draw_Diagonal_Arrow(self, x0, y0, xf, yf, arrowstyle = '<->'):
        arrow = arrows.DiagonalArrow(x0, y0, xf, yf, arrowstyle = arrowstyle)
        arrow.Draw(self.ax)

    def Draw_Reconnecting_Arrow_Anchored(self, i0, iF, position = 'above', arrowstyle = '<->'):
        if position == 'above':
            theta = - math.pi /2.
        else:
            pass

        x0 = self.x_offset + i0 * (self.element_width + self.interior_x_padding) + self.element_width / 2.
        y0 =  self.y_offset + self.element_height       
        xf = self.x_offset + iF * (self.element_width + self.interior_x_padding) + self.element_width / 2.

        stride = abs(xf - x0)
        self.Draw_Reconnecting_Arrow(x0, y0, stride, theta = theta, arrowstyle = arrowstyle)

    def Draw_Reconnecting_Arrow(self, x0, y0, stride, theta = 0.0, height = 1.0, arrowstyle = '<->'):
        arrow = arrows.ReconnectingArrow(x0, y0, stride, theta = theta, height = height, arrowstyle = arrowstyle)
        arrow.Draw(self.ax)

    # TODO: Update offsets
    def Draw_Corner_Arrow(self, x, y, radius, theta):
        arrow = arrows.CornerArrow(x, self.offset + y, radius, theta)
        arrow.Draw(self.ax)

    def Draw_Line(self, x0, y0, xf, yf):
        line = curves.Line(x0, y0, xf, yf)
        line.Draw(self.ax)

    def Draw_Centered_X_Anchored(self, i, color='red', inner_length = 0.2):
        x_center = self.left_padding + i * (self.element_width + self.interior_x_padding) + self.element_width / 2.
        y_center = self.y_offset + self.element_height / 2.
        length = self.element_width

        self.Draw_Centered_X(x_center, y_center, length)

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

    def Draw_Equilateral_Triangle(self, x0, y0, sidelength, theta, color = 'white'):
        t = triangles.EquilateralTriangle(x0, y0, sidelength, theta, color)
        t.Draw(self.ax)

    def Draw_Underline_Bar_Anchored(self, index_initial, index_final, height, spacer, linewidth = 0.1):
        if index_initial >= index_final:
            raise AssertionError("index_initial >= index_final")

        x0 = self.x_offset + index_initial * (self.element_width + self.interior_x_padding)
        xf = self.x_offset + index_final * (self.element_width + self.interior_x_padding) - linewidth
        y0 = self.y_offset - height - spacer
        yf = self.y_offset

        self.Draw_Underline_Bar_Floating(x0, y0, xf - x0, height, linewidth)
    
    
    def Draw_Underline_Bar_Floating(self, x0, y0, stride, height, linewidth = 0.1, color='red'):
        # Secondary calculations
        if height < linewidth:
            raise AssertionError("height < linewidth")
        elif stride < linewidth:
            raise AssertionError("stride < linewidth")

        height_lift = (height - linewidth) / 2.

        v0x = x0
        v0y = y0
        v1x = x0 + linewidth
        v1y = y0
        v2x = x0 + linewidth
        v2y = y0 + height_lift
        v3x = x0 + stride - linewidth
        v3y = y0 + height_lift
        v4x =  x0 + stride - linewidth
        v4y = y0
        v5x = x0 + stride
        v5y = y0
        v6x = x0 + stride
        v6y = y0 + height
        v7x = x0 + stride - linewidth
        v7y = y0 + height
        v8x = x0 + stride - linewidth
        v8y = y0 + height - height_lift
        v9x = x0 + linewidth
        v9y = y0 + height - height_lift
        v10x = x0 + linewidth
        v10y = y0 + height
        v11x = x0
        v11y = y0 + height
       
        vertices = np.array([(v0x, v0y), (v1x, v1y), (v2x, v2y), (v3x, v3y), (v4x, v4y), (v5x, v5y),
                             (v6x, v6y), (v7x, v7y), (v8x, v8y), (v9x, v9y), (v10x, v10y), (v11x, v11y), (v0x, v0y)])
        codes = np.array([1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        
        _path = path.Path(vertices, codes)

        path_patch = patches.PathPatch(_path, linewidth=1.5, facecolor = color, fill=True, antialiased=True)
        self.ax.add_patch(path_patch)
    
    def Draw_Square_With_Text(self, text, i, y0, color):
        x_coordinate = self.x_offset + i * (self.element_width + self.interior_x_padding)
        x_coordinate_text = x_coordinate + self.element_width/2.
        y_coordinate_text = self.y_offset + self.element_height/2. + y0

        rect = patches.Rectangle((x_coordinate, self.y_offset + y0), self.element_width, self.element_height, facecolor=color, edgecolor='black', linewidth=1.5)
        self.ax.add_patch(rect)
        self.ax.text(x_coordinate_text, y_coordinate_text, str(text), ha='center', va='center', fontweight='bold')

    def Draw_Text(self):
        pass
        
    # Update offsets
    def Draw_Array(self, array, x0, y0, padding, length, color):
        for i, value in enumerate(array):
            rect = patches.Rectangle((x0 + i * (length + padding), self.offset + y0), length, length, facecolor=color, edgecolor='black', linewidth=1.5)
            self.ax.add_patch(rect)
            self.ax.text(x0 + length/2. + i * (length + padding), self.offset + y0 + length/2., str(value), ha='center', va='center', fontweight='bold')

    def Step_Array_Down(self, offset_amount=0.0):
        self.y_offset = self.y_offset - offset_amount
        self.Recalculate_Axes_And_Diagram()

    # MatPlotLib related functions
    def Show(self):
        plt.show()

    def Save(self, name = 'data_structure.png'):
        plt.savefig(str(name), bbox_inches='tight', pad_inches=0.1)

    def Get_Element_Midpoint_By_Index(self, index):
        return self.x_offset + index * (self.element_width + self.interior_x_padding)

    # Calculates the required aspect ratio 2D
    # Always prioritizes mathematical space over display space
    def Recalculate_Axes_And_Diagram(self):
        self.axes_aspect_ratio = self.axes_width / self.axes_height

        # Width-based major axis
        if self.axes_aspect_ratio > 1.0:
            self.diagram_height = self.diagram_width / self.axes_aspect_ratio
        # Height-based major axis
        else:
            self.diagram_width = self.diagram_height * self.axes_aspect_ratio
        
        self.ax.set_xlim(0, self.axes_width)
        self.ax.set_ylim(0, self.axes_height)

        self.fig.set_figwidth(self.diagram_width)
        self.fig.set_figheight(self.diagram_height)

#        self.layout.Update_Axes(self.axes_width, self.axes_height)
   
    # This function allows the user to ask for extra space vertically
    def Scale_Axes_Height_By_Value(self, value):
        self.axes_height += value
        self.y_offset += value
        self.Recalculate_Axes_And_Diagram()


    # AXES: 

    def Get_Axes(self):
        return self.ax

    def Get_Figure(self):
        return self.fig

    def Get_Y_Offset(self):
        return self.y_offset
