# ASAPR - Advanced Scratch Assay Plotting Robot

This repository contains the code to execute in vitro cell analysis via scratch assays as done in the preprint "The use of 3D-printers opens a new world in performing 2D migration analyses - ASAPR"

## How to use this repository

Here we will discuss how to use this repository for your scratch essay and what you need.

### Bill of Materials

The used Materials including a short discription of each component can be found above in the BOM.xlsx file

### Preparation of Printer

In this chapter all necessary steps to prepare the printer are discussed.

#### Level the printbed (Not needed with autoleveling)

To level the printbed first home the printer. Then disable the motors so you can freely slide the printhead in the XY-plane.
Now slide a sheet of paper between your nozzle in the printhead and and your printbed. Visit every corner respectively and tighten/release the screws until you feel a bit of resistance.
The amount of resistance should be the same for each corner. You can also level the bed by eye so that the distance between the adapter and the printbed is the same for each corner.
The actual distance between insert and bed is not important it just has to be consistant.

#### Autolevel the printbed

If you want to use autoleveling, you first have to delete any old mesh and create a new one for your printbed and save it. You should find the necessary actions in the printer settings. There are many online tutorials that describe this process in detail.

#### Mount the positioning for your wells

The next step is to mount your positioning guide for the well on the buildplate. It is important that the sides of your guide/well align with the X- and Y-axis. A magnetic printbed is not recommended as it can slip and loose the position.
If you scratch wells with different sizes it is recommendet to have permanent position guides in the lowest XY-corner and variable guides for the other sides, see picture below.
![Guides](https://private-user-images.githubusercontent.com/90255355/366444479-c9b48ecf-ef6a-4154-91b4-a6085f6e785b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjYwNjE3NTIsIm5iZiI6MTcyNjA2MTQ1MiwicGF0aCI6Ii85MDI1NTM1NS8zNjY0NDQ0NzktYzliNDhlY2YtZWY2YS00MTU0LTkxYjQtYTYwODVmNmU3ODViLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTExVDEzMzA1MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTUxMjcwZDYzMDkwY2NmYjFhM2VlOTViNjk1MGE0OWZiNjI0NzYwNTNkMTNlYTkzMzQ1Zjk5NDc4Y2ZiYjAxODAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.w_yw0Ts_Tw3wBWX2hOzc8HQRbEjvpmOefd3-S50YJ5I)

This way you only have to determine the x_offset and y_offset once. The offsets are shown in the picture below.
![Offsets](https://private-user-images.githubusercontent.com/90255355/366444674-d6d47c4c-fe29-49a8-9c9d-e03ccb57e0a9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjYwNjE3NTUsIm5iZiI6MTcyNjA2MTQ1NSwicGF0aCI6Ii85MDI1NTM1NS8zNjY0NDQ2NzQtZDZkNDdjNGMtZmUyOS00OWE4LTljOWQtZTAzY2NiNTdlMGE5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTExVDEzMzA1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTU4Yjk3Yzk4MzhjNjMxNGI3NjYyMmZkOWU0YWRiMmU0NzZlMTI2NTdiMGZlN2RjM2VlNmE1YWUyYTAyZDRlMDcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.uleY0lAAZIpg1pic4BeYjsM3lOS_p29jfc6rElTdRWU)

The positioning guide used in the preprint can be found in this repository as well. It is possible to print it with the same printer that will later be used for scratching.

#### Measure offsets

There are two approaches on how to determine the offsets. The first one uses the "move" function of the printer itself and can be applied to all printers. The second one  is measuring the offset from the coordinate origin.

##### Using the printer

To measure the offsets you have to home your printer and put the well on the buildplate. Then use the "move" function of your printer to bring the z-axis high enough that you can insert a tip.
Using the "move" function the printer will always display the current position of the axis you are moving. This value is the offset we need.
First you have to move the tip to the X and Y edges closest to the home position respectively so that the tip barely touches them. For Y the printhead was moved to 24.8mm in the example picture below.
![Offset Y](pictures/offset_y.png)
To get your offset values for X and Y you still have to add the radius of the tip you used. For example it has a diameter of 0.4mm: offset_y = Y + d/2 = 24.8mm + 0.2mm = 25.0mm

For the Z offset just move the printhead until the tip touches the well, see picture:
![Offset Z](pictures/offset_z.png)
The Z value can directly be used as the offset. When using a different tip you have to adjust the Z offset again. It is possible to just measure the difference in length of the tips and adjust the offset accordingly.

##### Calculating from coordinate system

This approach can be used if the printers coordinate origin is marked on the buildplate. You can simply measure how far the well plate will be positioned from this origin in X and Y dimensions with a caliper gauge. The Z offset still has to be determined with the approach above, by using the printer.

### Preparation of your PC

You will need an installation of python version 3 or newer. When installing check the box that says "Add Python to PATH". Afterwards open a command window like powershell or cmd and enter the following commands sequentially:

~~~bash
python -m ensurepip --upgrade
pip install svgpathtools
~~~

This will install the python package manager and the package svgpathtools which is needed to process vector graphics.

### Script usage

After measuring all required offsets and preparing your pc you are ready to use the script. If your python is installed correctly you can just double click the GUI.py

The GUI will look like this:
![GUI](https://private-user-images.githubusercontent.com/90255355/366448982-884d83a1-e6c6-4964-a91c-cf8c9fa59219.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjYwNjE3NTUsIm5iZiI6MTcyNjA2MTQ1NSwicGF0aCI6Ii85MDI1NTM1NS8zNjY0NDg5ODItODg0ZDgzYTEtZTZjNi00OTY0LWE5MWMtY2Y4YzlmYTU5MjE5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTExVDEzMzA1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWUwNzNlMzBlMmVkYzcwYjk5MDI4ZjgzNGE3OTI1YWNmMGFkNjVlOTdhNDBmMTVkZGRiZTQwYjY1YjU5OWFkZDgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.1ysNOYLmC47thJHvhufNYyv85VS9Wzb4XWKl6xOu3sI)

#### Enter offsets

In the top left of the GUI you have to enter your measured offsets in mm. The tip offset determines the minimal distance between the center of the tip and the well wall. It HAS to be at least half of the tip diameter. For more robust scratching you might even increase it to 1-2 mm.

#### Choose pattern

Right next to the offsets you can choose between the patterns: mesh (mutiple lines), circles and svg grapics.
![Patterns](pictures/pattern.png)

##### Mesh

The mesh pattern is defined through the number of lines and the distance between them. It is also possible to scratch just one line through the center of the well. If the box for "Repeat with 90° flip" is ticked, the mesh will be scratched again rotated by 90° to create a criss cross pattern.
![Mesh](https://private-user-images.githubusercontent.com/90255355/366449025-db28b08b-c841-4aa9-a9e7-301c1939f099.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjYwNjE3NTUsIm5iZiI6MTcyNjA2MTQ1NSwicGF0aCI6Ii85MDI1NTM1NS8zNjY0NDkwMjUtZGIyOGIwOGItYzg0MS00YWE5LWE5ZTctMzAxYzE5MzlmMDk5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTExVDEzMzA1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdmZGEyMGZiOWQ5NmRkNGViYTIwNzhiMjM4MmRmMjg4MjFlZWRjNGJjMGZhNGQxNmExYWE1MTc1OTU5ZWQ1ZmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.22jz2PMN6PlEor-KjUMjWOgpyGrKaihQlsYNy3pJASQ)

##### Circles

The circles pattern is defined through the number of circles, distance between the circles and diameter of the inner most circle.
![Circles](https://private-user-images.githubusercontent.com/90255355/366449035-d2408d5e-7a97-44d5-8d3b-6d777415af6e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjYwNjE3NTUsIm5iZiI6MTcyNjA2MTQ1NSwicGF0aCI6Ii85MDI1NTM1NS8zNjY0NDkwMzUtZDI0MDhkNWUtN2E5Ny00NGQ1LThkM2ItNmQ3Nzc0MTVhZjZlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTExVDEzMzA1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTUyMzM3YmJkMjNmMWEwZDJlZjBjNjVmMGQxMWNkODViZTZlMzIxMDViOGZjMjZjYTBiOTc0NzNhNzUwMmZjYjgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.X5-_aTXnyX0lhmHGSh6JUubN4PSH6Y6hFkoYLGVSXgs)

##### SVG

To scratch a vector graphic you have to put the file in the same folder as the GUI.py and enter the name. The svg should only contain lines and curves as full area scratching is not supported yet. As the scratch will just follow the line like a trajectory, it is possible to create larger surfaces by putting lines close to one another. The svg will be scaled automatically to the maximun size inside the well. If you want it to be smaller you can adjust the scale parameter to values between 1 (maximun size) and zero (basically a point).
![SVG](https://private-user-images.githubusercontent.com/90255355/366449031-0ffc8c30-f217-4c1c-98f2-72a6498d6566.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjYwNjQ4NjcsIm5iZiI6MTcyNjA2NDU2NywicGF0aCI6Ii85MDI1NTM1NS8zNjY0NDkwMzEtMGZmYzhjMzAtZjIxNy00YzFjLTk4ZjItNzJhNjQ5OGQ2NTY2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTExVDE0MjI0N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTBmMDU1MmJiMWUyZDg4OTgyODIyOTRhYmMyNmIwMjM1M2ExNjM4NTg5MTk1NDIzNzFmNjM1N2M1MjJmODI0MDYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.wvKChsnhkhoRdtjMz2rJWERlHSqboqKIw1na7bqBJBI)

#### Movement settings

Next to the patterns you can enter the movement speed of the printhead during moving and scratching in mm/s. Be aware that there are limitations to these speeds in the printer settings, mainly noticeable for the z-speed. If you want to scratch your pattern multiple times you can increase the "Scratch Cycles" from 1 to how many you like. To use the autoleveling function of your printer it has to be enabled with a tickbox here.

#### Cleaning

If you want to clean the tip before/after scratching a well plate, you can place one or more cleaning containers and specify their coordinates in a "clean.txt" file. An example of the file content is provided below. The cleaning will draw circles with "Number" amount of cirlces, "Depth" and "Radius" inside the cleaning container. The depth is relative to the specified "Z" coordinate. The "/" marks the end of the data for one container. You can add as many of these sections as you like.

~~~bash
X: 150
Y: 120
Z: 30
Radius: 4
Depth: 10
Number: 20
/
~~~

When the "Pause Before Clean" checkbox is ticked the tip will wait 1 cm over the specified XYZ coordinates. This makes it easy to position your cleaning container without exactly measuring the coordinates.

#### Load well setting

On the right side of the GUI you have to provide the well data. As the wells are mostly standardized we are reading the well data from a *.txt file, as it is easy to share, modify and reuse. An example of such a file is included in the repository as "24well.txt".

In general the file contains seven values that completely describe the wells.

e.g 24well.txt

number_x: 6          # number of wells in x Direction
number_y: 4          # number of wells in y Direction
diameter: 15.5       # diameter of each well
depth: 17.3          # depth of each well
distance_well: 3.5   # distamce between each well
distance_x: 7.8      # distance from the outer well to the wall in x Direction
distance_y: 6.0      # distance from the outer well to the wall in y Direction

In case of uncertainties, there is also an image that shows these required values above.

#### Select wells to scratch

After loading the well file, the layout should be plotted in the central area of the GUI. By clicking a well it turns red and will be excluded from scratching. Dragging your clicked mouse and releasing it will also select/deselect all wells underneath. The well in the bottom left corner represents the well closest to the coordinate origin, wich is the home position of your printer. It is usually the bottom left corner of the printbed as well.

#### Generate G-Code

The final step is to enter the name of your *.gcode file and to generate the G-Code. BEFORE running it on the 3D-Printer be sure to read the next chapter. In the future there might be the option to send the generated G-Code right from the GUI over W-Lan, until then you need to save the G-Code on a SD-Card and plug into the 3d-printer.

### Running the G-Code

Before running the G-Code on your machine be sure to have the bed leveled or correctly prepared for the autoleveling option. The guides and the well should be in place by now. Also remove the scratching tip, as the printer will home before scratching. Otherwise it would drive the tip into the print bed. After starting the print the "M00" G-Code command will stop the printer before scratching to insert the tip. Make sure your printer firmware supports this command! After inserting the tip just continue the print, usually by pressing the knob.

After scratching remove the tip again and end the print.
