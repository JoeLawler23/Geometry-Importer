import unittest
import EZ_DXF

class Tests(unittest.TestCase):
    def test1(self):
        """
        No file found import_dxf_file throws an error
        """
        self.assertRaises(Exception, lambda: EZ_DXF.import_dxf_file(""))
    def test2(self):
        """
        File missing extension import_dxf_file
        """
        geometries = EZ_DXF.import_dxf_file("Test Files/One Circle")
        self.assertEquals(1, len(geometries))
    def test3(self):
        """
        No passed geometry to export_dxf_file throws an error
        """
        self.assertRaises(Exception, lambda: EZ_DXF.export_dxf_file("Test Files/test3.dxf",None))
    
if __name__ == '__main__':
    unittest.main()