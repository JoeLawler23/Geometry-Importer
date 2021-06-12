from typing import List, Tuple
import unittest
import importer

__author__ = 'Joseph Lawler'
__version__ = '1.1.0'

class DXF_Error_Tests(unittest.TestCase):
    """
    Test cases that should produce errors
    """
    def test_no_file_found(self):
        """
        No file found import_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_dxf_file(""))
    def test_no_extension(self):
        """
        File missing extension import_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: importer.export_dxf_file("Test Files/test3",[]))
    def test_no_geometries(self):
        """
        No passed geometry to export_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: importer.export_dxf_file("Test Files/test3.dxf",[]))

class DXF_Import_Tests(unittest.TestCase):
    """
    Test cases for individual geometries
    """
    def test_basic_point(self):
        """
        Basic Point - only one point in 2D
        """
        # Import 'Basic Point.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic Point.dxf")
        
        # Check if equal to predetermined values
        point = geometries[0][1][0]  # [0] - First geometry, [1] - Point's values/tuples, [0] - First value/tuple
        self.assertEqual(point,(0.0,0.0,0.0))  # Check point
    def test_complex_points(self):
        """
        Complex points - multiple points in 3D
        """
        # Import 'Complex Points.dxf'
        geometries = importer.import_dxf_file("Test Files/Complex Points.dxf")

        # Generate predetermined values
        points: List[Tuple[float,...]] = []
        points.append([(0.0,0.0,-25.0*10**3)])  # Point 1
        points.append([(25.0*10**3,0.0,-25.0*10**3)])  # Point 2
        points.append([(25.0*10**3,0.0,0.0)])  # Point 3
        points.append([(0.0,0.0,0.0)])  # Point 4

        # Check if each predetermined value has an associated imported value
        verified_geometries: int = 0
        for geometry in geometries:
            for point in points:
                geometry_values = geometry[1][0]
                if within_a_percent_tuple(point[0],geometry_values):
                    verified_geometries += 1
        self.assertEqual(verified_geometries, len(points))
    def test_basic_line(self):
        """
        Basic Line - only one line in 2D
        """
        # Import 'Basic Line.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic Line.dxf")

        # Check if equal to predetermined value
        line = geometries[0][1]
        self.assertEqual(line[0],(0.0,0.0,0.0))  # Check start point
        self.assertEqual(line[1],(50.0*10**3,0.0,0.0))  # Check end point
    def test_complex_lines(self):
        """
        Complex lines - multiple lines in 3D
        """
        # Import 'Complex Lines.dxf'
        geometries = importer.import_dxf_file("Test Files/Complex Lines.dxf")

        # Generate predetermined values
        lines: List[Tuple[float,...]] = []
        lines.append([(0.0,0.0,0.0),(50.0*10**3,0.0,0.0)])  # Horizontal Line (0.0,0.0,0.0)mm -> (50.0,0.0,0.0)mm
        lines.append([(0.0,-25.0*10**3,0.0),(50.0*10**3,-25.0*10**3,0.0)])  # Horizontal Line (0.0,-25.0,0.0)mm -> (50.0,-25.0,0.0)mm
        lines.append([(0.0,-50.0*10**3,0.0),(50.0*10**3,-50.0*10**3,0.0)])  # Horizontal Line (0.0,-50.0,0.0)mm -> (50.0,-50.0,0.0)mm
        lines.append([(0.0,-75.0*10**3,0.0),(50.0*10**3,-75.0*10**3,0.0)])  # Horizontal Line (0.0,-75.0,0.0)mm -> (50.0,-75.0,0.0)mm
        lines.append([(0.0,-100.0*10**3,0.0),(50.0*10**3,-100.0*10**3,0.0)])  # Horizontal Line (0.0,-100.0,0.0)mm -> (50.0,-100.0,0.0)mm
        lines.append([(0.0,0.0,25.0*10**3),(50.0*10**3,0.0,25.0*10**3)])  # Horizontal Line (0.0,0.0,25.0)mm -> (50.0,0.0,25.0)mm
        lines.append([(0.0,0.0,50.0*10**3),(50.0*10**3,0.0,50.0*10**3)])  # Horizontal Line (0.0,0.0,50.0)mm -> (50.0,0.0,50.0)mm
        lines.append([(0.0,0.0,75.0*10**3),(50.0*10**3,0.0,75.0*10**3)])  # Horizontal Line (0.0,0.0,75.0)mm -> (50.0,0.0,75.0)mm
        lines.append([(0.0,0.0,100.0*10**3),(50.0*10**3,0.0,100.0*10**3)])  # Horizontal Line (0.0,0.0,100.0)mm -> (50.0,0.0,100.0)mm
        lines.append([(50.0*10**3,0.0,100.0*10**3),(50.0*10**3,-100.0*10**3,0.0)])  # Diagonal Line 
        lines.append([(50.0*10**3,-25.0*10**3,0.0),(50.0*10**3,0.0,25.0*10**3)])  # Diagonal Line
        lines.append([(50.0*10**3,-50.0*10**3,0.0),(50.0*10**3,0.0,50.0*10**3)])  # Diagonal Line
        lines.append([(50.0*10**3,-75.0*10**3,0.0),(50.0*10**3,0.0,75.0*10**3)])  # Diagonal Line
        lines.append([(0.0,-25.0*10**3,0.0),(0.0,0.0,25.0*10**3)])  # Diagonal Line 
        lines.append([(0.0,-50.0*10**3,0.0),(0.0,0.0,50.0*10**3)])  # Diagonal Line 
        lines.append([(0.0,-75.0*10**3,0.0),(0.0,0.0,75.0*10**3)])  # Diagonal Line 
        lines.append([(0.0,-100.0*10**3,0.0),(50.0*10**3,-100.0*10**3,0.0)])  # Diagonal Line 

        # Check if each predetermined value has an associated imported value
        verified_geometries: int = 0
        for geometry in geometries:
            for line in lines:
                geometry_values = geometry[1]
                if within_a_percent_tuple(line[0],geometry_values[0]) and within_a_percent_tuple(line[1],geometry_values[1]):
                    verified_geometries += 1
        self.assertEqual(verified_geometries, len(lines))
    def test_basic_circles(self):
        """
        Basic Circle - only one circle in 2D
        """
        # Import 'Basic Circle.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic Circle.dxf")

        # Check if equal to predetermined values
        circle = geometries[0]
        self.assertEqual(circle[1][0],(0.0,0.0,0.0))  # Check center
        self.assertTrue(circle[1][1],(15000.0,0.0,360.0))  # Check radius, start angle, end angle
    def test_complex_circles(self):
        """
        Complex circles - multiple circles in 3D with various angles and positions
        """
        # Import 'Complex Circles.dxf'
        geometries = importer.import_dxf_file("Test Files/Complex Circles.dxf")

        # Generate predetermined values
        circles: List[Tuple[float,...]] = []
        circles.append([(0.0,0.0,0.0),(25*10**3,0.0,360.0)])  # Circle at 0,0,0 with radius 25mm 
        circles.append([(50.0*10**3,0.0,0.0),(20*10**3,0.0,360.0)])  # Circle at 50,0,0 with radius 20mm 
        circles.append([(100.0*10**3,0.0,0.0),(15*10**3,0.0,360.0)])  # Circle at 100,0,0 with radius 15mm 
        circles.append([(150.0*10**3,0.0,0.0),(10*10**3,0.0,360.0)])  # Circle at 150,0,0 with radius 10mm 
        circles.append([(200.0*10**3,0.0,0.0),(5*10**3,0.0,360.0)])  # Circle at 200,0,0 with radius 5mm 
        circles.append([(0.0,50.0*10**3,50.0*10**3),(25*10**3,0.0,360.0)])  # Circle at 0,50,50 with radius 25mm 
        circles.append([(50.0*10**3,50.0*10**3,50.0*10**3),(20*10**3,0.0,360.0)])  # Circle at 50,50,50 with radius 20mm 
        circles.append([(100.0*10**3,50.0*10**3,50.0*10**3),(15*10**3,0.0,360.0)])  # Circle at 100,50,50 with radius 15mm 
        circles.append([(150.0*10**3,50.0*10**3,50.0*10**3),(10*10**3,0.0,360.0)])  # Circle at 150,50,50 with radius 10mm 
        circles.append([(200.0*10**3,50.0*10**3,50.0*10**3),(5*10**3,0.0,360.0)])  # Circle at 200,50,50 with radius 5mm 
        
        # Check if each predetermined value has an associated imported value
        verified_geometries: int = 0
        for geometry in geometries:
            for circle in circles:
                geometry_values = geometry[1]
                if within_a_percent_tuple(circle[0],geometry_values[0]) and within_a_percent_tuple(circle[1],geometry_values[1]):
                    verified_geometries += 1
        self.assertEqual(verified_geometries, len(circles))
    def test_basic_arc(self):
        """
        Basic Arc - only one arc in 2D
        """
        # Import 'Basic Arc.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic Arc.dxf")

        # Check if equal to predetermined values
        arc = geometries[0][1]
        self.assertTrue(arc[0],(0.0,0.0,0.0))  # Check center
        self.assertTrue(within_a_percent_tuple(arc[1],(10.0*10**3,0.0,180.0)))  # Check radius, start angle, end angle
    def test_complex_arcs(self):
        """
        Complex Arcs - multiple Arcs in 3D
        """
        # Import 'Complex Arcs.dxf'
        geometries = importer.import_dxf_file("Test Files/Complex Arcs.dxf")

        # Generate predetermined values
        arcs: List[Tuple[float,...]] = []
        arcs.append([(0.0,0.0,0.0),(20.0*10**3,-90.0,90.0)])
        arcs.append([(0.0,-75.0*10**3,0.0),(25.0*10**3,-90.0,180.0)])
        arcs.append([(0.0,-75.0*10**3,0.0),(20.0*10**3,-90.0,180.0)])
        
        # Check if each predetermined value has an associated imported value
        verified_geometries: int = 0
        for geometry in geometries:
            for arc in arcs:
                geometry_values = geometry[1]
                if within_a_percent_tuple(arc[1],geometry_values[1]) and within_a_percent_tuple(arc[0],geometry_values[0]):
                    verified_geometries += 1
        self.assertEqual(verified_geometries, len(arcs))
    def test_basic_ellipse(self):
        """
        Basic Ellipse - only one ellipse in 2D
        """
        # Import 'Basic Ellipse.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic Ellipse.dxf")

        # Check if equal to predetermined values
        ellipse = geometries[0][1]
        self.assertTrue(ellipse[0],(0.0,0.0,0.0))  # Check center
        self.assertTrue(within_a_percent_tuple(ellipse[1],(25.0*10**3,0.0,0.0)))  # Length of Major Axis
        self.assertTrue(within_a_percent(ellipse[2][0],0.6))  # Ratio of Minor to Major Axis
    def test_complex_ellipsis(self):
        """
        Complex Ellipsis - multiple ellipses in 3D
        """
        # Import 'Complex Ellipses.dxf'
        geometries = importer.import_dxf_file("Test Files/Complex Ellipses.dxf")

        # Generate predetermined values
        ellipsis: List[Tuple[float,...]] = []
        ellipsis.append([(0.0,0.0,0.0),(25.0*10**3,0.0,0.0),0.5])  # Ellipse on x-axis
        ellipsis.append([(0.0,0.0,0.0),(-25.0*10**3,0.0,0.0),0.5])  # Ellipse on y-axis
        ellipsis.append([(50.0*10**3,0.0,0.0),(10.0*10**3,0.0,0.0),1.0])  # Ellipse with ratio 1.0
        ellipsis.append([(50.0*10**3,0.0,0.0),(0.0,20.0*10**3,0.0),0.5])  # Ellipse with ratio 0.5 with major axis on y
        ellipsis.append([(50.0*10**3,0.0,0.0),(20.0*10**3,0.0,0.0),0.5])  # Ellipse with ratio 0.5 with major axis on x
        
        # Check if each predetermined value has an associated imported value
        verified_geometries: int = 0
        for geometry in geometries:
            for ellipse in ellipsis:
                geometry_values = geometry[1]
                if within_a_percent_tuple(ellipse[0],geometry_values[0]) and within_a_percent_tuple(ellipse[1],geometry_values[1]) and within_a_percent(ellipse[2],geometry_values[2][0]):
                    verified_geometries += 1
        self.assertEqual(verified_geometries, 6)
    def test_basic_spline(self):
        """
        Basic Spline - only one line in 2D
        """
        # Import 'Basic Spline.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic Spline.dxf")

        # Check if equal to predetermined values
        spline = geometries[0][1]
        self.assertTrue(spline[0][0],5)  # Degree 5
        self.assertTrue(spline[0][1],1)  # Closed true
        self.assertTrue(spline[0][2],15)  # # Control Points
        self.assertTrue(spline[0+spline[0][1]],21)  # # Knots
        self.assertTrue(spline[1+spline[0][1]],15)  # # Weights
    def test_basic_lwpolyline(self):
        """
        Basic LWPolyline - only one line in 2D
        """
        # Import 'Basic LWPolyline.dxf'
        geometries = importer.import_dxf_file("Test Files/Basic LWPolyline.dxf")

        # Check if equal to predetermined values
        lwpolyline = geometries[0][1]
        self.assertTrue(within_a_percent_tuple(lwpolyline[0],(25.0*10**3,0.0,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(within_a_percent_tuple(lwpolyline[1],(0.0,0.0,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(within_a_percent_tuple(lwpolyline[2],(0.0,25.0*10**3,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(within_a_percent_tuple(lwpolyline[3],(25.0*10**3,25.0*10**3,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(lwpolyline[4])  # Closed true

class TXT_Error_Tests(unittest.TestCase):
    """
    Test cases that should produce errors
    """
    def test_no_file_found(self):
        """
        No file found import_txt_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_txt_file(""))
    def test_no_extension(self):
        """
        File missing extension import_txt_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_txt_file("Test Files/test_geometries"))

class TXT_Import_Tests(unittest.TestCase):
    """
    Tests for importing txt files
    """
    def test_2d_point(self):
        """
        One 2D point
        """
        geometries = importer.import_txt_file("Test Files/text_2d.txt")
        self.assertEqual(geometries[0][1],(1.1,2.2))
    def test_3d_point(self):
        """
        One 3D point
        """
        geometries = importer.import_txt_file("Test Files/text_3d.txt",)
        self.assertEqual(geometries[0][1],(1.1,2.2,3.3))
    def test_various_percision(self):
        """
        Varying percision of points
        """
        geometries = importer.import_txt_file("Test Files/text_precision.txt")
        self.assertEqual(geometries[0][1],(1.1,2.2,3.3))
        self.assertEqual(geometries[1][1],(1.11,2.22,3.33))
        self.assertEqual(geometries[2][1],(1.111,2.222,3.333))
        self.assertEqual(geometries[3][1],(1.1111,2.2222,3.3333))
    def test_no_points(self):
        """
        No points
        """
        geometries = importer.import_txt_file("Test Files/text_no_points.txt")
        self.assertEqual(len(geometries),0)

class CSV_Error_Tests(unittest.TestCase):
    """
    Test cases that should produce errors
    """
    def test_no_file_found(self):
        """
        No file found import_csv_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_csv_file(""))
    def test_no_extension(self):
        """
        File missing extension import_csv_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_csv_file("Test Files/test_geometries"))

class CSV_Import_Tests(unittest.TestCase):
    """
    Tests for importing csv files
    """
    def test_basic(self):
        """
        General test - one of each geometry
        """
        # Import 'test.csv'
        geometries = importer.import_csv_file("Test Files/test.csv")

        # POINT
        self.assertEqual(geometries[0][1][0],(1.0,2.0,3.0))

        # LINE
        self.assertEqual(geometries[1][1][0],(1.0,2.0,3.0))
        self.assertEqual(geometries[1][1][1],(4.0,5.0,6.0))

        # ARC
        self.assertEqual(geometries[2][1][0],(1.0,2.0,3.0))
        self.assertEqual(geometries[2][1][1],(4.0,5.0,6.0))

        # ELLIPSE
        self.assertEqual(geometries[3][1][0],(1.0,2.0,3.0))
        self.assertEqual(geometries[3][1][1],(4.0,0.0,0.0))
        self.assertEqual(geometries[3][1][2],(5.0,))

# Verification functions

def within_a_percent_tuple(tuple1: tuple[float,...], tuple2: tuple[float,...]) -> bool:
    for i in range (len(tuple1)):
        float1: float = tuple1[int(i)]
        float2: float = tuple2[int(i)]
        if float1 == 0 and abs(float2-float1) > 0.001:
            return False
        if float2 == 0 and abs(float1-float2) > 0.001:
            return False
        if float1 != 0 and float2 != 0 and abs( (float1 - float2) / float(float1) ) > 0.001: # less than a tenth of a percent
            return False
    return True

def within_a_percent(float1: float, float2: float) -> bool:
    if float1 == 0 and abs(float2-float1) > 0.001:
         return False
    if float1 != 0 and abs( (float1 - float2) / float(float1) ) > 0.001: # less than a tenth of a percent
         return False
    return True