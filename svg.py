import tkinter as tk
from tkinter import messagebox
from svgpathtools import svg2paths, CubicBezier, QuadraticBezier, Arc, Line, Path
import numpy as np
import sys
import os
from plotables import Plotables
from circlegrid import CircleGrid
from welzl import Welzl

class Svg(Plotables):
    def __init__(self):
        super.__init__()
        self.resolution = 0.1  # line length to approximate non-line segments of paths
        self.path_accuracy = 0.01  # if start and endpoint of a line are closer than this, they are considered the same point

    def generate_gcode(self, svg_paths_scaled, center_x, center_y, depth):
        gcode_name = self.gcode_name_field.get() 
        speed_move = float(self.speed_move_field.get())
        speed_scratch = float(self.speed_scratch_field.get())
        multi_scratch = int(self.multi_scratch_field.get())

        with open(f"{gcode_name}", 'w') as gcode:
            for _ in range(multi_scratch):
                previous_end = (-10**10, -10**10)  # Set initial end outside of coordinate range
                for path_index in range(len(svg_paths_scaled)):
                    svg_paths_scaled = Path()
                    for line in svg_paths_scaled[path_index]:
                        start = self.calculate_shifted_xy(start, center_x, center_y)
                        end = self.calculate_shifted_xy(end, center_x, center_y)
                        if Welzl.dist(start, previous_end) > self.path_accuracy:
                            gcode.writelines(f"G0 Z{self.move_height + depth:.2f} F{speed_move:.0f}\n")
                            gcode.writelines(f"G0 X{start[0]:.2f} Y{start[1]:.2f}\n")
                            gcode.writelines(f"G0 Z{depth:.2f}\n")
                            gcode.write(f"G0 F{speed_scratch:.0f}\n")
                        gcode.writelines(f"G0 X{end[0]:.2f} Y{end[1]:.2f}\n")
                        previous_end = end

                   
    def scale_svg(self):
        """Scales the svg to fit into a well."""
        tip_offset = float(self.tip_offset_field.get())  
        svg_file = self.svg_file_field.get()
        svg_scale = float(self.svg_scale_field.get())
        svg_lines, svg_paths, svg_attributes = self.approximate_svg_with_lines(svg_file, resolution=self.resolution)
        svg_center, svg_radius = self.perform_welzl(svg_lines)

        svg_paths_scaled = Path()
        for path_index in range(len(svg_paths)): 
            svg_path = Path()               
            for line in svg_paths[path_index]:
                start = self.calculate_scaled_xy(line.start, svg_center, svg_radius, svg_scale, tip_offset)
                end = self.calculate_scaled_xy(line.end, svg_center, svg_radius, svg_scale, tip_offset)
                svg_path.append(Line(complex(start[0], start[1]), complex(end[0], end[1])))

            fill_property = False
            if svg_attributes[path_index].get('style') is not None:
                find_value = svg_attributes[path_index].get('style').find('fill:none')
                fill_property = (find_value == -1)
            elif svg_attributes[path_index].get('fill') is not None:
                fill_property = (svg_attributes[path_index].get('fill') != 'none')
            else:
                messagebox.showwarning("Generate gcode", "No supported fill property found for one or more paths. Proceeding without fill for those paths.")

            if not fill_property:
                continue
            
            xmin, xmax, ymin, ymax = svg_path.bbox()

            tip_diameter = float(self.tip_diameter_field.get())
            overlap = float(self.svg_overlap_field.get())
            line_distance = tip_diameter - overlap * tip_diameter * 0.5
            svg_fill_path = Path()
            if (xmax - xmin) > (ymax - ymin):
                if (ymax - ymin) <= line_distance:
                    continue

                num_lines = int(np.ceil((ymax - ymin)) / line_distance) + 1
                y_coordinates = np.linspace(ymin, ymax, num_lines)
                for current_coordinate in y_coordinates[1:-1]:
                    helpline = Line(complex(xmin - 1, current_coordinate), complex(xmax + 1, current_coordinate))
                    intersections = svg_path.intersect(helpline)
                    number_intersections = len(intersections)
                    if number_intersections % 2 == 1:
                        helpline = Line(complex(xmin - 1, current_coordinate + line_distance * 0.05), complex(xmax + 1, current_coordinate + line_distance * 0.05))
                        intersections = svg_path.intersect(helpline)
                        number_intersections = len(intersections)
                    if number_intersections % 2 == 1:
                        helpline = Line(complex(xmin - 1, current_coordinate - line_distance * 0.05), complex(xmax + 1, current_coordinate - line_distance * 0.05))
                        intersections = svg_path.intersect(helpline)
                        number_intersections = len(intersections)
                    if number_intersections % 2 == 1:
                        if not fill_error_thrown:
                            messagebox.showerror("Generate gcode", "Could not fill form completely.")
                            fill_error_thrown = True
                        break

                    intersection_points = list()
                    y_coordinate = 0.0
                    for l in intersections:
                        point = helpline.point(l[1][0])
                        intersection_points.append(point.real)
                        y_coordinate = point.imag

                    intersection_points.sort()
                    for l in range(int(len(intersection_points) / 2)):
                        x_start = intersection_points[2 * l]
                        start_point = complex(x_start + tip_diameter * 0.2, y_coordinate)
                        x_end = intersection_points[2 * l + 1]
                        end_point = complex(x_end - tip_diameter * 0.2, y_coordinate)
                        line = Line(start_point, end_point)
                        svg_fill_path.append(line)

            else:
                if (xmax - xmin) <= line_distance:
                    continue

                num_lines = int(np.ceil((xmax - xmin)) / line_distance) + 1
                x_coordinates = np.linspace(xmin, xmax, num_lines)
                for current_coordinate in x_coordinates[1:-1]:
                    helpline = Line(complex(current_coordinate, ymax + 1), complex(current_coordinate, ymin - 1))
                    intersections = svg_path.intersect(helpline)
                    number_intersections = len(intersections)
                    if number_intersections % 2 == 1:
                        helpline = Line(complex(current_coordinate + line_distance * 0.05, ymax + 1), complex(current_coordinate + line_distance * 0.05, ymin - 1))
                        intersections = svg_path.intersect(helpline)
                        number_intersections = len(intersections)
                    if number_intersections % 2 == 1:
                        helpline = Line(complex(current_coordinate - line_distance * 0.05, ymax + 1), complex(current_coordinate - line_distance * 0.05, ymin - 1))
                        intersections = svg_path.intersect(helpline)
                        number_intersections = len(intersections)
                    if number_intersections % 2 == 1:
                        if not fill_error_thrown:
                            messagebox.showerror("Generate gcode", "Could not fill form.")
                            fill_error_thrown = True
                        break

                    intersection_points = list()
                    x_coordinate = 0.0
                    for l in intersections:
                        point = helpline.point(l[1][0])
                        intersection_points.append(point.imag)
                        x_coordinate = point.real

                    intersection_points.sort()
                    for l in range(int(len(intersection_points) / 2)):
                        y_start = intersection_points[2 * l]
                        start_point = complex(x_coordinate, y_start + tip_diameter * 0.2)
                        y_end = intersection_points[2 * l + 1]
                        end_point = complex(x_coordinate, y_end - tip_diameter * 0.2)
                        line = Line(start_point, end_point)
                        svg_fill_path.append(line)

            svg_paths_scaled.append(svg_path)
            svg_paths_scaled.append(svg_fill_path)


    def line_through_x(self, center_x, diameter, tip_offset, y_offset = 0):
        """Calculates the start and end points of a line through a circle in x direction, a y_offset<radius can be provided to shorten the line"""
        radius = diameter / 2.0
        offset_length = ((radius-tip_offset)**2-y_offset**2)**0.5
        start_x = center_x - offset_length
        end_x = center_x + offset_length

        return start_x, end_x
    
    def line_through_y(self, center_y, diameter, tip_offset, x_offset = 0):
        """Calculates the start and end points of a line through a circle in y direction, an x_offset<radius can be provided to shorten the line"""
        radius = diameter / 2.0
        offset_length = ((radius-tip_offset)**2-x_offset**2)**0.5
        start_y = center_y - offset_length
        end_y = center_y + offset_length

        return start_y, end_y

    def sample_segment(self, seg, chord_length=0.1):
        """
        Sample a non line segment into line segments with the length "chord_length".
        """
        #similar to implementation of seg2lines() in path.py from svgpathtools
        #num_lines = int(np.ceil(seg.length() / chord_length))
        num_lines = 20
        points = [seg.point(i) for i in np.linspace(0, 1, num_lines+1)]
        return [Line(points[i], points[i + 1]) for i in range(num_lines)]


    def approximate_svg_with_lines(self, svg_file, resolution=0.1):
        """
        Convert all paths in an SVG file into a list of line segments, as well as the paths and the attributes.
        """
        paths, attributes = svg2paths(svg_file)
        
        line_segments = []

        for path in paths:
            for segment in path:
                if isinstance(segment, Line):
                    line_segments.append(segment)
                elif isinstance(segment, (CubicBezier, QuadraticBezier, Arc)):
                    lines = self.sample_segment(segment, resolution)
                    line_segments.extend(lines)

        return line_segments, paths, attributes

    def calculate_scaled_xy(self, point, svg_center, svg_radius, svg_scale, tip_offset):
        """
        Calculates the scaled (X, Y) point from imaginary point.
        """
        x = (((point.real - svg_center[0]) / (svg_radius * 2)) * (svg_scale * (self.well_data['diameter'] - tip_offset * 2)))
        y = (((point.imag - svg_center[1]) / (svg_radius * 2)) * (svg_scale * (self.well_data['diameter'] - tip_offset * 2)))
        return (x, y)
    
    def calculate_shifted_xy(self, point, center_x, center_y):
        """
        Calculates the shifted (X, Y) point from imaginary point.
        """
        x = (point[0] + center_x)
        y = (point[1] + center_y)
        return (x, y)

    def perform_welzl(self, svg_lines):
        """Perform Welzl algorithm on svg_data and return center and radius of disk"""
        points = []
        for line in svg_lines:
            start = line.start
            end = line.end
            points.append((start.real, start.imag))
            points.append((end.real, end.imag))
        return Welzl.welzl(points)     