import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
from plotables import Plotables
from circlegrid import CircleGrid
from welzl import Welzl

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

    def generate_cleaning_program(self):
        """
        Load the cleaning data from a *.txt file and return gcode.
        """
        try:
            clean_data = {}
            clean_gcode = ";cleaning gcode\n"
            container = 0
            pause = self.pause_before_clean_state.get()
            # Extract data from file and generate gcode
            with open(self.clean_file_field.get(), "r") as file:
                for line in file:
                    if line[0] == "/":
                        container += 1
                        clean_gcode += f";cleaning container {container}\n"
                        clean_gcode += f"G0 Z{clean_data['Z'] + 10:.2f}\n"
                        clean_gcode += f"G0 X{clean_data['X']:.2f} Y{clean_data['Y']:.2f}\n"
                        if pause:
                            clean_gcode += "M0 \"Position cleaning container and press to continue\"\n"
                        clean_gcode += f"G0 X{clean_data['X']-clean_data['Radius']:.2f} Z{clean_data['Z']-clean_data['Depth']:.2f}\n"
                        for N in range(int(clean_data['Number'])):
                            clean_gcode += f"G2 I{clean_data['Radius']:.2f} F{self.clean_speed:.0f}\n"                
                        clean_data.clear()
                    else:
                        key, value = line.strip().split(": ")
                        clean_data[key] = float(value)
            return clean_gcode
        
        except FileNotFoundError:
            messagebox.showerror("Clean Program Error", "Cleaning program file not found.")
        except Exception as e:
            messagebox.showerror("Clean Program Error", str(e) + "Please check your clean.txt file for correctnes.")
            
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



    
