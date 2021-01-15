"""
Module for importing and exporting DXF files
"""

from logging import warning
from typing import Dict, Iterable, List, Tuple
import ezdxf

from ezdxf.math import Vertex

__author__ = 'Joseph Lawler'
__version__ = '1.0.0'


def import_dxf_file(filename: str) -> List[Dict [str, List[Tuple[float,...]]]]:
    """
    Importing a DXF file and returning a list of entities

    Args:
        filename (str): DXF filename

    Raises:
        Exception: If passed file name is not found, corrupt, or not a DXF file
        Warning: Unknown Geometry is found

    Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, 
        represented in nanometers and degrees

        List of supported geometries and how they are stored
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            CIRCLE: ('CIRCLE#': [RADIUS (#), CENTER (X,Y,Z), PLANE (X,Y,Z)])
            ARC: ('ARC#': [RADIUS/START ANGLE/END ANGLE(#,#,#), CENTER (X,Y,Z), PLANE (X,Y,Z)])
            ELLIPSE:
            SPLINE:
            LWPOLYLINE: 
    """

    # Account for missing file extension
    if not filename.endswith(".dxf"):
        # add extension
        filename = filename + ".dxf"

    # Import file
    try:
        dxf = ezdxf.readfile(filename)
    except (IOError, FileNotFoundError, ezdxf.DXFStructureError):
        # Catch errors
        raise Exception('Invalid/Corrupt DXF File') from None

    # Get all entities from dxf
    msp = dxf.modelspace()
    entities = msp.entity_space

    # Get conversion factor to nanometers
    units: int = dxf.units
    conversionFactor: float = {0:1.0,   #0 = Unitless (NO CONVERION USED)
    1:3.9370079*10**-5,                 #1 = Inches
    2:3.2808399*10**-6,                 #2 = Feet
    3:6.2137119*10**-10,                #3 = Miles
    4:1.0*10**-3,                       #4 = Millimeters
    5:1.0*10**-4,                       #5 = Centimeters
    6:1.0*10**-6,                       #6 = Meters
    7:1.0*10**-9,                       #7 = Kilometers
    8:39.37007874015748,                #8 = Microinches
    9:39.37007874015748*10**-3,         #9 = Mils
    10:1.093613*10**-6,                 #10 = Yards
    11:1.0*10**4,                       #11 = Angstroms
    12:1.0*10**3,                       #12 = Nanometers
    13:1.0,                             #13 = Microns (CONVERTED TO)
    14:1.0*10**-5,                      #14 = Decimeters
    15:1.0*10**-7,                      #15 = Decameters
    16:1.0*10**-8,                      #16 = Hectometers
    17:1.0*10**-15,                     #17 = Gigameters
    18:6.6845871226706*10**-18,         #18 = Astronomical units
    19:1.0570008340246*10**-22,         #19 = Light years
    20:3.2407792700054*10**-23,         #20 = Parsecs
    21:3.2808399*10**-6,                #21 = US Survey Feet
    22:3.9370079*10**-5,                #22 = US Survey Inch
    23:1.093613*10**-6,                 #23 = US Survey Yard
    24:6.2137119*10**-10}[units]        #24 = US Survey Mile

    # Geometry is a single geometric entity
    geometry: List[Dict [str, List[Tuple[[float], ...]]]] = []

    # Id in order to identify a specific entity
    id: int = 0

    # Cycle through all entities
    for e in entities:
        # Entity name
        name: str = e.DXFTYPE

        # Create points array for entity's points
        points: List[Tuple[[float], ...]] = [] 

        # Determine entity and get information to store
        if name == 'CIRCLE':
            points.append(e.dxf.radius*conversionFactor) # Radius
            points.append(tuple([conversionFactor*x for x in e.dxf.center.xyz]))# Center
            points.append(e.dxf.extrusion.xyz)# Plane
        elif name == 'LINE':
            points.append(tuple([conversionFactor*x for x in e.dxf.start.xyz]))# Start point
            points.append(tuple([conversionFactor*x for x in e.dxf.end.xyz]))# End point
        elif name == 'ARC':
            points.append([e.dxf.radius*conversionFactor,e.dxf.start_angle,e.dxf.end_angle])# Radius, Start angle, End angle NOTE angles go in a counter-clockwise rotation by defaul **
            points.append(tuple([conversionFactor*x for x in e.dxf.center.xyz]))# Center
            points.append(e.dxf.extrusion.xyz)# Plane
        elif name == 'ELLIPSE':
            points.append(tuple([conversionFactor*x for x in e.dxf.center.xyz]))# Center
            points.append(tuple([conversionFactor*x for x in e.dxf.major_axis.xyz]))# Length of major axis and the plane
            points.append(e.dxf.ratio)# Ratio of minor to major axis, Start of ellipse curve, End of ellipse curve
        elif name == 'SPLINE':
            control_points_counter: int = 0
            control_points: List[Tuple[[float], ...]] = [] 
            for i in e.control_points:
                 control_points.append(tuple([conversionFactor*x for x in i]))# Converting control points
                 control_points_counter += 1
            points.append([e.dxf.degree,e.CLOSED,control_points_counter])# Degree, Closed, Len control points NOTE closed is defined by whether or not the start and end match 1 = false and 0 = true
            points[1:1] = control_points# Add control points to end of points list
            points.append(e.knots)# Knot Points
            points.append(e.weights)# Weights Points
        elif name == 'LWPOLYLINE':
            # NOTE Seems like when creating a polygon in Fusion it will be stored as either a lwpolyline or a series of lines
            point: Tuple[[float], ...] = []
            count: int = 0
            for i in e.lwpoints.values: # Formating points
                if count%5 == 0 and count != 0:
                    points.append(point)
                    point = []
                point.append(i)
                count += 1
            points.append(point)
            for point in points: # Converting points
                point[0] *= conversionFactor
                point[1] *= conversionFactor
            points.append(e.closed) # Add boolean for whether or not the polyline is closed

        else:
            # Throw a warning when entity is not accounted for
            warning("UNKNOWN GEOMETRY: "+name)
        
        # Add entity name and corresponding points to array
        geometry.append({name+str(id): points})

        # Increment the id
        id+= 1

    # Return array of all entities    
    return geometry

def export_dxf_file(filename: str, scans: List[Dict [str, List[Tuple[float,...]]]], units: int = 13) -> bool:
    """
    Exporting a DXF file from a list of entities

    Args:
        filename (str): DXF filename
        scans (List[Dict [str, List[Tuple[float,...]]]]): List of geometries to write to DXF file
        units (int, optional): [description]. Units to export DXF in, defaults 13=Microns.

    Raises:
        Exception: If no scans are passed
        Warning: Unknown Geometry is found

    Returns:
        bool: True upon successful completion
    """

    # Create DXF file with given filename
    dxf = ezdxf.new('R2010')

    # Set output units
    dxf.units = units # 13 == Microns

    # Get modelspace
    msp = dxf.modelspace()
    
    # Check to make sure that scans is not null
    if len(scans) == 0:
        raise Exception('Scans contains no objects') from None

    # Add each entitiy in the passed list
    for entry in scans:
        for entity in entry:
            name: str = entity
            geometry_name: str = ''.join([i for i in name if not i.isdigit()])
            points: List[Tuple[[float], ...]] = entry.get(name)

            # Add geometry in proper format
            if geometry_name == 'CIRCLE':
                msp.add_circle(points[1],points[0],dxfattribs={'extrusion':points[2]})
            elif geometry_name == 'LINE':
                msp.add_line(points[0],points[1])
            elif geometry_name == 'ARC':
                msp.add_arc(points[1],points[0][0],points[0][1],points[0][2],True,dxfattribs={'extrusion':points[2]})
            elif geometry_name == 'ELLIPSE':
                msp.add_ellipse(points[0],points[1],points[2])
            elif geometry_name == 'SPLINE':
                control_points: Iterable[Vertex] = []
                for i in range(points[0][2]):
                    control_points.append(points[i+1])
                if points[0][1] == 1:
                    msp.add_rational_spline(control_points,points[points[0][2]+2],points[0][0],points[points[0][2]+1])
                else:
                    msp.add_closed_rational_spline(control_points,points[points[0][2]+2],points[0][0],points[points[0][2]+1])
            elif geometry_name == 'LWPOLYLINE':
                closed: bool = points[-1]
                del points[-1]
                msp.add_lwpolyline(points,dxfattribs={'closed':closed})
            else:
                # Throw a warning when entity is not accounted for
                warning("UNKNOWN GEOMETRY: "+geometry_name)

    # Append file extension if necessary
    if not filename.endswith(".dxf"):
        # add extension
        filename = filename + ".dxf"

    # Save DXF file
    dxf.saveas(filename)

    # Returns True if successful
    return True

if __name__ == "__main__":
    geometries = import_dxf_file("Test Files/Current Troubling Geometries.dxf")
    export_dxf_file("Test Files/Exported Current Troubling Geometries.dxf",geometries)