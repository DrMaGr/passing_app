import dash
from dash import html
import dash_cytoscape as cyto
from player_config import ALL_PLAYERS, TEAM_COLORS

# Initialize Dash app
app = dash.Dash(__name__)

# Create Nodes for Players (Draggable)
nodes = [
    {
        "data": {"id": player["label"], "label": player["label"]},
        "position": {"x": player["x"], "y": player["y"]},
        "classes": player["team"]
    }
    for player in ALL_PLAYERS
]

# Define Stylesheet for Teams
stylesheet = [
    {"selector": "node", "style": {"width": 25, "height": 25, "label": "data(label)", "text-valign": "center"}},
    {"selector": ".Essendon", "style": {"background-color": "black", "border-color": "red", "color": "white"}},
    {"selector": ".Opponent", "style": {"background-color": "white", "border-color": "blue", "color": "blue"}}
]

# Layout
app.layout = html.Div([
    html.H1("Hockey Field with Draggable Players"),

    cyto.Cytoscape(
        id="hockey-field",
        layout={"name": "preset"},  # Positions are manually defined
        style={"width": "800px", "height": "600px"},
        elements=nodes,
        stylesheet=stylesheet,
        userZoomingEnabled=False,  # Disable zooming
        userPanningEnabled=True,  # Enable panning
        boxSelectionEnabled=False,  # Disable box selection
    ),

    html.Div(id="output")  # Placeholder for output
])

# Run Dash App
if __name__ == "__main__":
    app.run_server(debug=True)
