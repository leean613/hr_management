import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import json
from datetime import datetime 

from app import app
from lib import lib_memberinfo


#Init
df_memberinfo = lib_memberinfo.get_database()

layout = html.Div(
    [
        html.H1(children = 'Employee Information'),
#        html.Div([
#            html.Div(children = 'Select Status', style = {'display': 'inline-block', 'margin': 10}),
#            dcc.Dropdown(
#                id = 'mi_ddown_status',
#                searchable = False,
#                options = [{'label': i, 'value': i} for i in ['dealing', 'temp', 'in', 'pending', 'out']],
#                value = 'in',
#                style = {
#                    'width': 150,
#                    'display': 'inline-block',
#                    'verticalAlign': 'middle'
#                }
#            ),
#            html.Button('Get data', id = 'mi_button_get', style = {'display': 'inline-block', 'marginLeft': 30}), 
#        ]),
#        html.Br(), 

        dt.DataTable(
            id = 'mi_table_info',
            columns = [{'name': i, 'id': i} for i in df_memberinfo.columns],
            data = df_memberinfo.to_dict('records'),
            editable = True,
            row_deletable = True,
            style_cell = {
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            tooltip_data = [
                {
                    column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()
                } for row in df_memberinfo.to_dict('rows')
            ],
            tooltip_duration = None
            ),
        html.Br(),         
        
        html.Button('Update', id = 'mi_button_update', style = {'display': 'inline-block', 'marginBottom': 100}),          

        # Hidden div inside the app that stores the intermediate value
        html.Div(id = 'mi_json', style = {'display': 'none'}),
#        html.Div(id = 'mi_json_detail', style = {'display': 'none'}),
        html.Br(),

        dcc.Link('Go to Tempo Monitor', href = '/apps/app_tempomonitor'),                     
        html.Br(),
        dcc.Link('Go to Trading System', href = '/apps/app2'),
        html.Br(),
        dcc.Link('Go back to Home', href = '/')
    ],
    style = {'textAlign': 'center'}
)
    
    
#@app.callback(
#    [
#        Output('mi_table_info', 'data'),
#        Output('mi_table_info', 'tooltip_data')
#    ],
#    [Input('mi_button_get', 'n_clicks')],
#    [
#        State('mi_ddown_status', 'value'),
#        State('mi_table_info', 'data'),
#        State('mi_table_info', 'tooltip_data')
#    ]
#)
#def get_table_info(n_clicks, status, data, tooltip_data):
#    if n_clicks:
#        df_newinfo = lib_memberinfo.get_database(status)
#        data = df_newinfo.to_dict('records')
#        tooltip_data = [
#            {
#                column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()
#            } for row in df_newinfo.to_dict('rows')
#        ]
#
#    return data, tooltip_data

    
    
    
    
    
    