import plotly.graph_objects as go

def member_tag(tag: str, x: float, y: float) -> dict:
    """
    create an annotation format function that can be called to display text for differnt lines
    """
    annotation = dict(  x=x,  # x-coordinate of the text
                        y=y,  # y-coordinate of the text
                        text=tag,  # Text to be displayed
                        showarrow=False,  # Do not show arrow
                        font=dict(
                            family="Arial",  # Font family
                            size=12,         # Font size
                            color="red"      # Font color
                            )
                        )
    return annotation

def truss_warren(   top_nodes: list[list[float]],
                    bot_nodes: list[list[float]],
                    axial_dict: dict
                ) -> go.Figure: 
    """
    create a visualization from the given nodes that dispalys a "Warren" pattern truss
    """
    # Setup and plot truss visualization
    fig = go.Figure()
    #top chord
    for i in range(len(top_nodes)-1):
        x_coord_i, y_coord_i = top_nodes[i]
        x_coord_j, y_coord_j = top_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False  
        )
        fig.add_trace(trace)
    x_tag = top_nodes[len(top_nodes) // 2][0]
    name_force = "TC  "+str(axial_dict["TC"])
    tag = member_tag(name_force, x_tag, top_nodes[0][1]*1.5)
    fig.add_annotation(tag)

    #bottom chord
    for i in range(len(bot_nodes)-1):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = bot_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
    name_force = "BC  "+str(axial_dict["BC"])
    tag = member_tag(name_force, x_tag, -500)
    fig.add_annotation(tag)

    #down webs
    for i in range(len(bot_nodes)):
        x_coord_i, y_coord_i = top_nodes[i]
        x_coord_j, y_coord_j = bot_nodes[i]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"WD{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_i*0.75)
        fig.add_annotation(tag)

    #up webs
    for i in range(len(bot_nodes)):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = top_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"WU{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_j*0.25)
        fig.add_annotation(tag)

    # Set layout properties with equal scale for both axes
    fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
    fig.layout.title.text = "Shape of Existing OWSJ"
    fig.layout.xaxis.title = "Length (mm)"
    fig.layout.yaxis.title = "Depth (mm)"
    
    return fig

def truss_mod_warren(   top_nodes: list[list[float]],
                        bot_nodes: list[list[float]],
                        axial_dict: dict
                    ) -> go.Figure: 
    """
    create a visualization from the given nodes that dispalys a "Modified Warren" pattern truss
    """
    # Setup and plot truss visualization
    fig = go.Figure()
    #top chord
    for i in range(len(top_nodes)-1):
        x_coord_i, y_coord_i = top_nodes[i]
        x_coord_j, y_coord_j = top_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False  
        )
        fig.add_trace(trace)
    x_tag = top_nodes[len(top_nodes) // 2][0]
    name_force = "TC  "+str(axial_dict["TC"])
    tag = member_tag(name_force, x_tag, top_nodes[0][1]*1.5)
    fig.add_annotation(tag)

    #bottom chord
    for i in range(len(bot_nodes)-1):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = bot_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
    name_force = "BC  "+str(axial_dict["BC"])
    tag = member_tag(name_force, x_tag, -500)
    fig.add_annotation(tag)

    #down webs
    for i in range(len(bot_nodes)):
        x_coord_i, y_coord_i = top_nodes[2*i]
        x_coord_j, y_coord_j = bot_nodes[i]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"WD{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_i*0.75)
        fig.add_annotation(tag)

    #up webs
    for i in range(len(bot_nodes)):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = top_nodes[2*i+2]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"WU{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_j*0.25)
        fig.add_annotation(tag)

    #verticals
    for i in range(len(bot_nodes)):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = top_nodes[2*i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"V{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, (y_coord_i+y_coord_j)/2)
        fig.add_annotation(tag)

    # Set layout properties with equal scale for both axes
    fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
    fig.layout.title.text = "Shape of Existing OWSJ"
    fig.layout.xaxis.title = "Length (mm)"
    fig.layout.yaxis.title = "Depth (mm)"
    
    return fig

def truss_pratt(top_nodes: list[list[float]],
                bot_nodes: list[list[float]],
                axial_dict: dict
                ) -> go.Figure: 
    """
    create a visualization from the given nodes that dispalys a "Pratt" pattern truss
    """
    # Setup and plot truss visualization
    fig = go.Figure()
    #top chord
    for i in range(len(top_nodes)-1):
        x_coord_i, y_coord_i = top_nodes[i]
        x_coord_j, y_coord_j = top_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False  
        )
        fig.add_trace(trace)
    x_tag = top_nodes[len(top_nodes) // 2][0]
    name_force = "TC  "+str(axial_dict["TC"])
    tag = member_tag(name_force, x_tag, top_nodes[0][1]*1.5)
    fig.add_annotation(tag)

    #bottom chord
    for i in range(len(bot_nodes)-1):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = bot_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
    name_force = "BC  "+str(axial_dict["BC"])
    tag = member_tag(name_force, x_tag, -500)
    fig.add_annotation(tag)

    #down webs
    for i in range(int((len(bot_nodes)+1)/2)):
        x_coord_i, y_coord_i = top_nodes[i]
        x_coord_j, y_coord_j = bot_nodes[i]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"WD{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_i*0.75)
        fig.add_annotation(tag)

    #up webs
    for i in range(int((len(bot_nodes)+1)/2)):
        i += int((len(bot_nodes)-1)/2) #start from the mid point of this list
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = top_nodes[i+2]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"WU{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_j*0.75)
        fig.add_annotation(tag)

    #verticals
    for i in range(len(bot_nodes)):
        x_coord_i, y_coord_i = bot_nodes[i]
        x_coord_j, y_coord_j = top_nodes[i+1]
        trace = go.Scatter(
            x=[x_coord_i, x_coord_j],
            y=[y_coord_i, y_coord_j],
            line={'color': 'black', 'width': 2},
            showlegend=False
        )
        fig.add_trace(trace)
        name = f"V{i}"
        name_force = f"{name}  {axial_dict[name]}"
        tag = member_tag(name_force, (x_coord_i+x_coord_j)/2, y_coord_j*0.25)
        fig.add_annotation(tag)

    # Set layout properties with equal scale for both axes
    fig.update_layout(yaxis=dict(scaleanchor='x', scaleratio=1))
    fig.layout.title.text = "Shape of Existing OWSJ"
    fig.layout.xaxis.title = "Length (mm)"
    fig.layout.yaxis.title = "Depth (mm)"
    
    return fig