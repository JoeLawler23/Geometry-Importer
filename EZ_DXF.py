"""
Module for importing and exporting DXF files
"""

from logging import warning
from typing import Dict, List, Tuple
import ezdxf

__author__ = 'Joseph Lawler'
__version__ = '1.0.0'


def import_dxf_file(filename: str) -> List[Dict [str, List[Tuple[float,...]]]]:
    """
    Importing a DXF file and returning a list of entities

    Args:
        filename (str): DXF filename

    Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names and a list of associated points in 2D/3D, represented in nanometers and degrees
        LINE: {'LINE': [START (X,Y,Z), END (X,Y,Z)]}
        CIRCLE: {'CIRCLE': [RADIUS (#), CENTER (X,Y,Z), PLANE (X,Y,Z)]}
        ARC:
    """

    # Account for missing file extension
    if not filename.endswith(".dxf"):
        # add extension
        filename = filename + ".dxf"

    # Import file
    try:
        dxf = ezdxf.readfile(filename)
    except IOError or ezdxf.DXFStructureError:
        # Catch errors
        # TODO make sure this is what he wants
        raise Exception ('Invalid/Corrupt DXF File')

    # Get all entities from dxf
    msp = dxf.modelspace()
    entities = msp.entity_space

    # Get conversion factor to nanometers
    # TODO throw warning if the unit to too big ???
    units: int = dxf.units
    #0 = Unitless (NO CONVERION USED)
    #1 = Inches
    #2 = Feet
    #3 = Miles
    #4 = Millimeters
    #5 = Centimeters
    #6 = Meters
    #7 = Kilometers
    #8 = Microinches
    #9 = Mils
    #10 = Yards
    #11 = Angstroms
    #12 = Nanometers
    #13 = Microns
    #14 = Decimeters
    #15 = Decameters
    #16 = Hectometers
    #17 = Gigameters
    #18 = Astronomical units
    #19 = Light years
    #20 = Parsecs
    #21 = US Survey Feet
    #22 = US Survey Inch
    #23 = US Survey Yard
    #24 = US Survey Mile
    conversionFactor: float = {0:1.0, 1:25400000, 2:304800000, 3:1609344000000, 4:1000000, 5:10000000, 6:1000000000, 7:1000000000000, 8:25.4, 
    9:25400, 10:914400000, 11:0.1, 12:1, 13:1000, 14:100000000, 15:10000000000, 16:100000000000, 17:1.0E+18, 18:1.495978707E+20, 19:9.461E+24,
    20:3.0856775814914E+25, 21:304800609.6, 22:25400050.8, 23:914400000, 24:1609347219000}[units]

    # Add entities to geometry
    geometry: List[Dict [str, List[Tuple[[float], ...]]]] = []
    for e in entities:

        # Entity name
        name: str = e.DXFTYPE

        # Create points array for entity's points
        points: List[Tuple[[float], ...]] = [] 

        # Determine entity and get information to store
        if name == 'CIRCLE':
            points.append(e.dxf.radius*conversionFactor) # Radius
            points.append(tuple([conversionFactor*x for x in e.dxf.center.xyz]))# Center
            points.append(e.dxf.extrusion.xyz)# Plane TODO does this need to be converted????
        elif name == 'LINE':
            points.append(tuple([conversionFactor*x for x in e.dxf.start.xyz]))# Start point
            points.append(tuple([conversionFactor*x for x in e.dxf.end.xyz]))# End point
        elif name == 'ARC':
            # TODO
            points.append([e.dxf.radius*conversionFactor,e.dxf.start_angle,e.dxf.end_angle])# Radius, Start angle, End angle
            points.append(tuple([conversionFactor*x for x in e.dxf.center.xyz]))# Center
            points.append(e.dxf.extrusion.xyz)# Plane TODO does this need to be converted????
        else:
            # Throw a warning when entity is not accounted for
            warning("UNKNOWN GEOMETRY: "+name)
        
        # Add entity name and corresponding points to array
        geometry.append({name: points})

    # Return array of all entities    
    return geometry

# def export_dxf_file(filename: str, scans: List[Dict[str, List[Tuple(float,..)]], **args = {}) -> bool:
#     # returns True if successful

if __name__ == "__main__":
    points = import_dxf_file("3D Examples.dxf")