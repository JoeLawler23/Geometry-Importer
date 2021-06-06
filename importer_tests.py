from typing import List, Tuple
import unittest
import importer

class DXF_Error_Tests(unittest.TestCase):
    """
    Test cases that should produce errors
    """
    def test_No_File_Found(self):
        """
        No file found import_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_dxf_file(""))
    def test_No_Extension(self):
        """
        File missing extension import_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: importer.export_dxf_file("Test Files/test3",[]))
    def test_No_Geometries(self):
        """
        No passed geometry to export_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: importer.export_dxf_file("Test Files/test3.dxf",[]))

class DXF_Import_Tests(unittest.TestCase):
    """
    Test cases for individual geometries
    """
    def test_Basic_Point(self):
        """
        Basic Point only one point in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic Point.dxf")
        point = geometries[0].get('POINT0')
        self.assertEquals(point,(0.0,0.0,0.0))  # Check point
    def test_Complex_Points(self):
        """
        Complex points multiple points in 3D
        """
        geometries = importer.import_dxf_file("Test Files/Complex Points.dxf")
        points: List[Tuple[float,...]] = []
        points.append([(0.0,0.0,-25.0*10**3)])  # Point 1
        points.append([(25.0*10**3,0.0,-25.0*10**3)])  # Point 2
        points.append([(25.0*10**3,0.0,0.0)])  # Point 3
        points.append([(0.0,0.0,0.0)])  # Point 4

        # Check if all 4 points are found in the imported file
        verified_geometries: int = 0
        for geometry in geometries:
            for point in points:
                geometry_values = list(geometry.values())
                if within_a_percent_tuple(point[0],geometry_values[0]) :
                    verified_geometries += 1
        self.assertEquals(verified_geometries, 4)
    def test_Basic_Line(self):
        """
        Basic Line only one line in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic Line.dxf")
        line = geometries[0].get('LINE0')
        self.assertEquals(line[0],(0.0,0.0,0.0))  # Check start point
        self.assertEquals(line[1],(50.0*10**3,0.0,0.0))  # Check end point
    def test_Complex_Lines(self):
        """
        Complex lines multiple lines in 3D
        """
        geometries = importer.import_dxf_file("Test Files/Complex Lines.dxf")
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

        # Check if all lines are found in imported file
        verified_geometries: int = 0
        for geometry in geometries:
            for line in lines:
                geometry_values = list(geometry.values())[0]
                if within_a_percent_tuple(line[0],geometry_values[0]) and within_a_percent_tuple(line[1],geometry_values[1]):
                    verified_geometries += 1
        self.assertEquals(verified_geometries, 17)
    def test_Basic_Circles(self):
        """
        Basic circle only one circle in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic Circle.dxf")
        circle = geometries[0].get('ARC0')
        self.assertEquals(circle[0],(0.0,0.0,0.0))  # Check center
        self.assertTrue(within_a_percent_tuple([15*10**3,0.0,360.0],circle[1]))  # Check radius
    def test_Complex_Circles(self):
        """
        Complex circles multiple circles in 3D with various angles and positions
        """
        geometries = importer.import_dxf_file("Test Files/Complex Circles.dxf")
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
        
        # Check if all circles are in imported file
        verified_geometries: int = 0
        for geometry in geometries:
            for circle in circles:
                geometry_values = list(geometry.values())[0]
                if within_a_percent_tuple(circle[1],geometry_values[1]) and within_a_percent_tuple(circle[0],geometry_values[0]):
                    verified_geometries += 1
        self.assertEquals(verified_geometries, 10)
    def test_Basic_Arc(self):
        """
        Basic Arc only one arc in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic Arc.dxf")
        arc = geometries[0].get('ARC0')
        self.assertTrue(arc[0],(0.0,0.0,0.0))  # Check center
        self.assertTrue(within_a_percent(arc[1][0],10.0*10**3))  # Check radius 10mm
        self.assertTrue(within_a_percent(arc[1][1],0.0))  # Check start angle
        self.assertTrue(within_a_percent(arc[1][2],180))  # Check end angle
        self.assertTrue(arc[1],(1.0,0.0,0.0))  # Check plane
    def test_Complex_Arcs(self):
        """
        Complex Arcs multiple Arcs in 3D
        """
        geometries = importer.import_dxf_file("Test Files/Complex Arcs.dxf")
        arcs: List[Tuple[float,...]] = []
        arcs.append([(0.0,0.0,0.0),(20.0*10**3,-90.0,90.0)])  # Arc 1
        arcs.append([(0.0,-75.0*10**3,0.0),(25.0*10**3,-90.0,180.0)])  # Arc 2
        arcs.append([(0.0,-75.0*10**3,0.0),(20.0*10**3,-90.0,180.0)])  # Arc 3
        
        # Check if all arcs are in imported file
        verified_geometries: int = 0
        for geometry in geometries:
            for arc in arcs:
                geometry_values = list(geometry.values())[0]
                if within_a_percent_tuple(arc[1],geometry_values[1]) and within_a_percent_tuple(arc[0],geometry_values[0]):
                    verified_geometries += 1
                    print(arc[1])
        self.assertEquals(verified_geometries, 3)
    def test_Basic_Ellipse(self):
        """
        Basic Ellipse only one ellipse in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic Ellipse.dxf")
        ellipse = geometries[0].get('ELLIPSE0')
        self.assertTrue(ellipse[0],(0.0,0.0,0.0))  # Check center
        self.assertTrue(within_a_percent_tuple(ellipse[1],(25.0*10**3,0.0,0.0)))  # Length of Major Axis 25mm
        self.assertTrue(within_a_percent(ellipse[2],0.6))  # Ratio of Minor to Major Axis 30:50
    def test_Complex_Ellipsis(self):
        """
        Complex Ellipsis multiple ellipses in 3D
        """
        geometries = importer.import_dxf_file("Test Files/Complex Ellipses.dxf")
        ellipsis: List[Tuple[float,...]] = []
        ellipsis.append([(0.0,0.0,0.0),(25.0*10**3,0.0,0.0),0.5])  # Ellipse on x-axis
        ellipsis.append([(0.0,0.0,0.0),(-25.0*10**3,0.0,0.0),0.5])  # Ellipse on y-axis
        ellipsis.append([(50.0*10**3,0.0,0.0),(10.0*10**3,0.0,0.0),1.0])  # Ellipse with ratio 1.0
        ellipsis.append([(50.0*10**3,0.0,0.0),(0.0,20.0*10**3,0.0),0.5])  # Ellipse with ratio 0.5 with major axis on y
        ellipsis.append([(50.0*10**3,0.0,0.0),(20.0*10**3,0.0,0.0),0.5])  # Ellipse with ratio 0.5 with major axis on x
        
        # Check if imported file contains all ellipsis
        verified_geometries: int = 0
        for geometry in geometries:
            for ellipse in ellipsis:
                geometry_values = list(geometry.values())[0]
                if within_a_percent_tuple(ellipse[0],geometry_values[0]) and within_a_percent_tuple(ellipse[1],geometry_values[1]) and within_a_percent(ellipse[2],geometry_values[2]):
                    verified_geometries += 1
        self.assertEquals(verified_geometries, 6)
    def test_Basic_Spline(self):
        """
        Basic Spline only one line in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic Spline.dxf")
        spline = geometries[0].get('SPLINE0')
        self.assertTrue(spline[0][0],5)  # Degree 5
        self.assertTrue(spline[0][1],1)  # Closed true
        self.assertTrue(spline[0][2],15)  # # Control Points
        self.assertTrue(spline[0+spline[0][1]],21)  # # Knots
        self.assertTrue(spline[1+spline[0][1]],15)  # # Weights
    def test_Complex_Splines(self):
        """
        Basic LWPolyline only one line in 2D
        """
        geometries = importer.import_dxf_file("Test Files/Basic LWPolyline.dxf")
        lwpolyline = geometries[0].get('LWPOLYLINE0')
        self.assertTrue(within_a_percent_tuple(lwpolyline[0],(25.0*10**3,0.0,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(within_a_percent_tuple(lwpolyline[1],(0.0,0.0,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(within_a_percent_tuple(lwpolyline[2],(0.0,25.0*10**3,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(within_a_percent_tuple(lwpolyline[3],(25.0*10**3,25.0*10**3,0.0,0.0,0.0)))  # First point (25,0,0)mm
        self.assertTrue(lwpolyline[4])  # Closed true

class TXT_Error_Tests(unittest.TestCase):
    """
    Test cases that should produce errors
    """
    def test_No_File_Found(self):
        """
        No file found import_txt_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_txt_file(""))
    def test_No_Extension(self):
        """
        File missing extension import_txt_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_txt_file("Test Files/test_geometries"))

class TXT_Import_Tests(unittest.TestCase):
    """
    Tests for importing txt files
    """
    def test_2D_Point(self):
        """
        One 2D point
        """
        geometries = importer.import_txt_file("Test Files/text_2d.txt")
        self.assertEqual(geometries[0].get('POINT0'),(1.1,2.2))
    def test_3D_Point(self):
        """
        One 3D point
        """
        geometries = importer.import_txt_file("Test Files/text_3d.txt",)
        self.assertEqual(geometries[0].get('POINT0'),(1.1,2.2,3.3))
    def test_Various_Percision(self):
        """
        Varying percision of points
        """
        geometries = importer.import_txt_file("Test Files/text_precision.txt")
        self.assertEqual(geometries[0].get('POINT0'),(1.1,2.2,3.3))
        self.assertEqual(geometries[1].get('POINT1'),(1.11,2.22,3.33))
        self.assertEqual(geometries[2].get('POINT2'),(1.111,2.222,3.333))
        self.assertEqual(geometries[3].get('POINT3'),(1.1111,2.2222,3.3333))
    def test_No_Points(self):
        """
        No points
        """
        geometries = importer.import_txt_file("Test Files/text_no_points.txt")
        self.assertEqual(len(geometries),0)

class CSV_Error_Tests(unittest.TestCase):
    """
    Test cases that should produce errors
    """
    def test_No_File_Found(self):
        """
        No file found import_csv_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_csv_file(""))
    def test_No_Extension(self):
        """
        File missing extension import_csv_file throws error
        """
        self.assertRaises(Exception, lambda: importer.import_csv_file("Test Files/test_geometries"))

class CSV_Import_Tests(unittest.TestCase):
    """
    Tests for importing csv files
    """

    def test_Basic(self):
        """
        General test, one of each geometry
        """
        geometries = importer.import_csv_file("Test Files/test.csv")

        # POINT
        self.assertEqual(geometries[0].get('POINT0')[0],(1.0,2.0,3.0))

        #LINE
        self.assertEqual(geometries[1].get('LINE1')[0],(1.0,2.0,3.0))
        self.assertEqual(geometries[1].get('LINE1')[1],(4.0,5.0,6.0))

        #CIRCLE
        self.assertEqual(geometries[2].get('CIRCLE2')[0],(1.0,2.0,3.0))
        self.assertEqual(geometries[2].get('CIRCLE2')[1],(4.0))

        #ARC
        self.assertEqual(geometries[3].get('ARC3')[0],(1.0,2.0,3.0))
        self.assertEqual(geometries[3].get('ARC3')[1],(4.0))
        self.assertEqual(geometries[3].get('ARC3')[2],(5.0))
        self.assertEqual(geometries[3].get('ARC3')[3],(6.0))

        #ELLIPSE
        self.assertEqual(geometries[4].get('ELLIPSE4')[0],(1.0,2.0,3.0))
        self.assertEqual(geometries[4].get('ELLIPSE4')[1],(4.0,0.0,0.0))
        self.assertEqual(geometries[4].get('ELLIPSE4')[2],(5.0))

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
