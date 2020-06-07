import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H1('App 2'),
    dcc.RadioItems(
        id = 'app-2-radios',
        options = [{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value = 'Orange'
    ),
    html.Div(id = 'app-2-content'),
    html.Br(),
    dcc.Link('Go to Tempo Monitor', href = '/apps/app_tempomonitor'),
    html.Br(),
    dcc.Link('Go to Employee Information', href = '/apps/app_memberinfo'),   
    html.Br(),
    dcc.Link('Go back to Home', href = '/')
])


@app.callback(Output('app-2-content', 'children'),
              [Input('app-2-radios', 'value')])
def app_2_radios(value):
    return 'You have selected "{}"'.format(value)