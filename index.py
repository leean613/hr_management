import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from app import app
from apps import app_tempomonitor, app_memberinfo, app2
from lib import lib_tempo



app.layout = html.Div([
    dcc.Location(id = 'index_url', refresh = False),
    html.Div(id = 'index_page_content')
])

index_layout = html.Div(
    [
        html.H1(children = 'qT-Tools'),
        html.Div(
            [
                html.Div(children = 'Username', style = {'width': 100, 'display': 'inline-block'}),
                html.Div(
                    dcc.Input(id = 'index_input_name', type = 'text', debounce = True, 
                              placeholder = 'Enter your name here.'), style = {'display': 'inline-block'}
                ),
                html.Div(children = 'Total Time', style = {'width': 100, 'display': 'inline-block'}),
                html.Div(
                    dcc.Input(id = 'index_input_totaltime', type = 'number'), style = {'display': 'inline-block'}
                ),
            ],
            style = {'margin-bottom': 10}
        ),
                           
        daq.BooleanSwitch(id = 'index_bswitch_start', on = False, color  = '#8ed62f', disabled = True, 
                          label = ['OFF', 'ON'], style = {'width': '50px', 'margin': 'auto'}),
        html.Div(id = 'index_text_name', style = {'padding': 10}),
        
        html.Br(),
        dcc.Link('Tempo Monitor', href = '/apps/app_tempomonitor'),
        html.Br(),
        dcc.Link('Employee Infomation', href = '/apps/app_memberinfo'),
        html.Br(),
        dcc.Link('Trading System', href = '/apps/app2'),
        #Hidden div inside the app that stores the intermediate value
        html.Div(id = 'index_hidden_div', style = {'display': 'none'}),
                                      
    ],
    style = {'textAlign': 'center'}
)


@app.callback(Output('index_page_content', 'children'),
              [Input('index_url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app_tempomonitor':
        return app_tempomonitor.layout
    elif pathname == '/apps/app_memberinfo':
        return app_memberinfo.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return index_layout
        
        
@app.callback(
    Output('index_bswitch_start', 'disabled'),
    [
        Input('index_input_name', 'value'),
        Input('index_input_totaltime', 'value')
    ]
)
def update_bswitch_start(username, totaltime):
    if username is None or len(username) == 0 or totaltime is None or totaltime < 1:
        return True
    else:
        return False
    

@app.callback(
    [
        Output('index_text_name', 'children'),
        Output('index_input_name', 'disabled')
    ],
    [Input('index_bswitch_start', 'on')],
    [State('index_input_name', 'value')]
)
def update_status(on, username):
    if username is None or len(username) == 0:
        return 'Enter your name and working time in hours.', False
    else:
        if on is True:            
            return 'Hi {}. Tempo is ON.'.format(username), True
        else:   
            return 'Goodbye {}. Tempo is OFF.'.format(username), False


@app.callback(
    Output('index_hidden_div', 'children'),
    [Input('index_bswitch_start', 'on')],
    [
        State('index_input_name', 'value'),
        State('index_input_totaltime', 'value')
    ]
)
def run_tempomonitor(on, username, totaltime):
    if on is True:
        totalsecs = totaltime * 3600
        lib_tempo.run_tempomonitor(username, totalsecs)

    return None
    

if __name__ == '__main__':
    app.run_server(debug = True)