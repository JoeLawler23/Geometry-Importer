"""
Module for importing and exporting DXF files based off of ezdxf
"""

from logging import warning
from typing import Dict, Iterable, List, Tuple
import ezdxf
from ezdxf.document import Drawing
from ezdxf.entitydb import EntitySpace
from ezdxf.layouts.layout import Modelspace
from ezdxf.math import Vertex
import re

__author__ = 'Joseph Lawler'
__version__ = '1.0.0'

CONVESION_FACTORS: List[float] = [
    1.0,                         #0 = Unitless (NO CONVERION USED)
    3.9370079*10**5,            #1 = Inches
    3.2808399*10**6,            #2 = Feet
    6.2137119*10**10,           #3 = Miles
    1.0*10**3,                  #4 = Millimeters
    1.0*10**4,                  #5 = Centimeters
    1.0*10**6,                  #6 = Meters
    1.0*10**9,                  #7 = Kilometers
    39.37007874015748,          #8 = Microinches
    39.37007874015748*10**3,    #9 = Mils
    1.093613*10**6,             #10 = Yards
    1.0*10**4,                  #11 = Angstroms
    1.0*10**3,                  #12 = Nanometers
    1.0,                        #13 = Microns (CONVERTED TO)
    1.0*10**5,                  #14 = Decimeters
    1.0*10**7,                  #15 = Decameters
    1.0*10**8,                  #16 = Hectometers
    1.0*10**15,                 #17 = Gigameters
    6.6845871226706*10**18,     #18 = Astronomical units
    1.0570008340246*10**22,     #19 = Light years
    3.2407792700054*10**23,     #20 = Parsecs
    3.2808399*10**6,            #21 = US Survey Feet
    3.9370079*10**5,            #22 = US Survey Inch
    1.093613*10**6,             #23 = US Survey Yard
    6.2137119*10**10            #24 = US Survey Mile
]

UNIT_TABLE: Dict[str,int] = {
    "in":1,     #Inches
    "ft":2,     #Feet
    "mi":3,     #Miles
    "mm":4,     #Milimeters
    "cm":5,     #Centimeters
    "m":6,      #Meters
    "km":7,     #Kilometers
    "ui":8,     #Microinches
    "mil":9,    #Mils
    "yd":10,    #Yards
    "a":11,     #Angstroms
    "nm":12,    #Nanometers
    "um":13,    #Microns
    "dm":14,    #Decimeters
    "dam":15,   #Decameters
    "hm":16,    #Hectometers
    "gm":17,    #Gigameters
    "au":18,    #Astronomical units
    "ly":19,    #Light years
    "pc":20,    #Parsecs
    "usft":22,  #US Survey Feet
    "usin":23,  #US Survey Inch
    "usyd":24,  #US Survey Yard
    "usmi":25   #US Survey Mile
}

def import_dxf_file(filename: str) -> List[Dict [str, List[Tuple[float,...]]]]:
    """
    Importing a DXF file and returning a list of entities

    Args:
        filename (str): DXF filename

    Raises:
        Exception: If passed file name is not found, corrupt, or not a DXF file
        Warning: Unknown Geometry is found

    Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, represented in microns and degrees

        List of supported geometries and how they are stored
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            CIRCLE: ('CIRCLE#': [RADIUS (#), CENTER (X,Y,Z), PLANE (X,Y,Z)])
            ARC: ('ARC#': [RADIUS/START ANGLE/END ANGLE(#,#,#), CENTER (X,Y,Z), PLANE (X,Y,Z)])
            ELLIPSE: ('ELLIPSE#': [CENTER (X,Y,Z), LENGTH OF MAJOR AXIS (X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE#': [DEGREE, CLOSED, # CONTROL POINTS (#,BOOLEAN,#), CONTROL POINT(S) (X,Y,Z), KNOTS (#,...), WEIGHTS (#,...)])
            LWPOLYLINE: ('LWPOLYLINE#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
    """

    # Import file
    try:
        dxf_drawing: Drawing = ezdxf.readfile(filename)
    except IOError as error:
        # Reraise error
        raise Exception('Invalid/Corrupt DXF File') from error
    except FileNotFoundError as error:
        # Reraise error
        raise Exception('File Not Found') from error
    except ezdxf.DXFStructureError and ezdxf.UnicodeDecodeError:
        # Catch errors
        warning("Invalid/Corrupted DXF Structures")
        return None

    # Get all entities from dxf
    modelspace: Modelspace = dxf_drawing.modelspace()
    entities: EntitySpace = modelspace.entity_space

    # Get conversion factor to nanometers
    units: int = dxf_drawing.units
    conversion_factor: float = CONVESION_FACTORS[units]

    # Geometry is a single geometric entity
    geometries: List[Dict [str, List[Tuple[float,...]]]] = []

    # Cycle through all entities
    for entity_index,entity in enumerate(entities):
        # Entity name
        name: str = entity.DXFTYPE

        # Create points array for entity's points
        points: List[Tuple[float,...]] = [] 

        # Determine entity and get information to store
        if name == 'CIRCLE':
            points.append(entity.dxf.radius*conversion_factor) # Radius
            points.append(tuple([conversion_factor*x for x in entity.dxf.center.xyz]))# Center
            points.append(entity.dxf.extrusion.xyz)# Plane
        elif name == 'LINE':
            points.append(tuple([conversion_factor*x for x in entity.dxf.start.xyz]))# Start point
            points.append(tuple([conversion_factor*x for x in entity.dxf.end.xyz]))# End point
        elif name == 'ARC':
            points.append([entity.dxf.radius*conversion_factor,entity.dxf.start_angle,entity.dxf.end_angle])# Radius, Start angle, End angle NOTE angles go in a counter-clockwise rotation by defaul **
            points.append(tuple([conversion_factor*x for x in entity.dxf.center.xyz]))# Center
            points.append(entity.dxf.extrusion.xyz)# Plane
        elif name == 'ELLIPSE':
            points.append(tuple([conversion_factor*x for x in entity.dxf.center.xyz]))# Center
            points.append(tuple([conversion_factor*x for x in entity.dxf.major_axis.xyz]))# Length of major axis
            points.append(entity.dxf.ratio)# Ratio of minor to major axis
            # NOTE fusion does not export any plane orientation information may need to look into later
        elif name == 'SPLINE':
            control_points_counter: int = 0
            control_points: List[Tuple[float,...]] = [] 
            for i in entity.control_points:
                 control_points.append(tuple([conversion_factor*x for x in i]))# Convert control points from vector to list of tuples
                 control_points_counter += 1
            points.append([entity.dxf.degree,entity.CLOSED,control_points_counter])# Degree, Closed, Len control points NOTE closed is defined by whether or not the start and end match 1 = false and 0 = true
            points[1:1] = control_points# Add control points to end of points list
            points.append(entity.knots)# Knots
            if len(entity.weights) == 0:
                weights: List[float] = []
                for i in range (len(entity.control_points)):
                        weights.append(1.0)
                points.append(weights) # Add an array of 1.0's
            else:
                points.append(entity.weights)# Add the given Weights
        elif name == 'LWPOLYLINE':
            point: Tuple[float,...] = []
            count: int = 0
            for i in entity.lwpoints.values: # Format points
                if count%5 == 0 and count != 0:
                    points.append(point)
                    point = []
                point.append(i)
                count += 1
            points.append(point)
            for point in points: # Convert first 2 points
                point[0] *= conversion_factor
                point[1] *= conversion_factor
            points.append(entity.closed) # Add boolean for whether or not the polyline is closed
        else:
            # Throw a warning when entity is not accounted for
            warning("UNKNOWN GEOMETRY: "+name)
        #end if
        
        # Add entity name and corresponding points to array
        geometries.append({name+str(entity_index): points})

    # Return array of all geometries    
    return geometries
    #end def

def export_dxf_file(filename: str, scans: List[Dict [str, List[Tuple[float,...]]]], exportunits: str = "um") -> bool:
    """
    Exporting a DXF file from a list of entities

    Args:
        filename (str): DXF filename
        scans (List[Dict [str, List[Tuple[float,...]]]]): List of geometries to write to DXF file
        units (int, optional): [description]. Units to export DXF in, defaults 13=Microns.

    Raises:
        Exception: If no scans are passed
        Exception: If no file extension is passed
        Exception: If invalid units are passed
        Warning: Unknown Geometry is found

    Returns:
        bool: True upon successful completion
    """

    # Create DXF file with given filename
    dxf_drawing: Drawing = ezdxf.new('R2010')

    # Set output units
    if exportunits in UNIT_TABLE:
        dxf_drawing.units = UNIT_TABLE[exportunits] #Set units to passed units
    else:
        raise Exception("Invalid Units {}", exportunits) from None

    # Get modelspace
    model_space: Modelspace = dxf_drawing.modelspace()
    
    # Check to make sure that scans is not null
    if len(scans) == 0:
        raise Exception('Scans contains no objects') from None

    # Add each entitiy in the passed list
    for entry in scans:
        for entity in entry:
            name: str = entity# Name of geometry
            geometry_name: str = ''.join([i for i in name if not i.isdigit()]) # Truncate name to just include the geometry
            points: List[Tuple[float,...]] = entry.get(name) # List to store geometry

            # Add geometry in proper format
            if geometry_name == 'CIRCLE':
                # Center, Radius, Attributes
                model_space.add_circle(points[1],points[0],dxfattribs={'extrusion':points[2]})
            elif geometry_name == 'LINE':
                # Start point, End point
                model_space.add_line(points[0],points[1])
            elif geometry_name == 'ARC':
                # Center, Radius, Start Angle, End Angle, IsCounterClockwise, Attributes
                model_space.add_arc(points[1],points[0][0],points[0][1],points[0][2],True,dxfattribs={'extrusion':points[2]})
            elif geometry_name == 'ELLIPSE':
                # Center, Length Major Axis, Ratio from Minor Axis to Major Axis
                model_space.add_ellipse(points[0],points[1],points[2],)
            elif geometry_name == 'SPLINE':
                control_points: Iterable[Vertex] = []
                for i in range(points[0][2]): # Convert list of tuples to iterable of vertices
                    control_points.append(points[i+1])
                if points[0][1] == 1:# Determine if the spline is open or closed
                    # Control Points, Weights, Degree, Knots
                    model_space.add_rational_spline(control_points,points[points[0][2]+2],points[0][0],points[points[0][2]+1])
                else:
                    # Control Points, Weights, Degree, Knots
                    model_space.add_closed_rational_spline(control_points,points[points[0][2]+2],points[0][0],points[points[0][2]+1])
            elif geometry_name == 'LWPOLYLINE':
                closed: bool = points[-1]
                del points[-1]
                # Points, Format = "xyseb" by default, Attributes
                model_space.add_lwpolyline(points,dxfattribs={'closed':closed})
            else:
                # Throw a warning when entity is not accounted for
                warning("UNKNOWN GEOMETRY: "+geometry_name)
            #end if

    # Catch filename with no extension and raise an error
    if not filename.endswith(".dxf"):
        raise Exception("Filename does not contain extension")

    # Save DXF file
    dxf_drawing.saveas(filename)

    # Returns True if successful
    return True
    #end def

def import_txt_file(filname: str, units: str = "um") -> List[Dict [str, List[Tuple[float,...]]]]:
    # Import text file
    try:
        lines: List[str] = open(filname).readlines()
    except FileNotFoundError as error:
        # Reraise error
        raise Exception('File Not Found') from error

    # Create empty list for geometries and index
    geometries: List[Dict [str, List[Tuple[float,...]]]] = []
    geometries_index = 0

    # Get conversion factor
    conversion_factor = CONVESION_FACTORS[UNIT_TABLE[units]]

    # Loop through all lines
    for line in lines:
        # Remove newline character
        line = line.rstrip('\n')

        # Determine if line is a valid point
        valid_point = re.fullmatch("\d+.\d+,\d+.\d+,\d+.\d+",line)

        if valid_point:
            # Get points, convert to float, multiply by conversion factor
            points: Tuple[float] = tuple(point*conversion_factor for point in map(float,re.findall("\d+.\d+",line)))
            
            # Add to geometries
            geometries.append({'POINT'+str(geometries_index): points})

            # Increase index
            geometries_index += 1

    # Return list of geometries
    return geometries
    #end def

if __name__ == "__main__":
    # TESTING ONLY
    import_txt_file("Test Files/text_geometries.txt")