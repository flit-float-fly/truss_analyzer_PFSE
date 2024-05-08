from rich import print
from PyNite import FEModel3D

def truss_model(top_nodes: list[list[float]],
                bot_nodes: list[list[float]],
                truss_type: str,
                f_load: float 
                ) -> FEModel3D:
    """
    Build and return an FE Model of an OWSJ to be analyzed and post-processed 
    - user defines geometry through span, depth and pattern selection
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
        if i == 0:
            model.def_support(name, 1, 1, 1, 1, 0, 0)
        if i == len(top_nodes)-1:
            model.def_support(name, 0, 1, 1, 1, 0, 0) 

    #Bot nodes
    bot_node_tags = []
    for i, node in enumerate(bot_nodes):
        name = f"B{i}"
        bot_node_tags.append(name)
        model.add_node(name=name, X=node[0], Y=node[1], Z=0.0)

    # Add elements to the nodes: top chord, bot chord, web
    #Top chord
    model.add_member(name="TC", i_node=top_node_tags[0], j_node=top_node_tags[-1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
    #Bot chord
    model.add_member(name="BC", i_node=bot_node_tags[0], j_node=bot_node_tags[-1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)

    #Add webs per truss type
    if truss_type == "Warren":
        #down webs
        for i in range(len(bot_nodes)):
            name = f"WD{i}"
            model.add_member(name=name, i_node=top_node_tags[i], j_node=bot_node_tags[i], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
        #up webs
        for i in range(len(bot_nodes)):
            name = f"WU{i}"
            model.add_member(name=name, i_node=bot_node_tags[i], j_node=top_node_tags[i+1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)

    elif truss_type == "Modified Warren":
        #down webs
        for i in range(len(bot_nodes)):
            name = f"WD{i}"
            model.add_member(name=name, i_node=top_node_tags[2*i], j_node=bot_node_tags[i], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
        #up webs
        for i in range(len(bot_nodes)):
            name = f"WU{i}"  
            print(name, top_node_tags[2*i+2])
            model.add_member(name=name, i_node=bot_node_tags[i], j_node=top_node_tags[2*i+2], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
        #verticals
        for i in range(len(bot_nodes)):
            name = f"V{i}"  
            model.add_member(name=name, i_node=bot_node_tags[i], j_node=top_node_tags[2*i+1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)

    else: #Pratt truss
        #down webs
        for i in range(int((len(bot_nodes)+1)/2)):
            name = f"WD{i}"
            model.add_member(name=name, i_node=top_node_tags[i], j_node=bot_node_tags[i], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
        #up webs
        for i in range(int((len(bot_nodes)+1)/2)):
            i += int((len(bot_nodes)-1)/2) #start from the mid point of this list
            name = f"WU{i}"  
            model.add_member(name=name, i_node=bot_node_tags[i], j_node=top_node_tags[i+2], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)
        #verticals
        for i in range(len(bot_nodes)):
            name = f"V{i}"  
            model.add_member(name=name, i_node=bot_node_tags[i], j_node=top_node_tags[i+1], material="Steel", Iy=Iy, Iz=Iz, J=J, A=A)

    # Add a load combo
    model.add_load_combo(name="LC", factors={"LC": 1})

    # Add Distributed and Point loads
    model.add_member_dist_load(member_name="TC", Direction="FY", w1=-f_load, w2=-f_load, x1=0, x2=top_nodes[-1][0], case="LC") 
    # for pt in pt_loads:
    #     model.add_member_pt_load(Member="M1", Direction="FY", P=-pt[0] , x=pt[1], case="LC")

    return model

# def truss_model_pp()