import numpy as np
import re
import streamlit as st
import truss_tables as tt


def remove_comma(cell):
    """
    Find cells that have have a comma in the number, then convert to float; cleaning the Canam data set
    """
    number = float(cell.replace(',', ''))
    return number

def find_span(cell):
    """
    find cells that have the text "SPAN" in them and pull out the length; cleaning the Omega data set
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

def member_selection(mem_type: str, mem: str):
    """
    to create the info for an "st.selectbox" for streamlit app
    """
    # import sizes from selected member type dataframe
    mem_type_sizes = list(tt.mem_properties()[mem_type]["size (in)"])
    if mem_type == "Round Bar":
        info = st.selectbox(f'Select {mem} Round Bar Dia (in)', mem_type_sizes)
    if mem_type == "U-Bar":
        info = st.selectbox(f'Select {mem} U-Bar Dims (in)', mem_type_sizes)
    if mem_type == "Double Angle":
        info = st.selectbox(f'Select {mem} Angle Dims (in)', mem_type_sizes)

    return info

def model_sw(len_dict: dict, type_dict: dict, n_diag: float, n_vert: float) -> float:
    """
    Take the calculated geometry and member details from input and using the properties
    Dataframes, calculate the self weight of the entire truss
    """
    mem_properties = tt.mem_properties()
    print(n_diag, n_vert)
    sw_dict = {}
    for mem, details in type_dict.items():
        sw_mem_L = float(mem_properties[details[0]]["Mass (kg/m)"][details[1]])
        sw_mem = (len_dict[mem]/1000)*sw_mem_L
        print(mem, sw_mem, len_dict[mem]/1000)
        sw_dict[mem] = sw_mem

    wt_total = 0
    for mem, wt in sw_dict.items():
        if mem == "Diagonal":
            wt_total += wt*n_diag
        elif mem == "Vertical":
            wt_total += wt*n_vert
        else:
            wt_total += wt

    return wt_total