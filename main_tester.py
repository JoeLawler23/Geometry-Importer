import importer
import alphabet_to_line
import geometry_to_line

if __name__ == '__main__':
    arc = geometry_to_line.circle_to_lines(importer.import_dxf_file('Test Files/Basic Circle.dxf'),3)
    importer.export_dxf_file('TEST.dxf',arc)
    importer.export_dxf_file('TEST1.dxf',importer.import_dxf_file('Test Files/Basic Circle.dxf'))