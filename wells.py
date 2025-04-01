import os
from tkinter import messagebox
from typing import Dict


class Wells:
    def __init__(self, root, columns, rows):
        self.window_width = root.winfo_width()
        self.window_height = root.winfo_height()
        self.rows = rows
        self.columns = columns
        self.diameter = 1
        self.depth = 1
        self.distance_well = 1
        self.distance_x = 1
        self.distance_y = 1
        self.cell_width = self.window_width / self.columns
        self.cell_height = self.window_height / self.rows
        self.selected_circles = []
        self.click_coords = (None, None)

        self.well_data = {}
        self.well_grid = None

        # set the canvas as given root
        self.canvas = root

        self.draw_grid()

        self.canvas.bind('<Button-1>', self.circle_click)
        self.canvas.bind('<ButtonRelease-1>', self.circle_release)

    def load_well_data(self, filepath) -> Dict[str, float]:
        """
        Load the well data from a *.txt file.
        """
        variables = {}
        try:            
            with open(filepath, "r") as file:
                for line in file:
                    name, value = line.strip().split(':')
                    variables[name.strip()] = float(value.strip())
            print("Loaded well file")
            messagebox.showinfo("Load well file", "Loaded well file: " + self.well_file_field.get() + "\n" + str(self.well_data))
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "Well file not found: " + self.well_file_field.get())
        except Exception as e:
            messagebox.showerror("Error", "An error occurred: " + str(e))
        #TODO check if all variables are present
        #TODO check if all variables are valid
        #TODO check if all variables are positive
        #TODO check if all variables are floats
        #TODO check if all variables are in the correct range
        self.columns = variables['number_x']
        self.rows = variables['number_y']
        self.diameter = variables['diameter']
        self.depth = variables['depth']
        self.distance_well = variables['distance_well']
        self.distance_x = variables['distance_x']
        self.distance_y = variables['distance_y']
        self.well_data.clear()
        self.well_data = variables
        return self.well_data
    
    def draw_grid(self):
        self.inner_canvas.delete("all")
        self.well_grid = Wells(self.inner_canvas, int(self.well_data['number_x']), int(self.well_data['number_y']))
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