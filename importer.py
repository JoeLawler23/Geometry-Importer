'''
Module for importing and exporting DXF/CSV/TXT files
'''

import csv
import re
from logging import warning
from typing import Dict, Iterable, List, Optional, Tuple

import ezdxf
from ezdxf.document import Drawing
from ezdxf.entitydb import EntitySpace
from ezdxf.layouts.layout import Modelspace
from ezdxf.math import Vertex

__author__ = 'Joseph Lawler'
__version__ = '1.0.0'

CONVERSION_FACTORS = (
    1.0,  # 0 = Unitless (NO CONVERION USED)
    3.9370079*10**5,  # 1 = Inches
    3.2808399*10**6,  # 2 = Feet
    6.2137119*10**10,  # 3 = Miles
    1.0*10**3,  # 4 = Millimeters
    1.0*10**4,  # 5 = Centimeters
    1.0*10**6,  # 6 = Meters
    1.0*10**9,  # 7 = Kilometers
    39.37007874015748,  # 8 = Microinches
    39.37007874015748*10**3,  # 9 = Mils
    1.093613*10**6,  # 10 = Yards
    1.0*10**4,  # 11 = Angstroms
    1.0*10**3,  # 12 = Nanometers
    1.0,  # 13 = Microns (CONVERTED TO)
    1.0*10**5,  # 14 = Decimeters
    1.0*10**7,  # 15 = Decameters
    1.0*10**8,  # 16 = Hectometers
    1.0*10**15,  # 17 = Gigameters
    6.6845871226706*10**18,  # 18 = Astronomical units
    1.0570008340246*10**22,  # 19 = Light years
    3.2407792700054*10**23,  # 20 = Parsecs
    3.2808399*10**6,  # 21 = US Survey Feet
    3.9370079*10**5,  # 22 = US Survey Inch
    1.093613*10**6,  # 23 = US Survey Yard
    6.2137119*10**10  # 24 = US Survey Mile
)

UNIT_TABLE = (
    'in',  # Inches  (value = 1)
    'ft',  # Feet
    'mi',  # Miles
    'mm',  # Milimeters
    'cm',  # Centimeters
    'm',  # Meters
    'km',  # Kilometers
    'ui',  # Microinches
    'mil',  # Mils
    'yd',  # Yards
    'a',  # Angstroms
    'nm',  # Nanometers
    'um',  # Microns
    'dm',  # Decimeters
    'dam',  # Decameters
    'hm',  # Hectometers
    'gm',  # Gigameters
    'au',  # Astronomical units
    'ly',  # Light years
    'pc',  # Parsecs
    'usft',  # US Survey Feet
    'usin',  # US Survey Inch
    'usyd',  # US Survey Yard
    'usmi',  # US Survey Mile
)


# Define type for containing geometry elements
TGeometryItem = Tuple[str, List[Tuple[float, ...]]]
TGeometryList = List[TGeometryItem]

def import_dxf_file(
    filename: str,
    allowedtypes: List[str] = []) -> TGeometryList:
    '''
    Summary:
        Import a DXF file and returning a list of entities
    Args:
        filename (str): filename of DXF file to read
        allowedtypes (List[str]): list of allowed geometry types (eg. POINT, LINE, ...),
        NOTE If the list is empty then all types will be imported.
    Raises:
        Exception: Passed file name is not found, corrupt, or not a DXF file
        Warning: Unknown Geometry is found
    Returns:
        TGeometryList: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, represented in microns and degrees
        List of supported geometries and their associated values
            POINT: ('POINT:#': [(X,Y,Z)])
            LINE: ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)]) NOTE this includes circles
            ELLIPSE: ('ELLIPSE:#': [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE:#': [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
            LWPOLYLINE: ('LWPOLYLINE:#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
    '''
    
    # Import file
    try:
        dxf_drawing: Drawing = ezdxf.readfile(filename)
    except OSError as error:
        # Reraise error
        raise Exception('Invalid/Corrupt/Missing DXF File') from error
    except ezdxf.DXFStructureError:
        # Catch errors
        warning('Invalid/Corrupted DXF Structures')
        return []
    #end try

    # Get all entities from dxf
    modelspace: Modelspace = dxf_drawing.modelspace()
    entities: EntitySpace = modelspace.entity_space

    # Get conversion factor to nanometers
    units = dxf_drawing.units
    conversion_factor: float = CONVERSION_FACTORS[units]

    # Create empty list of geometries
    geometries: TGeometryList = []

    # Cycle through all entities
    for entity_index, entity in enumerate(entities):
        # Entity name
        name: str = entity.DXFTYPE

        # Check if this is an allowed geometry type
        if allowedtypes and name not in allowedtypes:
            continue

        if name == 'POINT':
            # Create point entry: ('POINT:#': [(X,Y,Z)])
            one_point = (
                f'POINT:{entity_index}',
                    [
                        tuple([conversion_factor * x for x in entity.dxf.location]),
                    ]
            )

            # Add point to geometries
            geometries.append(one_point)

        elif name == 'LINE': 
            # Create line entry: ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
            line = (
                    f'LINE:{entity_index}',
                        [
                            tuple([conversion_factor * x for x in entity.dxf.start.xyz]),
                            tuple([conversion_factor * x for x in entity.dxf.end.xyz])
                        ]
            )

            # Add line to geometries
            geometries.append(line)

        elif name == 'ARC' or name == 'CIRCLE':  # Group Arc and Cirlces from dxf into one type internally
            
            # Set angles
            if name == 'CIRCLE':  # CIRCLE
                start_angle = 0.0
                end_angle = 360.0
            else:  # ARC
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle
            #end if

            # Create arc entry: ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)])
            arc = (
                    f'ARC:{entity_index}',
                    [
                        tuple([conversion_factor * x for x in entity.dxf.center.xyz]),
                        tuple([entity.dxf.radius * conversion_factor, start_angle, end_angle])
                    ]
            )

            # Add arc to geometries
            geometries.append(arc)

        elif name == 'ELLIPSE':
            # Create ellipse entry: ('ELLIPSE:#': [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            ellipse = (
                f'{name}:{entity_index}',
                [
                    tuple([conversion_factor * x for x in entity.dxf.center.xyz]),
                    tuple([conversion_factor * x for x in entity.dxf.major_axis.xyz]),
                    (entity.dxf.ratio, )
                ]
            )

            # Add ellipse to geometries
            geometries.append(ellipse)

        elif name == 'SPLINE':

            # Create variables
            points: List[Tuple[float, ...]] = []
            knots: Tuple[float, ...] = []
            weights: Tuple[float, ...] = []

            # Add degree,closed,#control points
            points.append(tuple([entity.dxf.degree, entity.CLOSED, len(entity.control_points)]))

            # Convert control points
            for index,point in enumerate(entity.control_points):
                points.append(tuple(conversion_factor*x for x in point))
            
            # Convert knots
            for knot in entity.knots:
                knots += (knot,)
            points.append(knots)

            # Create weights if necessary
            if len(entity.weights) == 0:
                for point in range(len(entity.control_points)):
                    weights += (1.0,)
            else:
                for point in range(len(entity.control_points)):
                    weights += (entity.weights[point],)
            points.append(weights)

            # Create spline entry: ('SPLINE:#': [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
            spline = (
                f'{name}:{entity_index}',points
            )

            # Add spline to geometries
            geometries.append(spline)

        elif name == 'LWPOLYLINE':
            points: List[Tuple[float, ...]] = []
            
            # Create points
            for index in range(int(len(entity.lwpoints.values)/5)):  # Format points
                value = entity.lwpoints.values
                value_index = 5*index
                points.append((conversion_factor*value[value_index],
                    conversion_factor*value[value_index+1],
                    value[value_index+2],
                    value[value_index+3],
                    value[value_index+4],))
            #end for

            # Add closed/open
            points.append((1.0 if entity.closed else 0.0))

            # Create lwpolyline entry: ('LWPOLYLINE:#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
            lwpolyline = (
                f'{name}:{entity_index}', points
            )

            # Add spline to geometries
            geometries.append(lwpolyline)

        # Unsupported geometries
        else:
            # Throw a warning when entity is not accounted for
            warning(f'UNKNOWN GEOMETRY: {name}')
        # end if
    #end for

    return geometries
#end def

def export_dxf_file(
    filename: str,
    scans: TGeometryList,
    exportunits: Optional[str] = 'um') -> bool:
    '''
    Summary:
        Export/create a DXF file from a list of entities
    Args:
        filename (str): DXF filename with path
        scans (List[Dict [str, List[Tuple[float,...]]]]): List of geometries to write to DXF file
        units (int, optional): [description]. Units to export DXF in, defaults 13=Microns.
        List of exportable geometries:
            POINT: ('POINT:#': [(X,Y,Z)])
            LINE: ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)]) NOTE this includes circles
            ELLIPSE: ('ELLIPSE:#': [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE:#': [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
            LWPOLYLINE: ('LWPOLYLINE:#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
    Raises:
        Exception: No scans are passed
        Exception: No file extension is passed
        Exception: Invalid units are passed
        Warning: Unknown Geometry is found
    Returns:
        bool: True upon successful completion
    '''
    # Create DXF file with given filename
    dxf_drawing: Drawing = ezdxf.new('R2010')

    # Set output units
    if exportunits in UNIT_TABLE:
        # Set units to passed units
        dxf_drawing.units = UNIT_TABLE.index(exportunits)
    else:
        raise Exception('Invalid Units {}', exportunits) from None

    # Get modelspace
    model_space: Modelspace = dxf_drawing.modelspace()

    # Check to make sure that scans is not null
    if len(scans) == 0:
        raise Exception('Scans contains no objects') from None

    # Add each entitiy in the passed list
    for entry in scans:

        # Name of geometry
        name = entry[0]  

        # Truncate name to just include the geometry
        geometry_name: str = ''.join([i for i in name if i.isalpha()])

        # List to store geometry
        points: List[Tuple[float, ...]] = entry[1]

        if geometry_name == 'POINT':

            # Create point from ('POINT:#': [(X,Y,Z)])
            model_space.add_point(points[0])

        elif geometry_name == 'LINE':

            # Create line from ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
            model_space.add_line(points[0], points[1])

        elif geometry_name == 'ARC':

            # Circle
            if points[1][1] == 0 and points[1][2] == 360:
                # Create circle from ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)])
                model_space.add_circle(points[0],points[1][0])

            else:
                # Create arc from ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)])
                model_space.add_arc(points[0], points[1][0], points[1][1], points[1][2], True)

        elif geometry_name == 'ELLIPSE':

            # Create ellipse from ('ELLIPSE:#': [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            model_space.add_ellipse(points[0], points[1], points[2][0])

        elif geometry_name == 'SPLINE':
            control_points: Iterable[Vertex] = []

            # Convert tuple to iterable of vertices
            for i in range(points[0][2]): control_points.append(points[i+1])

            # Determine if the spline is open or closed
            if points[0][1] == 1:  

                # Create spline from ('SPLINE:#': [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
                model_space.add_rational_spline(
                    control_points, points[points[0][2]+2], points[0][0], points[points[0][2]+1])
            else:

                # Create spline from ('SPLINE:#': [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
                model_space.add_closed_rational_spline(
                    control_points, points[points[0][2]+2], points[0][0], points[points[0][2]+1])

        elif geometry_name == 'LWPOLYLINE':

            # Get and remove closed boolean
            closed: bool = points[-1]
            del points[-1]
            
            # Create lwpolyline from LWPOLYLINE: ('LWPOLYLINE:#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
            model_space.add_lwpolyline(
                points, 
                dxfattribs={
                    'closed': closed
                    }
                )

        else:

            # Throw a warning when entity is not accounted for
            warning('UNKNOWN GEOMETRY: '+geometry_name)
        #end if
    #end for

    # Catch filename with no extension and raise an error
    if not filename.endswith('.dxf'):
        raise Exception('Filename does not contain extension')

    # Save DXF file
    dxf_drawing.saveas(filename)

    # Return True if successful
    return True
#end def


def import_txt_file(
    filename: str,
    units: Optional[str] = 'um') -> TGeometryList:
    '''
    Summary:
        Imports a list of points from a textfile
    Args:
        filname (str): TXT filename with path
        units (str, optional): Units to import TXT in, defaults to Microns.
    Raises:
        Exception: Passed file name is not found
    Returns:
        List[Dict [str, List[Tuple[float,...]]]]: A list of points followed by a unique ID # and a list of associated values in 2D/3D
        List of supported geometries and how they are stored
            POINT: ('POINT#': [LOCATION (X,Y,Z)])
    '''
    # Import text file
    # TODO: convert to use 'with' file context
    try:
        file = open(filename)
        lines: List[str] = file.readlines()
    except FileNotFoundError as error:
        # Reraise error
        raise Exception('File Not Found') from error
    #end try

    # Create empty list for geometries and index
    geometries: TGeometryList = []
    geometries_index = 0

    # Get conversion factor
    unit_index = UNIT_TABLE.index(units)
    conversion_factor = CONVERSION_FACTORS[unit_index + 1]

    # Loop through all lines
    for line in lines:
        # Remove newline character
        line = line.rstrip('\n')

        # Determine if line is a valid point
        valid_3d_point = re.fullmatch(r'\d+.\d+,\d+.\d+,\d+.\d+', line)
        valid_2d_point = re.fullmatch(r'\d+.\d+,\d+.\d+', line)

        if valid_3d_point or valid_2d_point:
            # Get points, convert to float, multiply by conversion factor
            points: Tuple[float] = tuple(
                point*conversion_factor for point in map(float, re.findall(r'\d+.\d+', line)))

            # Add to geometries
            geometries.append({'POINT'+str(geometries_index): points})

            # Increase index
            geometries_index += 1

    # Close text file
    file.close()

    # Return list of geometries
    return geometries
#end def


def export_txt_file(
    filename: str,
    scans: TGeometryList) -> bool:
    '''
    Summary:
        Creates/Overrides a TXT file with a list of points passed
    Args:
        filename (str): TXT filename with path
        scans (List[Dict [str, List[Tuple[float,...]]]]): List of geometries to write to TXT file
        List of Exportable Geometries:
            List of supported geometries and the format
            POINT: #.#,#.#,#.#
    Raises:
        Warning: Unknown/Unsupported Geometry is passed
    Returns:
        bool: Returns true upon successful completion
    '''
    # Create a new textfile if one does not already exist
    # NOTE will override existing files with the same name
    text_file = open(filename, 'w+')

    # Cycle through every geometry from the scans list
    for entry in scans:
        for entity in entry:

            # Get the point's x,y,(z)
            point = entry.get(entity)
            output: str = ''

            if entity[0:-1].lower() == 'point':
                # Generate formatted string based on point
                output = str(point[0])[1:-1]
            else:
                warning('Unsupported geometry')

            # Write to text file with newline
            text_file.write(output+'\n')

    # Close text_file
    text_file.close()

    # Return true upon successful completion
    return True
#end def


def import_csv_file(
    filename: str,
    allowedtypes: List[str] = [],
    units: Optional[str] = 'um') -> TGeometryList:
    '''
    Summary:
        Imports and formats geometries from a csv file
    Args:
        filname (str): CSV filename with path
        allowedtypes (List[str]): list of allowed geometry types (eg. POINT, LINE...),
        if the list is empty then all types will be imported.
        units (str, optional): Units to import CSV in, defaults to Microns.
    Raises:
        Exception: Passed file name is not found
     Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, represented in microns and degrees
        List of supported geometries and how they are stored
            POINT: ('POINT#': [LOCATION (X,Y,Z)])
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC#': [CENTER (X,Y,Z), RADIUS (#), START ANGLE (#), END ANGLE (#)]) NOTE includes circles
            ELLIPSE: ('ELLIPSE#': [CENTER (X,Y,Z), LENGTH OF MAJOR AXIS (#), RATIO OF MINOR TO MAJOR AXIS (#)])
    '''
    # TODO: convert to use 'with' file context
    try:
        file = open(filename, newline='')
        imported_csv: csv = csv.reader(file, delimiter=',')

    except FileNotFoundError as error:
        # Reraise error
        raise Exception('File Not Found') from error
    #end try

    # Get conversion factor
    # TODO: handle index error
    unit_index = UNIT_TABLE.index(units)
    conversion_factor = CONVERSION_FACTORS[unit_index + 1]

    # Create empty list for geometries and index
    geometries: TGeometryList = []

    # Skip first line (it should be a header line)
    next(imported_csv)

    # Loop through all entries
    for row in imported_csv:
        # Get geometry name
        name = row[1].upper()

        # Check if this is an allowed geometry type
        if allowedtypes and name not in allowedtypes:
            continue

        # Create points array for entry's points
        points: List[Tuple[float, ...]] = []

        # Format arguments
        if name == 'POINT':
            points.append(tuple(
                [point*conversion_factor for point in map(float, re.findall(r'\d+.\d+', row[2]))]))  # X,Y,Z

        elif name == 'LINE':
            points.append(tuple([point*conversion_factor for point in map(
                float, re.findall(r'\d+.\d+', row[2]))]))  # Start point
            points.append(tuple([point*conversion_factor for point in map(
                float, re.findall(r'\d+.\d+', row[3]))]))  # End point

        elif name == 'CIRCLE':
            points.append(tuple(
                [point*conversion_factor for point in map(float, re.findall(r'\d+.\d+', row[2]))]))  # Center
            # Radius TODO assumes degrees
            points.append(
                (conversion_factor*float(re.findall(r'\d+.\d+', row[3])[0])))

        elif name == 'ARC' or name == 'CIRCLE':
            points.append(tuple(
                [point*conversion_factor for point in map(float, re.findall(r'\d+.\d+', row[2]))]))  # Center
            points.append(
                (conversion_factor*float(re.findall(r'\d+.\d+', row[3])[0])))  # Radius
            points.append((float(row[4])))  # Start Angle
            points.append((float(row[5])))  # End Angle

        elif name == 'ELLIPSE':
            points.append(tuple(
                [point*conversion_factor for point in map(float, re.findall(r'\d+.\d+', row[2]))]))  # Center
            # Length of Major Axis NOTE assumed to be in the x-axis
            points.append(tuple([(float(row[3])), 0.0, 0.0]))
            points.append((float(row[4])))  # Ratio of Minor to Major Axis

        # Add entry to geometries
        # what's row[0]?
        geometries.append((name, points))
    
    #end for
    file.close()

    return geometries
# end def


def export_csv_file(
    filename: str,
    scans: TGeometryList) -> bool:
    '''
    Summary:
        Creates/Overrides a CSV file with a list of geometries passed
    Args:
        filename (str): CSV filename with path
        scans (List[Dict [str, List[Tuple[float,...]]]]): List of geometries to write to CSV file
        List of Exportable Geometries:
            List of supported geometries and the format
            POINT: ('POINT#': [LOCATION (X,Y,Z)])
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            CIRCLE: ('CIRCLE#': [RADIUS (#), CENTER (X,Y,Z), PLANE (X,Y,Z)])
            ARC: ('ARC#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#), PLANE (X,Y,Z)])
            ELLIPSE: ('ELLIPSE#': [CENTER (X,Y,Z), LENGTH/PLANE OF MAJOR AXIS (X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
    Raises:
        Warning: Unknown/Unsupported Geometry is passed
    Returns:
        bool: Returns true upon successful completion
    '''
    # NOTE will override existing files with the same name
    # Create a csv file if not already created
    output_table: csv = csv.writer(
        open(filename, 'w', newline=''), delimiter=',')
    output_table.writerow(['name', 'scantype', 'arg1', 'arg2', 'arg3', 'arg4'])

    # Cycle through every geometry from the scans list
    for entry in scans:
        for entity in entry:

            # Create an empty row
            row = ['', '', '', '', '', '']

            # Add name and scantype
            row[0] = entity
            scantype: str = ''.join(
                [i for i in entity.lower() if not i.isdigit()])
            row[1] = scantype

            # Get list of args
            args = entry.get(entity)

            # Format according to geometry
            if scantype == 'point':
                # Add x,y,z coordinate
                row[2] = str(args[0])[1:-1]
            elif scantype == 'line':
                # Add start point
                row[2] = str(args[0])[1:-1]
                # Add end point
                row[3] = str(args[1])[1:-1]
            elif scantype == 'circle':
                # Add center point
                row[2] = str(args[0])[1:-1]
                # Add radius
                row[3] = args[1]
            elif scantype == 'arc':
                # Add center point
                row[2] = str(args[0])[1:-1]
                # Add radius
                row[3] = args[1]
                # Add start angle
                row[4] = args[2]
                # Add end angle
                row[5] = args[3]
            elif scantype == 'ellipse':
                # Add center point
                row[2] = str(args[0])[1:-1]
                # Add length of major axis
                row[3] = str(args[1])[1:-1]
                # Add ratio of minor to major
                row[4] = args[2]
            else:
                warning('Unsupported geometry')

            # Add row to the table
            output_table.writerow(row)

    # Return true upon successful
    return True
#end def


def import_file(
    filename: str,
    units: Optional[str]) -> TGeometryList:
    '''
    Wrapper function for importing all filetypes
    Args:
        filname (str): Filename with path
        units (str, optional): Units to import in, defaults to Microns.
    Raises:
        Exception: Unknown filetype
    Returns:
        TGeometryList: List of geometries
    '''

    # Get file extension
    file_type: str = filename.split('.')[1].upper()

    # Run appropriate function
    # DXF file
    if (file_type == "DXF"):
        return import_dxf_file(filename)

    # CSV file
    elif (file_type == "CSV"):
        return import_csv_file(filename)

    # TXT file
    elif (file_type == "TXT"):
        return import_txt_file(filename)

    else:
        # Unknown filetype
        raise Exception('Filetype Unknown')
        # end if
#end def

if __name__ == '__main__':
    geometry = import_dxf_file("Test Files/Basic LWPolyline.dxf")
    export_dxf_file('TEST.dxf',geometry)