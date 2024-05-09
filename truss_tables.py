import pandas as pd
import pandas as pd
import truss_utils as tu

def canam() -> pd.DataFrame:
    """
    Import Canam tables from csv
    """
    canam_df = pd.read_csv('OWSJ_tables_canam.csv',header=1)
    canam_df.rename(columns={canam_df.columns[0]: 'span', canam_df.columns[1]: 'depth'}, inplace=True)
    canam_df['span'].ffill(inplace=True)
    canam_df['span']= canam_df['span']*1000
    canam_df['depth'] = canam_df['depth'].apply(tu.remove_comma)
    canam_df['depth'] = canam_df['depth'].astype(float)
    canam_df.name = "canam"

    return canam_df

def vulcraft() -> pd.DataFrame:
    """
    Import Vulcraft tables from csv
    """
    vulcraft_df = pd.read_csv('OWSJ_tables_vulcraft.csv', header=1)
    vulcraft_df.rename(columns={"Factored Load": 'value'}, inplace=True)
    vulcraft_df.columns = [col.lower() for col in vulcraft_df]
    #drop first, bridging & L/360 rows, then the "value" column
    vulcraft_df.drop(index=0, inplace=True)
    vulcraft_df = vulcraft_df[~vulcraft_df['value'].str.contains('Bridg.')]
            #back fill depths values before dropping the 'L/360' rows
    vulcraft_df['depth'].bfill(inplace=True)
    vulcraft_df = vulcraft_df[~vulcraft_df['value'].str.contains('L/360')]
    vulcraft_df = vulcraft_df.drop(columns=['value'])
    #convert all values  to float and mm
    vulcraft_df = vulcraft_df.astype(float)
    vulcraft_df['span'] = vulcraft_df['span']*1000
    vulcraft_df.name = "vulcraft"

    return vulcraft_df

def omega() -> pd.DataFrame:
    """
    Import Omega tables from csv
    """
    omega_df = pd.read_csv('OWSJ_tables_omega.csv', header=None)
    col_names = ["depth", "D/D", "E/D", "E/E", "F/E", "F/F", "G/F", "G/G", "H/G", "H/H", "K/H", "K/K", "L/K", "L/L"]
    omega_df.columns = col_names
    omega_df['span'] = omega_df['depth'].apply(tu.find_span)
    omega_df['span'].ffill(inplace=True)
    columns = ['span'] + [col for col in omega_df if col != 'span']
    omega_df['span'] = omega_df['span'].astype(float)
    omega_df = omega_df[columns]
    # Drop rows with useless info; cells with "DEPTH" OR "SPAN"
    omega_df = omega_df[~omega_df['depth'].str.contains('DEPTH') & ~omega_df['depth'].str.contains('SPAN')]
    omega_df['depth'] = omega_df['depth'].astype(float)
    omega_df.name = "omega"

    return omega_df

def mem_properties() -> pd.DataFrame:
    """
    Import member properties from Canam, organize based on member type
    """
    mem_properties_df = pd.read_csv("OWSJ_member_properties_canam.csv", header = None)

    # create round bar df
    round_bar_df = mem_properties_df.iloc[0:11]
    round_bar_df.dropna(how='all', inplace=True, axis=1)
    round_bar_df = round_bar_df.loc[2:]
    round_bar_df.reset_index(inplace=True, drop=True)
    round_bar_df.columns = ["size (in)", "Forming", "Mass (kg/m)", "Area (mm2)", "I (1e3 mm4)", "r (mm)"]
    round_bar_df.index = round_bar_df["size (in)"]

    # create U-Bar df
    u_bar_df = mem_properties_df.iloc[12:29]
    u_bar_df.dropna(how='all', inplace=True, axis=1)
    u_bar_df = u_bar_df.iloc[3:]
    u_bar_df.reset_index(inplace=True, drop=True)
    u_bar_df["size"] = u_bar_df.loc[:,:5].apply(lambda row: ' '.join(row.astype(str)), axis=1) #combine the first 6 columns into 1
    u_bar_df = pd.merge(u_bar_df["size"], u_bar_df.loc[:,7:])
    u_bar_df.columns = ["size (in)", "Forming", "Mass (kg/m)", "Area (mm2)", "y (mm)", "Ixx (1e3 mm4)", "rxx (mm)", "Iyy (1e3 mm4)", "ryy (mm)"]
    u_bar_df.index = u_bar_df["size (in)"]
    

    # create double angle df
    dbl_angle_df = mem_properties_df.iloc[30:89]
    dbl_angle_df.dropna(how='all', inplace=True, axis=1)
    dbl_angle_df = dbl_angle_df.iloc[3:]
    dbl_angle_df.reset_index(inplace=True, drop=True)
    dbl_angle_df["size"] = dbl_angle_df.loc[:,:5].apply(lambda row: ' '.join(row.astype(str)), axis=1) #combine the first 6 columns into 1
    dbl_angle_df = pd.merge(dbl_angle_df["size"], dbl_angle_df.loc[:,7:])
    dbl_angle_df.columns = ["size (in)", "Forming", "Mass (kg/m)", "Area (mm2)", "y (mm)", "Ixx (1e3 mm4)", "rxx (mm)", "12.7 gap (mm)", "19 gap (mm)", "25 gap (mm)", "35 gap (mm)", "45 gap (mm)", "60 gap (mm)", "rz (mm)"]
    dbl_angle_df.index = dbl_angle_df["size (in)"]
    

    mem_dict = {"Round Bar": round_bar_df,
                "U-Bar": u_bar_df,
                "Double Angle": dbl_angle_df}
    
    return mem_dict