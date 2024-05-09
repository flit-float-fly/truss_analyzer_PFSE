import math
from rich import print
import truss_model as tm
import streamlit as st
import truss_utils as tu
import truss_visulization as tv
import truss_tables as tt
import truss_sws as ts
import numpy as np

## TO DO:
# run a model to stress or c/d ratio of each element
# find dedicated database of shapes
# determine how "J" is calculated for FE model

st.header("FE Model of Existing Roof OWSJ")
st.write("Assumed Material Properties: E = 200e3 MPa, Density = 7850 kg/m3, Poisson Ratio = 0.28")

# User can input material and beam properties in the sidebar 
input_sidebar = st.sidebar
with input_sidebar:
    st.subheader("Existing Member Parameters; Units = N, mm")
    L = st.number_input("Truss Clear Span (mm)", value=15000)
    d = st.number_input("Truss Depth (mm)", value=800)
    n = st.number_input("Number of Web Members", value=8)
    s = st.number_input("Spacing of Joists (mm)", value=1960)
    DL = st.number_input("Specified Total Roof Dead Load (kPa) ", value=1.0)
    SL = st.number_input("Specified Roof Snow Load (kPa) ", value=1.2)

f_load = (1.25*DL + 1.5*SL)*(s/1000) #Expected factored design load for predicting self-weight, kN/m

# Import data from Canam, Vulcraft & Omega, and find expected self-weights of trusses
canam_df = tt.canam()
omega_df = tt.omega()
vulcraft_df = tt.vulcraft()
OWSJ_dfs = [canam_df, omega_df, vulcraft_df]
sws = ts.truss_self_weight(OWSJ_dfs, L, d, f_load)

#first set of model input columns
r1c1, r1c2, r1c3 = st.columns([1,1,1])
with r1c1:
    mfg = st.selectbox('Select Manufacturer', ["Canam", "Vulcraft", "Omega"])
with r1c2:
    truss_type = st.selectbox('Select Truss type', ["Warren", "Modified Warren", "Pratt"])
with r1c3:
    model_load = st.number_input("Model Loading (kN/m)", value=5)

# Determine truss coordinates and member geometry from inputs, and create the Figure to display
L_tc = L #the same for every case
L_vert = d #the same for every case

top_nodes = []
bot_nodes = []

if truss_type == "Warren":
    n_nodes_b = n/2
    n_nodes_t = n_nodes_b + 1
    x_coords_top = list(np.linspace(0, L, int(n_nodes_t)))
    for i, loc in enumerate(x_coords_top):
        t_node = [loc, d]
        top_nodes.append(t_node)
        if i == 0:
            continue
        else: 
            b_node = [loc-x_coords_top[1]/2, 0] 
            bot_nodes.append(b_node)
    # Member geometry
    n_diag = n
    n_vert = 0
    L_diag = math.sqrt((x_coords_top[1]/2)**2 + d**2)
    L_bc = L-x_coords_top[1]

elif truss_type == "Modified Warren":
    n_nodes_b = n/3
    n_nodes_t = 2*n_nodes_b + 1
    x_coords_top = list(np.linspace(0, L, int(n_nodes_t)))
    for i, loc in enumerate(x_coords_top):
        t_node = [loc, d]
        top_nodes.append(t_node)
        if (i % 2 != 0): #add a bottom node for every even top node
            b_node = [loc, 0] 
            bot_nodes.append(b_node)
    # Member geometry
    n_vert = n/3
    n_diag = n - n_vert
    L_diag = math.sqrt(x_coords_top[1]**2 + d**2)
    L_bc = L-x_coords_top[1]

else:
    n_nodes_b = (n-1)/2
    n_nodes_t = n_nodes_b + 2
    x_coords_top = list(np.linspace(0, L, int(n_nodes_t)))
    for i, loc in enumerate(x_coords_top):
        t_node = [loc, d]
        top_nodes.append(t_node)
        if (i == 0) or (i == n_nodes_t-1):
            continue
        else: 
            b_node = [loc, 0] 
            bot_nodes.append(b_node)
    # Member geometry
    n_vert = (n-1)/2
    n_diag = n - n_vert
    L_diag = math.sqrt(x_coords_top[1]**2 + d**2)
    L_bc = L-x_coords_top[1]

mem_len_dict = {"TC":L_tc,
                 "BC":L_bc,
                 "Diagonal":L_diag,
                 "Vertical":L_vert}

#compile properties for model configuration and analyze
truss_model = tm.truss_model(top_nodes, bot_nodes, truss_type, model_load)
truss_model.analyze() # Changes the model by performing the analysis and adding analysis results

#make a dict of axial response in members; map to same members shown in graphic
axial_dict = {}
axial_dict = {}
for mem in truss_model.Members:
    mem_mid = truss_model.Members[mem].L()/2
    ax = truss_model.Members[mem].axial(mem_mid, combo_name="LC")
    axial_dict[mem] = -int(ax/1000)

# second set of model input columns
r2c1, r2c2 = st.columns([1,1])
with r2c1:
    tc = st.selectbox('Select Top Chord type', ["Double Angle"])
    bc = st.selectbox('Select Bottom Chord type', ["Double Angle"])
    diagonal = st.selectbox('Select Diagonal type', ["Round Bar", "U-Bar", "Double Angle"])
    vert = st.selectbox('Select Vertical type', ["Round Bar", "U-Bar", "Double Angle"])
    st.write(f"Likely Self Weight of {mfg} OWSJ: {sws[mfg]} kg/m")

with r2c2:
    dim_tc = st.selectbox('Select TC Angle Dims (in)', list(tt.mem_properties()[tc]["size (in)"]))
    dim_bc = st.selectbox('Select BC Angle Dims (in)', list(tt.mem_properties()[bc]["size (in)"]))
    dim_diag = tu.member_selection(diagonal, "Diagonal")
    dim_vert = tu.member_selection(vert, "Vertical")

    #calculate the self weight from the model inputs
    mem_type_dict = {"TC":(tc, dim_tc),
                      "BC":(bc, dim_bc),
                      "Diagonal":(diagonal, dim_diag),
                      "Vertical":(vert, dim_vert)}
    sw_m = tu.model_sw(mem_len_dict, mem_type_dict, n_diag, n_vert)
    st.write(f"Self Weight of modeled OWSJ: {sw_m/(L/1000) :.2f} kg/m")
    # st.write(f"Self Weight of modeled OWSJ: {int(sw_m) :.2f} kg/m")

#build the visualization with inputs from the FE model
if truss_type == "Warren":
    fig = tv.truss_warren(top_nodes, bot_nodes, axial_dict)
elif truss_type == "Modified Warren":
    fig = tv.truss_mod_warren(top_nodes, bot_nodes, axial_dict)
else:
    fig = tv.truss_pratt(top_nodes, bot_nodes, axial_dict)

note1 = "Axial force (kN) shown in red"
note2 = "(-) compression; (+) Tension"
fig.add_annotation(tv.member_tag(note1, 2500, 4*d))
fig.add_annotation(tv.member_tag(note2, 2500, 3.25*d))

st.plotly_chart(fig)



st.subheader("Critical Design Lengths:")
st.write(f"Top Chord Lu: {x_coords_top[1] :.0f} mm")
st.write(f"Bottom Chord Lu: {x_coords_top[1] :.0f} mm")
st.write(f"Diagonal Lu: {L_diag :.0f} mm")
st.write(f"Vertical Lu: {L_vert :.0f} mm")

# # st.write(sws)
# sws_data = [
#     ['Canam', 'Vulcraft', 'Omega'],
#     [sws[0], sws[1], sws[2]]
#     ]

# # Display the table showing the approx. self weight for each mfg
# st.table(sws_data)

# #loop through different subgrade moduli; save to dict
# Fy_rxns_dict = {}
# for mod in inputs["subgrade_mods"]:
#     gb_model = truss.grade_beam(**beam_ppts, 
#                                       subgrade_modulus=mod, 
#                                       n_springs=n_springs,
#                                       UDL=inputs["UDL"], 
#                                       pt_loads=point_list)
#     gb_model.analyze() # Changes the model by performing the analysis and adding analysis results
#     rxn_kPa, x_sup = truss.grade_beam_post_process(gb_model, L, n_springs, w)
#     Fy_rxns_dict[mod] = rxn_kPa #update dict with corresponding pressures

# # st.write(gb_model.Members["M1"].DistLoads)
# # st.write(sum([gb_model.Nodes[i].RxnFY["LC"] for i in gb_model.Nodes]))
# # st.write(Fy_rxns_dict)