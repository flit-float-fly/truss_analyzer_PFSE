import math
from PyNite import FEModel3D
from rich import print
import pandas as pd
import matplotlib.pyplot as plt
import truss_model as truss
import streamlit as st
import plotly.graph_objects as go
import truss_utils as tu
import planesections as ps
import numpy as np

## TO DO:
# run a model to stress or c/d ratio of each element
# find dedicated database of shapes
# determine how "J" is calculated for FE model

st.header("Truss Model of Existing Steel OWSJ")
st.subheader("Assumed Material Properties: E = 200e3 MPa, Density = 7850 kg/m3, Poisson Ratio = 0.28")

# User can input material and beam properties in the sidebar 
input_sidebar = st.sidebar
with input_sidebar:
    st.subheader("Existing Member Parameters; Units = N, mm")
    L = st.number_input("Truss Clear Span (mm)", value=6000)
    d = st.number_input("Truss Depth (mm)", value=1000)
    n = st.number_input("Number of Web Members", value=12)

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

# Setup and plot truss visualization
fig = go.Figure()
#top chord
for i in range(len(top_nodes)-1):
    x_coord_i, y_coord_i = top_nodes[i]
    x_coord_j, y_coord_j = top_nodes[i+1]
    trace = go.Scatter(
        x=[x_coord_i, x_coord_j],
        y=[y_coord_i, y_coord_j],
        line={'color': 'green', 'width': 5},
        showlegend=False  
    )
    fig.add_trace(trace)
#bottom chord
for i in range(len(bot_nodes)-1):
    x_coord_i, y_coord_i = bot_nodes[i]
    x_coord_j, y_coord_j = bot_nodes[i+1]
    trace = go.Scatter(
        x=[x_coord_i, x_coord_j],
        y=[y_coord_i, y_coord_j],
        line={'color': 'red', 'width': 5},
        showlegend=False
    )
    fig.add_trace(trace)
#down webs
for i in range(len(bot_nodes)):
    x_coord_i, y_coord_i = top_nodes[i]
    x_coord_j, y_coord_j = bot_nodes[i]
    trace = go.Scatter(
        x=[x_coord_i, x_coord_j],
        y=[y_coord_i, y_coord_j],
        line={'color': 'blue', 'width': 5},
        showlegend=False
    )
    fig.add_trace(trace)
#up webs
for i in range(len(bot_nodes)):
    x_coord_i, y_coord_i = bot_nodes[i]
    x_coord_j, y_coord_j = top_nodes[i+1]
    trace = go.Scatter(
        x=[x_coord_i, x_coord_j],
        y=[y_coord_i, y_coord_j],
        line={'color': 'orange', 'width': 5},
        showlegend=False
    )
    fig.add_trace(trace)

fig.layout.title.text = "Shape of Existing OWSJ"
fig.layout.xaxis.title = "Length (mm)"
fig.layout.yaxis.title = "Depth (mm)"

st.plotly_chart(fig)

#compile properties for truss configuration
truss_ppts = {  "mat": "Steel",
                "L": L,
                "E": E,
                "nu": nu, 
                "rho": rho,
                "J": J}

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