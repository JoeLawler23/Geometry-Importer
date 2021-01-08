import unittest
import EZ_DXF

class Tests(unittest.TestCase):
    def test1(self):
        """
        No file found import_dxf_file
        """
        self.assertRaises(Exception ('Invalid/Corrupt DXF File'), EZ_DXF.import_dxf_file(""))
    def test2(self):
        """
        File missing extension import_dxf_file
        """
        geometries = EZ_DXF.import_dxf_file()
        self.assert(geometries.len == 10)
    def test3(self):
        """
        File missing extension export_dxf_file
        """
        pass
    def test4(self):
        """
        No passed geometry export_dxf_file
        """
        pass
    
if __name__ == '__main__':
    unittest.main()