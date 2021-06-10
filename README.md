## Geometry-Import:

# Features:
- Import geometries from DXF,CSV,TXT files and convert to nanometers
- Exclude certain geometries from importing
- Test suite for functions
- Dictionary of line based geometries representing the alphabeta and numbers(0-9)

# Importer Functions:

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
    

# Alphabet_To_Line Functions:

def create_letter(
      letter: str, 
      scans: TGeometryList
      ):
      
      Generate a list of lines from a DXF file representing a letter made only from lines
      Meant to be pasted into the LETTERS_NUMBERS dictionary as an entry

      Args:
          letter (str): filename
          scans (TGeometryList): letter geometries from importing the dxf file
      
def create_alphabet():
      
      Print out entire NUMBERS_LETTERS dictionary from the Letters folder
      
# Future Features:
- Auto down-converting geometries
- Converting 3D geometries into 2D geometries
- GUI


