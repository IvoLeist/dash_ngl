from base64 import b64decode
import glob
import gzip
import zlib

import dash_ngl
import dash
from dash.dependencies import Input, Output, State
from dash.dash import no_update

import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)
app.css.config.serve_locally = True

# Preset colors for the shown molecules
color_list = [
    '#e41a1c',
    '#377eb8',
    '#4daf4a',
    '#984ea3',
    '#ff7f00',
    '#ffff33',
    '#a65628',
    '#f781bf',
    '#999999',
]

# PDB examples
# . indicates that only one chain should be shown
# _ indicates that more than one protein should be shown
pdbs_list = [
    '1PNK',
    '1KMQ',
    '5L73',
    '4GWM',
    '3L9P',
    '6CHG',
    '3K8P',
    '2MRU',
    '1BNA',
    '6NZK',
    '6OHW',
]

# Placeholder which is loaded if no molecule is selected
data_dict = {
    'uploaded': False,
    'selectedValue': 'placeholder',
    'resetView': False,
    'chain': 'ALL',
    'color': '#e41a1c',
    'filename': 'placeholder',
    'ext': '',
    'config': {'type': '', 'input': ''},
}


# Canvas container to display the structures
component_id = 'nglViewer'
viewer = html.Div(
    id='ngl-biomolecule-viewer',
    children=[dash_ngl.DashNgl(id=component_id, data=[data_dict])],
)

about_html = [
    html.H4(className='what-is', children='What is Ngl Molecule Viewer?',),
    html.P(
        'Ngl Molecule Viewer is a visualizer that allows you'
        'to view biomolecules in multiple representations:'
        'sticks, spheres, and cartoons.'
    ),
    html.P(
        'You can select a preloaded structure, or upload your own,'
        'in the "Data" tab. A sample structure is also'
        'available to download.'
    ),
    html.P('Additionally you can show multiple structures and/or ' 'specify a chain'),
    html.P(
        'In the "View" tab, you can change the style and'
        'coloring of the various components of your molecule.'
    ),
]

data_tab = [
    html.Div(className='app-controls-name', children='Select structure',),
    dcc.Dropdown(
        id='pdb-dropdown',
        clearable=False,
        options=[{'label': k, 'value': k} for k in pdbs_list],
        value='1BNA',
        placeholder='placeholder'
    ),
    html.Div(
        className='app-controls-name',
        children='Show multiple structures & specify a chain',
    ),
    dcc.Input(id='pdb-string', placeholder='pdbID1.chain_pdbID2.chain',),
    html.Button('submit', id='btn-pdbString'),
    html.Button('reset view', id='btn-resetView'),

    html.Div(
        title='Upload biomolecule to view here',
        className='app-controls-block',
        id='ngl-upload-container',
        children=[
            dcc.Upload(
                id='ngl-upload-data',
                className='control-upload',
                children=html.Div(
                    ['Drag and drop or click to upload (multiple) pdb/cif file(s).',]
                ),
                # Allow multiple files to be uploaded
                multiple=True,
            ),
            html.Div(id='uploaded-files', children=html.Div([''])),
            html.Div(id='warning_div', children=html.Div(['']))
        ],
    ),
    html.Div(id='ngl-data-info'),
]

view_tab = [
    html.Div(
        title='select chain color',
        className='app-controls-block',
        id='ngl-mols-color',
        children=[
            html.P(
                'Chain colors',
                style={'font-weight': 'bold', 'margin-bottom': '10px',},
            ),
            dcc.Input(
                id='molecules-chain-color',
                value=','.join(color_list),
            ),
        ],
    ),
    html.Div(
        title='select background color',
        className='app-controls-block',
        id='ngl-style-color',
        children=[
            html.P(
                'Background color',
                style={'font-weight': 'bold', 'margin-bottom': '10px',},
            ),
            dcc.Dropdown(
                id='stage-bg-color',
                options=[
                    {'label': c, 'value': c.lower()} for c in ['black', 'white',]
                ],
                value='white',
            ),
        ],
    ),
    html.Div(
        title='Camera settings',
        className='app-controls-block',
        id='ngl-selection-display',
        children=[
            html.P(
                'Camera settings',
                style={'font-weight': 'bold', 'margin-bottom': '10px',},
            ),
            dcc.Dropdown(
                id='stage-camera-type',
                options=[
                    {'label': k.capitalize(), 'value': k,}
                    for k in ['perspective', 'orthographic',]
                ],
                value='perspective',
            ),
        ],
    ),
    html.Div(
        title='select render quality',
        className='app-controls-block',
        id='ngl-style',
        children=[
            html.P(
                'Render quality',
                style={'font-weight': 'bold', 'margin-bottom': '10px',},
            ),
            dcc.Dropdown(
                id='stage-render-quality',
                options=[
                    {'label': c, 'value': c.lower(),}
                    for c in ['auto', 'low', 'medium', 'high',]
                ],
                value='auto',
            ),
        ],
    ),
]

tabs = html.Div(
    id='ngl-control-tabs',
    className='control-tabs',
    children=[
        dcc.Tabs(
            id='ngl-tabs',
            value='what-is',
            children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='control-tab', children=about_html),
                ),
                dcc.Tab(
                    label='Data',
                    value='upload-select',
                    children=html.Div(className='control-tab', children=data_tab),
                ),
                dcc.Tab(
                    label='View',
                    value='view-options',
                    children=[html.Div(className='control-tab', children=view_tab)],
                ),
            ],
        ),
    ],
)

# LAYOUT
app.layout = html.Div(
    id='main-page',
    children=[
        html.Div(
            id='app-page-header',
            children=[html.H1('Ngl Molecule Viewer')],
            style={'background': '#e7625f', 'color': 'white'},
        ),
        html.Div(
            id='app-page-content',
            children=[
                html.Div(
                    id='ngl-body',
                    className='app-body',
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


def createDict(selection, chain, color, filename, ext, contents, resetView=False, uploaded=False):
    return {
        'filename': filename,
        'ext': ext,
        'selectedValue': selection,
        'chain': chain,
        'color': color,
        'config': {'type': 'text/plain', 'input': contents},
        'resetView': resetView,
        'uploaded': uploaded,
    }


# Helper function to load structures from local storage
def getLocalData(selection, pdb_id, color, uploadedFiles, resetView=False):

    chain = 'ALL'

    # Check if only one chain should be shown
    if '.' in pdb_id:
        pdb_id, chain = pdb_id.split('.')

    if pdb_id not in pdbs_list:
        if pdb_id in uploadedFiles:
            print('Already uploaded')
            # print(files[:-1].split(','))
            fname = [i for i in uploadedFiles[:-1].split(',') if pdb_id in i][0]
            print(fname)

            content = ''
            return createDict(
                selection,
                chain,
                color,
                fname,
                fname.split('.')[1],
                content,
                resetView,
                uploaded=False,
            )
        return data_dict

    # get path to protein structure
    fname = [f for f in glob.glob('data/' + pdb_id + '.*')][0]

    if "gz" in fname:
        ext = fname.split('.')[-2] 
        with gzip.open(fname, 'r') as f:
            content = f.read().decode('UTF-8')
    else:
        ext = fname.split('.')[-1]
        with open(fname, 'r') as f:
            content = f.read()

    filename = fname.split('/')[-1]

    return createDict(
        selection, chain, color, filename, ext, content, resetView, uploaded=False
    )


# Helper function to load structures from uploaded content
def getUploadedData(uploaded_content):
    data = []
    uploads = []

    ext = 'pdb'
    chain = 'ALL'

    for i, content in enumerate(uploaded_content):
        content_type, content = str(content).split(',')
        print (content_type)
        #print (content_string)

        if "gzip" in content_type:
            print ("gzip")
            content = zlib.decompress(
                b64decode(content),
                zlib.MAX_WBITS | 16
            )
        else:
            content = b64decode(content)

        content = content.decode('UTF-8')

        pdb_id = content.split('\n')[0].split()[-1]
        if 'data_' in pdb_id:
            pdb_id = pdb_id.split('_')[1]
            ext = 'cif'
        print(pdb_id)

        filename = pdb_id + '.' + ext
        uploads.append(filename)

        data.append(
            createDict(
                pdb_id,
                chain,
                color_list[i],
                filename,
                ext,
                content,
                resetView=False,
                uploaded=True,
            )
        )

    return data, uploads


# CB viewport
@app.callback(
    [
        Output(component_id, 'data'),
        Output('pdb-dropdown', 'options'),
        Output('uploaded-files', 'children'),
        Output('pdb-dropdown', 'placeholder'),
        Output('warning_div', 'children') 
    ],
    [
        Input('pdb-dropdown', 'value'),
        Input('ngl-upload-data', 'contents'),
        Input('btn-pdbString', 'n_clicks'),
        Input('btn-resetView', 'n_clicks'),
    ],
    [
        State('pdb-string', 'value'),
        State('pdb-dropdown', 'options'),
        State('uploaded-files', 'children'),
        State('molecules-chain-color', 'value'),
    ],
)
def display_output(
    selection, uploaded_content, pdbString_clicks, resetView_clicks, pdbString, dropdown_options, files, colors
):
    print('selection,pdbString_clicks,pdbString,type uploaded_content', 'files')
    print(selection, pdbString_clicks, pdbString, type(uploaded_content), type(files))

    input_id = None
    options = dropdown_options
    colors_list = colors.split(',')
    files = files['props']['children'] if isinstance(files, dict) else ''.join(files)
    print(files)

    ctx = dash.callback_context
    if ctx.triggered:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    print('triggred', input_id)

    if input_id is None:
        return [data_dict], options, files, no_update, no_update

    if input_id == 'pdb-dropdown':
        print('dropdown changed')
        print(files)
        pdb_id = selection

        if pdb_id in files:
            print('Already uploaded')
            print(files[:-1].split(','))
            fname = [i for i in files[:-1].split(',') if pdb_id in i][0]
            print(fname)

            content = ''
            chain = 'ALL'
            return (
                [
                    createDict(
                        pdb_id,
                        chain,
                        colors_list[0],
                        fname,
                        fname.split('.')[1],
                        content,
                        resetView=False,
                        uploaded=False,
                    )
                ],
                options,
                files,
            )

        data = [getLocalData(selection, pdb_id, color_list[0], files, resetView=False)]
        return data, options, files, no_update, no_update

    # TODO submit and reset view in one button
    if input_id in ['btn-pdbString', 'btn-resetView']:
        warning = ''

        if pdbString is None:
            return no_update, no_update, no_update, no_update, no_update

        resetView = False
        if input_id == 'btn-resetView':
            resetView = True

        data = []
        if len(pdbString) > 3:
            pdb_id = pdbString
            if '_' in pdbString:
                for i, pdb_id in enumerate(pdbString.split('_')):
                    if i <= len(colors_list)-1:
                        data.append(getLocalData(
                            pdbString, pdb_id, color_list[i], files, resetView=resetView))
                    else:
                        data.append(data_dict)
                        warning = 'more molecules selected as chain colors defined \
                                   either remove one molecule or add a extra color in the view tab \
                                   and reset view before submitting it again.'
                        return data, options, files, no_update, warning
            else:
                data.append(getLocalData(
                    pdbString, pdb_id, color_list[0], files, resetView=resetView))
        else:
            data.append(data_dict)

        return data, options, files, 'Select a molecule', warning

    if input_id == 'ngl-upload-data':
        data, uploads = getUploadedData(uploaded_content)

        for pdb_id, ext in [e.split('.') for e in uploads]:
            if pdb_id not in [e['label'] for e in options]:
                options.append({'label': pdb_id, 'value': pdb_id})
                print('uploaded', pdb_id)
                files += pdb_id + '.' + ext + ','

        return data, options, files, pdb_id, no_update


# CB stage
@app.callback(
    Output(component_id, 'stageParameters'),
    [
        Input('stage-bg-color', 'value'),
        Input('stage-camera-type', 'value'),
        Input('stage-render-quality', 'value'),
    ],
)
def update_stage(bgcolor, camera_type, quality):
    return {
        'backgroundColor': bgcolor,
        'cameraType': camera_type,
        'quality': quality,
    }

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8051)
