import dash_ngl
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

import json
import gzip

import dash_bio as dashbio
import six.moves.urllib.request as urlreq

##This goes in a mount loop

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

needle_dict={
             'x':[],
             'y':[],
             'mutationGroups':[],
             'domains':[],
}

pdbs_list=['5L73','4GWM','3L9P','5L73.A_4GWM.A_3L9P.A',
           '6CHG','6CHG.A','3K8P','6CHG.A_3K8P.D'
          ]

needle_test = urlreq.urlopen(
 "https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/" + 
 "needle_PIK3CA.json"
).read()

mdata_needle = json.loads(needle_test)
print(mdata_needle)

alignment_test = urlreq.urlopen(
    'https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/' +
    'alignment_viewer_p53.fasta'
).read().decode('utf-8')

alignment_test=alignment_test.split(">")[:4]
alignment_test=">".join(alignment_test)
print (alignment_test)


path="/net/home.isilon/ag-russell/bq_gdiwan/projects/repeats/hhblits/pfam_vs_pdb/genome_hhblits/HUMAN/"
pdbs_pf=path+"100_ptns_json_long_names.json"

###Custom Functions
def createProteinDict():
    with open (pdbs_pf,'r') as f:
        data=json.load(f)

    proteins_dict={ k.split("| ")[0].strip():data[k] for k in data }
    proteins_list=[p for p in data]
    
    return proteins_dict,proteins_list

def getData(value,chain,color,filename,gzip_bool):

    if gzip_bool==True:
        ext="cif"
        with gzip.open(filename, 'r') as f:
            contents = f.read().decode("utf-8")
    else:
        ext = filename.split('.')[-1]
        with open(filename, 'r') as f:
            contents = f.read()

    # print (type(contents))

    # print (ext)

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

proteins_dict,proteins_list=createProteinDict()
print (proteins_dict)

dropdown_list=[{'label': k, 'value': k } for k in pdbs_list]
dropdown_list=dropdown_list+[{'label': k,'value': k.split("|")[0].strip()} for k in proteins_list]
#print("start dropdown list")
#print (dropdown_list)
#print("stop dropdown list")

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

##needle_plot
needle_plot=html.Div([
    	        dashbio.NeedlePlot(
                    id='dashbio-needleplot',
                    mutationData=mdata_needle,
                    domainStyle={
                        'displayMinorDomains': True,
                        'domainColor': color_list
                    }

              ),
            ],style={'display': 'inline-block',
                 'width': 'calc(100% - 500px)',
                 'float': 'left',
                 'textAlign':'center',
                 'marginTop': '50px',
                 'marginRight':'50px'
                }
            )

##alignment_plot
alignment_plot=html.Div([
                    dashbio.AlignmentChart(
                        id='my-alignment-viewer',
                        data=alignment_test,
                        tilewidth=50,
                        showconservation=True,
                        showgap=True,
                        showconsensus=True,

                    ),
                    html.Div(id='alignment-viewer-output')
                ],style={'display': 'inline-block',
                 'width': 'calc(100% - 500px)',
                 'float': 'left',
                 'textAlign':'center',
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
                    options=dropdown_list,
                    #     [
                    #     {'label': k, 
                    #      'value': k.split("|")[0].strip()
                    #     } for k in proteins_list
                    # ],
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
        dcc.Tab(label='DEBUG', children=[
            html.Div(style=styles['tab'], children=[
                html.P("Orientation Matrix:"),
                html.Button("get current orientation",id="get-orientation-button"),
                html.Pre(
                    id='orientation-matrix-json-output',
                )
            ])
        ]),
    ]),
    needle_plot,
    alignment_plot
])

# ################################# APP LAYOUT ################################
app.layout = html.Div(id='dark-theme-container',children=[
    html.Div(id='dark-theme-components', children=[
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ])
])

#'''
##CB viewport
@app.callback([Output('viewport', 'data'),
               Output('dashbio-needleplot','mutationData')],
              [Input('pdb-dropdown', 'value')])
def display_output(uniprot_id):
    
    needle_dict={
             'x':[],
             'y':[],
             'mutationGroups':[],
             'domains':[],
            } 
    
    
    print(uniprot_id) 
    chain='ALL'
    data_list=[]

    except_bool=False

    if uniprot_id ==None:
        data_list.append(data_dict)
    else:
        if uniprot_id in proteins_dict:
            gzip_bool=True

            pdb_list=proteins_dict[uniprot_id]['pdb']
            coords_list=proteins_dict[uniprot_id]['coords']

            print (pdb_list)
            print (coords_list)

            for i,pdb in enumerate(pdb_list):
                print(i,pdb)
                color=color_list[i]
                print (color)

                coord=coords_list[i]

                needle_dict['x'].append(coord)
                needle_dict['y'].append(1)
                needle_dict['mutationGroups'].append('Domain')
                needle_dict["domains"].append({'name':pdb,'coord':coord})

                if "." in pdb:
                    pdb_id,chain=pdb.split(".")
                else:
                    pdb_id=pdb

                #change to CIF
                pf="/net/home.isilon/ds-russell/pdb-cif/"+pdb_id[1:3].lower()+"/"+pdb_id.lower()+".cif.gz"
                #pf="/net/home.isilon/ds-russell/pdb-biounit/"+pdb_id[1:3].lower()+"/"+pdb_id.lower()+".pdb1.gz"
                print(pf)
                
                #check if pdb is there
                try:
                    data_list.append(getData(pdb_id,chain,color,pf,gzip_bool))
                    print(pf," - try successful")
                except:
                    print(pf," - except")
                    except_bool = True
                    pass
                    # data_list.append([data_dict])
        else:
            color='#e41a1c'
            gzip_bool=False
            print ("HERE")
            pdb_id = uniprot_id
            if "_" in pdb_id:
                for e in pdb_id.split("_"):
                    pdb_id,chain=e.split(".")
                    data_list.append(getData(pdb_id,chain,color,"data/"+pdb_id+".pdb",gzip_bool))
            else:
                if "." in pdb_id:
                    pdb_id,chain=uniprot_id.split(".")
                data_list.append(getData(pdb_id,chain,color,"data/"+pdb_id+".pdb",gzip_bool)) 
    
    if except_bool==True:
        print ("except bool==True")
        data_list=[data_dict]

    print (needle_dict)
    
    return data_list,needle_dict
        
#CB stage
@app.callback(Output('viewport', 'stageParameters'),
              [Input('stage-bg-color', 'value'),
               Input('stage-camera-type', 'value')])
def update_stage(bgcolor, camera_type):
    return {'backgroundColor': bgcolor,
            'cameraType': camera_type,
            }

@app.callback(Output('orientation-matrix-json-output', 'children'),
              [Input('get-orientation-button', 'n_clicks'),
               Input('viewport','stageParameters')])
def update_stage(clicks,params):
    if clicks!=None:
        return json.dumps(params, indent=2)
#'''

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)