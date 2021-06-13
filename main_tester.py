from re import A
import importer
import alphabet_to_line

if __name__ == '__main__':
    converted = importer.import_dxf_file('Test Files/Basic Ellipse.dxf',['LINE'],True)
    importer.export_dxf_file("TEST3.dxf", converted, 'mm')
    # converted = importer.import_dxf_file('Test Files/Basic Ellipse.dxf',['ARC'],True,2,0,'mm')
    # importer.export_dxf_file("TEST2.dxf", converted, 'mm')