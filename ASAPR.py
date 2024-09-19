import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line
import random
import math
from typing import List, Tuple
import sys
import os

### FUNCTIONS AND VARIABLES###
# Default values
offset_x_default = 33.95
offset_y_default = -3.95
offset_z_default = 54
tip_offset_default = 1
number_default = ""
distance_default = ""
rect_scratch_default = False
inner_radius_default = ""
svg_file_default = "lab.svg"
svg_scale_default = 1
speed_move_default = 300
speed_scratch_default = 300
auto_leveling_default = True
multi_scratch_default = 1
clean_file_default = "clean.txt"
clean_before_default = False
clean_after_default = False
pause_before_clean_default = False
well_file_default = "24well.txt"
gcode_name_default = "scratch.gcode"

# Global Variables and advanced configuration parameters
well_data = {}
well_grid = None
move_height = 5 #height that the scratcher moves above the cells to travel between scratches
clean_speed = 60
resolution = 20 #number of points to sample from svg path
path_accuracy = 0.01 #if start and endpoint of a line are closer than this, they are considered the same point

# Define types for welzl's algorithm
Point = Tuple[float, float]
Disk = Tuple[Point, float]
# Increase recursion limit, needed for complex SVGs as welzl's algorithm is recursive
sys.setrecursionlimit(10**5)

def line_through_x(center_x, diameter, tip_offset, y_offset = 0):
    """Calculates the start and end points of a line through a circle in x direction, a y_offset<radius can be provided to shorten the line"""
    radius = diameter / 2.0
    offset_length = ((radius-tip_offset)**2-y_offset**2)**0.5
    start_x = center_x - offset_length
    end_x = center_x + offset_length

    return start_x, end_x
def line_through_y(center_y, diameter, tip_offset, x_offset = 0):
    """Calculates the start and end points of a line through a circle in y direction, an x_offset<radius can be provided to shorten the line"""
    radius = diameter / 2.0
    offset_length = ((radius-tip_offset)**2-x_offset**2)**0.5
    start_y = center_y - offset_length
    end_y = center_y + offset_length

    return start_y, end_y

class CircleGrid:
    def __init__(self, root, columns, rows):
        self.width = root.winfo_width()
        self.height = root.winfo_height()
        self.rows = rows
        self.columns = columns
        self.cell_width = self.width / self.columns
        self.cell_height = self.height / self.rows
        self.selected_circles = []
        self.click_coords = (None, None)

        # set the canvas as given root
        self.canvas = root

        self.draw_grid()

        self.canvas.bind('<Button-1>', self.circle_click)
        self.canvas.bind('<ButtonRelease-1>', self.circle_release)

    def draw_grid(self):
        #check how big the circles can be
        if self.cell_width < self.cell_height:
            self.cell_height = self.cell_width
        else:
            self.cell_width = self.cell_height

        #create circles and text
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height

                circle_number = int((self.rows-row-1) * self.columns + col + 1)
                circle_name = chr(65 + row) + str(col + 1)
                self.canvas.create_oval(x1, y1, x2, y2, tags=f'circle{circle_number}', outline='black')
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=circle_name, tags = f'{circle_name}')

    def circle_click(self, event):
        #Check if click was inside grid
        if event.x < 0 or event.x > (self.cell_width * self.columns) or event.y < 0 or event.y > (self.cell_height * self.rows):
            self.click_coords = (None, None)
            return
        col,_ = divmod(event.x, self.cell_height)
        row,_ = divmod(event.y, self.cell_width)
        self.click_coords = (int(col), int(row))

    def circle_release(self, event):
        #Check if release was inside grid:
        if event.x < 0 or event.x > (self.cell_width * self.columns) or event.y < 0 or event.y > (self.cell_height * self.rows):
            self.click_coords = (None, None)
            return

        col,_ = divmod(event.x, self.cell_height)
        row,_ = divmod(event.y, self.cell_width)

        # Check if the click was inside the circle grid
        if self.click_coords[0] != None:
            cols = (self.click_coords[0], int(col))
            rows = (self.click_coords[1], int(row))
            # Iterate through the selected circles and change their color
            for current_col in range(min(cols), max(cols)+1):
                for current_row in range(min(rows), max(rows)+1):
                    circle_number = int((self.rows-current_row-1) * self.columns + current_col + 1)
                    item = self.canvas.find_withtag(f'circle{circle_number}')
                    if circle_number in self.selected_circles:
                        self.selected_circles.remove(circle_number)
                        self.canvas.itemconfig(item, fill='')
                    else:
                        self.selected_circles.append(circle_number)
                        self.canvas.itemconfig(item, fill='red')

        self.click_coords = (None, None)

    def get_selected_circles(self):
        return self.selected_circles

# Functions for welzl's algorithm
def dist(p1: Point, p2: Point) -> float:
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
def circle_from_two_points(p1: Point, p2: Point) -> Disk:
    """Return the minimal disk that passes through two points."""
    center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    radius = dist(p1, p2) / 2
    return center, radius
def circle_from_three_points(p1: Point, p2: Point, p3: Point) -> Disk:
    """Return the minimal disk that passes through three points."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if d == 0:
        d1 = dist(p1, p2)
        d2 = dist(p2, p3)
        d3 = dist(p1, p3)
        if d1 >= d2 and d1 >= d3:
            return circle_from_two_points(p1, p2)
        elif d2 >= d1 and d2 >= d3:
            return circle_from_two_points(p2, p3)
        else:
            return circle_from_two_points(p1, p3)
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    center = (ux, uy)
    radius = dist(center, p1)
    return center, radius
def trivial(R: List[Point]) -> Disk:
    """Return the minimal disk that passes through points in R."""
    if len(R) == 0:
        return (0, 0), 0
    elif len(R) == 1:
        return R[0], 0
    elif len(R) == 2:
        return circle_from_two_points(R[0], R[1])
    elif len(R) == 3:
        return circle_from_three_points(R[0], R[1], R[2])
    else:
        raise ValueError("R can contain at most 3 points")
def is_in_disk(p: Point, d: Disk) -> bool:
    """Check if point p is inside or on the boundary of disk d."""
    center, radius = d
    return dist(p, center) <= radius
def welzl(P: List[Point], R: List[Point] = []) -> Disk:
    """Welzl's algorithm to find the minimal disk enclosing P with R on the boundary."""
    if len(P) == 0 or len(R) == 3:
        return trivial(R)

    p = random.choice(P)
    P.remove(p)

    D = welzl(P, R)
    
    if is_in_disk(p, D):
        P.append(p)
        return D

    R.append(p)
    D = welzl(P, R)
    R.remove(p)
    P.append(p)
    
    return D
def perform_welzl(svg_lines):
    """Perform Welzl algorithm on svg_data and return center and radius of disk"""
    points = []
    for line in svg_lines:
            start = line.start
            end = line.end
            points.append((start.real, start.imag))
            points.append((end.real, end.imag))
    return welzl(points)
# Functions for SVG to lines
def sample_path(path, num_points=20):
    """
    Sample a path into line segments.
    """
    points = [path.point(i / num_points) for i in range(num_points + 1)]
    lines = [Line(points[i], points[i + 1]) for i in range(num_points)]
    return lines
def approximate_svg_with_lines(svg_file, num_points=20):
    """
    Convert all paths in an SVG file into sets of line segments.
    """
    paths, _ = svg2paths(svg_file)
    line_segments = []

    for path in paths:
        for segment in path:
            if isinstance(segment, Line):
                line_segments.append(segment)
            elif isinstance(segment, (CubicBezier, QuadraticBezier, Arc)):
                lines = sample_path(segment, num_points)
                line_segments.extend(lines)

    return line_segments
def calculate_scaled_xy(point, svg_center, svg_radius, svg_scale, tip_offset, center_x, center_y):
    """
    Calculates the scaled (X, Y) point from imaginary point.
    """
    x = (((point.real - svg_center[0]) / (svg_radius * 2)) * (svg_scale * (well_data['diameter'] - tip_offset * 2)) + center_x)
    y = (((point.imag - svg_center[1]) / (svg_radius * 2)) * (svg_scale * (well_data['diameter'] - tip_offset * 2)) + center_y)
    return (x, y)

# Create the root window
root = tk.Tk()
root.geometry("800x500")
root.title("Scratch me Baby!") # Haha 

# Create the outer canvas
outer_canvas = tk.Canvas(root, width=800, height=500)
outer_canvas.pack()

# Create the inner canvas
inner_canvas_size = (550, 345)
inner_canvas = tk.Canvas(outer_canvas, width=inner_canvas_size[0], height=inner_canvas_size[1], bg="white")
inner_canvas.place(x=50, y=105)  

# Create labels for the input fields
label_x = tk.Label(outer_canvas, text="X Offset")
label_y = tk.Label(outer_canvas, text="Y Offset")
label_z = tk.Label(outer_canvas, text="Z Offset")
label_tip = tk.Label(outer_canvas, text="Tip Offset")
label_x.place(x=50, y=5)
label_y.place(x=50, y=30)
label_z.place(x=50, y=55)
label_tip.place(x=50, y=80)

# Create a validation command
def validate_float(input, min_value=None, max_value=None):
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

# Register the validation command with the canvas
validate_input = outer_canvas.register(lambda input: validate_float(input, min_value=-99999999, max_value=99999999))
validate_int = outer_canvas.register(lambda input: input.isdigit() or input == "")
validate_scale = outer_canvas.register(lambda input: validate_float(input, min_value=0, max_value=1))


# Create Input fields for offset
offset_x_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
offset_y_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
offset_z_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
tip_offset_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
offset_x_field.place(x=120, y=5)
offset_y_field.place(x=120, y=30)
offset_z_field.place(x=120, y=55)
tip_offset_field.place(x=120, y=80)
offset_x_field.insert(0, offset_x_default)
offset_y_field.insert(0, offset_y_default)
offset_z_field.insert(0, offset_z_default)
tip_offset_field.insert(0, tip_offset_default)

# Create a label for the pattern selection
label_pattern = tk.Label(outer_canvas, text="Pattern")
label_pattern.place(x=200, y=5)
label_number = tk.Label(outer_canvas, text="Line Number")
label_number.place(x=290, y=5)
label_distance = tk.Label(outer_canvas, text="Line Distance")
label_distance.place(x=290, y=30)
label_rect_scratch = tk.Label(outer_canvas, text="Repeat with 90° flip")
label_rect_scratch.place(x=290, y=55)
label_inner_radius = tk.Label(outer_canvas, text="Inner Radius")
label_inner_radius.place(x=290, y=55)
label_inner_radius.place_forget()  # Hide the label

def update_labels(*args):
    selected_pattern = pattern_value.get()
    if selected_pattern == "Mesh":
        label_number.config(text="Line Number")
        label_distance.config(text="Line Distance")
        label_inner_radius.place_forget()  # Hide the label
        inner_radius_field.place_forget()  # Hide the input field
        svg_file_field.place_forget()   # Hide the input field
        svg_scale_field.place_forget()  # Hide the input field
        label_rect_scratch.place(x=290, y=55)  # Show the label
        rect_scratch_checkbox.place(x=425, y=55)  # Show the checkbox
    elif selected_pattern == "Circles":
        label_number.config(text="Circle Number")
        label_distance.config(text="Circle Distance")
        label_inner_radius.config(text="Inner Radius")
        label_inner_radius.place(x=290, y=55)  # Show the label
        inner_radius_field.place(x=380, y=55)  # Show the input field
        label_rect_scratch.place_forget()  # Hide the label
        svg_file_field.place_forget()   # Hide the input field
        svg_scale_field.place_forget()  # Hide the input field
    elif selected_pattern == "SVG":
        label_number.config(text="SVG File")
        label_distance.config(text="SVG Scale")
        label_inner_radius.place_forget()
        inner_radius_field.place_forget()
        label_rect_scratch.place_forget()  # Hide the label
        rect_scratch_checkbox.place_forget()  # Hide the checkbox
        svg_file_field.place(x=380, y=5)    # Show the input field
        svg_scale_field.place(x=380, y=30)  # Show the input field
        
# Create a dropdown menu for the pattern selection
pattern_value = tk.StringVar(outer_canvas)
pattern_value.set("Mesh")  # default value
pattern_value.trace_add("write", update_labels)  # Call update_labels whenever pattern changes
pattern_dropdown = tk.OptionMenu(outer_canvas, pattern_value, "Mesh", "Circles", "SVG")
pattern_dropdown.place(x=200, y=30)

# Create input fields for the pattern parameters
number_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_int, '%P'))
distance_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
rect_scratch_state = tk.BooleanVar()
rect_scratch_checkbox = tk.Checkbutton(outer_canvas, var=rect_scratch_state)
inner_radius_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
svg_file_field = tk.Entry(outer_canvas, width=10)
svg_scale_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_scale, '%P'))
number_field.place(x=380, y=5)
distance_field.place(x=380, y=30)
rect_scratch_checkbox.place(x=425, y=55)
inner_radius_field.place(x=380, y=55)
inner_radius_field.place_forget()  # Hide the input field
svg_file_field.place(x=380, y=5)
svg_file_field.place_forget()   # Hide the input field
svg_scale_field.place(x=380, y=30)
svg_scale_field.place_forget()  # Hide the input field
number_field.insert(0, number_default)
distance_field.insert(0, distance_default)
rect_scratch_state.set(rect_scratch_default)
inner_radius_field.insert(0, inner_radius_default)
svg_file_field.insert(0, svg_file_default)
svg_scale_field.insert(0, svg_scale_default)


# Create Speed input labels
label_speed_move = tk.Label(outer_canvas, text="Travel Speed")
label_speed_move.place(x=470, y=5)
label_speed_scratch = tk.Label(outer_canvas, text="Scratch Speed")
label_speed_scratch.place(x=470, y=30)

# Create Input fields for speed
speed_move_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
speed_scratch_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
speed_move_field.place(x=550, y=5)
speed_scratch_field.place(x=550, y=30)
speed_move_field.insert(0, speed_move_default)
speed_scratch_field.insert(0, speed_scratch_default)

# Create Input field for scratching multiple times
label_multi_scratch = tk.Label(outer_canvas, text="Scratch Cycles")
label_multi_scratch.place(x=470, y=55)
multi_scratch_field  = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_int, '%P'))
multi_scratch_field.place(x=550, y=55)
multi_scratch_field.insert(0, multi_scratch_default)

# Create a bool checkbox for auto leveling
auto_leveling_state = tk.BooleanVar()
auto_leveling_state.set(auto_leveling_default)  # default value
auto_leveling_checkbox = tk.Checkbutton(outer_canvas, text="Auto Leveling", var=auto_leveling_state)
auto_leveling_checkbox.place(x=470, y=80)

# Create input field label for well file path
label_well_file = tk.Label(outer_canvas, text="Well File Path:")
label_well_file.place(x=650, y=140)

# Create input field for well file path
well_file_field = tk.Entry(outer_canvas, width=20)
well_file_field.insert(0, well_file_default)  # default value
well_file_field.place(x=650, y=165)

# Create Button to load well file
def load_well_data():
    """Loads the well data from a *.txt file"""
    try:
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        well_file_path = current_directory + "\\" + well_file_field.get()
        well_data.clear()
        global well_grid
        with open(well_file_path, "r") as file:
            for line in file:
                key, value = line.strip().split(": ")
                well_data[key] = float(value)
        inner_canvas.delete("all")
        well_grid = CircleGrid(inner_canvas, int(well_data['number_x']), int(well_data['number_y']))
        print("Loaded well file")
        messagebox.showinfo("Load well file", "Loaded well file: " + well_file_field.get()+ "\n" + str(well_data))
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "Well file not found: " + well_file_field.get())
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: " + str(e))
    return well_data
load_well_file_button = tk.Button(outer_canvas, text="Load Well File", command=load_well_data)
load_well_file_button.place(x=650, y=190)

# Create input field for gcode name
label_gcode_name = tk.Label(outer_canvas, text="G-Code Name:")
label_gcode_name.place(x=650, y=215)
gcode_name_field = tk.Entry(outer_canvas, width=20)
gcode_name_field.insert(0, "scratch.gcode")  # default value
gcode_name_field.place(x=650, y=240)

# Create Button to load cleaning program
def generate_cleaning_program():
    """Loads the cleaning data from a *.txt file and returns gcode"""
    try:
        clean_data = {}
        clean_gcode = ";cleaning gcode\n"
        container = 0
        pause = pause_before_clean_state.get()
        # Extract data from file and generate gcode
        with open(clean_file_field.get(), "r") as file:
            for line in file:
                if line[0] == "/":
                    container += 1
                    clean_gcode += f";cleaning container {container}\n"
                    clean_gcode += f"G0 Z{clean_data['Z']+10:.2f}\n"
                    clean_gcode += f"G0 X{clean_data['X']:.2f} Y{clean_data['Y']:.2f}\n"
                    if pause:
                        clean_gcode += "M0 \"Position cleaning container and press to continue\"\n"
                    clean_gcode += f"G0 X{clean_data['X']-clean_data['Radius']:.2f} Z{clean_data['Z']-clean_data['Depth']:.2f}\n"
                    for N in range(int(clean_data['Number'])):
                        clean_gcode += f"G2 I{clean_data['Radius']:.2f} F{clean_speed:.0f}\n"                
                    clean_data.clear()
                else:
                    key, value = line.strip().split(": ")
                    clean_data[key] = float(value)
        return clean_gcode
    
    except FileNotFoundError:
        messagebox.showerror("Clean Program Error", "Cleaning program file not found.")
    except Exception as e:
        messagebox.showerror("Clean Program Error", str(e) + "Please check your clean.txt file for correctnes.")

# Create input field for cleaning file
label_clean_file = tk.Label(outer_canvas, text ="Clean File Path")
label_clean_file.place(x=650, y=5)
clean_file_field = tk.Entry(outer_canvas, width=20)
clean_file_field.insert(0, clean_file_default)
clean_file_field.place(x=650, y=35)

# Create bool checkboxes for cleaning options
clean_before_state = tk.BooleanVar()
clean_before_state.set(clean_before_default)  # default value
clean_before_checkbox = tk.Checkbutton(outer_canvas, text="Clean Before", var=clean_before_state)
clean_before_checkbox.place(x=650, y=60)

clean_after_state = tk.BooleanVar()
clean_after_state.set(clean_after_default)  # default value
clean_after_checkbox = tk.Checkbutton(outer_canvas, text="Clean After", var=clean_after_state)
clean_after_checkbox.place(x=650, y=85)

pause_before_clean_state = tk.BooleanVar()
pause_before_clean_state.set(pause_before_clean_default)  # default value
pause_before_clean_checkbox = tk.Checkbutton(outer_canvas, text="Pause Before Clean", var=pause_before_clean_state)
pause_before_clean_checkbox.place(x=650, y=110)

# Function to generate gcode
def generate_gcode():
    try:
        print(well_data)
        # get varaiables from input fields
        gcode_name = gcode_name_field.get()
        offset_x = float(offset_x_field.get())
        offset_y = float(offset_y_field.get())
        offset_z = float(offset_z_field.get())
        tip_offset = float(tip_offset_field.get())
        pattern = pattern_value.get()
        if pattern == "Mesh":
            mesh_line_number = int(number_field.get())
            mesh_line_distance = float(distance_field.get())
            rect_scratch = rect_scratch_state.get()
        elif pattern == "Circles":
            circle_number = int(number_field.get())
            circle_distance = float(distance_field.get())
        elif pattern == "SVG":
            svg_path = svg_file_field.get()
            svg_scale = float(svg_scale_field.get())
            #Load svg path as well and prepare for transposal
            svg_lines = approximate_svg_with_lines(svg_path, num_points=resolution)
            svg_center, svg_radius = perform_welzl(svg_lines)
        speed_move = float(speed_move_field.get())
        speed_scratch = float(speed_scratch_field.get())
        multi_scratch = int(multi_scratch_field.get())
        auto_leveling = auto_leveling_state.get()
        try:
            skipped_wells = well_grid.get_selected_circles()
        except:
            messagebox.showerror("Generate gcode", "Please load well file first!")
            return

        # open gcode file
        gcode = open(f"{gcode_name}", 'w')

        #add beginning gcode
        gcode.writelines("G21\n")   #set to mm
        gcode.writelines("G28\n")   #home printhead
        gcode.writelines(f"G0 X{offset_x:.2f} Y{offset_y:.2f} Z{offset_z:.2f}\n")   #move to offset location
        gcode.writelines(f"F{speed_move:.0f}\n\n")  #set movement speed to XXX units/min i guess
        if auto_leveling:
            gcode.writelines("M420 S1\n")

        #move nozzle to insert tip
        gcode.writelines(f"G0 Z{offset_z+30:.2f}\n")
        gcode.writelines("M0 \"Please insert tip to start scratching :)\"\n\n")

        #clean if specified
        if clean_before_state.get():
            gcode.writelines(generate_cleaning_program())

        #iterate through short side of well
        for number_y in range (int(well_data['number_y'])):
            # iterate through long side of well
            for number_x in range (int(well_data['number_x'])):

                #check if well number is on list for not scratching
                well_number = int(number_y * well_data['number_x'] + number_x + 1)
                well_name = chr(64 + int(well_data["number_y"]) - number_y) + str(number_x + 1)
                if well_number in skipped_wells:
                    print(f"Skipped well {well_number:.0f}, Name: {well_name}")
                    continue

                #calculate center points for well
                center_x = well_data['distance_x'] + number_x * (well_data['diameter'] + well_data['distance_well']) + well_data['diameter'] / 2 + offset_x
                center_y = well_data['distance_y'] + number_y * (well_data['diameter'] + well_data['distance_well']) + well_data['diameter'] / 2 + offset_y
                depth = offset_z - well_data['depth']

                #move above center of well and into it
                gcode.writelines(f";GCODE for well number {well_number}, Name: {well_name}\n")
                gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z{offset_z+move_height:.2f}\n")
                gcode.writelines(f"G0 Z{depth+move_height:.2f}\n")

                #adds gcode according to pattern
                if pattern == "Mesh":
                    if mesh_line_distance*(mesh_line_number-1)+tip_offset*2 >= well_data['diameter']: #check if mesh is possible
                        print("The mesh is not possible with current settings of line number and distance!")
                        messagebox.showerror("Pattern", "Mesh not possible with selected line number and distance!")
                        return

                    y_cordinates = [center_y+(i-mesh_line_number/2)*mesh_line_distance+mesh_line_distance/2 for i in range(mesh_line_number)]
                    for y_position in y_cordinates:
                        start_x, end_x = line_through_x(center_x, well_data['diameter'], tip_offset, y_offset=center_y-y_position)
                        gcode.writelines(f"G0 X{start_x:.2f} Y{y_position:.2f}\n")
                        gcode.writelines(f"G0 Z{depth:.2f}\n")
                        gcode.writelines(f"G0 X{end_x:.2f} F{speed_scratch:.0f}\n")
                        for ii in range(multi_scratch-1):
                            if ii % 2 == 0:
                                gcode.writelines(f"G0 X{start_x:.2f}\n")
                            else:
                                gcode.writelines(f"G0 X{end_x:.2f}\n")
                        gcode.writelines(f"G0 Z{depth+move_height:.2f} F{speed_move:.0f}\n")
                    if rect_scratch:
                        x_coordinates = [center_x+(i-mesh_line_number/2)*mesh_line_distance+mesh_line_distance/2 for i in range(mesh_line_number)]
                        for x_position in x_coordinates:
                            start_y, end_y = line_through_y(center_y, well_data['diameter'], tip_offset, x_offset=center_x-x_position)
                            gcode.writelines(f"G0 X{x_position:.2f} Y{start_y:.2f}\n")
                            gcode.writelines(f"G0 Z{depth:.2f}\n")
                            gcode.writelines(f"G0 Y{end_y:.2f} F{speed_scratch:.0f}\n")
                            for ii in range(multi_scratch-1):
                                if ii % 2 == 0:
                                    gcode.writelines(f"G0 Y{start_y:.2f}\n")
                                else:
                                    gcode.writelines(f"G0 Y{end_y:.2f}\n")
                            gcode.writelines(f"G0 Z{depth+move_height:.2f} F{speed_move:.0f}\n")

                elif pattern == "Circles":   #check if circles possible
                    circle_inner_radius = float(inner_radius_field.get())
                    if circle_inner_radius+(circle_number-1)*circle_distance+tip_offset >= well_data['diameter']/2:
                        print("The cirlces are not possible with current settings of line number and distance!")
                        messagebox.showerror("Pattern", "Circles not possible with selected line number and distance!")
                        return
                    
                    radii = [circle_inner_radius+i*circle_distance for i in range(circle_number)]
                    for radius in radii:
                        gcode.writelines(f"G0 X{center_x-radius:.2f}\n")
                        gcode.writelines(f"G0 Z{depth:.2f}\n")
                        gcode.writelines(f"G2 I{radius:.2f} F{speed_scratch:.0f}\n")
                        for _ in range(multi_scratch-1):
                            gcode.writelines(f"G2 I{radius:.2f}\n")
                        gcode.writelines(f"G0 Z{depth+move_height:.2f} F{speed_move:.0f}\n")

                elif pattern == "SVG":
                    for _ in range(multi_scratch):
                        previous_end = (-10**10, -10**10) # Set initial end outside of coordinate range
                        for line in svg_lines:
                            start = calculate_scaled_xy(line.start, svg_center, svg_radius, svg_scale, tip_offset, center_x, center_y)
                            end = calculate_scaled_xy(line.end, svg_center, svg_radius, svg_scale, tip_offset, center_x, center_y)
                            # When next path starts at end of same path no raise of tip and move to start needed
                            if dist(start, previous_end) > path_accuracy:
                                gcode.writelines(f"G0 Z{move_height+depth:.2f} F{speed_move:.0f}\n")
                                gcode.writelines(f"G0 X{start[0]:.2f} Y{start[1]:.2f}\n")
                                gcode.writelines(f"G0 Z{depth:.2f}\n")
                                gcode.write(f"G0 F{speed_scratch:.0f}\n")
                            gcode.writelines(f"G0 X{end[0]:.2f} Y{end[1]:.2f}\n")
                            previous_end = end  

                # This case should not happen tbh
                else: 
                    print("Your specified pattern does not exist")
                    messagebox.showerror("Pattern", f"Pattern {pattern} doesn't exist!")
                    exit(1)

                #move above well to go to next one
                gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z{offset_z+move_height:.2f}\n\n")

        #clean if specified
        if clean_after_state.get():
            gcode.writelines(generate_cleaning_program())

        #return to start and close
        gcode.writelines(f"G0 X{offset_x:.2f} Y{offset_y:.2f} Z{offset_z+30:.2f}\n")
        gcode.writelines("M0 \"Please remove the tip to end print :)\"\n")
        gcode.writelines("M30\n")
        gcode.close()
        print(f"Succesfully generated {gcode_name}!")
        messagebox.showinfo("Generate gcode", f"Succesfully generated {gcode_name}!")
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

# Create a button to generate the gcode
generate_gcode_button = tk.Button(outer_canvas, text="Generate G-Code", command=generate_gcode)
generate_gcode_button.place(x=650, y=265)

# Run the main loop
root.mainloop()
