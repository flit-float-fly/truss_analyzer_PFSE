import numpy as np
import re
import pandas as pd

def remove_comma(cell):
    """
    Find cells that have have a comma in the number, then convert to float; cleaning the Canam data set
    """
    number = float(cell.replace(',', ''))
    return number

def find_span(cell):
    """
    find cells that have the text "SPAN" in them; cleaning the Omega data set
    """
    if "SPAN" in cell:
        match_span = re.search(r'\b(\d+)\b', cell)
        return match_span.group(1)
    else:
        return np.nan
    
def find_adjacent_numbers(numbers, target):
    """
    Find numbers adjacent to target number for running interpolations
    """
    sorted_numbers = np.sort(numbers) # Sort the list of numbers
    index = np.searchsorted(sorted_numbers, target) # Find the index of the target number
    # Get the two numbers adjacent to the target number
    if index == 0:
        return sorted_numbers[0], sorted_numbers[0]
    elif index == len(sorted_numbers):
        return sorted_numbers[-1], sorted_numbers[-1]
    else:
        return sorted_numbers[index - 1], sorted_numbers[index]
            
def isolate_sw(cell):
    sw = float(cell.split("\n")[0])
    return sw
