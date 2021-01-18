import unittest
import dxf

class Error_Tests(unittest.TestCase):
    """Test cases that may produce errors

    Args:
        Test1: No file found import_dxf_file throws proper error
        Test2: File missing extension import_dxf_file should not throw error
        Test3: No passed geometry to export_dxf_file throws proper error
    """
    def test1(self):
        """
        No file found import_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: dxf.import_dxf_file(""))
    def test2(self):
        """
        File missing extension import_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: dxf.export_dxf_file("Test Files/test3",None))
    def test3(self):
        """
        No passed geometry to export_dxf_file throws error
        """
        self.assertRaises(Exception, lambda: dxf.export_dxf_file("Test Files/test3.dxf",None))

class Geometry_Tests(unittest.TestCase):
    """Test cases for individual geometries

    Args:
        Test1: Basic circle only one circle in 3D
        Test2: Complex circles multiple circles in 3D with various angles and positions
    """
    def test1(self):
        """
        Basic circle only one circle in 3D
        """
        geometries = dxf.import_dxf_file("Test Files/Basic Circle.dxf")
        circle = geometries[0].get('CIRCLE0')
        self.assertTrue(within_a_percent(0.015,circle[0]))# check radius
        self.assertEquals(circle[1],(0.0,0.0,0.0))# check center
        self.assertEquals(circle[2],(0.0,0.0,1.0))# check 3D orientation (On Z-axis)
    def test2(self):
        """
        Complex circles multiple circles in 3D with various angles and positions
        """
        geometries = dxf.import_dxf_file("Test Files/Complex Circles.dxf")
        # TODO rewrite as a loop
        
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

if __name__ == '__main__':
    unittest.main()