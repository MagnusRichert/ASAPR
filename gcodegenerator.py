import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
from wells import Wells
from welzl import Welzl
#TODO one functions generates GCODE based on list of lines and circles (maybe bezier curves)
#TODO one function generates GCODE for each well (previous function plus well data)
#TODO All GCODE related activities should be here and not in the other functions (then only one class needs to be modified for different output format)
class GCodeGenerator:
    def __init__(self):
        self.filepath = "scratch.gcode"
        self.gcode = ""

        self.offset_x = 0.0
        self.offset_y = 0.0
        self.offset_z = 0.0
        self.tip_offset = 0.0
        self.tip_diameter = 0.0

        self.speed_move = 300
        self.speed_scratch = 300

    
            
    def generate_gcode(self):
        """
        Generate the G-Code based on the input parameters and selected pattern.
        """
        try:
            print(self.well_data)
            # Get variables from input fields
            gcode_name = self.gcode_name_field.get()
            offset_x = float(self.offset_x_field.get())
            offset_y = float(self.offset_y_field.get())
            offset_z = float(self.offset_z_field.get())
            pattern = self.pattern_value.get()
            try:
                skipped_wells = self.well_grid.get_selected_circles()
            except:
                messagebox.showerror("Generate gcode", "Please load well file first!")
                return
            
            with open(f"{gcode_name}", 'w') as gcode:
                # Iterate through short side of well
                for number_y in range(int(self.well_data['number_y'])):
                    # Iterate through long side of well
                    for number_x in range(int(self.well_data['number_x'])):
                        well_number = int(number_y * self.well_data['number_x'] + number_x + 1)
                        well_name = chr(64 + int(self.well_data["number_y"]) - number_y) + str(number_x + 1)
                        if well_number in skipped_wells:
                            print(f"Skipped well {well_number:.0f}, Name: {well_name}")
                            continue

                        # Calculate center points for well
                        center_x = self.well_data['distance_x'] + number_x * (self.well_data['diameter'] + self.well_data['distance_well']) + self.well_data['diameter'] / 2 + offset_x
                        center_y = self.well_data['distance_y'] + number_y * (self.well_data['diameter'] + self.well_data['distance_well']) + self.well_data['diameter'] / 2 + offset_y
                        depth = offset_z - self.well_data['depth']

                        # Move above center of well and into it
                        gcode.writelines(f";GCODE for well number {well_number}, Name: {well_name}\n")
                        gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z{offset_z + self.move_height:.2f}\n")
                        gcode.writelines(f"G0 Z{depth + self.move_height:.2f}\n")

                        # Add gcode according to pattern
                        if pattern == "Mesh":
                            self.generate_gcode_mesh(center_x, center_y, depth)
                        elif pattern == "Circles":
                            if not self.generate_gcode_circles(center_x, center_y, depth):
                                return
                                                   
                        elif pattern == "SVG":
                            self.generate_gcode_svg(center_x, center_y, depth)
                        else:
                            print("Your specified pattern does not exist")
                            messagebox.showerror("Pattern", f"Pattern {pattern} doesn't exist!")
                            exit(1)

                        # Move above well to go to next one
                        gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z{offset_z + self.move_height:.2f}\n\n")

                # Clean if specified
                if self.clean_after_state.get():
                    gcode.writelines(self.generate_cleaning_program())

                # Return to start and close
                gcode.writelines(f"G0 X{offset_x:.2f} Y{offset_y:.2f} Z{offset_z + 30:.2f}\n")
                gcode.writelines("M0 \"Please remove the tip to end print :)\"\n")
                gcode.writelines("M30\n")

            print(f"Successfully generated {gcode_name}!")
            messagebox.showinfo("Generate gcode", f"Successfully generated {gcode_name}!")
        except FileNotFoundError as e:
            print(f"Error: File not found - {str(e)}")
            messagebox.showerror("Generate gcode", f"Error: File not found - {str(e)}")
        except PermissionError as e:
            print(f"Error: Permission denied - {str(e)}")
            messagebox.showerror("Generate gcode", f"Error: Permission denied - {str(e)}")
        except ValueError as e:
            print(f"Error: Invalid value - {str(e)}")
            messagebox.showerror("Generate gcode", f"Error: Check your inputs and make sure you have entered numbers everywhere.")
        except Exception as e:
            print(f"Error while generating gcode: {str(e)}")
            messagebox.showerror("Generate gcode", f"Error while generating gcode: {str(e)}")

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


from typing import List, Tuple

class GCodeGenerator:
    def __init__(self):
        self.gcode_lines: List[str] = []

    def generate_gcode(self, pattern: str, parameters: dict) -> List[str]:
        """
        Generate G-code based on the specified pattern and parameters.

        Args:
            pattern (str): The pattern type (e.g., 'circle', 'mesh', 'svg').
            parameters (dict): A dictionary of parameters required for the pattern.

        Returns:
            List[str]: A list of G-code lines.
        """
        self.gcode_lines = ["G21 ; Set units to millimeters", "G90 ; Absolute positioning"]

        if pattern == 'circle':
            self.generate_circle_gcode(parameters)
        elif pattern == 'mesh':
            self.generate_mesh_gcode(parameters)
        elif pattern == 'svg':
            self.generate_svg_gcode(parameters)
        else:
            raise ValueError(f"Unknown pattern: {pattern}")

        self.gcode_lines.append("M2 ; End of program")
        return self.gcode_lines

    def generate_circle_gcode(self, parameters: dict) -> None:
        """
        Generate G-code for a circle pattern.

        Args:
            parameters (dict): A dictionary of parameters for the circle pattern.
        """
        center_x = parameters.get('center_x', 0)
        center_y = parameters.get('center_y', 0)
        radius = parameters.get('radius', 10)
        feed_rate = parameters.get('feed_rate', 1000)

        self.gcode_lines.append(f"G0 X{center_x} Y{center_y} ; Move to center")
        self.gcode_lines.append(f"G2 I{radius} J0 F{feed_rate} ; Draw circle")

    def generate_mesh_gcode(self, parameters: dict) -> None:
        """
        Generate G-code for a mesh pattern.

        Args:
            parameters (dict): A dictionary of parameters for the mesh pattern.
        """
        start_x = parameters.get('start_x', 0)
        start_y = parameters.get('start_y', 0)
        end_x = parameters.get('end_x', 100)
        end_y = parameters.get('end_y', 100)
        spacing = parameters.get('spacing', 10)
        feed_rate = parameters.get('feed_rate', 1000)

        for x in range(start_x, end_x + 1, spacing):
            self.gcode_lines.append(f"G0 X{x} Y{start_y} ; Move to start of line")
            self.gcode_lines.append(f"G1 Y{end_y} F{feed_rate} ; Draw vertical line")

        for y in range(start_y, end_y + 1, spacing):
            self.gcode_lines.append(f"G0 X{start_x} Y{y} ; Move to start of line")
            self.gcode_lines.append(f"G1 X{end_x} F{feed_rate} ; Draw horizontal line")

    def generate_svg_gcode(self, parameters: dict) -> None:
        """
        Generate G-code for an SVG pattern.

        Args:
            parameters (dict): A dictionary of parameters for the SVG pattern.
        """
        svg_path = parameters.get('svg_path', '')
        scale = parameters.get('scale', 1.0)
        feed_rate = parameters.get('feed_rate', 1000)

        # Placeholder for SVG processing logic
        # This would involve parsing the SVG file and converting it to G-code
        self.gcode_lines.append(f"; SVG file: {svg_path}")
        self.gcode_lines.append(f"; Scale: {scale}")
        self.gcode_lines.append(f"; Feed rate: {feed_rate}")

        # Example of adding G-code for SVG path (this would be more complex in reality)
        self.gcode_lines.append("G0 X0 Y0 ; Move to start of SVG path")
        self.gcode_lines.append("G1 X10 Y10 F1000 ; Example line from SVG path")

    def save_gcode_to_file(self, filename: str) -> None:
        """
        Save the generated G-code to a file.

        Args:
            filename (str): The name of the file to save the G-code to.
        """
        with open(filename, 'w') as file:
            for line in self.gcode_lines:
                file.write(line + '\n')    



    
