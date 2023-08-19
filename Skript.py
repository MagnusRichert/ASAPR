###IMPORTS


###FUNCTIONS
def load_well_data(file_path):
    data = {}
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split(": ")
            data[key] = float(value)
    return data

def line_through_circle(center_x, diameter):
    radius = diameter / 2.0
    start_x = center_x - radius
    end_x = center_x + radius

    return start_x, end_x

def generate_gcode(data):
    # open gcode file
    gcode_name = input('Please enter the name of your G-Code and dont forget .gcode an the end: ')
    gcode = open("gcode_name", 'w')
    # iterate through short side of well
    for width in range (int(data['number_short'])):
        # iterate through long side of well
        for length in range (int(data['number_long'])):
            center_x = data['distance_short'] + length * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
            center_y = data['distance_long'] + width * (data['diameter'] + data['distance_well']) + data['diameter'] / 2
            print(center_x, center_y, '\n')

    close(gcode_name)

###TEST VARIABLES / remove later


###MAIN SKRIPT
if __name__ == '__main__':
    try:
        file_path = input('Please enter the filename of your well data and press Enter: ')
        data = load_well_data(file_path)
        print(data)
        print('Starting G-Code generation...')
        generate_gcode(data)

        


    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")