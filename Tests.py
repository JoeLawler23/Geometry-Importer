import unittest
import EZ_DXF

class Error_Tests(unittest.TestCase):
    """Test cases that may produce errors

    Args:
        Test1: No file found import_dxf_file throws proper error
        Test2: File missing extension import_dxf_file should not throw error
        Test3: No passed geometry to export_dxf_file throws proper error
    """
    def test1(self):
        """
        No file found import_dxf_file throws proper error
        """
        self.assertRaises(Exception, lambda: EZ_DXF.import_dxf_file(""))
    def test2(self):
        """
        File missing extension import_dxf_file
        - Should properly append the file extension
        """
        geometries = EZ_DXF.import_dxf_file("Test Files/Basic Circle")
        self.assertEquals(1, len(geometries))
    def test3(self):
        """
        No passed geometry to export_dxf_file throws proper error
        """
        self.assertRaises(Exception, lambda: EZ_DXF.export_dxf_file("Test Files/test3.dxf",None))

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
        geometries = EZ_DXF.import_dxf_file("Test Files/Basic Circle.dxf")
        circle = geometries[0].get('CIRCLE0')
        self.assertEquals(circle[0],15.0*(10**6))# check radius
        self.assertEquals(circle[1],(0.0,0.0,0.0))# check center
        self.assertEquals(circle[2],(0.0,0.0,1.0))# check 3D orientation (On Z-axis)
    def test2(self):
        """
        Complex circles multiple circles in 3D with various angles and positions
        """
        geometries = EZ_DXF.import_dxf_file("Test Files/Complex Circles.dxf")
        circle0 = geometries[0].get('CIRCLE0')
        circle1 = geometries[1].get('CIRCLE1')
        circle2 = geometries[2].get('CIRCLE2')
        circle3 = geometries[3].get('CIRCLE3')
        circle4 = geometries[4].get('CIRCLE4')
        circle5 = geometries[5].get('CIRCLE5')
        circle6 = geometries[6].get('CIRCLE6')
        circle7 = geometries[7].get('CIRCLE7')
        circle8 = geometries[8].get('CIRCLE8')
        circle9 = geometries[9].get('CIRCLE9')
        
        #circle one
        self.assertTrue(within_a_percent(circle0[0],25.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle0[1],(0.0,0.0,0.0)))# check center
        self.assertTrue(within_a_percent_tuple(circle0[2],(0.0,0.0,1.0)))# check 3D orientation

        #circle two
        self.assertTrue(within_a_percent(circle1[0],20.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle1[1],(50.0*10**6,0.0,0.0)))# check center
        self.assertTrue(within_a_percent_tuple(circle1[2],(0.0,0.0,1.0)))# check 3D orientation
        
        #circle three
        self.assertTrue(within_a_percent(circle2[0],15.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle2[1],(100.0*10**6,0.0,0.0)))# check center
        self.assertTrue(within_a_percent_tuple(circle2[2],(0.0,0.0,1.0)))# check 3D orientation
        
        #circle four
        self.assertTrue(within_a_percent(circle3[0],10.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle3[1],(150.0*10**6,0.0,0.0)))# check center
        self.assertTrue(within_a_percent_tuple(circle3[2],(0.0,0.0,1.0)))# check 3D orientation
        
        #circle five
        self.assertTrue(within_a_percent(circle4[0],5.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle4[1],(200.0*10**6,0.0,0.0)))# check center
        self.assertTrue(within_a_percent_tuple(circle4[2],(0.0,0.0,1.0)))# check 3D orientation

        #circle six
        self.assertTrue(within_a_percent(circle5[0],10.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle5[1],(150.0*10**6,50.0*10**6,50.0*10**6)))# check center
        self.assertTrue(within_a_percent_tuple(circle5[2],(0.0,-1.0,0.0)))# check 3D orientation

        #circle two
        self.assertTrue(within_a_percent(circle6[0],20.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle6[1],(50.0*10**6,50.0*10**6,50.0*10**6)))# check center
        self.assertTrue(within_a_percent_tuple(circle6[2],(0.0,-1.0,0.0)))# check 3D orientation
        
        #circle three
        self.assertTrue(within_a_percent(circle7[0],25.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle7[1],(0.0,50.0*10**6,50.0*10**6)))# check center
        self.assertTrue(within_a_percent_tuple(circle7[2],(0.0,-1.0,0.0)))# check 3D orientation
        
        #circle four
        self.assertTrue(within_a_percent(circle8[0],15.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle8[1],(100.0*10**6,50.0*10**6,50.0*10**6)))# check center
        self.assertTrue(within_a_percent_tuple(circle8[2],(0.0,-1.0,0.0)))# check 3D orientation
        
        #circle five
        self.assertTrue(within_a_percent(circle9[0],5.0*10**6))# check radius
        self.assertTrue(within_a_percent_tuple(circle9[1],(200.0*10**6,50.0*10**6,50.0*10**6)))# check center
        self.assertTrue(within_a_percent_tuple(circle9[2],(0.0,-1.0,0.0)))# check 3D orientation
        
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