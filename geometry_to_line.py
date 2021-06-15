from logging import warning
from typing import List, Tuple
import math
import ezdxf
from ezdxf.document import Drawing
from ezdxf.entities.lwpolyline import LWPolyline

from ezdxf.layouts.layout import Modelspace

__author__ = 'Joseph Lawler'
__version__ = '1.1.0'

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

# FIXME FIX SEGMENT_LENGTH implementation

# Default conversion parameter
NUM_SEGMENTS = 10

# Define type for containing geometry elements
TGeometryItem = Tuple[str, List[Tuple[float, ...]]]
TGeometryList = List[TGeometryItem]

def lines_to_points(given_lines: TGeometryList, num_segments: float = 0, segment_length: float = 0, units: str = 'um') -> TGeometryList:
    """
    Convert lines to a series of point geometries

    Args:
        given_lines (TGeometryList): Given line to convert
        num_segments (float, optional): Number of points to convert the given arc into. Defaults to 0.
        segment_length (float, optional): Length between points. Defaults to 0.
        units (str, optional): Units of segment_length. Defaults to 'um'.
    Raises:
        Warning: Invalid units
    Returns:
        TGeometryList: List of points generated from given lines
    """

    # Generated Points
    points: TGeometryList = []

    # Point index
    point_index: int = 0

    # Run through all given lines
    for line in given_lines:
        
        # Get start and end points
        values = line[1]
        start_point = values[0]
        end_point = values[1]

        # Make sure start and end points are not the same
        if not start_point == end_point:

            # Set conversion factor
            if units in UNIT_TABLE:
                # Set units to passed units
                conversion_factor = CONVERSION_FACTORS[UNIT_TABLE.index(units)+1]
            else:
                conversion_factor = 1
                raise Exception('Invalid Units {}', units) from None

            # Create points based on number of segments desired
            if num_segments:

                # Calc segment length based on num_segments
                x_difference = (end_point[0] - start_point[0]) / num_segments  

            # Create lines based on minimum line length TODO get working
            elif segment_length:

                # Calc segment angle based on min_length
                segment_length = segment_length*conversion_factor

                # Calc num_segments from segment_length
                num_segments = ((start_point[1] - end_point[1]) / segment_length)  
            else:

                # Default param
                num_segments = NUM_SEGMENTS

                # Calc segment length based on num_segments
                x_difference = (end_point[0] - start_point[0]) / num_segments  

            # Define slope
            slope = 0.0

            # Used as indicator for special cases
            slope_type: str = 'NONE'

            if (start_point[1]-end_point[1]) == 0:

                # Horizontal line
                slope_type = 'HORIZONTAL'

            elif (start_point[0]-end_point[0]) == 0:

                # Vertical line
                slope_type = 'VERTICAL'

            else:

                # Calculate the slope using point slope form
                slope = ((start_point[1]-end_point[1])/(start_point[0]-end_point[0]))
            #end if

            # Calculate y-intercept
            y_intercept = start_point[1] - slope*start_point[0]

            # Generate points based on x-values
            for index in range(0,num_segments):

                if slope_type == 'NONE':

                    # Calculate next point for a normal slope
                    x = start_point[0] + x_difference*index*(1 if (start_point[0] - end_point[0]) > 0 else -1)
                    y = x*slope + y_intercept

                elif slope_type == 'HORIZONTAL':

                    # Calculate next point for a horizontal slope
                    x = start_point[0] + x_difference*index
                    y = start_point[1]

                elif slope_type == 'VERTICAL':

                    # Calculate next point for vertical slope
                    y_difference = ((end_point[1] - start_point[1])/num_segments)
                    x = start_point[0]
                    y = start_point[1] + y_difference*index

                # Create point entry: ('POINT:#': [(X,Y,Z)])
                point = (
                    f'POINT:{point_index}',
                        [
                            tuple([x,y,0.0]),
                        ]
                )

                # Update point_index
                point_index += 1

                # Add point to points
                points.append(point)
        else:
            # Same start and end point
            # Create point entry: ('POINT:#': [(X,Y,Z)])
            point = (
                f'POINT:{point_index}',
                    [
                        tuple([start_point[0],start_point[1],0.0]),
                    ]
            )

            # Add point to points
            points.append(point)

        # end if
    #end for

    return points
#end def

def arc_to_lines(given_arcs: TGeometryList, num_segments: float = 0, segment_length: float = 0, units: str = 'um') -> TGeometryList:
    """
    Converts arcs to a series of line geometries

    Args:
        given_arcs (TGeometryList): Given arc to convert
        num_segments (float, optional): Number of lines to convert the given arc into. Defaults to 0.
        segment_length (float, optional): Length of the lines to convert the given arc into. Defaults to 0.
        units (str, optional): Units of segment_length. Defaults to 'um'.
    Raises:
        Warning: Invalid units
    Returns:
        TGeometryList: List of lines generated from given arcs
    """
    
    # Generated Lines
    lines: TGeometryList = [] 

    # Line index
    line_index: int = 0
    
    # Run through all given arcs
    for arc in given_arcs:

        # If an arc
        if arc[0].__contains__('ARC'):

            # Define arc values
            values = arc[1]
            center = values[0]
            radius = values[1][0]
            start_angle = values[1][1]
            end_angle = values[1][2]
            degree = end_angle - start_angle

            # Points
            points: List[Tuple[float, ...]] = []

            # Set conversion factor
            if units in UNIT_TABLE:
                # Set units to passed units
                conversion_factor = CONVERSION_FACTORS[UNIT_TABLE.index(units)+1]
            else:
                conversion_factor = 1
                raise Exception('Invalid Units {}', units) from None

            # Create lines based on number of segments desired
            if num_segments > 2:

                # Calc segment angle based on num_segments
                segment_angle = degree/(num_segments)  

            # Create lines based on minimum line length TODO add catch for too long segment length
            elif segment_length > 0:

                # Calc segment angle based on min_length
                segment_angle = (segment_length*conversion_factor/(radius*2*math.pi))*360

                # Calc num_segments from segment_angle
                num_segments = int(degree/segment_angle)
            else:

                # Default param
                num_segments = NUM_SEGMENTS

                # Calc segment angle based on num_segments
                segment_angle = degree/(num_segments)  

            # For each point on the arc
            for index in range(0, num_segments+1):

                # Calc point's angle
                angle = start_angle + (segment_angle * index) 

                # Convert to cartesian
                x = radius*math.cos(math.radians(angle))/conversion_factor  
                y = radius*math.sin(math.radians(angle))/conversion_factor 

                # Add point with center offset
                points.append([x+center[0], y+center[1], center[2]]) 
            #end for

            # Make each point into a line
            for index in range(0, num_segments):

                # Create line entry: ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
                line = (
                        f'LINE:{line_index}',
                        [
                            tuple([conversion_factor * x for x in points[index]]),
                            tuple([conversion_factor * x for x in points[index+1]])
                        ]
                )

                # Update line_index
                line_index += 1

                # Add line to lines
                lines.append(line)
            #end for

            # Connect ends
            if end_angle - start_angle == 360:

                # Create line entry: ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
                line = (
                        f'LINE:{line_index}',
                        [
                            tuple([conversion_factor * x for x in points[num_segments]]),
                            tuple([conversion_factor * x for x in points[0]])
                        ]
                )

                #Update line_index
                line_index += 1

                # Add line to lines
                lines.append(line)
        else:

            # If not an arc just add
            lines.append(arc)

        #end if
    #end if
    return lines
#end def

def ellipse_to_arcs(given_ellipsis: TGeometryList, num_segments: float = 0, segment_length: float = 0, units: str = 'um') -> TGeometryList:
    '''
    Converts ellipsis into a series of arcs

    Args:
        given_ellipsis (TGeometryList): Given ellipses to convert
        num_segments (float, optional): Number of arcs to convert the given ellipse into. Defaults to 0.
        segment_length (float, optional): Size of the arc to convert the given ellipse into. Defaults to 0.
        units (str, optional): Units of segment length.
    Raises:
        Warning: Segment length > circumfrance
        Warning: Divide by zero error
        Warning: Invalid units
    Returns:
        TGeometryList: List of arcs generated from given ellipse
    '''

    # List of arcs that will be generated
    arcs: TGeometryList = []

    # Arc index
    arc_index: int = 0

    # Run through all given ellipses
    for ellipse in given_ellipsis:

        # Define ellipse values
        values = ellipse[1]
        center = values[0]
        major_radius = values[1][0] # a
        minor_radius = values[2][0] * major_radius # b

        # Define points list for arc mid and end points
        points: List[Tuple[float, ...]] = []

        # Define angle to create points list from
        angle: float = []

        # Set conversion factor
        if units in UNIT_TABLE:
            # Set units to passed units
            conversion_factor = CONVERSION_FACTORS[UNIT_TABLE.index(units)+1]
        else:
            conversion_factor = 1
            raise Exception('Invalid Units {}', units) from None

        if num_segments:

            # Calculate angle length from num_segments
            angle = (360/num_segments)/2 

        elif segment_length:

            # Circumfrance of Ellipse
            # = 2*PI*sqrt((a^2 + b^2)/2)
            circumfrance = 2*math.pi*math.sqrt((major_radius*major_radius + minor_radius*minor_radius)/2)

            if segment_length/conversion_factor > circumfrance:
                warning('Invalid segment_length: segment_length > circumfrance')
                continue

            # Calculate angle length from segment_length
            angle = (segment_length/circumfrance) * 360

            # Calculate the number of segments 
            # num_segments = 

        else:

            # Default param
            num_segments = NUM_SEGMENTS
            
            # Calculate angle length from num_segments
            angle = (360/num_segments)/2 
        
        #end if

        # Define as start angle
        theta = 0

        # Generate key points to define arcs by
        # Need to generate 2x number of points to account for midpoints
        for index in range(0,2*num_segments):  

            # Calculate current angle and radius
            theta = index*angle
            radius = major_radius*minor_radius / (
                math.sqrt(math.pow(minor_radius*math.cos(math.radians(theta)),2) + 
                math.pow((major_radius*math.sin(math.radians(theta))),2))
            )

            # Convert to cartesian
            x:float = radius*math.cos(math.radians(theta))
            y:float = radius*math.sin(math.radians(theta))

            # Add point with center offset
            points.append([x+center[0], y+center[1], center[2]])  
        
        #end for

        # Find arc that encompasses 3 points
        for index in range(0,num_segments):

            # Define 3 points to create arc from
            p1x: float = points[2*index][0]
            p1y: float = points[2*index][1]
            p2x: float = points[2*index+1][0]
            p2y: float = points[2*index+1][1]
            p3x: float = points[((2*index+2)%(len(points)))][0]
            p3y: float = points[((2*index+2)%(len(points)))][1]

            try:
                # Derived formula for calculating the arc's center
                cx: float = ((p1x*p1x + p1y*p1y - p2x*p2x - p2y*p2y) - (((2*p1y - 2*p2y)*(p1x*p1x + p1y*p1y -p3x*p3x - p3y*p3y))/(2*p1y -2*p3y)))/((2*p1x - 2*p2x) - ((2*p1y-2*p2y)*(2*p1x-2*p3x))/(2*p1y-2*p3y))
                cy: float = ((p1x*p1x + p1y*p1y - p3x*p3x - p3y*p3y)/(2*p1y - 2*p3y))-(cx*((2*p1x-2*p3x)/(2*p1y - 2*p3y)))
            except ZeroDivisionError:
                warning ('Divide by zero error')
            
            # Calculate the radius of arc given the arc's center-point
            radius: float = math.sqrt(math.pow(p1x-cx,2) + math.pow(p1y-cy,2))

            # Calculate angle range for arc
            start_angle = (math.degrees(math.atan2((p1y-cy),(p1x-cx))))
            end_angle = math.degrees(math.atan2((p3y-cy),(p3x-cx)))
            
            # Create arc entry: ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)])
            arc = (
                    f'ARC:{arc_index}',
                        [
                            tuple([cx/conversion_factor,cy/conversion_factor,0]),
                            tuple([radius/conversion_factor,start_angle,end_angle])
                        ]
            )
            
            # Update arc_index
            arc_index += 1

            # Add arc to list of arcs
            arcs.append(arc)

        #end for
    #end for

    # Return all created arcs
    return arcs
#end def
    
def lwpolyline_to_arcs_lines(given_lwpolylines: TGeometryList)-> TGeometryList:
    """
    Convert lwpolyline into a list of arcs and lines

    Args:
        given_lwpolylines (TGeometryList): Given polyline

    Returns:
        TGeometryList: List of arcs and lines that represent the given geometry
    """

    # List of arcs and lines that will be generated
    arcs_lines: TGeometryList = []

    # Arc index
    arcs_lines_index: int = 0

    # Run through all given lwpolylines 
    for lwpolyline in given_lwpolylines:

        # Create DXF file with given filename
        dxf_drawing: Drawing = ezdxf.new('R2010')

        # Create modelspace
        model_space: Modelspace = dxf_drawing.modelspace()

        # Polyline values
        points = lwpolyline[1]

        # Create lwpolyline entity
        # Get and remove closed boolean
        closed: bool = points[-1]
        del points[-1]

        # Convert points to proper units
        values: List[Tuple[float, ...]] = []
        for i in range(len(points)): values.append(tuple(point/1 for point in points[i]))

        # Create lwpolyline from LWPOLYLINE: ('LWPOLYLINE:#:' POINT VALUES [X,Y,Z,START WIDTH,END WIDTH,BULGE], CLOSED/OPEN [BOOLEAN])
        model_space.add_lwpolyline(
            values, 
            dxfattribs={
                'closed': closed
                }
            )

        # Use dxf explode method to create arc and lines from lwpolyline
        dxf_lwpolyline = model_space.entity_space.entities[0]
        converted_lwpolyline =  dxf_lwpolyline.explode()

        # Convert from ezdxf format to TGeometryList format
        for entity in converted_lwpolyline.entities:

            # Get enetity name
            name: str = entity.DXFTYPE

            if name == 'LINE':

                # Create line entry: ('LINE:#': [START (X,Y,Z), END (X,Y,Z)])
                line = (
                        f'LINE:{arcs_lines_index}',
                        [
                            tuple([1 * x for x in entity.dxf.start.xyz]),
                            tuple([1 * x for x in entity.dxf.end.xyz])
                        ]
                )

                # Add line to list of arcs and lines
                arcs_lines.append(line)

            elif name == 'ARC':
                 
                # Create arc entry: ('ARC:#': [CENTER (X,Y,Z), RADIUS/START ANGLE/END ANGLE(#,#,#)])
                arc = (
                        f'ARC:{arcs_lines_index}',
                            [
                                tuple([1 * x for x in entity.dxf.center.xyz]),
                                tuple([entity.dxf.radius * 1, 
                                    entity.dxf.start_angle, 
                                    entity.dxf.end_angle
                                ])
                            ]
                )
                
                # Add arc to list of arcs and lines
                arcs_lines.append(arc)
            #end if
            
            # Update index
            arcs_lines_index += 1

        #end for

    #end for

    # Return list of arcs and lines
    return arcs_lines
#end def

def spline_to_lines(given_lwpolyline: TGeometryList, num_segments: float = 0, segment_length: float = 0, units: str = 'um')-> TGeometryList:

    # Create modelspace
    # Create lwpolyline entity
    # Use flatten method to create lines from spline
    # Convert to my format

    # spl = model_space.entity_space.entities
    # sasdfa = spl[0].flattening(0.10)
    # print
    print

def convert_to(given_geometry_type: str, return_geometry_type: str, given_geometry: TGeometryList, num_segments: float = 0, min_length: float = 0, units: str = 'um') -> TGeometryList:
    '''
    Wrapper function to down convert any given geometry to a sub-geometry type

    Args:
        given_geometry_type (str): Geometry type of passed values
        return_geometry_type (str): Desired geometry type
        given_geometry (Dict[str, List[Tuple[float, ...]]]): Geometry to be converted values
        num_segments (float): Number of segments to divide given geometry into to produce the return geometry
        min_length (float): Minimum length of segments to divide given geometry into to produce return geometry

    Returns:
        TGeometryList: Desired geometry type values
    '''

    if given_geometry_type == return_geometry_type:

        # No need to convert
        return given_geometry

    elif given_geometry_type == 'LINE': 
        
        # Lines can only be directly converted into points
        return convert_to('POINT', return_geometry_type, lines_to_points(given_geometry, num_segments, min_length, units))

    elif given_geometry_type == 'ARC':  
        
        # Arcs can only be directly converted into lines
        return convert_to('LINE', return_geometry_type, arc_to_lines(given_geometry, num_segments, min_length, units))

    elif given_geometry_type == 'ELLIPSE':  
        
        # Ellipses can only be directly converted into arcs
        return convert_to('ARC', return_geometry_type, ellipse_to_arcs(given_geometry, num_segments, min_length, units))

    elif given_geometry_type == 'LWPOLYLINE':

        # LWPolylines are directly converted to arcs and lines
        return convert_to('ARC', return_geometry_type, lwpolyline_to_arcs_lines(given_geometry))

    elif given_geometry_type == 'SPLINE':

        # LWPolylines are directly converted to arcs and lines
        return convert_to('LINE', return_geometry_type, spline_to_lines(given_geometry, num_segments, min_length, units))

    #end if
#end def

