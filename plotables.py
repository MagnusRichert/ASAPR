
import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
from plotables import Plotables
from circlegrid import CircleGrid
from welzl import Welzl

class Plotables:
    def __init__(self):
        pass

    def generate_gcode(self):
        """Defined by subclasses"""
        pass

        def generate_gcode_initial(self):
        # Get variables from input fields
        gcode_name = self.gcode_name_field.get()
        offset_x = float(self.offset_x_field.get())
        offset_y = float(self.offset_y_field.get())
        offset_z = float(self.offset_z_field.get())
        speed_move = float(self.speed_move_field.get())
        auto_leveling = self.auto_leveling_state.get()
         # Open gcode file
        with open(f"{gcode_name}", 'w') as gcode:
            # Add beginning gcode
            gcode.writelines("G21\n")  # Set to mm
            gcode.writelines("G28\n")  # Home printhead
            gcode.writelines(f"G0 X{offset_x:.2f} Y{offset_y:.2f} Z{offset_z:.2f}\n")  # Move to offset location
            gcode.writelines(f"F{speed_move:.0f}\n\n")  # Set movement speed
            if auto_leveling:
                gcode.writelines("M420 S1\n")

            # Move nozzle to insert tip
            gcode.writelines(f"G0 Z{offset_z + 30:.2f}\n")
            gcode.writelines("M0 \"Please insert tip to start scratching :)\"\n\n")

            # Clean if specified
            if self.clean_before_state.get():
                gcode.writelines(self.generate_cleaning_program())