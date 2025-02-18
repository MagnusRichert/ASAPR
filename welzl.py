import random
import math
from typing import List, Tuple

class Welzl:
    """
    Welzl's algorithm implementation for finding the minimal enclosing disk for a set of points.

    Classes:
        Welzl: Contains static methods to compute the minimal enclosing disk using Welzl's algorithm.

    Type Definitions:
        Point: A tuple representing a point in 2D space with x and y coordinates as floats.
        Disk: A tuple representing a disk with a center (Point) and a radius (float).

    Static Methods:
        dist(p1: 'Welzl.Point', p2: 'Welzl.Point') -> float:
            Calculate the Euclidean distance between two points.

        circle_from_two_points(p1: 'Welzl.Point', p2: 'Welzl.Point') -> 'Welzl.Disk':
            Return the minimal disk that passes through two points.

        circle_from_three_points(p1: 'Welzl.Point', p2: 'Welzl.Point', p3: 'Welzl.Point') -> 'Welzl.Disk':
            Return the minimal disk that passes through three points.

        trivial(R: List['Welzl.Point']) -> 'Welzl.Disk':
            Return the minimal disk that passes through points in R.

        is_in_disk(p: 'Welzl.Point', d: 'Welzl.Disk') -> bool:
            Check if point p is inside or on the boundary of disk d.

        welzl(P: List['Welzl.Point'], R: List['Welzl.Point'] = []) -> 'Welzl.Disk':
            Welzl's algorithm to find the minimal disk enclosing P with R on the boundary.

        perform_welzl(svg_lines):
            Perform Welzl algorithm on svg_data and return center and radius of disk.
    """
    Point = Tuple[float, float]
    Disk = Tuple[Point, float]

    @staticmethod
    def dist(p1: 'Welzl.Point', p2: 'Welzl.Point') -> float:
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    @staticmethod
    def circle_from_two_points(p1: 'Welzl.Point', p2: 'Welzl.Point') -> 'Welzl.Disk':
        """Return the minimal disk that passes through two points."""
        center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        radius = Welzl.dist(p1, p2) / 2
        return center, radius

    @staticmethod
    def circle_from_three_points(p1: 'Welzl.Point', p2: 'Welzl.Point', p3: 'Welzl.Point') -> 'Welzl.Disk':
        """Return the minimal disk that passes through three points."""
        ax, ay = p1
        bx, by = p2
        cx, cy = p3
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if d == 0:
            d1 = Welzl.dist(p1, p2)
            d2 = Welzl.dist(p2, p3)
            d3 = Welzl.dist(p1, p3)
            if d1 >= d2 and d1 >= d3:
                return Welzl.circle_from_two_points(p1, p2)
            elif d2 >= d1 and d2 >= d3:
                return Welzl.circle_from_two_points(p2, p3)
            else:
                return Welzl.circle_from_two_points(p1, p3)
        ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
        uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
        center = (ux, uy)
        radius = Welzl.dist(center, p1)
        return center, radius

    @staticmethod
    def trivial(R: List['Welzl.Point']) -> 'Welzl.Disk':
        """Return the minimal disk that passes through points in R."""
        if len(R) == 0:
            return (0, 0), 0
        elif len(R) == 1:
            return R[0], 0
        elif len(R) == 2:
            return Welzl.circle_from_two_points(R[0], R[1])
        elif len(R) == 3:
            return Welzl.circle_from_three_points(R[0], R[1], R[2])
        else:
            raise ValueError("R can contain at most 3 points")

    @staticmethod
    def is_in_disk(p: 'Welzl.Point', d: 'Welzl.Disk') -> bool:
        """Check if point p is inside or on the boundary of disk d."""
        center, radius = d
        return Welzl.dist(p, center) <= radius

    @staticmethod
    def welzl(P: List['Welzl.Point'], R: List['Welzl.Point'] = []) -> 'Welzl.Disk':
        """Welzl's algorithm to find the minimal disk enclosing P with R on the boundary."""
        if len(P) == 0 or len(R) == 3:
            return Welzl.trivial(R)

        p = random.choice(P)
        P.remove(p)

        D = Welzl.welzl(P, R)

        if Welzl.is_in_disk(p, D):
            P.append(p)
            return D

        R.append(p)
        D = Welzl.welzl(P, R)
        R.remove(p)
        P.append(p)

        return D


