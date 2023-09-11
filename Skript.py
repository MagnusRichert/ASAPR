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
    gcode.writelines("G28\n")
    gcode.writelines("G0 "+start_coordinates+"\n")
    gcode.writelines("G92 X0 Y0 Z0\n") # set new home to..
    gcode.writelines("G0 F300\n\n")  #set speed to 300 units/min i guess

    #iterate through short side of well
    for width in range (int(data['number_short'])):
        # iterate through long side of well
        for length in range (int(data['number_long'])):

            #check if well number is on list for not scratching
            well_number = width * data['number_long'] + length + 1
            if well_number in []:
                print(f"Skipped well {well_number:.0f}")
                continue

            #calculate center points for well
            center_x = data['distance_short'] + length * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
            center_y = data['distance_long'] + width * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
            depth = data['depth']

            #move above center of well and into it
            gcode.writelines(f";GCODE for well number {well_number}\n")
            gcode.writelines(f"G0 X{center_x:.2f} Y{center_y:.2f} Z10\n")
            gcode.writelines(f"G0 Z{-depth/2:.2f}\n")

            #adds gcode according to pattern
            if pattern == "line":
                start_x, end_x = line_through_x(center_x, data['diameter'], data['tip_offset'])
                gcode.writelines(f"G0 X{start_x:.2f}\n")
                gcode.writelines(f"G0 Z{-depth:.2f}\n")
                gcode.writelines(f"G0 X{end_x:.2f}\n")
                gcode.writelines(f"G0 Z{-depth/2:.2f}\n")

            elif pattern == "mesh":
                #side_offset = input("Specify a side offset. The outermost lines will wil") #for later maybe
                line_distance = data['diameter']/(mesh_line_number+1)
                for ii in range(mesh_line_number):
                    y_postition = center_y - data['diameter']/2 + line_distance * (1+ii)
                    start_x, end_x = line_through_x(center_x, data['diameter'], data['tip_offset'], y_offset=center_y-y_postition)
                    gcode.writelines(f"G0 X{start_x:.2f} Y{y_postition:.2f}\n")
                    gcode.writelines(f"G0 Z{-depth:.2f}\n")
                    gcode.writelines(f"G0 X{end_x:.2f}\n")
                    gcode.writelines(f"G0 Z{-depth/2:.2f}\n")

            elif pattern == "circle":
                pass


            else: 
                print("Your specified pattern does not exist")

            #move above well to go to next one
            gcode.writelines(f"G00 X{center_x:.2f} Y{center_y:.2f} Z10\n\n")

    #return to start and close
    gcode.writelines("G0 X0 Y0 Z10\n")
    gcode.writelines("M00 \"Please remove the tip to end print :)\\n"")
    gcode.writelines("M30\n")
    gcode.close()
    print(f"Succesfully generated {gcode_name}!")

###TEST VARIABLES / remove later
circle_radius = 6
mesh_line_number = 8
start_coordinates = "X50 Y50 Z30"


###MAIN SKRIPT
if __name__ == '__main__':

    file_path = input('Please enter the filename of your well data and press Enter: ')
    data = load_well_data(file_path)
    print(data)
    pattern = input('Please specify the pattern you want: line, mesh: ')
    print('Starting G-Code generation...')
    generate_gcode(data, pattern)

    try:
        pass
    except FileNotFoundError:
        print("File not found.")
    #except Exception as e:
    #    print(f"An error occurred: {e}")