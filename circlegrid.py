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