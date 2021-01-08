"""
Module for importing and exporting DXF files
"""

from typing import Dict, List, Tuple
import ezdxf

__author__ = 'Joseph Lawler'
__version__ = '1.0.0'


def import_dxf_file(filename: str) -> List[Dict [str, List[Tuple[float,...]]]]:
    """
    Importing a DXF file and returning a list of entities

    Args:
        filename (str): DXF filename

    Returns:
        List[Dict [str, List[tuple(float)]]]: A list of all geometry names in terms of str and a list of associated points in 2D/3D
        LINE: {'LINE': [START (X,Y,Z), END (X,Y,Z)]}
        CIRCLE: {'CIRCLE': [RADIUS (#), CENTER (X,Y,Z), PLANE (X,Y,Z)]}
        ARC:
    """

    # account for missing file extension
    if not filename.endswith(".dxf"):
        # add extension
        filename = filename + ".dxf"

    # import file
    try:
        dxf = ezdxf.readfile(filename)
    except IOError or ezdxf.DXFStructureError:
        #  catch errors
        # TODO make sure this is what he wants
        raise Exception

    # get all entities from dxf
    msp = dxf.modelspace()
    units = dxf.units
    entities = msp.entity_space

    # add entities to geometry
    geometry: List[Dict [str, List[Tuple[[float], ...]]]] = []
    for e in entities:

        # entity name
        name: str = e.DXFTYPE
        points: List[Tuple[[float], ...]] = [] 

        # determine entity and get information to store
        # TODO determine all entities and how to store for each entity
        # TODO convert to microns
        print(name)
        if name == 'CIRCLE':
            points.append(e.dxf.radius)
            points.append(e.dxf.center.xyz)
            points.append(e.dxf.extrusion.xyz)
        if name == 'LINE':
            points.append(e.dxf.start.xyz)
            points.append(e.dxf.end.xyz)
        if name == 'ARC':
            # TODO
            print("ARC")
        geometry.append({name: points})
    return geometry

# def export_dxf_file(filename: str, scans: List[Dict[str, List[Tuple(float,..)]], **args = {}) -> bool:
#     # returns True if successful

if __name__ == "__main__":
    points = import_dxf_file("3D Examples.dxf")
    print('END')