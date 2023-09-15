###IMPORTS


###FUNCTIONS
def load_well_data(file_path):
    """Loads the well data from a .txt file"""
    data = {}
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split(": ")
            data[key] = float(value)
    return data

def line_through_x(center_x, diameter, tip_offset, y_offset = 0):
    """Calculates the start and end points of a line through a circle in x direction, a y_offset<radius can be provided to shorten the line"""
    radius = diameter / 2.0
    offset_length = ((radius-tip_offset)**2-y_offset**2)**0.5
    start_x = center_x - offset_length
    end_x = center_x + offset_length

    return start_x, end_x

def generate_gcode(data, pattern):
    # open gcode file
    gcode_name = input('Please enter the name of your G-Code and dont forget .gcode an the end: ')
    gcode = open(f"{gcode_name}", 'w')

    #add beginning gcode
    gcode.writelines("G21\n")   #set to mm
    gcode.writelines("G28\n")   #home printhead
    gcode.writelines(f"G0 X{offset_x:.2f} Y{offset_y:.2f} Z{offset_z:.2f}\n")   #move to offset location
    gcode.writelines("G92 X0 Y0 Z0\n") #set current position as home
    gcode.writelines(f"F{speed_move:.0f}\n\n")  #set movement speed to XXX units/min i guess

    #move nozzle to insert tip
    gcode.writelines(f"G0 Z30\n")
    gcode.writelines("M00 \"Please insert tip to start scratching :)\"\n\n")


    #iterate through short side of well
    for number_y in range (int(data['number_y'])):
        # iterate through long side of well
        for number_x in range (int(data['number_x'])):

            #check if well number is on list for not scratching
            well_number = int(number_y * data['number_x'] + number_x + 1)
            if well_number in skipped_wells:
                print(f"Skipped well {well_number:.0f}")
                continue

            #calculate center points for well
            center_x = data['distance_x'] + number_x * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
            center_y = data['distance_y'] + number_y * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
            depth = data['depth']

            #move above center of well and into it
            gcode.writelines(f";GCODE for well number {well_number}\n")
            gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z10\n")
            gcode.writelines(f"G0 Z{-depth/2:.2f}\n")

            #adds gcode according to pattern
            if pattern == "mesh":
                if mesh_line_distance*mesh_line_number >= data['diameter'] and mesh_line_number > 1: #check if mesh is possible
                    print("The mesh is not possible with current settings of line number and distance!")
                    exit(1)

                y_cordinates = [center_y+(i-mesh_line_number/2)*mesh_line_distance+mesh_line_distance/2 for i in range(mesh_line_number)]
                for y_position in y_cordinates:
                    start_x, end_x = line_through_x(center_x, data['diameter'], offset_tip, y_offset=center_y-y_position)
                    gcode.writelines(f"G0 X{start_x:.2f} Y{y_position:.2f}\n")
                    gcode.writelines(f"G0 Z{-depth:.2f}\n")
                    gcode.writelines(f"G0 X{end_x:.2f} F{speed_scratch:.0f}\n")
                    if double_scratch:
                        gcode.writelines(f"G0 X{start_x:.2f}\n")
                    gcode.writelines(f"G0 Z{-depth/2:.2f} F{speed_move:.0f}\n")

            elif pattern == "circles":   #check if circles possible
                if circle_inner_radius+circle_number*circle_distance >= data['diameter'] and circle_number > 1:
                    print("The cirlces are not possible with current settings of line number and distance!")
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

            #move above well to go to next one
            gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z10\n\n")

    #return to start and close
    gcode.writelines("G0 X0 Y0 Z30\n")
    gcode.writelines("M0 \"Please remove the tip to end print :)\"\n")
    gcode.writelines("M30\n")
    gcode.close()
    print(f"Succesfully generated {gcode_name}!")

###TEST VARIABLES / remove later
file_path = "24well.txt"
mesh_line_number = 6    #number of lines in mesh pattern
mesh_line_distance = 1.2  #distance between mesh lines
circle_inner_radius = 7   #radius in mm
circle_distance = 1     #distance of circles
circle_number = 3
offset_tip = 0.5
offset_x = 100
offset_y = 40
offset_z = 50
pattern = "circles"
speed_scratch = 50*60
speed_move = 100*60
double_scratch = True
skipped_wells = []


###MAIN SKRIPT
if __name__ == '__main__':

    if input("Use predefined values yes/no:") != "yes":
        file_path = input('Please enter the filename of your well data (6well.txt) and press Enter: ')
        offset_tip = float(input("Enter tip offset:"))
        offset_x = float(input("Enter x offset:"))
        offset_y = float(input("Enter y offset:"))
        offset_z = float(input("Enter z offset:"))
        pattern = input("Scratch pattern mesh/circles: ")
        if pattern == "mesh":
            mesh_line_number = int(input("Enter number of lines: "))
            mesh_line_distance = float(input("Enter distance between lines: "))
        else:
            circle_inner_radius = float(input("Enter inner radius: "))
            circle_distance = float(input("Enter distance between circles: "))
            circle_number = int(input("Enter number of circles: "))

        if input("Do you want to scratch each line back and forth yes/no: ") != "yes":
            double_scratch = False
        speed_scratch = float(input("Enter scratch speed(mm/s): "))*60
        speed_move = float(input("Enter movement speed(mm/s): "))*60
        skipped_wells_input = input("Enter a list of wells to skip like 2,4,5,11:")
        skipped_wells = list(map(int, skipped_wells_input.split(','))) if skipped_wells_input.strip() else []




    data = load_well_data(file_path)
    print('Starting G-Code generation...')
    generate_gcode(data, pattern)

    try:
        pass
    except FileNotFoundError:
        print("File not found.")
    #except Exception as e:
    #    print(f"An error occurred: {e}")