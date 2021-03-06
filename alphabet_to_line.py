from typing import Dict, List, Tuple
import importer
import os

__author__ = 'Joseph Lawler'
__version__ = '1.2.1'

# ALPHABET consisting of A-Z uppercase only and 0-9
ALPHABET: Dict[str, List[Tuple[float, ...]]] = {
    '0': [(8000.0,8500.0),(6500.0,10000.0),   
            (6500.0,10000.0),(3000.0,10000.0),
            (3000.0,10000.0),(1500.0,8500.0), 
            (1500.0,8500.0),(1500.0,1500.0),  
            (1500.0,1500.0),(3000.0,0.0),     
            (3000.0,0.0),(6500.0,0.0),        
            (6500.0,0.0),(8000.0,1500.0),     
            (8000.0,1500.0),(8000.0,8500.0),  
            (1500.0,1500.0),(8000.0,8500.0),],
    '1': [(5000.0,10000.0),(5000.0,0.0),
            (5000.0,10000.0),(3500.0,8500.0),
            (3000.0,0.0),(7000.0,0.0),],
    '2': [(2500.0,8500.0),(4000.0,10000.0),
            (6500.0,10000.0),(8000.0,8500.0),
            (8000.0,8500.0),(8000.0,6500.0),
            (8000.0,6500.0),(6500.0,5000.0),
            (4000.0,5000.0),(2500.0,3500.0),
            (2500.0,3500.0),(2500.0,0.0),
            (8000.0,0.0),(8000.0,1500.0),
            (2500.0,8500.0),(2500.0,7000.0),
            (6500.0,10000.0),(4000.0,10000.0),
            (6500.0,5000.0),(4000.0,5000.0),
            (8000.0,0.0),(2500.0,0.0),],
    '3': [(2500.0,7000.0),(2500.0,8500.0),
            (2500.0,8500.0),(4000.0,10000.0),
            (6500.0,10000.0),(8000.0,8500.0),
            (8000.0,8500.0),(8000.0,6500.0),
            (8000.0,6500.0),(6500.0,5000.0),
            (6500.0,5000.0),(8000.0,3500.0),
            (8000.0,3500.0),(8000.0,1500.0),
            (8000.0,1500.0),(6500.0,0.0),
            (4000.0,0.0),(2500.0,1500.0),
            (2500.0,1500.0),(2500.0,3000.0),
            (6500.0,5000.0),(4000.0,5000.0),
            (4000.0,10000.0),(6500.0,10000.0),
            (6500.0,0.0),(4000.0,0.0),],
    '4': [(6500.0,10000.0),(6500.0,0.0),
            (2500.0,10000.0),(2500.0,5000.0),
            (2500.0,5000.0),(6500.0,5000.0),],
    '5': [(8000.0,10000.0),(2500.0,10000.0),
            (2500.0,10000.0),(2500.0,5000.0),
            (2500.0,5000.0),(6500.0,5000.0),
            (6500.0,5000.0),(8000.0,3500.0),
            (8000.0,3500.0),(8000.0,1500.0),
            (8000.0,1500.0),(6500.0,0.0),
            (6500.0,0.0),(4000.0,0.0),
            (4000.0,0.0),(2500.0,1500.0),
            (2500.0,1500.0),(2500.0,3000.0),],
    '6': [(-8000.0,-7000.0),(-8000.0,-8500.0),
            (-8000.0,-8500.0),(-6500.0,-10000.0),
            (-6500.0,-10000.0),(-4000.0,-10000.0),
            (-4000.0,-10000.0),(-2500.0,-8500.0),
            (-2500.0,-8500.0),(-2500.0,-1500.0),
            (-2500.0,-1500.0),(-4000.0,0.0),
            (-4000.0,0.0),(-6500.0,0.0),
            (-6500.0,0.0),(-8000.0,-1500.0),
            (-8000.0,-1500.0),(-8000.0,-3500.0),
            (-8000.0,-3500.0),(-6500.0,-5000.0),
            (-6500.0,-5000.0),(-2500.0,-5000.0),],
    '7': [(2500.0,10000.0),(7500.0,10000.0),
            (7500.0,10000.0),(5000.0,0.0),],
    '8': [(6500.0,5000.0),(8000.0,6500.0),
            (8000.0,6500.0),(8000.0,8500.0),
            (8000.0,8500.0),(6500.0,10000.0),
            (6500.0,10000.0),(4000.0,10000.0),
            (4000.0,10000.0),(2500.0,8500.0),
            (2500.0,8500.0),(2500.0,6500.0),
            (2500.0,6500.0),(4000.0,5000.0),
            (4000.0,5000.0),(6500.0,5000.0),
            (6500.0,5000.0),(8000.0,3500.0),
            (8000.0,3500.0),(8000.0,1500.0),
            (8000.0,1500.0),(6500.0,0.0),
            (6500.0,0.0),(4000.0,0.0),
            (4000.0,0.0),(2500.0,1500.0),
            (2500.0,1500.0),(2500.0,3500.0),
            (2500.0,3500.0),(4000.0,5000.0),],
    '9': [(2500.0,3000.0),(2500.0,1500.0),
            (2500.0,1500.0),(4000.0,0.0),
            (4000.0,0.0),(6500.0,0.0),
            (6500.0,0.0),(8000.0,1500.0),
            (8000.0,1500.0),(8000.0,8500.0),
            (8000.0,8500.0),(6500.0,10000.0),
            (6500.0,10000.0),(4000.0,10000.0),
            (4000.0,10000.0),(2500.0,8500.0),
            (2500.0,8500.0),(2500.0,6500.0),
            (2500.0,6500.0),(4000.0,5000.0),
            (4000.0,5000.0),(8000.0,5000.0),],
    'A': [(5000.0,10000.0),(2320.508,0.0),
            (5000.0,10000.0),(7679.492,0.0),
            (3660.254,5000.0),(6339.746,5000.0),],
    'B': [(7500.0,4000.0),(6500.0,5000.0),
            (6500.0,5000.0),(7500.0,6000.0),
            (7500.0,6000.0),(7500.0,9000.0),
            (7500.0,9000.0),(6500.0,10000.0),
            (6500.0,10000.0),(2500.0,10000.0),
            (2500.0,10000.0),(2500.0,0.0),
            (2500.0,0.0),(6500.0,0.0),
            (6500.0,0.0),(7500.0,1000.0),
            (7500.0,1000.0),(7500.0,4000.0),
            (2500.0,5000.0),(6500.0,5000.0),],
    'C': [(1500.0,8500.0),(3000.0,10000.0),
            (3000.0,10000.0),(6500.0,10000.0),
            (6500.0,10000.0),(8000.0,8500.0),
            (8000.0,8500.0),(8000.0,7000.0),
            (1500.0,8500.0),(1500.0,1500.0),
            (1500.0,1500.0),(3000.0,0.0),
            (3000.0,0.0),(6500.0,0.0),
            (6500.0,0.0),(8000.0,1500.0),
            (8000.0,1500.0),(8000.0,3000.0),],
    'D': [(7500.0,1500.0),(6000.0,0.0),
            (6000.0,0.0),(2500.0,0.0),
            (2500.0,0.0),(2500.0,10000.0),
            (2500.0,10000.0),(6000.0,10000.0),
            (6000.0,10000.0),(7500.0,8500.0),
            (7500.0,8500.0),(7500.0,1500.0),],
    'E': [(7500.0,10000.0),(2500.0,10000.0),
            (2500.0,10000.0),(2500.0,0.0),
            (2500.0,0.0),(7500.0,0.0),
            (2500.0,5000.0),(6000.0,5000.0),],
    'F': [(2500.0,10000.0),(2500.0,0.0),
            (2500.0,5000.0),(6000.0,5000.0),
            (2500.0,10000.0),(7500.0,10000.0),],
    'G': [(8000.0,7000.0),(8000.0,8500.0),
            (8000.0,8500.0),(6500.0,10000.0),
            (6500.0,10000.0),(3000.0,10000.0),
            (3000.0,10000.0),(1500.0,8500.0),
            (1500.0,8500.0),(1500.0,1500.0),
            (1500.0,1500.0),(3000.0,-0.0),
            (3000.0,-0.0),(6500.0,-0.0),
            (6500.0,-0.0),(8000.0,1500.0),
            (8000.0,1500.0),(8000.0,4000.0),
            (8000.0,4000.0),(5000.0,4000.0),],
    'H': [(2500.0,5000.0),(7500.0,5000.0),
            (2500.0,10000.0),(2500.0,0.0),
            (7500.0,10000.0),(7500.0,0.0),],
    'I': [(-5000.0,0.0),(-5000.0,-10000.0),
            (-2500.0,-10000.0),(-7500.0,-10000.0),
            (-2500.0,0.0),(-7500.0,0.0),],
    'J': [(7500.0,10000.0),(7500.0,1500.0),
            (7500.0,1500.0),(6000.0,0.0),
            (6000.0,0.0),(3500.0,0.0),
            (3500.0,0.0),(2000.0,1500.0),
            (2000.0,1500.0),(2000.0,3000.0),],
    'K': [(2500.0,0.0),(2500.0,10000.0),
            (2500.0,5000.0),(6500.0,10000.0),
            (2500.0,5000.0),(6500.0,0.0),],
    'L': [(-2500.0,-10000.0),(-2500.0,0.0),
            (-2500.0,0.0),(-6500.0,0.0),],
    'M': [(1500.0,0.0),(1500.0,10000.0),
            (8500.0,10000.0),(8500.0,0.0),
            (1500.0,10000.0),(5000.0,2500.0),
            (5000.0,2500.0),(8500.0,10000.0),],
    'N': [(2500.0,0.0),(2500.0,10000.0),
            (2500.0,10000.0),(7500.0,0.0),
            (7500.0,0.0),(7500.0,10000.0),],
    'O': [(8000.0,1500.0),(8000.0,8500.0),
            (8000.0,8500.0),(6500.0,10000.0),
            (6500.0,10000.0),(3000.0,10000.0),
            (3000.0,10000.0),(1500.0,8500.0),
            (1500.0,8500.0),(1500.0,1500.0),
            (1500.0,1500.0),(3000.0,0.0),
            (3000.0,0.0),(6500.0,0.0),
            (6500.0,0.0),(8000.0,1500.0),],
    'P': [(2500.0,0.0),(2500.0,10000.0),
            (2500.0,10000.0),(6000.0,10000.0),
            (6000.0,10000.0),(7500.0,8500.0),
            (7500.0,8500.0),(7500.0,6500.0),
            (7500.0,6500.0),(6000.0,5000.0),
            (6000.0,5000.0),(2500.0,5000.0),],
    'Q': [(3000.0,10000.0),(1500.0,8500.0),
            (1500.0,8500.0),(1500.0,1500.0),
            (1500.0,1500.0),(3000.0,0.0),
            (3000.0,0.0),(6500.0,0.0),
            (6500.0,0.0),(8000.0,1500.0),
            (8000.0,1500.0),(8000.0,8500.0),
            (8000.0,8500.0),(6500.0,10000.0),
            (6500.0,10000.0),(3000.0,10000.0),
            (8000.0,0.0),(6000.0,2000.0),],
    'R': [(2500.0,0.0),(2500.0,10000.0),
            (2500.0,10000.0),(6000.0,10000.0),
            (6000.0,10000.0),(7500.0,8500.0),
            (7500.0,8500.0),(7500.0,6500.0),
            (7500.0,6500.0),(6000.0,5000.0),
            (6000.0,5000.0),(2500.0,5000.0),
            (6000.0,5000.0),(7500.0,3500.0),
            (7500.0,3500.0),(7500.0,0.0),],
    'S': [(8000.0,7000.0),(8000.0,8500.0),
            (8000.0,8500.0),(6500.0,10000.0),
            (6500.0,10000.0),(3000.0,10000.0),
            (3000.0,10000.0),(1500.0,8500.0),
            (1500.0,8500.0),(1500.0,6500.0),
            (1500.0,6500.0),(3000.0,5000.0),
            (3000.0,5000.0),(6500.0,5000.0),
            (6500.0,5000.0),(8000.0,3500.0),
            (8000.0,3500.0),(8000.0,1500.0),
            (8000.0,1500.0),(6500.0,0.0),
            (6500.0,0.0),(3000.0,0.0),
            (3000.0,0.0),(1500.0,1500.0),
            (1500.0,1500.0),(1500.0,3000.0),],
    'T': [(5000.0,0.0),(5000.0,10000.0),
            (5000.0,10000.0),(7500.0,10000.0),
            (2500.0,10000.0),(5000.0,10000.0),],
    'U': [(-1500.0,-10000.0),(-1500.0,-1500.0),
            (-1500.0,-1500.0),(-3000.0,0.0),
            (-3000.0,0.0),(-6500.0,0.0),
            (-6500.0,0.0),(-8000.0,-1500.0),
            (-8000.0,-1500.0),(-8000.0,-10000.0),],
    'V': [(-5000.0,0.0),(-2500.0,-10000.0),
            (-5000.0,0.0),(-7500.0,-10000.0),],
    'W': [(0.0,10000.0),(2500.0,0.0),
            (2500.0,0.0),(5000.0,7500.0),
            (5000.0,7500.0),(7500.0,0.0),
            (7500.0,0.0),(10000.0,10000.0),],
    'X': [(2500.0,10000.0),(7500.0,0.0),
            (7500.0,10000.0),(2500.0,0.0),],
    'Y': [(-2500.0,-10000.0),(-5000.0,-5000.0),
            (-5000.0,-5000.0),(-7500.0,-10000.0),
            (-5000.0,-5000.0),(-5000.0,0.0),],
    'Z': [(2500.0,10000.0),(7500.0,10000.0),
            (7500.0,10000.0),(2500.0,0.0),
            (2500.0,0.0),(7500.0,0.0),],
}

# Define type for containing geometry elements
TGeometryItem = Tuple[str, List[Tuple[float, ...]]]
TGeometryList = List[TGeometryItem]

def create_letter_from_dxf(letter: str, scans: TGeometryList):
    '''
    Summary:
      Generate a list of lines from a DXF file representing a letter

    Args:
      letter (str): filename
      scans (TGeometryList): letter geometries from importing the dxf file
    '''

    # Letter header
    output: str = "'"+letter+"'"+': ['

    # Cycle through all geometries for the given letter
    for geometry_index, geometry in enumerate(scans):

        # Geometry's values
        values: List[Tuple[float, ...]] = geometry[1]

        # Start point
        output += '({x},{y}),'.format(x = round(values[0][0],3), y = round(values[0][1],3))

        # End point
        output += '({x},{y}),\n\t'.format(x = round(values[1][0],3), y = round(values[1][1],3))
            
    #end for

    # Replace last comma with bracket and add new line
    if geometry_index == len(scans)-1:
        output = output[:len(output)-2] + '],'

    # Print output
    print(output) 
#end def

def create_alphabet(path: str):
    '''
    Summary:
        Print out a list of all dxf files, letters only drawn from lines, in the Letters folder
    Args:
        path (str): Path to Letters folder
    '''

    # Gather a list of all letters in the passed path
    # NOTE current path location src/autolazeql/fileio/Letters
    list = os.listdir(path)

    # Add starting bracket
    print('{')

    # Run create letter for each letter
    for name in list:

        # Generate individual letter path
        # NOTE down converts everything to lines
        letter_geometries = importer.import_dxf_file(path+'/'+name,['LINE'],True)

        # Remove file extension
        letter = name.rstrip('.dxf')

        # Run create letter
        create_letter_from_dxf(letter, letter_geometries)

    #end for

    # Add closing bracket
    print('}')
#end def

# Used to create ALPHABET
if __name__ == "__main__":
     create_alphabet('/Letters')