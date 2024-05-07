import math
from PyNite import FEModel3D
from rich import print
import pandas as pd
import matplotlib.pyplot as plt
import truss_model as tm
import streamlit as st
import plotly.graph_objects as go
import truss_utils as tu
import truss_visulization as tv
import truss_tables as tb
import truss_sws as ts
import planesections as ps
import numpy as np

## TO DO:
# run a model to stress or c/d ratio of each element
# find dedicated database of shapes
# determine how "J" is calculated for FE model

st.header("Truss Model of Existing Steel OWSJ")
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

f_load = (1.25*DL + 1.5*SL)*(s/1000) #Expected factored design load for predicting self-weight

# Determine truss coordinates from inputs
#nodes
top_nodes = []
bot_nodes = []
d_w = L/(n/2)
for i, loc in enumerate(list(np.linspace(0, L, int(n/2+1)))):
    t_node = [loc, d]
    top_nodes.append(t_node)
    if i == 0:
        continue
    else: 
        b_node = [loc-d_w/2, 0] 
        bot_nodes.append(b_node)

# Create visualization from nodes
fig = tv.truss_visualization(top_nodes, bot_nodes)
st.plotly_chart(fig)

# Import data from Canam, Vulcraft & Omega, and find expected self-weights of trusses
canam_df = tb.canam()
omega_df = tb.omega()
vulcraft_df = tb.vulcraft()
OWSJ_dfs = [canam_df, omega_df, vulcraft_df]
sws = ts.truss_self_weight(OWSJ_dfs, L, d, f_load)
# st.write(sws)
sws_data = [
    ['Canam', 'Vulcraft', 'Omega'],
    [sws[0], sws[1], sws[2]]
    ]

# Display the table
st.table(sws_data)

#compile properties for truss configuration
# truss_model = tm.truss(top_nodes=top_nodes,
#                        bot_nodes=bot_nodes
#                        )
# truss_model.analyze() # Changes the model by performing the analysis and adding analysis results

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