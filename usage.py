import glob

import dash_ngl
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

app = dash.Dash(__name__)

# Preset colors for the shown molecules
color_list = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
]

# PDB examples
# . indicates that only one chain should be shown
# _ indicates that more than one protein should be shown
dropdown_options = [
    "1PNK",
    "5L73",
    "4GWM",
    "3L9P",
    "6CHG",
    "3K8P",
    "2MRU",
    "1BNA",
    "6NZK",
    "6OHW"
]

# Placeholder which is loaded if no molecule is selected
data_dict = {
    "selectedValue": "placeholder",
    "chain": "ALL",
    "color": "#e41a1c",
    "filename": "placeholder",
    "ext": "",
    "config": {"type": "", "input": ""},
}


# Canvas container to display the structures
component_id = "nglViewer"
viewer = html.Div(
    id="ngl-viewer-stage",
    children=[dash_ngl.DashNgl(
        id=component_id,
        data=[data_dict]
        )],
    style={
        "display": "inline-block",
        "width": "calc(100% - 500px)",
        "float":"left",
        "marginTop": "50px",
        "marginRight": "50px",
    },
)

#"width": "calc(100% - 500px)",

###Define app layout
label_width = 4
col_width = 8

styles = {"tab": {"height": "calc(98vh - 115px)"}}

theme = {
    "dark": True,
    "detail": "#007439",
    "primary": "#00EA64",
    "secondary": "#6E6E6E",
}


# ROOT LAYOUT
rootLayout = html.Div(
    [
        # header
        html.Div(
            children=[html.H1("PStruc")],
            style={"backgroundColor": "#3aaab2", "height": "7vh"},
        ),
        viewer,
        # using dcc.Loading leads to remounting with every selection change
        #dcc.Loading(viewer),
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Data",
                    children=[
                        # daq.ToggleSwitch(
                        #     id='toggle-theme',
                        #     label=['Light', 'Dark'],
                        #     style={'width': '250px', 'margin': 'auto'},
                        #     value=False
                        # ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="pdb-dropdown",
                                    clearable=False,
                                    options=[
                                        {"label": k, "value": k}
                                        for k in dropdown_options
                                    ],
                                    placeholder="Select a molecule",
                                ),
                                dcc.Input(
                                    id="pdb-string",
                                    placeholder="pdbID1.chain_pdbID2.chain",
                                ),
                                html.Button("Submit", id="button"),
                            ],
                            style={"width": "100%", "display": "inline-block"},
                        ),
                    ],
                ),
                dcc.Tab(
                    label="View",
                    children=[
                        html.Div(
                            style=styles["tab"],
                            children=[
                                html.Div(["Camera settings"]),
                                dcc.Dropdown(
                                    id="stage-camera-type",
                                    options=[
                                        {"label": k.capitalize(), "value": k}
                                        for k in ["perspective", "orthographic"]
                                    ],
                                    value="perspective",
                                ),
                                html.Div(["Background"]),
                                dcc.Dropdown(
                                    id="stage-bg-color",
                                    options=[
                                        {"label": c, "value": c.lower()}
                                        for c in ["black", "white"]
                                    ],
                                    value="white",
                                ),
                                html.Div(["Render quality"]),
                                dcc.Dropdown(
                                    id="stage-render-quality",
                                    options=[
                                        {"label": c, "value": c.lower()}
                                        for c in ['auto', 'low', 'medium', 'high']
                                    ],
                                    value="auto",
                                ),
                            ],
                        )
                    ],
                ),
            ],
        ),
    ]
)

# APP LAYOUT
app.layout = html.Div(
    id="dark-theme-container",
    children=[
        html.Div(
            id="dark-theme-components",
            children=[daq.DarkThemeProvider(
                theme=theme,
                children=rootLayout)],
        )
    ],
)

# Helper function to load the data
def getData(selection, pdb_id, color):

    chain = "ALL"

    # Check if only one chain should be shown
    if "." in pdb_id:
        pdb_id, chain = pdb_id.split(".")

    if pdb_id not in dropdown_options:
        return data_dict
    else:
        # get path to protein structure
        fname = [f for f in glob.glob("data/" + pdb_id + ".*")][0]

        with open(fname, "r") as f:
            contents = f.read()

        return {
            "selectedValue": selection,
            "chain": chain,
            "color": color,
            "filename": fname.split("/")[-1],
            "ext": fname.split(".")[-1],
            "config": {"type": "text/plain", "input": contents},
        }


##CB viewport
@app.callback(
    Output(component_id, "data"),
    [Input("pdb-dropdown", "value"),
     Input("button", "n_clicks")],
    [State("pdb-string", "value")],
)
def display_output(selection, n_clicks, value):
    data = []
    print(selection, n_clicks, value)

    if selection is None and value is None:
        data.append(data_dict)

    if selection is not None and value is None:
        pdb_id = selection
        data.append(getData(selection, pdb_id, color_list[0]))

    elif value is not None and n_clicks > 0:
        if len(value) > 4:
            pdb_id = value
            if "_" in value:
                for i, pdb_id in enumerate(value.split("_")):
                    data.append(getData(value, pdb_id, color_list[i]))
            else:
                data.append(getData(value, pdb_id, color_list[0]))
        else:
            data.append(data_dict)
    return data


# CB stage
@app.callback(
    Output(component_id, "stageParameters"),
    [Input("stage-bg-color", "value"),
     Input("stage-camera-type", "value"),
     Input("stage-render-quality", "value")]
)
def update_stage(bgcolor, camera_type, quality):
    return {
        "backgroundColor": bgcolor,
        "cameraType": camera_type,
        "quality": quality,
    }


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
