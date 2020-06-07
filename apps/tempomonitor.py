import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import json
import os
from datetime import datetime, timedelta 

from app import app
from lib import tempo



layout = html.Div(
    [
        html.H1(children = 'Tempo Monitor'),

        html.Div(  
            [
                html.Div(children='Name', style = {'display': 'inline-block', 'marginRight': 10}),
                html.Div(
                    dcc.Input(id = 'tpm_input_name', type = 'text',
                              placeholder = 'Enter member\'s name'), style = {'display': 'inline-block'}
                ),
                              
                html.Div(children = 'Date', style = {'display': 'inline-block', 'marginLeft': 30, 'marginRight': 10}),
                dcc.DatePickerSingle(
                    id = 'tpm_date_check',
                    date = datetime.now().strftime("%Y-%m-%d"),
                    style = {'display': 'inline-block'}
                )
            ] 
        ),
        html.Br(),


        dcc.Dropdown(
            id = 'tpm_ddown_fulltime',
            searchable = False,
            placeholder = 'Select time to check',
            style = {
                'width': 500,
                'display': 'inline-block',
                'verticalAlign': 'middle'
            }
        ),
        html.Br(),

        html.Div(
            [
                html.Div(style = {'width': '30%', 'display': 'inline-block'}),
                html.Div(
                    [
                        html.H3(children = 'Webcam'),
                        html.Img(id = 'tpm_webcam', style = {'height': '90%', 'width': '90%', 'border': '2px black solid'})
                    ],
                    style = {'width': '20%', 'display': 'inline-block'}
                ),
                html.Div(
                    [
                        html.H3(children = 'Screen'),
                        html.Img(id = 'tpm_screen', style = {'height': '90%', 'width': '90%', 'border': '2px black solid'})
                    ],
                    style = {'width': '20%', 'display': 'inline-block'}
                ),
                html.Div(style = {'width': '30%', 'display': 'inline-block'}),
            ]
        ),
        html.Br(),                     
        html.Button('Run Check', id = 'tpm_button_run', style = {'display': 'inline-block'}),
        html.Br(),
        html.Div(
            dt.DataTable(id = 'tpm_dtable_time',
                         columns = [{'name': i, 'id': i} for i in ['Working Time', 'Free Time']]),
                         style = {'display': 'inline-block'}
        ),
                         
        html.H2(children = 'Detail'),
        dcc.Dropdown(
            id = 'tpm_ddown_reporttime',
            searchable = False,
            placeholder = 'Select time to review',
            style = {
                'width': 500,
                'display': 'inline-block',
                'verticalAlign': 'middle'
            }
        ),
        html.Div(id = 'tpm_text_note', style = {'padding': 10}),
                 
        html.Div(
            [
                html.Div(style = {'width': '30%', 'display': 'inline-block'}),
                html.Div(
                    [
                        html.H3(children = 'Before'),
                        html.Img(id = 'tpm_img_before',
                                 style = {'height': '90%', 'width': '90%', 'border': '2px black solid'})
                    ],
                    style = {'width': '20%', 'display': 'inline-block'}
                ),
                html.Div(
                    [
                        html.H3(children = 'After'),
                        html.Img(id = 'tpm_img_after',
                                 style = {'height': '90%', 'width': '90%', 'border': '2px black solid'})
                    ],
                    style = {'width': '20%', 'display': 'inline-block'}
                ),
                html.Div(style = {'width': '30%', 'display': 'inline-block'}),
            ]
         ),
 
         # Hidden div inside the app that stores the intermediate value
         html.Div(id = 'tpm_json_report', style = {'display': 'none'}),
                          
        html.Br(),
        dcc.Link('Go to Trading System', href='/apps/app2'),
        html.Br(),
        dcc.Link('Go back to Home', href='/')
    ],
    style = {'textAlign': 'center'}
)

                        
@app.callback(
    Output('tpm_button_run', 'disabled'),
    [
        Input('tpm_input_name', 'value'),
        Input('tpm_date_check', 'date'),
    ]
)
def update_tpm_button(name, date):
    if name is None or len(name) == 0 or date is None:
        return True
    else:
        return False


@app.callback(
    Output('tpm_json_report', 'children'),
    [
        Input('tpm_input_name', 'value'),
        Input('tpm_date_check', 'date'),
    ]
)
def get_tpm_database(name, date):
    json_data = pd.DataFrame().to_json(orient = 'split', date_format = 'iso')

    if name is not None and len(name) > 0 and date is not None:
        json_data = tempo.get_database(name, date)
                      
    return json_data
            

@app.callback([Output('tpm_ddown_fulltime', 'options'), Output('tpm_ddown_fulltime', 'value')],
              [Input('tpm_json_report', 'children')])
def update_tpm_ddown_fulltime(json_data):
    options = []
    value = None
    df_fulltime = pd.read_json(json_data, orient = 'split')
    
    if len(df_fulltime) > 0:
        options = [{'label': i, 'value': i} for i in df_fulltime['TIME']]
        value = df_fulltime['TIME'].values[0]
    
    return options, value
    

@app.callback([Output('tpm_webcam', 'src'), Output('tpm_screen', 'src')],
              [Input('tpm_json_report', 'children'), Input('tpm_ddown_fulltime', 'value')])
def update_image_src(json_data, fulltime_value):
    df_fulltime = pd.read_json(json_data, orient = 'split')
    
    if len(df_fulltime) > 0:
        if fulltime_value is not None:
            webcam_b64 = df_fulltime.loc[df_fulltime['TIME'] == fulltime_value, 'WEBCAM'].values[0]
            screen_b64 = df_fulltime.loc[df_fulltime['TIME'] == fulltime_value, 'SCREEN'].values[0]

            return 'data:image/png;base64,{}'.format(webcam_b64), 'data:image/png;base64,{}'.format(screen_b64)
    else:
        return None, None
    
    
#@app.callback(
#    Output('tpm_json_report', 'children'),
#    [Input('tpm_button_run', 'n_clicks')],
#    [
#        State('tpm_input_name', 'value'),
#        State('daterange', 'date')
#    ]
#)
#def run_tpm_tempo(n_clicks, name, date):
#    report_dict = {}
#    
#    if n_clicks:
#        time_report_df, detail_report_df = tempo.check_images(name, date)
#        report_dict = {
#            'time_report_df': time_report_df.to_json(orient = 'split', date_format = 'iso'),
#            'detail_report_df': detail_report_df.to_json(orient = 'split', date_format = 'iso'),
#              }
#                      
#    return json.dumps(report_dict)
    
    
    
    
    
                        