import sys
from ui import Application
#TODO add logging for all Files
#TODO add types for all functions and variables
#TODO add tests for all functions
#TODO add docstrings for all functions
#TODO Add error handling

if __name__ == "__main__":
    # Increase recursion limit, needed for complex SVGs as welzl's algorithm is recursive
    sys.setrecursionlimit(10**5)
    #create UI
    app = Application()
    app.run()


