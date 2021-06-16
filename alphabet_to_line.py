from typing import Dict, List, Tuple
import importer
import os

__author__ = 'Joseph Lawler'
__version__ = '1.2.0'

# LETTERS_NUMBERS
LETTERS_NUMBERS: Dict[str, List[Dict[str, List[Tuple[float, ...]]]]] = {
    '0': [{'LINE0': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE1': ((0.65, 1.0, 0.0), (0.3, 1.0, 0.0))},
          {'LINE2': ((0.3, 1.0, 0.0), (0.15, 0.85, 0.0))},
          {'LINE3': ((0.15, 0.85, 0.0), (0.15, 0.15, 0.0))},
          {'LINE4': ((0.15, 0.15, 0.0), (0.3, 0.0, 0.0))},
          {'LINE5': ((0.3, 0.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE6': ((0.65, 0.0, 0.0), (0.8, 0.15, 0.0))},
          {'LINE7': ((0.8, 0.15, 0.0), (0.8, 0.85, 0.0))},
          {'LINE8': ((0.15, 0.15, 0.0), (0.8, 0.85, 0.0))}],

    '1': [{'LINE0': ((0.5, 1.0, 0.0), (0.5, 0.0, 0.0))},
          {'LINE1': ((0.5, 1.0, 0.0), (0.35, 0.85, 0.0))},
          {'LINE2': ((0.3, 0.0, 0.0), (0.7, 0.0, 0.0))}],

    '2': [{'LINE0': ((0.25, 0.85, 0.0), (0.4, 1.0, 0.0))},
          {'LINE1': ((0.65, 1.0, 0.0), (0.8, 0.85, 0.0))},
          {'LINE2': ((0.8, 0.85, 0.0), (0.8, 0.65, 0.0))},
          {'LINE3': ((0.8, 0.65, 0.0), (0.65, 0.5, 0.0))},
          {'LINE4': ((0.4, 0.5, 0.0), (0.25, 0.35, 0.0))},
          {'LINE5': ((0.25, 0.35, 0.0), (0.25, 0.0, 0.0))},
          {'LINE6': ((0.8, 0.0, 0.0), (0.8, 0.15, 0.0))},
          {'LINE7': ((0.25, 0.85, 0.0), (0.25, 0.7, 0.0))},
          {'LINE8': ((0.65, 1.0, 0.0), (0.4, 1.0, 0.0))},
          {'LINE9': ((0.65, 0.5, 0.0), (0.4, 0.5, 0.0))},
          {'LINE10': ((0.8, 0.0, 0.0), (0.25, 0.0, 0.0))}],

    '3': [{'LINE0': ((0.25, 0.7, 0.0), (0.25, 0.85, 0.0))},
          {'LINE1': ((0.25, 0.85, 0.0), (0.4, 1.0, 0.0))},
          {'LINE2': ((0.65, 1.0, 0.0), (0.8, 0.85, 0.0))},
          {'LINE3': ((0.8, 0.85, 0.0), (0.8, 0.65, 0.0))},
          {'LINE4': ((0.8, 0.65, 0.0), (0.65, 0.5, 0.0))},
          {'LINE5': ((0.65, 0.5, 0.0), (0.8, 0.35, 0.0))},
          {'LINE6': ((0.8, 0.35, 0.0), (0.8, 0.15, 0.0))},
          {'LINE7': ((0.8, 0.15, 0.0), (0.65, 0.0, 0.0))},
          {'LINE8': ((0.4, 0.0, 0.0), (0.25, 0.15, 0.0))},
          {'LINE9': ((0.25, 0.15, 0.0), (0.25, 0.3, 0.0))},
          {'LINE10': ((0.65, 0.5, 0.0), (0.4, 0.5, 0.0))},
          {'LINE11': ((0.4, 1.0, 0.0), (0.65, 1.0, 0.0))},
          {'LINE12': ((0.65, 0.0, 0.0), (0.4, 0.0, 0.0))}],

    '4': [{'LINE0': ((0.65, 1.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.25, 0.5, 0.0))},
          {'LINE2': ((0.25, 0.5, 0.0), (0.65, 0.5, 0.0))}],

    '5': [{'LINE0': ((0.8, 1.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.25, 0.5, 0.0))},
          {'LINE2': ((0.25, 0.5, 0.0), (0.65, 0.5, 0.0))},
          {'LINE3': ((0.65, 0.5, 0.0), (0.8, 0.35, 0.0))},
          {'LINE4': ((0.8, 0.35, 0.0), (0.8, 0.15, 0.0))},
          {'LINE5': ((0.8, 0.15, 0.0), (0.65, 0.0, 0.0))},
          {'LINE6': ((0.65, 0.0, 0.0), (0.4, 0.0, 0.0))},
          {'LINE7': ((0.4, 0.0, 0.0), (0.25, 0.15, 0.0))},
          {'LINE8': ((0.25, 0.15, 0.0), (0.25, 0.3, 0.0))}],

    '6': [{'LINE0': ((-0.8, -0.7, 0.0), (-0.8, -0.85, 0.0))},
          {'LINE1': ((-0.8, -0.85, 0.0), (-0.65, -1.0, 0.0))},
          {'LINE2': ((-0.65, -1.0, 0.0), (-0.4, -1.0, 0.0))},
          {'LINE3': ((-0.4, -1.0, 0.0), (-0.25, -0.85, 0.0))},
          {'LINE4': ((-0.25, -0.85, 0.0), (-0.25, -0.15, 0.0))},
          {'LINE5': ((-0.25, -0.15, 0.0), (-0.4, 0.0, 0.0))},
          {'LINE6': ((-0.4, 0.0, 0.0), (-0.65, 0.0, 0.0))},
          {'LINE7': ((-0.65, 0.0, 0.0), (-0.8, -0.15, 0.0))},
          {'LINE8': ((-0.8, -0.15, 0.0), (-0.8, -0.35, 0.0))},
          {'LINE9': ((-0.8, -0.35, 0.0), (-0.65, -0.5, 0.0))},
          {'LINE10': ((-0.65, -0.5, 0.0), (-0.25, -0.5, 0.0))}],

    '7': [{'LINE0': ((0.25, 1.0, 0.0), (0.75, 1.0, 0.0))},
          {'LINE1': ((0.75, 1.0, 0.0), (0.5, 0.0, 0.0))}],

    '8': [{'LINE0': ((0.65, 0.5, 0.0), (0.8, 0.65, 0.0))},
          {'LINE1': ((0.8, 0.65, 0.0), (0.8, 0.85, 0.0))},
          {'LINE2': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE3': ((0.65, 1.0, 0.0), (0.4, 1.0, 0.0))},
          {'LINE4': ((0.4, 1.0, 0.0), (0.25, 0.85, 0.0))},
          {'LINE5': ((0.25, 0.85, 0.0), (0.25, 0.65, 0.0))},
          {'LINE6': ((0.25, 0.65, 0.0), (0.4, 0.5, 0.0))},
          {'LINE7': ((0.4, 0.5, 0.0), (0.65, 0.5, 0.0))},
          {'LINE8': ((0.65, 0.5, 0.0), (0.8, 0.35, 0.0))},
          {'LINE9': ((0.8, 0.35, 0.0), (0.8, 0.15, 0.0))},
          {'LINE10': ((0.8, 0.15, 0.0), (0.65, 0.0, 0.0))},
          {'LINE11': ((0.65, 0.0, 0.0), (0.4, 0.0, 0.0))},
          {'LINE12': ((0.4, 0.0, 0.0), (0.25, 0.15, 0.0))},
          {'LINE13': ((0.25, 0.15, 0.0), (0.25, 0.35, 0.0))},
          {'LINE14': ((0.25, 0.35, 0.0), (0.4, 0.5, 0.0))}],

    '9': [{'LINE0': ((0.25, 0.3, 0.0), (0.25, 0.15, 0.0))},
          {'LINE1': ((0.25, 0.15, 0.0), (0.4, 0.0, 0.0))},
          {'LINE2': ((0.4, 0.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE3': ((0.65, 0.0, 0.0), (0.8, 0.15, 0.0))},
          {'LINE4': ((0.8, 0.15, 0.0), (0.8, 0.85, 0.0))},
          {'LINE5': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE6': ((0.65, 1.0, 0.0), (0.4, 1.0, 0.0))},
          {'LINE7': ((0.4, 1.0, 0.0), (0.25, 0.85, 0.0))},
          {'LINE8': ((0.25, 0.85, 0.0), (0.25, 0.65, 0.0))},
          {'LINE9': ((0.25, 0.65, 0.0), (0.4, 0.5, 0.0))},
          {'LINE10': ((0.4, 0.5, 0.0), (0.8, 0.5, 0.0))}],

    'A': [{'LINE0': ((0.5, 1.0, 0.0), (0.2321, 0.0, 0.0))},
          {'LINE1': ((0.5, 1.0, 0.0), (0.7679, 0.0, 0.0))},
          {'LINE2': ((0.366, 0.5, 0.0), (0.634, 0.5, 0.0))}],

    'B': [{'LINE0': ((0.25, 0.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.65, 1.0, 0.0))},
          {'LINE2': ((0.65, 1.0, 0.0), (0.75, 0.9, 0.0))},
          {'LINE3': ((0.75, 0.9, 0.0), (0.75, 0.6, 0.0))},
          {'LINE4': ((0.75, 0.6, 0.0), (0.65, 0.5, 0.0))},
          {'LINE5': ((0.65, 0.5, 0.0), (0.75, 0.4, 0.0))},
          {'LINE6': ((0.75, 0.4, 0.0), (0.75, 0.1, 0.0))},
          {'LINE7': ((0.75, 0.1, 0.0), (0.65, 0.0, 0.0))},
          {'LINE8': ((0.25, 0.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE9': ((0.65, 0.5, 0.0), (0.25, 0.5, 0.0))}],

    'C': [{'LINE0': ((0.15, 0.85, 0.0), (0.3, 1.0, 0.0))},
          {'LINE1': ((0.3, 1.0, 0.0), (0.65, 1.0, 0.0))},
          {'LINE2': ((0.65, 1.0, 0.0), (0.8, 0.85, 0.0))},
          {'LINE3': ((0.8, 0.85, 0.0), (0.8, 0.7, 0.0))},
          {'LINE4': ((0.15, 0.85, 0.0), (0.15, 0.15, 0.0))},
          {'LINE5': ((0.15, 0.15, 0.0), (0.3, 0.0, 0.0))},
          {'LINE6': ((0.3, 0.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE7': ((0.65, 0.0, 0.0), (0.8, 0.15, 0.0))},
          {'LINE8': ((0.8, 0.15, 0.0), (0.8, 0.3, 0.0))}],

    'D': [{'LINE0': ((0.75, 0.15, 0.0), (0.6, 0.0, 0.0))},
          {'LINE1': ((0.6, 0.0, 0.0), (0.25, 0.0, 0.0))},
          {'LINE2': ((0.25, 0.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE3': ((0.25, 1.0, 0.0), (0.6, 1.0, 0.0))},
          {'LINE4': ((0.6, 1.0, 0.0), (0.75, 0.85, 0.0))},
          {'LINE5': ((0.75, 0.15, 0.0), (0.75, 0.85, 0.0))}],

    'E': [{'LINE0': ((0.75, 1.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.25, 0.0, 0.0))},
          {'LINE2': ((0.25, 0.0, 0.0), (0.75, 0.0, 0.0))},
          {'LINE3': ((0.25, 0.5, 0.0), (0.6, 0.5, 0.0))}],

    'F': [{'LINE0': ((0.25, 1.0, 0.0), (0.25, 0.0, 0.0))},
          {'LINE1': ((0.25, 0.5, 0.0), (0.6, 0.5, 0.0))},
          {'LINE2': ((0.25, 1.0, 0.0), (0.75, 1.0, 0.0))}],

    'G': [{'LINE0': ((0.8, 0.7, 0.0), (0.8, 0.85, 0.0))},
          {'LINE1': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE2': ((0.65, 1.0, 0.0), (0.3, 1.0, 0.0))},
          {'LINE3': ((0.3, 1.0, 0.0), (0.15, 0.85, 0.0))},
          {'LINE4': ((0.15, 0.85, 0.0), (0.15, 0.15, 0.0))},
          {'LINE5': ((0.15, 0.15, 0.0), (0.3, -0.0, 0.0))},
          {'LINE6': ((0.3, -0.0, 0.0), (0.65, -0.0, 0.0))},
          {'LINE7': ((0.65, -0.0, 0.0), (0.8, 0.15, 0.0))},
          {'LINE8': ((0.8, 0.15, 0.0), (0.8, 0.4, 0.0))},
          {'LINE9': ((0.8, 0.4, 0.0), (0.5, 0.4, 0.0))}],

    'H': [{'LINE0': ((0.25, 0.5, 0.0), (0.75, 0.5, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.25, 0.0, 0.0))},
          {'LINE2': ((0.75, 1.0, 0.0), (0.75, 0.0, 0.0))}],

    'I': [{'LINE0': ((-0.5, 0.0, 0.0), (-0.5, -1.0, 0.0))},
          {'LINE1': ((-0.25, -1.0, 0.0), (-0.75, -1.0, 0.0))},
          {'LINE2': ((-0.25, 0.0, 0.0), (-0.75, 0.0, 0.0))}],

    'J': [{'LINE0': ((0.75, 1.0, 0.0), (0.75, 0.15, 0.0))},
          {'LINE1': ((0.75, 0.15, 0.0), (0.6, 0.0, 0.0))},
          {'LINE2': ((0.6, 0.0, 0.0), (0.35, 0.0, 0.0))},
          {'LINE3': ((0.35, 0.0, 0.0), (0.2, 0.15, 0.0))},
          {'LINE4': ((0.2, 0.15, 0.0), (0.2, 0.3, 0.0))}],

    'K': [{'LINE0': ((0.25, 0.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 0.5, 0.0), (0.65, 1.0, 0.0))},
          {'LINE2': ((0.25, 0.5, 0.0), (0.65, 0.0, 0.0))}],

    'L': [{'LINE0': ((-0.25, -1.0, 0.0), (-0.25, 0.0, 0.0))},
          {'LINE1': ((-0.25, 0.0, 0.0), (-0.65, 0.0, 0.0))}],

    'M': [{'LINE0': ((0.15, 0.0, 0.0), (0.15, 1.0, 0.0))},
          {'LINE1': ((0.85, 1.0, 0.0), (0.85, 0.0, 0.0))},
          {'LINE2': ((0.15, 1.0, 0.0), (0.5, 0.25, 0.0))},
          {'LINE3': ((0.5, 0.25, 0.0), (0.85, 1.0, 0.0))}],

    'N': [{'LINE0': ((0.25, 0.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.75, 0.0, 0.0))},
          {'LINE2': ((0.75, 0.0, 0.0), (0.75, 1.0, 0.0))}],

    'O': [{'LINE0': ((0.8, 0.15, 0.0), (0.8, 0.85, 0.0))},
          {'LINE1': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE2': ((0.65, 1.0, 0.0), (0.3, 1.0, 0.0))},
          {'LINE3': ((0.3, 1.0, 0.0), (0.15, 0.85, 0.0))},
          {'LINE4': ((0.15, 0.85, 0.0), (0.15, 0.15, 0.0))},
          {'LINE5': ((0.15, 0.15, 0.0), (0.3, 0.0, 0.0))},
          {'LINE6': ((0.3, 0.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE7': ((0.8, 0.15, 0.0), (0.65, 0.0, 0.0))}],

    'P': [{'LINE0': ((0.25, 0.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.6, 1.0, 0.0))},
          {'LINE2': ((0.6, 1.0, 0.0), (0.75, 0.85, 0.0))},
          {'LINE3': ((0.75, 0.85, 0.0), (0.75, 0.65, 0.0))},
          {'LINE4': ((0.75, 0.65, 0.0), (0.6, 0.5, 0.0))},
          {'LINE5': ((0.6, 0.5, 0.0), (0.25, 0.5, 0.0))}],

    'Q': [{'LINE0': ((0.3, 1.0, 0.0), (0.15, 0.85, 0.0))},
          {'LINE1': ((0.15, 0.85, 0.0), (0.15, 0.15, 0.0))},
          {'LINE2': ((0.15, 0.15, 0.0), (0.3, 0.0, 0.0))},
          {'LINE3': ((0.3, 0.0, 0.0), (0.65, 0.0, 0.0))},
          {'LINE4': ((0.65, 0.0, 0.0), (0.8, 0.15, 0.0))},
          {'LINE5': ((0.8, 0.15, 0.0), (0.8, 0.85, 0.0))},
          {'LINE6': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE7': ((0.3, 1.0, 0.0), (0.65, 1.0, 0.0))},
          {'LINE8': ((0.8, 0.0, 0.0), (0.6, 0.2, 0.0))}],

    'R': [{'LINE0': ((0.25, 0.0, 0.0), (0.25, 1.0, 0.0))},
          {'LINE1': ((0.25, 1.0, 0.0), (0.6, 1.0, 0.0))},
          {'LINE2': ((0.6, 1.0, 0.0), (0.75, 0.85, 0.0))},
          {'LINE3': ((0.75, 0.85, 0.0), (0.75, 0.65, 0.0))},
          {'LINE4': ((0.75, 0.65, 0.0), (0.6, 0.5, 0.0))},
          {'LINE5': ((0.6, 0.5, 0.0), (0.25, 0.5, 0.0))},
          {'LINE6': ((0.6, 0.5, 0.0), (0.75, 0.35, 0.0))},
          {'LINE7': ((0.75, 0.35, 0.0), (0.75, 0.0, 0.0))}],

    'S': [{'LINE0': ((0.8, 0.7, 0.0), (0.8, 0.85, 0.0))},
          {'LINE1': ((0.8, 0.85, 0.0), (0.65, 1.0, 0.0))},
          {'LINE2': ((0.65, 1.0, 0.0), (0.3, 1.0, 0.0))},
          {'LINE3': ((0.3, 1.0, 0.0), (0.15, 0.85, 0.0))},
          {'LINE4': ((0.15, 0.85, 0.0), (0.15, 0.65, 0.0))},
          {'LINE5': ((0.15, 0.65, 0.0), (0.3, 0.5, 0.0))},
          {'LINE6': ((0.3, 0.5, 0.0), (0.65, 0.5, 0.0))},
          {'LINE7': ((0.65, 0.5, 0.0), (0.8, 0.35, 0.0))},
          {'LINE8': ((0.8, 0.35, 0.0), (0.8, 0.15, 0.0))},
          {'LINE9': ((0.8, 0.15, 0.0), (0.65, 0.0, 0.0))},
          {'LINE10': ((0.65, 0.0, 0.0), (0.3, 0.0, 0.0))},
          {'LINE11': ((0.3, 0.0, 0.0), (0.15, 0.15, 0.0))},
          {'LINE12': ((0.15, 0.15, 0.0), (0.15, 0.3, 0.0))}],

    'T': [{'LINE0': ((0.5, 0.0, 0.0), (0.5, 1.0, 0.0))},
          {'LINE1': ((0.5, 1.0, 0.0), (0.75, 1.0, 0.0))},
          {'LINE2': ((0.25, 1.0, 0.0), (0.5, 1.0, 0.0))}],

    'U': [{'LINE0': ((-0.15, -1.0, 0.0), (-0.15, -0.15, 0.0))},
          {'LINE1': ((-0.15, -0.15, 0.0), (-0.3, 0.0, 0.0))},
          {'LINE2': ((-0.3, 0.0, 0.0), (-0.65, 0.0, 0.0))},
          {'LINE3': ((-0.65, 0.0, 0.0), (-0.8, -0.15, 0.0))},
          {'LINE4': ((-0.8, -0.15, 0.0), (-0.8, -1.0, 0.0))}],

    'V': [{'LINE0': ((-0.5, 0.0, 0.0), (-0.25, -1.0, 0.0))},
          {'LINE1': ((-0.5, 0.0, 0.0), (-0.75, -1.0, 0.0))}],

    'W': [{'LINE0': ((0.0, 1.0, 0.0), (0.25, 0.0, 0.0))},
          {'LINE1': ((0.25, 0.0, 0.0), (0.5, 0.75, 0.0))},
          {'LINE2': ((0.5, 0.75, 0.0), (0.75, 0.0, 0.0))},
          {'LINE3': ((0.75, 0.0, 0.0), (1.0, 1.0, 0.0))}],

    'X': [{'LINE0': ((0.25, 1.0, 0.0), (0.75, 0.0, 0.0))},
          {'LINE1': ((0.75, 1.0, 0.0), (0.25, 0.0, 0.0))}],

    'Y': [{'LINE0': ((-0.25, -1.0, 0.0), (-0.5, -0.5, 0.0))},
          {'LINE1': ((-0.5, -0.5, 0.0), (-0.75, -1.0, 0.0))},
          {'LINE2': ((-0.5, -0.5, 0.0), (-0.5, 0.0, 0.0))}],

    'Z': [{'LINE0': ((0.25, 1.0, 0.0), (0.75, 1.0, 0.0))},
          {'LINE1': ((0.75, 1.0, 0.0), (0.25, 0.0, 0.0))},
          {'LINE2': ((0.25, 0.0, 0.0), (0.75, 0.0, 0.0))}],

}

def create_letter_from_dxf(letter: str, scans: List[Dict[str, List[Tuple[float, ...]]]]):
    '''
    Summary:
      Generate a list of lines from a DXF file representing a letter made only from lines

      Accepted Geometries: * All other geometries are ignored *
      - Point
      - Line
      - LWPolyline

    Args:
      letter (str): filename
      scans (List[Dict[str, List[Tuple[float, ...]]]]): letter geometries from importing the dxf file
    '''

    output: str = "'"+letter+"'"+': ['
    geometry_index = 0

    for entry_index, entry in enumerate(scans):
        for entity in entry:
            name: str = entity  # Name of the geometry including number
            # Truncate name to just include the geometry
            geometry_name: str = ''.join([i for i in name if not i.isdigit()])
            points: List[Tuple[float, ...]] = entry.get(
                name)  # List to store geometry

            if geometry_name == 'LINE':  # Line output
                output += "\t{'%s%d': (" % (geometry_name, geometry_index)
                output += str(tuple(float(format(round(x/10000, 4), '.4f'))
                              for x in points[0])) + ', '
                output += str(tuple(float(format(round(x/10000, 4), '.4f'))
                              for x in points[1]))+')}'+',\n'
                geometry_index += 1
            elif geometry_name == 'POINT':  # Point output
                output += "\t{'%s%d': (" % (geometry_name, geometry_index)
                output += str(tuple(float(format(round(x/10000, 4), '.4f'))
                              for x in points[0]))
                output += ',\n'
                geometry_index += 1
            elif geometry_name == 'LWPOLYLINE':  # Polyline output
                for point_index in range(len(points)-2):
                    output += "\t{'%s%d': (" % ('LINE', geometry_index)
                    output += str(tuple(float(format(
                        round(points[point_index][i]/10000, 4), '.4f')) for i in range(0, 3))) + ', '
                    output += str(tuple(float(format(round(
                        points[point_index+1][i]/10000, 4), '.4f')) for i in range(0, 3))) + ')},\n'
                    geometry_index += 1

                if points[-1]:
                    output += "\t{'%s%d': (" % ('LINE', geometry_index)
                    output += str(tuple(
                        float(format(round(points[0][i]/10000, 4), '.4f')) for i in range(0, 3))) + ', '
                    output += str(tuple(float(
                        format(round(points[-2][i]/10000, 4), '.4f')) for i in range(0, 3))) + ')},\n'
                    geometry_index += 1

        # Replace last comma with bracket and add new line
        if entry_index == len(scans)-1:
            output = output[:len(output)-2] + '],\n'

    print(output)  # Print output

def create_alphabet():
    '''
    Summary:
      Print out a list of all dxf files, letters only drawn from lines, in the Letters folder
    '''
    # Generate dictionary
    list = os.listdir('Letters')
    print('}')
    for name in list:
        letter_geometries = importer.import_dxf_file('Letters/'+name)
        letter = name.rstrip('.dxf')
        create_letter_from_dxf(letter, letter_geometries)
    print('}')

