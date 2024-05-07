import plotly.graph_objects as go

def truss_visualization(top_nodes: list[list[float]], bot_nodes: list[list[float]]) -> go.Figure: 
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

    # Set layout properties with equal scale for both axes
    fig.update_layout(
        yaxis=dict(scaleanchor='x', scaleratio=1)
        )
    fig.layout.title.text = "Shape of Existing OWSJ"
    fig.layout.xaxis.title = "Length (mm)"
    fig.layout.yaxis.title = "Depth (mm)"
    # fig.layout.yaxis.range = [0,500]
    
    return fig