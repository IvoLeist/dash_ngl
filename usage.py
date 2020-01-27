import dash_ngl
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

data_dict={'filename':'placeholder',
           'ext':'',
           'config':{'type':'',
                     'input':''
                    }  
          } 

def getData(filename):
    with open(filename, 'r') as f:
        contents = f.read()

    ext = filename.split('.')[-1]
    return {
        'filename': filename.split("/")[-1],
        'ext': ext,
        'config':{
            'type': 'text/plain',
            'input': contents
        }
    }

app.layout = html.Div([
    dash_ngl.DashNgl(
        id='viewport',
        data=data_dict
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[
            #to be added
            {'label': 'Penicillin Acylase', 'value': '1PNK'},
            {'label': '4GWM', 'value': '4GWM'}, 
            {'label': '6REG', 'value': '6REG'},
    ],
    placeholder="Select a molecule",
    ),
])

@app.callback(Output('viewport', 'data'), 
             [Input('dropdown', 'value')])
def display_output(value):
    print(value)
    if value==None:
        return data_dict
    else:
        print ("getData")
        return getData('data/'+value+'.pdb')

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)