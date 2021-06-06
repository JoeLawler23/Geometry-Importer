# Geometry-Import

Importer:

Python module that can read in a DXF,CSV,TXT files, extract basic geometric elements, and output a list of each element along with the coordinates of each element and any pertinent attributes.

Functions:

import_dxf_file(filename: str) -> List[Dict [str, List[Tuple[float,...]]]]

    Summary:
        Import a DXF file and returning a list of entities

    Args:
        filename (str): DXF filename with path
    
    Raises:
        Exception: Passed file name is not found, corrupt, or not a DXF file
        Warning: Unknown Geometry is found
    
    Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, represented in microns and degrees
    
        List of supported geometries and how they are stored
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            CIRCLE: ('CIRCLE#': [CENTER (X,Y,Z), RADIUS (#), PLANE (X,Y,Z)])
            ARC: ('ARC#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#), PLANE (X,Y,Z)])
            ELLIPSE: ('ELLIPSE#': [CENTER (X,Y,Z), LENGTH/PLANE OF MAJOR AXIS (X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE#': [DEGREE, CLOSED, # CONTROL POINTS (#,BOOLEAN,#), CONTROL POINT(S) (X,Y,Z), KNOTS (#,...), WEIGHTS (#,...)])
            LWPOLYLINE: ('LWPOLYLINE#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])

export_dxf_file(filename: str, scans: List[Dict [str, List[Tuple[float,...]]]], exportunits: str = "um") -> bool

    Summary:
        Export/create a DXF file from a list of entities

    Args:
        filename (str): DXF filename with path
        scans (List[Dict [str, List[Tuple[float,...]]]]): List of geometries to write to DXF file
        units (int, optional): [description]. Units to export DXF in, defaults 13=Microns.

        List of exportable geometries:
            List of supported geometries and the format
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            CIRCLE: ('CIRCLE#': [CENTER (X,Y,Z), RADIUS (#), PLANE (X,Y,Z)])
            ARC: ('ARC#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#), PLANE (X,Y,Z)])
            ELLIPSE: ('ELLIPSE#': [CENTER (X,Y,Z), LENGTH/PLANE OF MAJOR AXIS (X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE#': [DEGREE, CLOSED, # CONTROL POINTS (#,BOOLEAN,#), CONTROL POINT(S) (X,Y,Z), KNOTS (#,...), WEIGHTS (#,...)])
            LWPOLYLINE: ('LWPOLYLINE#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])

    Raises:
        Exception: No scans are passed
        Exception: No file extension is passed
        Exception: Invalid units are passed
        Warning: Unknown Geometry is found

    Returns:
        bool: True upon successful completion

import_txt_file(filname: str, units: str = "um") -> List[Dict [str, List[Tuple[float,...]]]]

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

export_txt_file(filename: str, scans: List[Dict [str, List[Tuple[float,...]]]]) -> bool:

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

import_csv_file(filename: str) -> List[Dict [str, List[Tuple[float,...]]]]

    Summary:
        Imports and formats geometries from a csv file

    Args:
        filname (str): CSV filename with path
        units (str, optional): Units to import CSV in, defaults to Microns.

    Raises:
        Exception: Passed file name is not found

     Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, represented in microns and degrees

        List of supported geometries and how they are stored
            POINT: ('POINT#': [LOCATION (X,Y,Z)])
            LINE: ('LINE#': [START (X,Y,Z), END (X,Y,Z)])
            CIRCLE: ('CIRCLE#': [RADIUS (#), CENTER (X,Y,Z), PLANE (X,Y,Z)])
            ARC: ('ARC#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#), PLANE (X,Y,Z)])
            ELLIPSE: ('ELLIPSE#': [CENTER (X,Y,Z), LENGTH/PLANE OF MAJOR AXIS (X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])

export_csv_file(filename: str, scans: List[Dict [str, List[Tuple[float,...]]]]) -> bool:
    
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


Alphabet To Line:

Create an alphabet of letters and numbers in which each letter/numbers is a collection of lines.
Letter/Number DXF files are in the Letters folder

Functions:

def create_letter_from_dxf(letter: str, scans: List[Dict[str, List[Tuple[float, ...]]]]):

    Generate a list of lines from a DXF file representing a letter made only from lines

    Accepted Geometries: * All other geometries are ignored *
    - Point
    - Line
    - LWPolyline

    Args:
        letter (str): filename
        scans (List[Dict[str, List[Tuple[float, ...]]]]): letter geometries from importing the dxf file

def create_alphabet():
    Print out a list of all dxf files, letters only drawn from lines, in the Letters folder


