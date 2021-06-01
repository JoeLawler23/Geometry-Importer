
from typing import Dict, List, Tuple
import math

def arc_to_lines(scans: List[Dict[str, List[Tuple[float, ...]]]], num_segments: float = 0, min_length: float = 0, units: str = 'um') -> List[Dict[str, List[Tuple[float, ...]]]]:
    # Will default to using min_length if both params are specified
    # Units passed will be treated as nanometers

    # Get values
    values = list(scans[0].values())[0]
    center: float = values[0]
    radius: float
    degree: float
    start_angle: float

    if list(scans[0].keys())[0].startswith('CIRCLE'):
        radius = values[1]
        degree = 360.0
        start_angle = 0
    elif list(scans[0].keys())[0].startswith('ARC'):
        radius = values[1][0]
        degree = values[1][2] - values[1][1]
        start_angle = values[1][1]
    
    # Generated Lines
    lines: List[Dict[str, List[Tuple[float, ...]]]] = []
    
    # Points 
    points: List[Tuple[float, ...]] = []

    # Use number of segments by default if no param is passed
    if num_segments > 2 or min_length == 0:
        # Create lines based on number of segments desired
        # Generate number of angles based off of num segments desired

        # Calc segment angle based on num_segments
        segment_angle = degree/(num_segments)
    
    # TODO need to fix
    elif min_length > 0:
        # Calc segment angle based on min_length
        # conversion_factor: float = CONVESION_FACTORS[UNIT_TABLE[units]]
        segment_angle = (math.sin(((min_length*1)/2)/radius))/2

        num_segments = int(degree/segment_angle)

    # For each point on the circle
    for i in range(0,num_segments+1):
        angle = start_angle + (segment_angle * i) # Calc point's angle
        x = radius*math.cos(math.radians(angle)) # Convert to cartesian
        y = radius*math.sin(math.radians(angle)) # Convert to cartesian
        points.append([x+center[0],y+center[1],center[2]]) # Add center offset

    # Make each point into a line
    for i in range(0,num_segments):
        lines.append({'LINE'+str(i) : [points[i],points[i+1]]})

    return lines

def circle_to_lines(scans: List[Dict[str, List[Tuple[float, ...]]]], num_segments: float = 0, min_length: float = 0) -> List[Dict[str, List[Tuple[float, ...]]]]:
    return arc_to_lines(scans, num_segments, min_length)

# def ellipse_to_lines():

# def lwpolyline_to_lines():

# def spline_to_lines():

def circle_to_arc():
    print
