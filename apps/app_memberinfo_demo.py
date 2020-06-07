import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import json
from datetime import datetime 

from app import app
from lib import lib_memberinfo


layout = html.Div(
    [
        html.H1(children = 'Employee Information'),

        html.Div(children = 'Full Name', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(
            id = 'mi_input_name', type = 'text', debounce = True,
            placeholder = 'Enter employee\'s name', style = {'display': 'inline-block'}
        ),
                    
        html.Div(children = 'Alias', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_alias', type = 'text', style = {'display': 'inline-block'}),
        html.Br(),

        html.Div(children = 'Email', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_email', type = 'text', style = {'display': 'inline-block'}),

        html.Div(children = 'Title', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_title', type = 'text', style = {'display': 'inline-block'}),

        html.Div(children = 'Position', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_position', type = 'text', style = {'display': 'inline-block'}),
        html.Br(),

        html.Div(children = 'Facebook', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_facebook', type = 'text', style = {'display': 'inline-block'}),

        html.Div(children = 'Phone', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_phone', type = 'text', style = {'display': 'inline-block'}),
        html.Br(),

        html.Div(children = 'CV', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_cv', type = 'text', style = {'display': 'inline-block'}),

        html.Div(children = 'Introducer', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_introducer', type = 'text', style = {'display': 'inline-block'}),
        html.Br(),

        html.Div(children = 'Start Date', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_startdate', type = 'text', style = {'display': 'inline-block'}),

        html.Div(children = 'Out Date', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_outdate', type = 'text', style = {'display': 'inline-block'}),

        html.Div(children = 'Min Hours', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_minhour', type = 'text', style = {'display': 'inline-block'}),
        html.Br(),

        html.Div(children = 'Wish', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_wish', type = 'text', style = {'display': 'inline-block'}),
                  
        html.Div(children = 'Ability', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_ability', type = 'text', style = {'display': 'inline-block'}),
                  
        html.Div(children = 'Excel Skill', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_excel', type = 'text', style = {'display': 'inline-block'}),   
        html.Br(),

        html.Div(children = 'Action', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_action', type = 'text', style = {'display': 'inline-block'}),
                  
        html.Div(children = 'Comment', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_comment', type = 'text', style = {'display': 'inline-block'}),          
        html.Br(),

        html.Div(children = 'Date Modified', style = {'display': 'inline-block', 'margin': 10}),
        dcc.Input(id = 'mi_datemodified', type = 'text', style = {'display': 'inline-block'}),              
        html.Br(),         
        
        html.Button('Submit', id = 'mi_button_submit', style = {'display': 'inline-block'}),          

        # Hidden div inside the app that stores the intermediate value
        html.Div(id = 'mi_json_memberinfo', style = {'display': 'none'}),
#        html.Div(id = 'mi_json_detail', style = {'display': 'none'}),

        html.Br(),
        dcc.Link('Go to Tempo Monitor', href = '/apps/app_tempomonitor'),                     
        html.Br(),
        dcc.Link('Go to Trading System', href='/apps/app2'),
        html.Br(),
        dcc.Link('Go back to Home', href='/')
    ],
    style = {'textAlign': 'center'}
)
        
        
@app.callback(
    Output('mi_button_submit', 'disabled'),
    [Input('mi_input_name', 'value')]
)
def update_tpm_button(name):
    if name is None or len(name) == 0:
        return True
    else:
        return False
    
    
@app.callback(
    [
        Output('mi_alias', 'value'),
        Output('mi_email', 'value'),
        Output('mi_title', 'value'),
        Output('mi_position', 'value'),
        Output('mi_facebook', 'value'),
        Output('mi_phone', 'value'),
        Output('mi_cv', 'value'),
        Output('mi_introducer', 'value'),
        Output('mi_startdate', 'value'),
        Output('mi_outdate', 'value'),
        Output('mi_minhour', 'value'),
        Output('mi_wish', 'value'),
        Output('mi_ability', 'value'),
        Output('mi_excel', 'value'),
        Output('mi_action', 'value'),
        Output('mi_comment', 'value'),
        Output('mi_datemodified', 'value')
    ],
    [Input('mi_input_name', 'value')]
)
def update_mi_memberinfo(name):
    if name is not None and len(name) > 0:
        df_memberinfo = lib_memberinfo.get_database(name.upper())

        if len(df_memberinfo) > 0:
            return df_memberinfo['ALIAS'][0], df_memberinfo['EMAIL'][0], df_memberinfo['TITLE'][0], df_memberinfo['FULLTIME_PARTTIME'][0], \
                   df_memberinfo['FACEBOOK'][0], df_memberinfo['PHONE'][0], df_memberinfo['CV'][0], df_memberinfo['INTRODUCER'][0], \
                   df_memberinfo['STARTDATE'][0], df_memberinfo['OUTDATE'][0], df_memberinfo['MINHOUR'][0], df_memberinfo['WISH'][0], \
                   df_memberinfo['ABILITY'][0], df_memberinfo['EXCEL'][0], df_memberinfo['ACTION'][0], df_memberinfo['COMMENT'][0], \
                   df_memberinfo['DATE_MODIFIED'][0]
                      
    return '', '', '', '', '', '', '', '', '', \
           '', '', '', '', '', '', '', ''
