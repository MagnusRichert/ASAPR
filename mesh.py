import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
from plotables import Plotables
from circlegrid import CircleGrid
from welzl import Welzl


class Mesh(Plotables):
    def __init__(self):
        super().__init__()
        
    def generate_gcode(self, center_x, center_y, depth):
        gcode_name = self.gcode_name_field.get()
        tip_offset = float(self.tip_offset_field.get())           
        speed_move = float(self.speed_move_field.get())
        speed_scratch = float(self.speed_scratch_field.get())
        multi_scratch = int(self.multi_scratch_field.get())
        mesh_line_number = int(self.number_field.get())
        mesh_line_distance = float(self.distance_field.get())
        rect_scratch = self.rect_scratch_state.get()
        if mesh_line_distance * (mesh_line_number - 1) + tip_offset * 2 >= self.well_data['diameter']:
            print("The mesh is not possible with current settings of line number and distance!")
            messagebox.showerror("Pattern", "Mesh not possible with selected line number and distance!")
            return
        
        with open(f"{gcode_name}", 'w') as gcode:
            y_coordinates = [center_y + (i - mesh_line_number / 2) * mesh_line_distance + mesh_line_distance / 2 for i in range(mesh_line_number)]
            for y_position in y_coordinates:
                start_x, end_x = self.line_through_x(center_x, self.well_data['diameter'], tip_offset, y_offset=center_y - y_position)
                gcode.writelines(f"G0 X{start_x:.2f} Y{y_position:.2f}\n")
                gcode.writelines(f"G0 Z{depth:.2f}\n")
                gcode.writelines(f"G0 X{end_x:.2f} F{speed_scratch:.0f}\n")
                for ii in range(multi_scratch - 1):
                    if ii % 2 == 0:
                        gcode.writelines(f"G0 X{start_x:.2f}\n")
                    else:
                        gcode.writelines(f"G0 X{end_x:.2f}\n")
                gcode.writelines(f"G0 Z{depth + self.move_height:.2f} F{speed_move:.0f}\n")
            if rect_scratch:
                x_coordinates = [center_x + (i - mesh_line_number / 2) * mesh_line_distance + mesh_line_distance / 2 for i in range(mesh_line_number)]
                for x_position in x_coordinates:
                    start_y, end_y = self.line_through_y(center_y, self.well_data['diameter'], tip_offset, x_offset=center_x - x_position)
                    gcode.writelines(f"G0 X{x_position:.2f} Y{start_y:.2f}\n")
                    gcode.writelines(f"G0 Z{depth:.2f}\n")
                    gcode.writelines(f"G0 Y{end_y:.2f} F{speed_scratch:.0f}\n")
                    for ii in range(multi_scratch - 1):
                        if ii % 2 == 0:
                            gcode.writelines(f"G0 Y{start_y:.2f}\n")
                        else:
                            gcode.writelines(f"G0 Y{end_y:.2f}\n")
                    gcode.writelines(f"G0 Z{depth + self.move_height:.2f} F{speed_move:.0f}\n")