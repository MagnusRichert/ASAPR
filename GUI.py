import tkinter as tk
from tkinter import messagebox

### FUNCTIONS AND VARIABLES###
data = {}
well_grid = None

def line_through_x(center_x, diameter, tip_offset, y_offset = 0):
    """Calculates the start and end points of a line through a circle in x direction, a y_offset<radius can be provided to shorten the line"""
    radius = diameter / 2.0
    offset_length = ((radius-tip_offset)**2-y_offset**2)**0.5
    start_x = center_x - offset_length
    end_x = center_x + offset_length

    return start_x, end_x

class CircleGrid:
    def __init__(self, root, columns, rows):
        self.width = root.winfo_width()
        self.height = root.winfo_height()
        self.rows = rows
        self.columns = columns
        self.cell_width = self.width / self.columns
        self.cell_height = self.height / self.rows
        self.selected_circles = []

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()

        self.draw_grid()

        self.canvas.bind('<Button-1>', self.circle_click)

    def draw_grid(self):
        #check how big the circles can be
        if self.cell_width < self.cell_height:
            self.cell_height = self.cell_width
        else:
            self.cell_width = self.cell_height

        for row in range(self.rows):
            for col in range(self.columns):
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height

                circle_number = int((self.rows-row-1) * self.columns + col + 1)
                circle_name = chr(65 + row) + str(col + 1)
                self.canvas.create_oval(x1, y1, x2, y2, tags=f'circle{circle_number}', outline='black')
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=circle_name)

    def circle_click(self, event):
        col,_ = divmod(event.x, self.cell_height)
        row,_ = divmod(event.y, self.cell_width)
        circle_number = int((self.rows-row-1) * self.columns + col + 1)
        item = self.canvas.find_withtag(f'circle{circle_number}')

        if circle_number in self.selected_circles:
            self.selected_circles.remove(circle_number)
            self.canvas.itemconfig(item, fill='')
        else:
            self.selected_circles.append(circle_number)
            self.canvas.itemconfig(item, fill='red')

    def get_selected_circles(self):
        return self.selected_circles

# Create the root window
root = tk.Tk()
root.geometry("800x500")

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
def validate_float(input):
    if input == "":  # Allow empty input
        return True
    try:
        float(input)
        return True
    except ValueError:
        return False

validate_input = outer_canvas.register(validate_float)
validate_int = outer_canvas.register(lambda input: input.isdigit())


# Create Input fields for offset
offset_x_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
offset_y_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
offset_z_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
tip_offset_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
offset_x_field.place(x=120, y=5)
offset_y_field.place(x=120, y=30)
offset_z_field.place(x=120, y=55)
tip_offset_field.place(x=120, y=80)

# Create a label for the pattern selection
label_pattern = tk.Label(outer_canvas, text="Pattern")
label_pattern.place(x=200, y=5)
label_number = tk.Label(outer_canvas, text="Line Number")
label_number.place(x=290, y=5)
label_distance = tk.Label(outer_canvas, text="Line Distance")
label_distance.place(x=290, y=30)
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
    elif selected_pattern == "Circles":
        label_number.config(text="Circle Number")
        label_distance.config(text="Circle Distance")
        label_inner_radius.config(text="Inner Radius")
        label_inner_radius.place(x=290, y=55)  # Show the label
        inner_radius_field.place(x=380, y=55)  # Show the input field
        
# Create a dropdown menu for the pattern selection
pattern_value = tk.StringVar(outer_canvas)
pattern_value.set("Mesh")  # default value
pattern_value.trace_add("write", update_labels)  # Call update_labels whenever pattern changes
pattern_dropdown = tk.OptionMenu(outer_canvas, pattern_value, "Mesh", "Circles")
pattern_dropdown.place(x=200, y=30)

# Create input fields for the pattern parameters
number_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_int, '%P'))
distance_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
inner_radius_field = tk.Entry(outer_canvas, width=10, validate="key", validatecommand=(validate_input, '%P'))
number_field.place(x=380, y=5)
distance_field.place(x=380, y=30)
inner_radius_field.place(x=380, y=55)
inner_radius_field.place_forget()  # Hide the input field

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

# Create a bool checkbox for double scratching
double_scratch_state = tk.BooleanVar()
double_scratch_state.set(False)  # default value
double_scratch_checkbox = tk.Checkbutton(outer_canvas, text="Double Scratch", var=double_scratch_state)
double_scratch_checkbox.place(x=470, y=55)

# Create a bool checkbox for auto leveling
auto_leveling_state = tk.BooleanVar()
auto_leveling_state.set(False)  # default value
auto_leveling_checkbox = tk.Checkbutton(outer_canvas, text="Auto Leveling", var=auto_leveling_state)
auto_leveling_checkbox.place(x=470, y=80)

# Create input field label for well file path
label_well_file = tk.Label(outer_canvas, text="Well File Path:")
label_well_file.place(x=650, y=130)

# Create input field for well file path
well_file_field = tk.Entry(outer_canvas, width=20)
well_file_field.insert(0, "24well.txt")  # default value
well_file_field.place(x=650, y=155)

#Create Button to load well file
def load_well_data():
    """Loads the well data from a .txt file"""
    data.clear()
    global well_grid
    with open(well_file_field.get(), "r") as file:
        for line in file:
            key, value = line.strip().split(": ")
            data[key] = float(value)
    well_grid = CircleGrid(inner_canvas, int(data['number_x']), int(data['number_y']))

    print("Loaded well file")
    messagebox.showinfo("Load well file", "Loaded well file: " + well_file_field.get()+ "\n" + str(data))        
    return data
load_well_file_button = tk.Button(outer_canvas, text="Load Well File", command=load_well_data)
load_well_file_button.place(x=650, y=180)

# Create input field for gcode name
label_gcode_name = tk.Label(outer_canvas, text="G-Code Name:")
label_gcode_name.place(x=650, y=205)
gcode_name_field = tk.Entry(outer_canvas, width=20)
gcode_name_field.insert(0, "scratch.gcode")  # default value
gcode_name_field.place(x=650, y=230)

# Create Button to generate gcode
def generate_gcode():
    #try:
    if True:
        print(data)
        # get varaiables from input fields
        gcode_name = gcode_name_field.get()
        offset_x = float(offset_x_field.get())
        offset_y = float(offset_y_field.get())
        offset_z = float(offset_z_field.get())
        tip_offset = float(tip_offset_field.get())
        pattern = pattern_value.get()
        mesh_line_number = int(number_field.get())
        mesh_line_distance = float(distance_field.get())
        circle_number = int(number_field.get())
        circle_distance = float(distance_field.get())
        speed_move = float(speed_move_field.get())
        speed_scratch = float(speed_scratch_field.get())
        double_scratch = double_scratch_state.get()
        auto_leveling = auto_leveling_state.get()
        skipped_wells = well_grid.get_selected_circles()

        # open gcode file
        gcode = open(f"{gcode_name}", 'w')

        #add beginning gcode
        gcode.writelines("G21\n")   #set to mm
        gcode.writelines("G28\n")   #home printhead
        gcode.writelines(f"G0 X{offset_x:.2f} Y{offset_y:.2f} Z{offset_z:.2f}\n")   #move to offset location
        gcode.writelines("G92 X0 Y0 Z0\n") #set current position as home
        gcode.writelines(f"F{speed_move:.0f}\n\n")  #set movement speed to XXX units/min i guess
        if auto_leveling:
            gcode.writelines("M420 S1\n")

        #move nozzle to insert tip
        gcode.writelines(f"G0 Z30\n")
        gcode.writelines("M00 \"Please insert tip to start scratching :)\"\n\n")


        #iterate through short side of well
        for number_y in range (int(data['number_y'])):
            # iterate through long side of well
            for number_x in range (int(data['number_x'])):

                #check if well number is on list for not scratching
                well_number = int(number_y * data['number_x'] + number_x + 1)
                well_name = chr(64 + int(data["number_y"]) - number_y) + str(number_x + 1)
                if well_number in skipped_wells:
                    print(f"Skipped well {well_number:.0f}, Name: {well_name}")
                    continue

                #calculate center points for well
                center_x = data['distance_x'] + number_x * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
                center_y = data['distance_y'] + number_y * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
                depth = data['depth']

                #move above center of well and into it
                gcode.writelines(f";GCODE for well number {well_number}, Name: {well_name}\n")
                gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z10\n")
                gcode.writelines(f"G0 Z{-depth/2:.2f}\n")

                #adds gcode according to pattern
                if pattern == "Mesh":
                    if mesh_line_distance*mesh_line_number >= data['diameter'] and mesh_line_number > 1: #check if mesh is possible
                        print("The mesh is not possible with current settings of line number and distance!")
                        messagebox.showinfo("Pattern", "Mesh not possible with selected line number and distance!")
                        exit(1)

                    y_cordinates = [center_y+(i-mesh_line_number/2)*mesh_line_distance+mesh_line_distance/2 for i in range(mesh_line_number)]
                    for y_position in y_cordinates:
                        start_x, end_x = line_through_x(center_x, data['diameter'], tip_offset, y_offset=center_y-y_position)
                        gcode.writelines(f"G0 X{start_x:.2f} Y{y_position:.2f}\n")
                        gcode.writelines(f"G0 Z{-depth:.2f}\n")
                        gcode.writelines(f"G0 X{end_x:.2f} F{speed_scratch:.0f}\n")
                        if double_scratch:
                            gcode.writelines(f"G0 X{start_x:.2f}\n")
                        gcode.writelines(f"G0 Z{-depth/2:.2f} F{speed_move:.0f}\n")

                elif pattern == "Circles":   #check if circles possible
                    circle_inner_radius = float(inner_radius_field.get())
                    if circle_inner_radius+circle_number*circle_distance >= data['diameter'] and circle_number > 1:
                        print("The cirlces are not possible with current settings of line number and distance!")
                        messagebox.showinfo("Pattern", "Circles not possible with selected line number and distance!")
                        exit(1)
                    radii = [circle_inner_radius+i*circle_distance for i in range(circle_number)]
                    for radius in radii:
                        gcode.writelines(f"G0 X{center_x-radius:.2f}\n")
                        gcode.writelines(f"G0 Z{-depth:.2f}\n")
                        gcode.writelines(f"G2 I{radius:.2f} F{speed_scratch:.0f}\n")
                        if double_scratch:
                            gcode.writelines(f"G3 I{radius:.2f}\n")
                        gcode.writelines(f"G0 Z{-depth/2:.2f} F{speed_move:.0f}\n")



                else: 
                    print("Your specified pattern does not exist")
                    messagebox.showinfo("Pattern", f"Pattern {pattern} doesn't exist!")
                    exit(1)

                #move above well to go to next one
                gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z10\n\n")

        #return to start and close
        gcode.writelines("G0 X0 Y0 Z30\n")
        gcode.writelines("M0 \"Please remove the tip to end print :)\"\n")
        gcode.writelines("M30\n")
        gcode.close()
        print(f"Succesfully generated {gcode_name}!")
        messagebox.showinfo("Generate gcode", f"Succesfully generated {gcode_name}!")
    #except Exception as e:
        #print(f"Error while generating gcode: {str(e)}")
        #messagebox.showerror("Generate gcode", f"Error while generating gcode: {str(e)}")
    
generate_gcode_button = tk.Button(outer_canvas, text="Generate G-Code", command=generate_gcode)
generate_gcode_button.place(x=650, y=255)


# Run the main loop
root.mainloop()