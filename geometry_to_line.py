from logging import warning
from typing import Dict, List, Tuple
import math

from ezdxf.lldxf.const import VRM_2D_OPTIMIZED

CONVESION_FACTORS: List[float] = [
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
]

UNIT_TABLE: Dict[str, int] = {
    'in': 1,  # Inches
    'ft': 2,  # Feet
    'mi': 3,  # Miles
    'mm': 4,  # Milimeters
    'cm': 5,  # Centimeters
    'm': 6,  # Meters
    'km': 7,  # Kilometers
    'ui': 8,  # Microinches
    'mil': 9,  # Mils
    'yd': 10,  # Yards
    'a': 11,  # Angstroms
    'nm': 12,  # Nanometers
    'um': 13,  # Microns
    'dm': 14,  # Decimeters
    'dam': 15,  # Decameters
    'hm': 16,  # Hectometers
    'gm': 17,  # Gigameters
    'au': 18,  # Astronomical units
    'ly': 19,  # Light years
    'pc': 20,  # Parsecs
    'usft': 22,  # US Survey Feet
    'usin': 23,  # US Survey Inch
    'usyd': 24,  # US Survey Yard
    'usmi': 25  # US Survey Mile
}

def arc_to_lines(scans: List[Dict[str, List[Tuple[float, ...]]]], num_segments: float = 0, segment_length: float = 0, units: str = 'um') -> List[Dict[str, List[Tuple[float, ...]]]]:
    # Will default to using min_length if both params are specified
    # Units passed will be treated as nanometers

    for arc in scans:
        values = scans.get(arc)
        center = values[0]
        radius = values[1][0]
        start_angle = values[1][1]
        end_angle = values[1][2]
        degree = end_angle - start_angle

        # Generated Lines
        lines: List[Dict[str, List[Tuple[float, ...]]]] = []

        # Points
        points: List[Tuple[float, ...]] = []

        # Create lines based on number of segments desired
        if num_segments > 2:
            segment_angle = degree/(num_segments)  # Calc segment angle based on num_segments

        # Create lines based on minimum line length
        elif segment_length > 0:
            # Calc segment angle based on min_length
            conversion_factor: float = CONVESION_FACTORS[UNIT_TABLE[units]]
            segment_angle = (segment_length*conversion_factor/(radius*2*math.pi))*360

            num_segments = int(degree/segment_angle)
        else:
            warning('Invalid/Corrupted DXF Structures')
            return None

        # For each point on the arc
        for i in range(0, num_segments+1):
            angle = start_angle + (segment_angle * i)  # Calc point's angle
            x = radius*math.cos(math.radians(angle))/conversion_factor  # Convert to cartesian
            y = radius*math.sin(math.radians(angle))/conversion_factor  # Convert to cartesian
            points.append([x+center[0], y+center[1], center[2]])  # Add point with center offset

        # Make each point into a line
        for i in range(0, num_segments):
            lines.append({'LINE'+str(i): [points[i], points[i+1]]})  # Convert points into lines
        
        # Connect ends
        if end_angle - start_angle == 360:
            lines.append({'LINE'+str(num_segments): [points[num_segments], points[0]]})

    return lines


def ellipse_to_arcs(scans: List[Dict[str, List[Tuple[float, ...]]]], num_segments: float = 0, segment_length: float = 0, units: str = 'um') -> List[Dict[str, List[Tuple[float, ...]]]]:
    
    #num segments denotes the number of arcs

    for ellipse in scans:
        values = scans.get(ellipse)
        center = values[0]
        major_radius = values[1][0] # a
        minor_radius = values[2] * major_radius # b

        # 0. CONVERT TO POLAR 
        # 0 = theta
        # r(0) = a*b / sqrt((b*cos(0))^2 + (a*sin(0))^2)

        # Points
        points: List[Tuple[float, ...]] = []

        # Calculate Points NumSegments
        angle = (360/num_segments)/2  # num points

        # # Calculate Points SegmentLength
        # # Circumfrance of Ellipse
        # # = 2*PI*sqrt((a^2 + b^2)/2)
        # circumfrance = 2*math.pi*math.sqrt((major_radius*major_radius + minor_radius*minor_radius)/2)
        # angle = (segment_length/circumfrance) * 360 # NOTE segment length has to be less than the circufrance
        
        # Calculate points
        conversion_factor: float = CONVESION_FACTORS[UNIT_TABLE[units]]
        theta = 0
        for i in range(0,2*num_segments):  # Need to generate 2x to account for midpoints
            theta = i*angle
            radius = major_radius*minor_radius / (
            math.sqrt(math.pow(minor_radius*math.cos(math.radians(theta)),2) + 
            math.pow((major_radius*math.sin(math.radians(theta))),2)))

            x:float = radius*math.cos(math.radians(theta)) # Convert to cartesian
            y:float = radius*math.sin(math.radians(theta)) # Convert to cartesian
            print('{0},{1},{2}'.format(round(x,10),round(y,10),round(theta,10)))  # DEBUGGING
            points.append([x+center[0], y+center[1], center[2]])  # Add point with center offset

        # Find arc that encompasses 2 points
        arcs: List[Dict[str, List[Tuple[float, ...]]]] = []
        for i in range(0,num_segments):
            # Debugging
            # v1 = 2*i
            # v2 = 2*i+1
            # v3 = ((2*i+2)%(len(points)))
            p1x = points[2*i][0]
            p1y = points[2*i][1]
            p2x = points[2*i+1][0]
            p2y = points[2*i+1][1]
            p3x = points[((2*i+2)%(len(points)))][0]
            p3y = points[((2*i+2)%(len(points)))][1]

            # Calculate
            # Center point
            cx = ((p1x*p1x + p1y*p1y - p2x*p2x - p2y*p2y) - (((2*p1y - 2*p2y)*(p1x*p1x + p1y*p1y -p3x*p3x - p3y*p3y))/(2*p1y -2*p3y)))/((2*p1x - 2*p2x) - ((2*p1y-2*p2y)*(2*p1x-2*p3x))/(2*p1y-2*p3y))

            try:
                cx = ((p1x*p1x + p1y*p1y - p2x*p2x - p2y*p2y) - (((2*p1y - 2*p2y)*(p1x*p1x + p1y*p1y -p3x*p3x - p3y*p3y))/(2*p1y -2*p3y)))/((2*p1x - 2*p2x) - ((2*p1y-2*p2y)*(2*p1x-2*p3x))/(2*p1y-2*p3y))
                cy = ((p1x*p1x + p1y*p1y - p3x*p3x - p3y*p3y)/(2*p1y - 2*p3y))-(cx*((2*p1x-2*p3x)/(2*p1y - 2*p3y)))
            except ZeroDivisionError as e:
                warning ('Divide by zero error')
            # Radius 
            r = math.sqrt(math.pow(p1x-cx,2) + math.pow(p1y-cy,2))

            # Angles # TODO THIS IS THE ISSUE HAS TO DO WITH INVERTING THE ANGLE * SINE/COSINE CURVE
            negation= (-1 if p2x < 0 or p2y < 0 else 1)
            start_angle = (180 if negation < 0 else 0)+-1*(math.degrees(math.atan((p1y+cy)/(p1x+cx))))  # When the start point intersects with the point of the next arc
            end_angle = (180 if negation < 0 else 0)+-1*(180+(math.degrees(math.atan((p3y+cy)/(p3x+cx)))))  # When the start point intersects with the point of the next arc
            arcs.append({'ARC'+str(i):(tuple([cx/conversion_factor,cy/conversion_factor,0]),tuple([r/conversion_factor,start_angle,end_angle]),tuple([0,0,1]))})
            print()

        # FIND ARC STEPS:
        # 0. CONVERT TO POLAR
        # 1. Given two points on the ellipse find the midpoint between them
        # 2. Find the tangent line of that midpoint using derivative
        # 3. Now you have 3 points that define a circle
        # 4. Using those 3 points u can solve for center x,y


    return arcs
    


def convert_to(given_geometry_type: str, return_geometry_type: str, given_geometry: List[Dict[str, List[Tuple[float, ...]]]], num_segments: float = 0, min_length: float = 0, units: str = 'um') -> List[Dict[str, List[Tuple[float, ...]]]]:
    '''[summary]

    Args:
        given_geometry_type (str): Geometry type of passed values
        return_geometry_type (str): Desired geometry type
        given_geometry (Dict[str, List[Tuple[float, ...]]]): Geometry to be converted values
        num_segments (float): Number of segments to divide given geometry into to produce the return geometry
        min_length (float): Minimum length of segments to divide given geometry into to produce return geometry

    Returns:
        List[Dict[str, List[Tuple[float, ...]]]]: Desired geometry type values
    '''
    if given_geometry_type == return_geometry_type:
        return given_geometry
    elif given_geometry_type == 'ARC':  # Arcs can only be directly converted into lines
        return convert_to('LINE', return_geometry_type, arc_to_lines(given_geometry, num_segments, min_length, units))
    elif given_geometry_type == 'ELLIPSE':  # Ellipses can only directly be down converted into arcs
        return convert_to('ARC', return_geometry_type, ellipse_to_arcs(given_geometry, num_segments, min_length, units))

    # MAYBE BE RECURSIVE AND ONLY RETURN ONCE THE GIVEN AND RETURN TYPES ARE THE SAME


# FUNCTIONS TO ADD
# def convert() -> converts one geometry into another
# def arc_to_lines
# def ellipse_to_arc
# def spline_to ?
# def lwpolyline_to ?
# def lines_to_points
