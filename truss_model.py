import math
from rich import print
from PyNite import FEModel3D
import numpy as np

def truss(top_nodes: list,
          bot_nodes: list, 
              ) -> FEModel3D:
    """
    Build and return an FE Model to be analyzed and post-processed that represents a beam supported by n
    number of springs.
    - user defines total nbumber of springs
    - Subgrade modulus input in the form of force/volume ie: kN/m3 or lb/in3
    all other inputs are in this function.
    """
    #define shear modulus

    E = 200000 #MPa
    nu = 0.28 #Steel poisson ratio
    rho = 7850*9.81/1e9 #density in N/mm3
    G = E/(2*(1+nu))

    # Develop database of members; start with a unitary member to get the model running
    Iz = 1
    Iy = 1
    A = 1
    J = 1 #need to determine what this actually is

    # Define the model base; start adding properties
    model = FEModel3D() # Creates an empty model
    model.add_material("Steel", E, G, nu, rho)
    
    # Add nodes to the model
    #Top nodes
    top_node_tags = []
    for i, node in enumerate(top_nodes):
        name = f"T{i}"
        top_node_tags.append(name)
        model.add_node(name=name, X=node[0], Y=node[1], Z=0.0)
        if i == 0 or i == len(top_nodes)-1:
            model.def_support(name, 1, 0, 1, 1, 0, 0) 

    #Bot nodes
    bot_node_tags = []
    for i, node in enumerate(bot_nodes):
        name = f"B{i}"
        bot_node_tags.append(name)
        model.add_node(name=name, X=node[0], Y=node[1], Z=0.0)

    # Add elements to the nodes: top chord, bot chord, web
    #Top chord
    for i, node in enumerate(top_node_tags[:-1]):
        name = f"TC{i}"
        model.add_member(name=name, i_node=node, j_node=top_node_tags[i+1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
    #Bot chord
    for i, node in enumerate(bot_node_tags[:-1]):
        name = f"BC{i}"
        model.add_member(name=name, i_node=node, j_node=bot_node_tags[i+1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
    #down webs
    for i, node in enumerate(bot_node_tags):
        name = f"W{i*2}"
        model.add_member(name=name, i_node=top_node_tags[i], j_node=node, material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
        name = f"W{i*2+1}"
        model.add_member(name=name, i_node=node, j_node=top_node_tags[i+1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)

    # Add a load combo
    model.add_load_combo(name="LC", factors={"LC": 1})

    # Add Distributed and Point loads
    # for mem in model.Members:
    #     if "T" in mem:
    #         model.add_member_dist_load(member_name=mem, Direction="FY", w1=-UDL[100], w2=-UDL[100], x1=0, x2=mem., case="LC") 
    # for pt in pt_loads:
    #     model.add_member_pt_load(Member="M1", Direction="FY", P=-pt[0] , x=pt[1], case="LC")

    return model

# def grade_beam_post_process(model: FEModel3D, L: float, n_springs: float, w:float) -> list[float]:
#     """
#     take the analyzed grade beam model and order the results to be displayed.
#     specifically refers to the model defined in "grade_beam"
#     it's assumed that the units are alway N and mm
#     """
#     A_dx = L/n_springs * w
#     kPa = []
#     x_sup = []
#     for node_name, node in model.Nodes.items():
#         kPa.append(node.RxnFY["LC"]/A_dx*1000)
#         x_sup.append(node.X)

#     return kPa, x_sup
