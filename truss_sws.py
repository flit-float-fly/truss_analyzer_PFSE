import numpy as np
import pandas as pd
import truss_utils as tu

def truss_self_weight(OWSJ_dfs: list[pd.DataFrame], span: float, depth: float, f_load: float) -> list[float]:
    """
    Investigate each truss supplier's tables to approximate the likely self-weight (kN/m) of the existing truss 
    """
    expected_sw_canam = 0
    expected_sw_vulcraft = 0
    expected_sw_omega = 0
    for df in OWSJ_dfs:
        name = df.name
        span = float(span)
        depth = float(depth)
        f_load = float(f_load)
        print(name)
        span_mask = (df['span'] < 1.05*span) & (df['span'] > 0.95*span) 
        depth_mask = (df['depth'] < 1.05*depth) & (df['depth'] > 0.95*depth)
        df = df.loc[span_mask & depth_mask]
        #Omega
        if name == "omega":
            cols = [col for col in df.columns if '/' in col]
            df_sliced = df[cols]
            chords = []
            sws = []
            for column in df_sliced.columns:
                for index, cell_value in enumerate(df_sliced[column]):
                    try:
                        f = float(cell_value.split("\n")[0])
                        sw = float(cell_value.split("\n")[2])
                        if (f > 0.97*f_load) & (f < 1.03*f_load):
                            chords.append((column, sw))
                            sws.append(sw)
                    except:
                        continue
            if sws == []:
                expected_sw_omega = "no values found in that range"
            else:
                expected_sw_omega = round(np.mean(sws),2)
        #Vulcraft         
        elif name == "vulcraft":
            col_nums = [float(col) for col in df.columns if "." in col] #convert factored headers to float
            adjacent_f_loads = tu.find_adjacent_numbers(col_nums, f_load) #find interpolated, likely average self weight
            df = df[[str(min(adjacent_f_loads)), str(max(adjacent_f_loads))]]
            if adjacent_f_loads[1] == adjacent_f_loads[0]:
                expected_sw_vulcraft = round(df[str(adjacent_f_loads[0])].values.mean(),2)
            else:
                ratio = (f_load - min(adjacent_f_loads))/(abs(adjacent_f_loads[1] - adjacent_f_loads[0]))
                df[str(f_load)] = (df[str(max(adjacent_f_loads))] - df[str(min(adjacent_f_loads))])*ratio + df[str(min(adjacent_f_loads))]
                expected_sw_vulcraft = round(df[str(f_load)].values.mean(),2)
        #Canam
        elif name == "canam":
            col_nums = [float(col) for col in df.columns if "." in col] #convert factored headers to float
            adjacent_f_loads = tu.find_adjacent_numbers(col_nums, f_load) #find interpolated, likely average self weight
            df = df[[str(min(adjacent_f_loads)), str(max(adjacent_f_loads))]]
            df = df.map(tu.isolate_sw)
            if adjacent_f_loads[1] == adjacent_f_loads[0]:
                expected_sw_canam = round(df[str(adjacent_f_loads[0])].values.mean(),2)
            else:
                ratio = (f_load - min(adjacent_f_loads))/(abs(adjacent_f_loads[1] - adjacent_f_loads[0]))
                df[str(f_load)] = (df[str(max(adjacent_f_loads))] - df[str(min(adjacent_f_loads))])*ratio + df[str(min(adjacent_f_loads))]
                expected_sw_canam = round(df[str(f_load)].values.mean(),2)

    sws_dict = {"Canam": expected_sw_canam,
                "Vulcraft": expected_sw_vulcraft,
                "Omega": expected_sw_omega}
    
    return sws_dict