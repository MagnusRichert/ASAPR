
from tkinter import messagebox


class Cleaner:
    def __init__(self):
        pass
    
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