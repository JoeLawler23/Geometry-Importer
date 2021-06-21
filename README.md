## Geometry-Import:

# Release 1.2.1
- Updated alphabet to line to conform to new geometry type

# Release 1.2.0
- Automatically down convert all geometry types for all file types
- Down convert based on number of segments or segment length
- Test suite functions for testing down conversion
- Formatting and cleanup

# Release 1.1.0
- Migrated geometry format from dictionary to tuple
- Can now exclude certain geometries from import
- Overhaul of formatting
- Caught un-closed file errors
- Updated readme and function headers
- Alphabet and tests updated to reflect new geometry format

# Release 1.0.0
- Import geometries from DXF,CSV,TXT files and convert to nanometers
- Exclude certain geometries from importing
- Test suite for functions
- Dictionary of line based geometries representing the alphabeta and numbers(0-9)

# Importer Functions:

get_hifi_geometry(
    geometry: str,
    allowedtypes: List[str]
    ) -> str:

    Summary:
        Return the highest fidelity geometry given a list of geometries for a specific geometry type
    Args:
        geometry (str): geometry type to search below
        allowedtypes (List[str]): list of allowed geometry types (eg. POINT, LINE, ...)
    Returns:
        str: highest fidelity geometry from allowedtypes list

import_dxf_file(
    filename: str,
    allowedtypes: List[str] = []
    ) -> TGeometryList:

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
            POINT: ('POINT:#', [(X,Y,Z)])
            LINE: ('LINE:#', [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC:#', [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)]) NOTE Includes circles
            ELLIPSE: ('ELLIPSE:#', [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE:#', [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
            LWPOLYLINE: ('LWPOLYLINE:#', POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])

def export_dxf_file(
    filename: str,
    scans: TGeometryList,
    exportunits: Optional[str] = 'um'
    ) -> bool:

    Summary:
        Export/create a DXF file from a list of entities
    Args:
        filename (str): DXF filename with path
        scans (TGeometryList): List of geometries to write to DXF file
        exportunits (str, optional): Units to export DXF in, defaults 'um'=Microns.
        List of exportable geometries:
            POINT: ('POINT:#', [(X,Y,Z)])
            LINE: ('LINE:#', [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC:#', [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)]) NOTE Includes circles
            ELLIPSE: ('ELLIPSE:#', [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
            SPLINE: ('SPLINE:#', [DEGREE, CLOSED, # CONTROL POINT(S) (#,BOOLEAN,#)], CONTROL POINT(S) [(X,Y,Z)], KNOT(S) [#,...], WEIGHT(S) [#,...])
            LWPOLYLINE: ('LWPOLYLINE:#', POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
    Raises:
        Exception: No scans are passed
        Exception: No file extension is passed
        Exception: Invalid units are passed
        Warning: Unknown Geometry is found
    Returns:
        bool: True upon successful completion

import_txt_file(
    filename: str,
    units: Optional[str] = 'um'
    ) -> TGeometryList:

    Summary:
        Imports a list of points from a textfile
    Args:
        filname (str): TXT filename with path
        units (str, optional): Units to import TXT in, defaults to Microns.
    Raises:
        Exception: Passed file name is not found
    Returns:
        TGeometryList: A list of points followed by a unique ID # and a list of associated values in 2D/3D
        List of supported geometries and how they are stored
            POINT: ('POINT:#', [(X,Y,Z)])

export_txt_file(
    filename: str,
    scans: TGeometryList,
    exportunits: Optional[str] = 'um'
    ) -> bool:

    Summary:
        Creates/Overrides a TXT file with a list of points passed
    Args:
        filename (str): TXT filename with path
        scans (TGeometryList): List of geometries to write to TXT file
        exportunits (str, optional): Units to export TXT in, defaults to Microns.
        List of Exportable Geometries:
            List of supported geometries and the format
            POINT: #.#,#.#,#.#
    Raises:
        Warning: Unknown/Unsupported Geometry is passed
    Returns:
        bool: Returns true upon successful completion

import_csv_file(
    filename: str,
    allowedtypes: List[str] = [],
    units: Optional[str] = 'um',
    header: Optional[bool] = True
    ) -> TGeometryList:
    
    Summary:
        Imports and formats geometries from a csv file
    Args:
        filname (str): CSV filename with path
        allowedtypes (List[str]): List of allowed geometry types (eg. POINT, LINE...),
        NOTE If the list is empty then all types will be imported.
        units (str, optional): Units to import CSV in, defaults to 'um'=Microns.
        header (bool, optional): Flag to remove header line
    Raises:
        Exception: Passed file name is not found
        Warning: Passed units are not valid
     Returns:
        TGeometryList: A list of all geometry names followed by a unique ID # and a list of associated points in 2D/3D, represented in microns and degrees
        List of supported geometries and how they are stored
            POINT: ('POINT:#', [(X,Y,Z)])
            LINE: ('LINE:#', [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC:#', [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)]) NOTE Includes circles
            ELLIPSE: ('ELLIPSE:#', [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])

export_csv_file(
    filename: str,
    scans: TGeometryList,
    exportunits: Optional[str] = 'um',
    header: Optional[bool] = True
    ) -> bool:
    
    Summary:
        Creates/Overrides a CSV file with a list of geometries passed
    Args:
        filename (str): CSV filename with path
        scans (TGeometryList): List of geometries to write to CSV file
        exportunits (str, optional): Units to export CSV in, defaults 'um'=Microns.
        header (bool, optional): Flag to add header line
        List of Exportable Geometries:
            List of supported geometries and the format
            POINT: ('POINT:#', [(X,Y,Z)])
            LINE: ('LINE:#', [START (X,Y,Z), END (X,Y,Z)])
            ARC: ('ARC:#', [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)]) NOTE Includes circles
            ELLIPSE: ('ELLIPSE:#', [CENTER (X,Y,Z), MAJOR AXIS ENDPOINT(X,Y,Z), RATIO OF MINOR TO MAJOR AXIS (#)])
    Raises:
        Warning: Unknown/Unsupported Geometry is passed
    Returns:
        bool: Returns true upon successful completion

import_file(
    filename: str,
    allowedtypes: List[str] = [],
    units: Optional[str] = 'um',
    header: Optional[bool] = True,
    convert: Optional[bool] = False,
    num_segments: float = 0, 
    segment_length: float = 0, 
    segment_units: str = 'um'
    ) -> TGeometryList:
    
    Summary:
        Wrapper function for importing all filetypes
    Args:
        filname (str): Filename with path
        allowedtypes (List[str]): List of allowed geometry types (eg. POINT, LINE...),
        NOTE If the list is empty then all types will be imported.
        units (str, optional): Units to import CSV in, defaults to 'um'=Microns.
        header (bool, optional): Flag to remove header line
        convert (bool, optional): flag for whether to convert non-allowed geometry types to allowable geometry types
        num_segments (float, optional): Number of segments to divide given geometry into to produce the return geometry. Defaults to 0.
        segment_length (float, optional): Length of segments to divide given geometry into to produce return geometry. Defaults to 0.
        units (str, optional): Units for segment length. Defaults to 'um'.
    Raises:
        Exception: Unknown filetype
    Returns:
        TGeometryList: List of geometries    

# Alphabet_To_Line Functions:

create_letter(
      letter: str, 
      scans: TGeometryList
      ):

      Summary:
        Generate a list of lines from a DXF file representing a letter
        Meant to be pasted into the ALPHABET dictionary as an entry

      Args:
        letter (str): filename
        scans (TGeometryList): letter geometries from importing the dxf file
      
create_alphabet():
      
      Summary:
        Print out entire ALPHABET dictionary from the Letters folder
      
# Geometry_To_Line Functions:

lines_to_points(
    given_lines: TGeometryList, 
    num_segments: float = 0, 
    segment_length: float = 0, 
    units: str = 'um'
    ) -> TGeometryList:
    
    Summary:
        Convert lines to a series of point geometries
    Args:
        given_lines (TGeometryList): Given line to convert
        num_segments (float, optional): Number of points to convert the given arc into. Defaults to 0.
        segment_length (float, optional): Length between points. Defaults to 0.
        units (str, optional): Units of segment_length. Defaults to 'um'.
    Raises:
        Warning: Invalid units
        Warning: segment_length is too large - check units
    Returns:
        TGeometryList: List of points generated from given lines

arc_to_lines(
    given_arcs: TGeometryList, 
    num_segments: float = 0, 
    segment_length: float = 0, 
    units: str = 'um'
    ) -> TGeometryList:
    
    Summary:
        Converts arcs to a series of line geometries
    Args:
        given_arcs (TGeometryList): Given arc to convert
        num_segments (float, optional): Number of lines to convert the given arc into. Defaults to 0.
        segment_length (float, optional): Length of the lines to convert the given arc into. Defaults to 0.
        units (str, optional): Units of segment_length. Defaults to 'um'.
    Raises:
        Warning: Invalid units
        Warning: segment_length is too large - check units
    Returns:
        TGeometryList: List of lines generated from given arcs 


ellipse_to_arcs(
    given_ellipsis: TGeometryList, 
    num_segments: float = 0
    ) -> TGeometryList:

    Summary:
        Converts ellipsis into a series of arcs
    Args:
        given_ellipsis (TGeometryList): Given ellipses to convert
        num_segments (float, optional): Number of arcs to convert the given ellipse into. Defaults to 0.
    Raises:
        Warning: Divide by zero error
        Warning: Invalid units
    Returns:
        TGeometryList: List of arcs generated from given ellipse

lwpolyline_to_arcs_lines(
    given_lwpolylines: TGeometryList
    )-> TGeometryList:
    
    Summary:
        Convert lwpolyline into a list of arcs and lines
    Args:
        given_lwpolylines (TGeometryList): Given polyline
    Returns:
        TGeometryList: List of arcs and lines that represent the given geometry
    
spline_to_lines(
    given_spline: TGeometryList
    )-> TGeometryList:

    Summary:
        Convert spline into a list of lines
    Args:
        given_spline (TGeometryList): Given spline
    Returns:
        TGeometryList: List of lines that represent the given geometry

convert_to(
    given_geometry_type: str, 
    return_geometry_type: str, 
    given_geometry: TGeometryList, 
    num_segments: float = 0, 
    segment_length: float = 0, 
    units: str = 'um'
    ) -> TGeometryList:
    
    Summary:
        Wrapper function to down convert any given geometry to a sub-geometry type
    Args:
        given_geometry_type (str): Geometry type of passed values
        return_geometry_type (str): Desired geometry type
        given_geometry (TGeometryList): Geometry to be converted values
        num_segments (float, optional): Number of segments to divide given geometry into to produce the return geometry. Defaults to 0.
        segment_length (float, optional): Length of segments to divide given geometry into to produce return geometry. Defaults to 0.
        units (str, optional): Units for segment length. Defaults to 'um'.
    Returns:
        TGeometryList: Desired geometry type return values
