import tkinter as tk
from tkinter import messagebox
from typing import Dict, Tuple, List
import os
from .wells import Wells
from .gcodegenerator import GCodeGenerator
from .welzl import Welzl

#TODO Add File Seelction Dialogs
#TODO Make prettier

class Application:
    def __init__(self):
        """
        Initialize the UI class with default values and create the UI elements.
        """
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("Scratch me Baby!")  # Haha

        # Default values
        #TODO move values into a config file
        #TODO add a reset button
        #TODO add a save button
        #TODO add a load button
        self.offset_x_default = 33.95
        self.offset_y_default = -3.95
        self.offset_z_default = 54
        self.tip_offset_default = 1
        self.tip_diameter_default = 0.5
        self.number_default = ""
        self.distance_default = ""
        self.rect_scratch_default = False
        self.inner_radius_default = ""
        self.svg_file_default = "lab.svg"
        self.svg_scale_default = 1
        self.svg_overlap_default = 0.5
        self.speed_move_default = 300
        self.speed_scratch_default = 300
        self.auto_leveling_default = True
        self.multi_scratch_default = 1
        self.clean_file_default = "clean.txt"
        self.clean_before_default = False
        self.clean_after_default = False
        self.pause_before_clean_default = False
        self.well_file_default = "24well.txt"
        self.gcode_name_default = "scratch.gcode"

        # Advanced configuration parameters 
        self.move_height = 5  # height that the scratcher moves above the cells to travel between scratches
        self.clean_speed = 60

        # Create the outer canvas
        self.outer_canvas = tk.Canvas(self.root, width=800, height=500)
        self.outer_canvas.pack()

        # Create the inner canvas
        self.inner_canvas_size = (550, 345)
        self.inner_canvas = tk.Canvas(self.outer_canvas, width=self.inner_canvas_size[0], height=self.inner_canvas_size[1], bg="white")
        self.inner_canvas.place(x=50, y=140)
        self.wells = Wells(self.inner_canvas)

        # Create labels for the input fields
        self.create_labels()

        # Create input fields for offset
        self.create_offset_fields()

        # Create a dropdown menu for the pattern selection
        self.create_pattern_dropdown()

        # Create input fields for the pattern parameters
        self.create_pattern_fields()

        # Create input fields for speed
        self.create_speed_fields()

        # Create input field for scratching multiple times
        self.create_multi_scratch_field()

        # Create a bool checkbox for auto leveling
        self.create_auto_leveling_checkbox()

        # Create input field for well file path
        self.create_well_file_field()

        # Create input field for gcode name
        self.create_gcode_name_field()

        # Create input field for cleaning file
        self.create_clean_file_field()

        # Create bool checkboxes for cleaning options
        self.create_cleaning_options()

        # Create a button to generate the gcode
        self.create_generate_gcode_button()

    def run(self) -> None:
        """
        Run the Tkinter main loop.
        """
        self.root.mainloop()

    def create_labels(self) -> None:
        """
        Create labels for the input fields.
        """
        self.label_x = tk.Label(self.outer_canvas, text="X Offset")
        self.label_y = tk.Label(self.outer_canvas, text="Y Offset")
        self.label_z = tk.Label(self.outer_canvas, text="Z Offset")
        self.label_tip_offset = tk.Label(self.outer_canvas, text="Tip Offset")
        self.label_tip_diameter = tk.Label(self.outer_canvas, text="Tip Diameter")
        self.label_x.place(x=50, y=5)
        self.label_y.place(x=50, y=30)
        self.label_z.place(x=50, y=55)
        self.label_tip_offset.place(x=50, y=80)
        self.label_tip_diameter.place(x=50, y=105)

    def create_offset_fields(self) -> None:
        """
        Create input fields for offset values.
        """
        self.validate_input = self.outer_canvas.register(lambda input: self.validate_float(input, min_value=-99999999, max_value=99999999))
        self.offset_x_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.offset_y_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.offset_z_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.tip_offset_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.tip_diameter_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.offset_x_field.place(x=120, y=5)
        self.offset_y_field.place(x=120, y=30)
        self.offset_z_field.place(x=120, y=55)
        self.tip_offset_field.place(x=120, y=80)
        self.tip_diameter_field.place(x=120, y=105)
        self.offset_x_field.insert(0, self.offset_x_default)
        self.offset_y_field.insert(0, self.offset_y_default)
        self.offset_z_field.insert(0, self.offset_z_default)
        self.tip_offset_field.insert(0, self.tip_offset_default)
        self.tip_diameter_field.insert(0, self.tip_diameter_default)

    def create_pattern_dropdown(self) -> None:
        """
        Create a dropdown menu for the pattern selection.
        """
        self.label_pattern = tk.Label(self.outer_canvas, text="Pattern")
        self.label_pattern.place(x=200, y=5)
        self.pattern_value = tk.StringVar(self.outer_canvas)
        self.pattern_value.set("Mesh")  # default value
        self.pattern_value.trace_add("write", self.update_labels)  # Call update_labels whenever pattern changes
        self.pattern_dropdown = tk.OptionMenu(self.outer_canvas, self.pattern_value, "Mesh", "Circles", "SVG")
        self.pattern_dropdown.place(x=200, y=30)

    def create_pattern_fields(self) -> None:
        """
        Create input fields for the pattern parameters.
        """
        self.label_number = tk.Label(self.outer_canvas, text="Line Number")
        self.label_number.place(x=290, y=5)
        self.label_distance = tk.Label(self.outer_canvas, text="Line Distance")
        self.label_distance.place(x=290, y=30)
        self.label_rect_scratch = tk.Label(self.outer_canvas, text="Repeat with 90° flip")
        self.label_rect_scratch.place(x=290, y=55)
        self.label_inner_radius = tk.Label(self.outer_canvas, text="Inner Radius")
        self.label_inner_radius.place(x=290, y=55)
        self.label_inner_radius.place_forget()  # Hide the label

        self.validate_int = self.outer_canvas.register(lambda input: input.isdigit() or input == "")
        self.validate_scale = self.outer_canvas.register(lambda input: self.validate_float(input, min_value=0, max_value=1))

        self.number_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_int, '%P'))
        self.distance_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.rect_scratch_state = tk.BooleanVar()
        self.rect_scratch_checkbox = tk.Checkbutton(self.outer_canvas, var=self.rect_scratch_state)
        self.inner_radius_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.svg_file_field = tk.Entry(self.outer_canvas, width=10)
        self.svg_scale_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_scale, '%P'))
        self.svg_overlap_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_scale, '%P'))
        self.number_field.place(x=380, y=5)
        self.distance_field.place(x=380, y=30)
        self.rect_scratch_checkbox.place(x=425, y=55)
        self.inner_radius_field.place(x=380, y=55)
        self.inner_radius_field.place_forget()  # Hide the input field
        self.svg_file_field.place(x=380, y=5)
        self.svg_file_field.place_forget()  # Hide the input field
        self.svg_scale_field.place(x=380, y=30)
        self.svg_scale_field.place_forget()  # Hide the input field
        self.svg_overlap_field.place(x=380, y=55)
        self.svg_overlap_field.place_forget()  # Hide the input field
        self.number_field.insert(0, self.number_default)
        self.distance_field.insert(0, self.distance_default)
        self.rect_scratch_state.set(self.rect_scratch_default)
        self.inner_radius_field.insert(0, self.inner_radius_default)
        self.svg_file_field.insert(0, self.svg_file_default)
        self.svg_scale_field.insert(0, self.svg_scale_default)
        self.svg_overlap_field.insert(0, self.svg_overlap_default)

    def create_speed_fields(self) -> None:
        """
        Create input fields for speed values.
        """
        self.label_speed_move = tk.Label(self.outer_canvas, text="Travel Speed")
        self.label_speed_move.place(x=470, y=5)
        self.label_speed_scratch = tk.Label(self.outer_canvas, text="Scratch Speed")
        self.label_speed_scratch.place(x=470, y=30)

        self.speed_move_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.speed_scratch_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_input, '%P'))
        self.speed_move_field.place(x=550, y=5)
        self.speed_scratch_field.place(x=550, y=30)
        self.speed_move_field.insert(0, self.speed_move_default)
        self.speed_scratch_field.insert(0, self.speed_scratch_default)

    def create_multi_scratch_field(self) -> None:
        """
        Create input field for scratching multiple times.
        """
        self.label_multi_scratch = tk.Label(self.outer_canvas, text="Scratch Cycles")
        self.label_multi_scratch.place(x=470, y=55)
        self.multi_scratch_field = tk.Entry(self.outer_canvas, width=10, validate="key", validatecommand=(self.validate_int, '%P'))
        self.multi_scratch_field.place(x=550, y=55)
        self.multi_scratch_field.insert(0, self.multi_scratch_default)

    def create_auto_leveling_checkbox(self) -> None:
        """
        Create a bool checkbox for auto leveling.
        """
        self.auto_leveling_state = tk.BooleanVar()
        self.auto_leveling_state.set(self.auto_leveling_default)  # default value
        self.auto_leveling_checkbox = tk.Checkbutton(self.outer_canvas, text="Auto Leveling", var=self.auto_leveling_state)
        self.auto_leveling_checkbox.place(x=470, y=80)

    def create_well_file_field(self) -> None:
        """
        Create input field for well file path.
        """
        self.label_well_file = tk.Label(self.outer_canvas, text="Well File Path:")
        self.label_well_file.place(x=650, y=140)
        self.well_file_field = tk.Entry(self.outer_canvas, width=20)
        self.well_file_field.insert(0, self.well_file_default)  # default value
        self.well_file_field.place(x=650, y=165)
        self.load_well_file_button = tk.Button(self.outer_canvas, text="Load Well File", command=self.load_well_data)
        self.load_well_file_button.place(x=650, y=190)

    def load_well_data(self) -> None:
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        well_file_path = os.sep.join([current_directory, self.well_file_field.get()])
        self.wells.load_well_data(well_file_path)

    def create_gcode_name_field(self) -> None:
        """
        Create input field for gcode name.
        """
        self.label_gcode_name = tk.Label(self.outer_canvas, text="G-Code Name:")
        self.label_gcode_name.place(x=650, y=215)
        self.gcode_name_field = tk.Entry(self.outer_canvas, width=20)
        self.gcode_name_field.insert(0, self.gcode_name_default)  # default value
        self.gcode_name_field.place(x=650, y=240)

    def create_clean_file_field(self) -> None:
        """
        Create input field for cleaning file.
        """
        self.label_clean_file = tk.Label(self.outer_canvas, text="Clean File Path")
        self.label_clean_file.place(x=650, y=5)
        self.clean_file_field = tk.Entry(self.outer_canvas, width=20)
        self.clean_file_field.insert(0, self.clean_file_default)
        self.clean_file_field.place(x=650, y=35)

    def create_cleaning_options(self) -> None:
        """
        Create bool checkboxes for cleaning options.
        """
        self.clean_before_state = tk.BooleanVar()
        self.clean_before_state.set(self.clean_before_default)  # default value
        self.clean_before_checkbox = tk.Checkbutton(self.outer_canvas, text="Clean Before", var=self.clean_before_state)
        self.clean_before_checkbox.place(x=650, y=60)

        self.clean_after_state = tk.BooleanVar()
        self.clean_after_state.set(self.clean_after_default)  # default value
        self.clean_after_checkbox = tk.Checkbutton(self.outer_canvas, text="Clean After", var=self.clean_after_state)
        self.clean_after_checkbox.place(x=650, y=85)

        self.pause_before_clean_state = tk.BooleanVar()
        self.pause_before_clean_state.set(self.pause_before_clean_default)  # default value
        self.pause_before_clean_checkbox = tk.Checkbutton(self.outer_canvas, text="Pause Before Clean", var=self.pause_before_clean_state)
        self.pause_before_clean_checkbox.place(x=650, y=110)

    def create_generate_gcode_button(self) -> None:
        """
        Create a button to generate the gcode.
        """
        self.generate_gcode_button = tk.Button(self.outer_canvas, text="Generate G-Code", command=self.generate_gcode)
        self.generate_gcode_button.place(x=650, y=265)

    def validate_float(self, input, min_value=None, max_value=None):
        """
        Validate if the input is a float and within the specified range.
        """
        if input == "" or input == "-":  # Allow empty input and - sign
            return True
        try:
            value = float(input)
            # Check if the value is within the desired range
            if min_value is not None and value < min_value:
                return False
            if max_value is not None and value > max_value:
                return False
            return True
        except ValueError:
            return False

    def update_labels(self, *args) -> None:
        """
        Update labels based on the selected pattern.
        """
        selected_pattern = self.pattern_value.get()
        if selected_pattern == "Mesh":
            self.label_number.config(text="Line Number")
            self.label_distance.config(text="Line Distance")
            self.label_inner_radius.place_forget()  # Hide the label
            self.inner_radius_field.place_forget()  # Hide the input field
            self.svg_file_field.place_forget()  # Hide the input field
            self.svg_scale_field.place_forget()  # Hide the input field
            self.svg_overlap_field.place_forget()  # Hide the input field
            self.label_rect_scratch.place(x=290, y=55)  # Show the label
            self.rect_scratch_checkbox.place(x=425, y=55)  # Show the checkbox
        elif selected_pattern == "Circles":
            self.label_number.config(text="Circle Number")
            self.label_distance.config(text="Circle Distance")
            self.label_inner_radius.config(text="Inner Radius")
            self.label_inner_radius.place(x=290, y=55)  # Show the label
            self.inner_radius_field.place(x=380, y=55)  # Show the input field
            self.label_rect_scratch.place_forget()  # Hide the label
            self.svg_file_field.place_forget()  # Hide the input field
            self.svg_scale_field.place_forget()  # Hide the input field
            self.svg_overlap_field.place_forget()  # Hide the input field
        elif selected_pattern == "SVG":
            self.label_number.config(text="SVG File")
            self.label_distance.config(text="SVG Scale")
            self.label_inner_radius.config(text="Overlap")
            self.label_inner_radius.place(x=290, y=55)  # Show the label
            self.inner_radius_field.place_forget()
            self.label_rect_scratch.place_forget()  # Hide the label
            self.rect_scratch_checkbox.place_forget()  # Hide the checkbox
            self.svg_file_field.place(x=380, y=5)  # Show the input field
            self.svg_scale_field.place(x=380, y=30)  # Show the input field
            self.svg_overlap_field.place(x=380, y=55)  # Show the input field



    def generate_gcode(self) -> None:
        """
        Generate G-code based on the user inputs and save it to a file.
        """
        # Check if well data is loaded
        if not self.well_data:
            messagebox.showerror("Generate G-code", "Please load well file first!")
            return

        # Get the G-code file name
        gcode_name = self.gcode_name_field.get()
        if not gcode_name:
            messagebox.showerror("Generate G-code", "Please enter a G-code file name!")
            return

        # Get the pattern type
        pattern = self.pattern_value.get()

        # Get the offset values
        offset_x = float(self.offset_x_field.get())
        offset_y = float(self.offset_y_field.get())
        offset_z = float(self.offset_z_field.get())

        # Get the skipped wells (assuming you have a way to get this list)
        skipped_wells = []  # Replace with actual logic to get skipped wells

        # Initialize the GCodeGenerator
        gcode_generator = GCodeGenerator()

        # Open the G-code file for writing
        with open(gcode_name, 'w') as gcode_file:
            # Iterate through the wells
            for number_y in range(int(self.well_data['number_y'])):
                for number_x in range(int(self.well_data['number_x'])):
                    well_number = int(number_y * self.well_data['number_x'] + number_x + 1)
                    well_name = chr(64 + int(self.well_data["number_y"]) - number_y) + str(number_x + 1)
                    if well_number in skipped_wells:
                        print(f"Skipped well {well_number:.0f}, Name: {well_name}")
                        continue

                    # Calculate center points for the well
                    center_x = self.well_data['distance_x'] + number_x * (self.well_data['diameter'] + self.well_data['distance_well']) + self.well_data['diameter'] / 2 + offset_x
                    center_y = self.well_data['distance_y'] + number_y * (self.well_data['diameter'] + self.well_data['distance_well']) + self.well_data['diameter'] / 2 + offset_y
                    depth = offset_z - self.well_data['depth']

                    # Move above center of well and into it
                    gcode_file.write(f";GCODE for well number {well_number}, Name: {well_name}\n")
                    gcode_file.write(f"G0 X{center_x:.2f} Y{center_y:.2f} Z{offset_z + self.move_height:.2f}\n")
                    gcode_file.write(f"G0 Z{depth + self.move_height:.2f}\n")

                    # Generate G-code for the selected pattern
                    if pattern == "Mesh":
                        gcode_lines = gcode_generator.generate_gcode('mesh', {
                            'center_x': center_x,
                            'center_y': center_y,
                            'depth': depth,
                            'spacing': float(self.distance_field.get()),
                            'feed_rate': float(self.speed_scratch_field.get())
                        })
                    elif pattern == "Circles":
                        gcode_lines = gcode_generator.generate_gcode('circle', {
                            'center_x': center_x,
                            'center_y': center_y,
                            'radius': float(self.inner_radius_field.get()),
                            'feed_rate': float(self.speed_scratch_field.get())
                        })
                    elif pattern == "SVG":
                        gcode_lines = gcode_generator.generate_gcode('svg', {
                            'svg_path': self.svg_file_field.get(),
                            'scale': float(self.svg_scale_field.get()),
                            'feed_rate': float(self.speed_scratch_field.get())
                        })
                    else:
                        messagebox.showerror("Generate G-code", f"Unknown pattern: {pattern}")
                        return

                    # Write the generated G-code lines to the file
                    for line in gcode_lines:
                        gcode_file.write(line + '\n')

        messagebox.showinfo("Generate G-code", f"G-code generated and saved to {gcode_name}")   