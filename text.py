from typing import Dict, List, Tuple
import importer
import os

# DICTIONARY
DICTIONARY: Dict [str, List[Dict [str, List[Tuple[float,...]]]]] = {
    "A": {  "LINE0": ((0.5, 1.0, 0.0),(0.2321, 0.0, 0.0)),
            "LINE1": ((0.5, 1.0, 0.0),(0.7679, 0.0, 0.0)),
            "LINE2": ((0.366, 0.5, 0.0),(0.634, 0.5, 0.0))},

    "B": {  "LINE0": ((0.25, 0.0, 0.0),(0.25, 1.0, 0.0)),
            "LINE1": ((0.25, 1.0, 0.0),(0.65, 1.0, 0.0)),
            "LINE2": ((0.65, 1.0, 0.0),(0.75, 0.9, 0.0)),
            "LINE3": ((0.75, 0.9, 0.0),(0.75, 0.6, 0.0)),
            "LINE4": ((0.75, 0.6, 0.0),(0.65, 0.5, 0.0)),
            "LINE5": ((0.65, 0.5, 0.0),(0.75, 0.4, 0.0)),
            "LINE6": ((0.75, 0.4, 0.0),(0.75, 0.1, 0.0)),
            "LINE7": ((0.75, 0.1, 0.0),(0.65, 0.0, 0.0)),
            "LINE8": ((0.65, 0.5, 0.0),(0.25, 0.5, 0.0))}
    }

def create_letter_from_dxf(letter: str,scans: List[Dict [str, List[Tuple[float,...]]]]):

    output: str = '"'+letter+'"'+': {'
    geometry_index = 0

    for entry_index,entry in enumerate(scans):
        for entity in entry:
            name: str = entity# Name of the geometry including number
            geometry_name: str = ''.join([i for i in name if not i.isdigit()]) # Truncate name to just include the geometry
            points: List[Tuple[float,...]] = entry.get(name) # List to store geometry

            if geometry_name == 'LINE':  # Line output
                output += '\t"%s%d": (' % (geometry_name, geometry_index)
                output += str(tuple(float(format(round(x/10000,4),'.4f')) for x in points[0])) + "," 
                output += str(tuple(float(format(round(x/10000,4),'.4f')) for x in points[1]))+')'+',\n'
                geometry_index += 1
            elif geometry_name == 'POINT': # Point output
                output += '\t"' + geometry_name + str(geometry_index) + ": " + str(tuple(format(round(x/10000,4),'.4f') for x in points[0]))
                output += ',\n'
                geometry_index += 1
            elif geometry_name == 'LWPOLYLINE': # Polyline output
                for point_index in range(len(points)-2):
                    output += '\t"%s%d": (' % ('LINE', geometry_index)
                    output += str(tuple(float(format(round(points[point_index][i]/10000,4),'.4f')) for i in range(0,3))) + ","
                    output += str(tuple(float(format(round(points[point_index+1][i]/10000,4),'.4f')) for i in range(0,3))) + "),\n"
                    geometry_index += 1
        
        # Replace last comma with bracket and add new line
        if entry_index == len(scans)-1:
            output = output[:len(output)-2] + "},\n"

    print(output) # Print output

if __name__ == "__main__":
    list = os.listdir("Letters")
    for name in list:
        letter_geometries = importer.import_dxf_file("Letters/"+name)
        letter = name.rstrip('.dxf')
        create_letter_from_dxf(letter,letter_geometries)
    