import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
from plotables import Plotables
from circlegrid import CircleGrid
from welzl import Welzl


class Circles(Plotables):
    def __init__(self):
        super().__init__()

    def generate_gcode(self, center_x, center_y, depth):
        gcode_name = self.gcode_name_field.get()
        tip_offset = float(self.tip_offset_field.get())            
        speed_move = float(self.speed_move_field.get())
        speed_scratch = float(self.speed_scratch_field.get())
        multi_scratch = int(self.multi_scratch_field.get())
        circle_number = int(self.number_field.get())
        circle_distance = float(self.distance_field.get())
        circle_inner_radius = float(self.inner_radius_field.get())
        if circle_inner_radius + (circle_number - 1) * circle_distance + tip_offset >= self.well_data['diameter'] / 2:
            print("The circles are not possible with current settings of line number and distance!")
            messagebox.showerror("Pattern", "Circles not possible with selected line number and distance!")
            return False
        with open(f"{gcode_name}", 'w') as gcode:
            radii = [circle_inner_radius + i * circle_distance for i in range(circle_number)]
            for radius in radii:
                gcode.writelines(f"G0 X{center_x - radius:.2f}\n")
                gcode.writelines(f"G0 Z{depth:.2f}\n")
                gcode.writelines(f"G2 I{radius:.2f} F{speed_scratch:.0f}\n")
                for _ in range(multi_scratch - 1):
                    gcode.writelines(f"G2 I{radius:.2f}\n")
                gcode.writelines(f"G0 Z{depth + self.move_height:.2f} F{speed_move:.0f}\n")
                return True

       