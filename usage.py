import dash_ngl
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

import json
import gzip

styleSheets_path="/assets/"
stylesheets = [
                 styleSheets_path+"svg.css",
               ]

app = dash.Dash(__name__)
#app = dash.Dash(__name__, external_stylesheets=stylesheets)

color_list=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00',
            '#ffff33','#a65628','#f781bf','#999999']

data_dict={
           'selectedValue':'placeholder',
           'chain':'ALL',
           'color':'#e41a1c',
           'filename':'placeholder',
           'ext':'',
           'config':{'type':'',
                     'input':''
                    }  
          }

pdbs_list=['5L73','4GWM','3L9P','5L73.A_4GWM.A_3L9P.A',
           '6CHG','3K8P','6CHG.A_3K8P.D'
          ]

def getData(value,chain,color,filename):

    ext = filename.split('.')[-1]
    with open(filename, 'r') as f:
        contents = f.read()

    return {
        'selectedValue':value,
        'chain':chain,
        'color':color,
        'filename': filename.split("/")[-1],
        'ext': ext,
        'config':{
            'type': 'text/plain',
            'input': contents
        }
    }

###Define app layout
label_width = 4
col_width = 8

styles={
    'tab':{'height':'calc(98vh - 115px)'}
}

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

##NGL viewer
viewer=html.Div([
            dash_ngl.DashNgl(
                    id='viewport',
                    data=data_dict
            )
        ],style={'display': 'inline-block',
                 'width': 'calc(100% - 500px)',
                 'float': 'left',
                 'marginTop': '50px',
                 'marginRight':'50px'
                }
        )

# ########################## ROOT LAYOUT ######################################
rootLayout=html.Div([
    #header
    html.Div(children=[html.H1("PStruc")],
             style = {'backgroundColor' : '#3aaab2','height':'7vh'}
             ),

    viewer,
    #if you use dcc.Loading viewer the app goes into a mount loop!
    # dcc.Loading(viewer),

    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Data', children=[

            # daq.ToggleSwitch(
            #     id='toggle-theme',
            #     label=['Light', 'Dark'],
            #     style={'width': '250px', 'margin': 'auto'}, 
            #     value=False
            # ),

            html.Div([
                dcc.Dropdown(
                    id='pdb-dropdown',
                    clearable=False,
                    options=[{'label': k, 'value': k } for k in pdbs_list],
                    placeholder='Select a molecule',
                )],
                style={'width': '100%', 'display': 'inline-block'}
            ), 
        ]),

        dcc.Tab(label='View', children=[
            html.Div(style=styles['tab'], children=[
                html.Div(["Camera settings"]),
                dcc.Dropdown(id='stage-camera-type',
                                options=[{'label': k.capitalize(), 'value': k} for k in ['perspective', 'orthographic']],
                                value='perspective'),
                
                html.Div(["Background"]), 
                dcc.Dropdown(id='stage-bg-color',
                                options=[{'label': c, 'value': c.lower()} for c in ['black','white']],
                                value='white')
            ])
        ]),
    ]),
])

# ################################# APP LAYOUT ################################
app.layout = html.Div(id='dark-theme-container',children=[
    html.Div(id='dark-theme-components', children=[
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ])
])

##CB viewport
@app.callback(Output('viewport', 'data'),
              [Input('pdb-dropdown', 'value')]
             )
def display_output(uniprot_id):
    
    print(uniprot_id) 
    color='#e41a1c'
    chain='ALL'
    data_list=[]

    if uniprot_id==None:
        data_list.append(data_dict)
    else:
        pdb_id = uniprot_id
        if "_" in pdb_id:
            for i,e in enumerate(pdb_id.split("_")):
                pdb_id,chain=e.split(".")
                data_list.append(getData(pdb_id,chain,color_list[i],"data/"+pdb_id+".pdb"))
        else:
            if "." in pdb_id:
                pdb_id,chain=uniprot_id.split(".")
            data_list.append(getData(pdb_id,chain,color,"data/"+pdb_id+".pdb"))

    return data_list
        
#CB stage
@app.callback(Output('viewport', 'stageParameters'),
              [Input('stage-bg-color', 'value'),
               Input('stage-camera-type', 'value')])
def update_stage(bgcolor, camera_type):
    return {'backgroundColor': bgcolor,
            'cameraType': camera_type,
            }

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)