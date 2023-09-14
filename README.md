# Scratch me Baby

An approach to automating Scratch Essays with 3D Printers and Custom G-Code.

## What is a scratch essay?

Divide cells and study regrowth
![Cell growth](https://cytosmart.com/sites/default/files/inline-images/wound-healing-assay-fig-1.jpeg)

## Why do we need to automate it?

- repeatable
- manual labor sucks, otherwise done by hand, not accurate
- cheap (current alternativve machine expensive)

## What can be done with this repository?
- scratch custom wells
- use one of 3 scratch patterns: line, mesh, circle

## How to use this repository
Here we will discuss how to use this repository for your scratch essay and what you need

### Bill of Materials
- 3D-Printer (no auto leveling preferrably)
- Luer Lock adapter with M6 thread
- tip for Luer Lock adapter
- 7mm wrench
- piece of paper

### Preparation
In this chapter all necessary steps to prepare the printer are discussed.

#### Remove the nozzle
The first step is to remove the nozzle of the old printer with a 7mm wrench. Afterwards screw in the Luer Lock adapter that will be used to hold the tips.

#### Level the printbed
To level the printbed first home the printer. Then disable the motors so you can freely slide the printhead in the XY-plane.
Now slide a sheet of paper between your adapter in the printhead and and your printbed. Visit every corner respectively and tighten/release the screws until you feel a bit of resistance.
The amount of resistance should be the same for each corner. You can also level the bed by eye so that the distance between the adapter and the printbed is the same for each corner.
The actual distance between insert and bed is not important it just has to be consistant.

#### Autolevel the printbed
In developement...

#### Mount the posiotioning for your wells
The next step is to mount your positioning guide for the well on the buildplate. It is important that the sides of your guide/well align with the X- and Y-axis. A magnetic printbed is not recommended as it can slip and loose the position.
If you scratch wells with different sizes it is recommendet to have permanent position guides in the lowest XY-corner and variable guides for the other sides, see picture below.
![Positioning Guides](pictures/guide.png)
This way you only have to get the x_offset and y_offset once. The offsets are shown in the picture below.
![Offset](pictures/offset.png)

#### Measure offsets
To measure the offsets you have to home your printer and put the well on the buildplate. Then use the "move" function of your printer to bring the z-axis high enough that you can insert a tip.
Using the "move" function the printer will always display the current position of the axis you are moving. This value is the offset we need.
First you have to move the tip to the X and Y edges closest to the home position respectively so that the tip barely touches them. For Y the printhead was moved to 24.8mm in the example picture below.
![Offset Y](pictures/offset_y.png)
To get your offset values for X and Y you still have to add the radius of the tip you used. For example it has a diameter of 0.4mm: offset_y = Y + d/2 = 24.8mm + 0.2mm = 25.0mm

For the Z offset just move the printhead until the tip touches the well, see picture:
![Offset Z](pictures/offset_z.png)
The Z value can directly be used as the offset. When using a different tip you have to adjust the Z offset again. It is possible to just measure the difference in length of the tips and adjust the offset accordingly.



### Skript usage
In development...

