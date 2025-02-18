import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
import ui



if __name__ == "__main__":
    # Increase recursion limit, needed for complex SVGs as welzl's algorithm is recursive
    sys.setrecursionlimit(10**5)
    #create tkinter root window
    root = tk.Tk()
    ui.Ui(root)
    root.mainloop()



