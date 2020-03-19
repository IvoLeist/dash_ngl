import base64
import glob

import dash_ngl
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)
app.css.config.serve_locally = True


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
    "6OHW",
]

# Placeholder which is loaded if no molecule is selected
data_dict = {
    "uploaded": False,
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
    id="ngl-biomolecule-viewer",
    children=[dash_ngl.DashNgl(id=component_id, data=[data_dict])],
)

about_html = [
    html.H4(className="what-is", children="What is Ngl Molecule Viewer?",),
    html.P(
        "Ngl Molecule Viewer is a visualizer that allows you"
        "to view biomolecules in multiple representations:"
        "sticks, spheres, and cartoons."
    ),
    html.P(
        "You can select a preloaded structure, or upload your own,"
        'in the "Data" tab. A sample structure is also'
        "available to download."
    ),
    html.P("Additionally you can show multiple structures and/or " "specify a chain"),
    html.P(
        'In the "View" tab, you can change the style and'
        "coloring of the various components of your molecule."
    ),
]

data_tab = [
    html.Div(className="app-controls-name", children="Select structure",),
    dcc.Dropdown(
        id="pdb-dropdown",
        clearable=False,
        options=[{"label": k, "value": k} for k in dropdown_options],
        value="1BNA",
    ),
    html.Div(
        className="app-controls-name",
        children="Show multiple structures & specify a chain",
    ),
    dcc.Input(id="pdb-string", placeholder="pdbID1.chain_pdbID2.chain",),
    html.Button("Submit", id="button"),
    html.Div(
        title="Upload biomolecule to view here",
        className="app-controls-block",
        id="ngl-upload-container",
        children=[
            dcc.Upload(
                id="ngl-upload-data",
                className="control-upload",
                children=html.Div(["Drag and drop or click to upload a file.",]),
                # Allow multiple files to be uploaded
                multiple=True,
            ),
        ],
    ),
    html.Div(id="ngl-data-info"),
]

view_tab = [
    html.Div(
        title="select background color",
        className="app-controls-block",
        id="ngl-style-color",
        children=[
            html.P(
                "Background color",
                style={"font-weight": "bold", "margin-bottom": "10px",},
            ),
            dcc.Dropdown(
                id="stage-bg-color",
                options=[
                    {"label": c, "value": c.lower(),} for c in ["black", "white",]
                ],
                value="white",
            ),
        ],
    ),
    html.Div(
        title="Camera settings",
        className="app-controls-block",
        id="ngl-selection-display",
        children=[
            html.P(
                "Camera settings",
                style={"font-weight": "bold", "margin-bottom": "10px",},
            ),
            dcc.Dropdown(
                id="stage-camera-type",
                options=[
                    {"label": k.capitalize(), "value": k,}
                    for k in ["perspective", "orthographic",]
                ],
                value="perspective",
            ),
        ],
    ),
    html.Div(
        title="select render quality",
        className="app-controls-block",
        id="ngl-style",
        children=[
            html.P(
                "Render quality",
                style={"font-weight": "bold", "margin-bottom": "10px",},
            ),
            dcc.Dropdown(
                id="stage-render-quality",
                options=[
                    {"label": c, "value": c.lower(),}
                    for c in ["auto", "low", "medium", "high",]
                ],
                value="auto",
            ),
        ],
    ),
]

tabs = html.Div(
    id="ngl-control-tabs",
    className="control-tabs",
    children=[
        dcc.Tabs(
            id="ngl-tabs",
            value="what-is",
            children=[
                dcc.Tab(
                    label="About",
                    value="what-is",
                    children=html.Div(className="control-tab", children=about_html),
                ),
                dcc.Tab(
                    label="Data",
                    value="upload-select",
                    children=html.Div(className="control-tab", children=data_tab),
                ),
                dcc.Tab(
                    label="View",
                    value="view-options",
                    children=[html.Div(className="control-tab", children=view_tab)],
                ),
            ],
        ),
    ],
)

# LAYOUT
app.layout = html.Div(
    id="main-page",
    children=[
        html.Div(
            id="app-page-header",
            children=[html.H1("Ngl Molecule Viewer")],
            style={"background": "#e7625f", "color": "white"},
        ),
        html.Div(
            id="app-page-content",
            children=[
                html.Div(
                    id="ngl-body",
                    className="app-body",
                    children=[
                        tabs,
                        viewer,
                        # using dcc.Loading leads to remounting with every selection change
                        # dcc.Loading(viewer),
                    ],
                ),
            ],
        ),
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
            "uploaded": False,
            "selectedValue": selection,
            "chain": chain,
            "color": color,
            "filename": fname.split("/")[-1],
            "ext": fname.split(".")[-1],
            "config": {"type": "text/plain", "input": contents},
        }


# CB viewport
@app.callback(
    Output(component_id, "data"),
    [
        Input("pdb-dropdown", "value"),
        Input("ngl-upload-data", "contents"),
        Input("button", "n_clicks"),
    ],
    [State("pdb-string", "value")],
)
def display_output(selection, upload_content, n_clicks, value):
    data = []
    print(selection, n_clicks, value)

    if selection is None and value is None and upload_content is None:
        data.append(data_dict)

    if selection is not None and value is None and upload_content is None:
        pdb_id = selection
        data.append(getData(selection, pdb_id, color_list[0]))

    if value is not None and n_clicks > 0:
        if len(value) > 4:
            pdb_id = value
            if "_" in value:
                for i, pdb_id in enumerate(value.split("_")):
                    data.append(getData(value, pdb_id, color_list[i]))
            else:
                data.append(getData(value, pdb_id, color_list[0]))
        else:
            data.append(data_dict)

    if upload_content is not None:
        data = []
        print("upload not None")
        content_type, content_string = str(upload_content).split(",")
        decoded_contents = base64.b64decode(content_string).decode("UTF-8")
        pdb_id = decoded_contents.split("\n")[0].split()[-1]
        print(pdb_id)

        data.append(
            {
                "uploaded": True,
                "selectedValue": pdb_id,
                "chain": "ALL",
                "color": color_list[0],
                "filename": pdb_id + ".pdb",
                "ext": "pdb",
                "config": {"type": "text/plain", "input": decoded_contents},
            }
        )
    return data


# CB stage
@app.callback(
    Output(component_id, "stageParameters"),
    [
        Input("stage-bg-color", "value"),
        Input("stage-camera-type", "value"),
        Input("stage-render-quality", "value"),
    ],
)
def update_stage(bgcolor, camera_type, quality):
    return {
        "backgroundColor": bgcolor,
        "cameraType": camera_type,
        "quality": quality,
    }


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
