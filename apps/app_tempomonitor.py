import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import json
from datetime import datetime 

from app import app
from lib import lib_tempo



layout = html.Div(
    [
        html.H1(children = 'Tempo Monitor'),

        html.Div(  
            [
                html.Div(children='Name', style = {'display': 'inline-block', 'marginRight': 10}),
                dcc.Input(
                    id = 'tpm_input_name', type = 'text',
                    placeholder = 'Enter employee\'s name', style = {'display': 'inline-block'}
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
                'width': 300,
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
                columns = [{'name': i, 'id': i} for i in ['WORKING_TIME', 'FREE_TIME']]),
                style = {'display': 'inline-block'}
        ),
                         
        html.H2(children = 'Detail'),
        dcc.Dropdown(
            id = 'tpm_ddown_detailtime',
            searchable = False,
            placeholder = 'Select time to review',
            style = {
                'width': 300,
                'display': 'inline-block',
                'verticalAlign': 'middle'
            }
        ),
        html.Div(id = 'tpm_text_result', style = {'padding': 10}),
                 
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
        html.Div(id = 'tpm_json_full', style = {'display': 'none'}),
        html.Div(id = 'tpm_json_detail', style = {'display': 'none'}),
        html.Br(),

        dcc.Link('Go to Employee Information', href = '/apps/app_memberinfo'),                     
        html.Br(),
        dcc.Link('Go to Trading System', href = '/apps/app2'),
        html.Br(),
        dcc.Link('Go back to Home', href = '/')
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
    Output('tpm_json_full', 'children'),
    [
        Input('tpm_input_name', 'value'),
        Input('tpm_date_check', 'date'),
    ]
)
def get_tpm_database(name, date):
    json_full = pd.DataFrame().to_json(orient = 'split', date_format = 'iso')

    if name is not None and len(name) > 0 and date is not None:
        json_full = lib_tempo.get_database(name, date)
                      
    return json_full
            

@app.callback(
    [
        Output('tpm_ddown_fulltime', 'options'),
        Output('tpm_ddown_fulltime', 'value')
    ],
    [Input('tpm_json_full', 'children')]
)
def update_tpm_ddown_fulltime(json_full):
    options = []
    value = None
    df_fulltime = pd.read_json(json_full, orient = 'split')
    
    if len(df_fulltime) > 0:
        options = [{'label': i, 'value': i} for i in df_fulltime['TIME']]
        value = df_fulltime['TIME'].values[0]
    
    return options, value
    

@app.callback(
    [
        Output('tpm_webcam', 'src'),
        Output('tpm_screen', 'src')
    ],
    [
        Input('tpm_json_full', 'children'),
        Input('tpm_ddown_fulltime', 'value')
    ]
)
def update_tpm_images_full(json_full, ddown_fulltime):
    df_fulltime = pd.read_json(json_full, orient = 'split')
    
    if len(df_fulltime) > 0:
        if ddown_fulltime is not None:
            webcam_b64 = df_fulltime.loc[df_fulltime['TIME'] == ddown_fulltime, 'WEBCAM'].values[0]
            screen_b64 = df_fulltime.loc[df_fulltime['TIME'] == ddown_fulltime, 'SCREEN'].values[0]

            return 'data:image/png;base64,{}'.format(webcam_b64), 'data:image/png;base64,{}'.format(screen_b64)
    else:
        return None, None
        
        
@app.callback(
    Output('tpm_json_detail', 'children'),
    [Input('tpm_button_run', 'n_clicks')],
    [State('tpm_json_full', 'children')]
)
def run_tpm_tempo(n_clicks, json_full):
    dict_detail = {}
    
    if n_clicks:
        df_detail = pd.read_json(json_full, orient = 'split')
        if len(df_detail) > 0:
            dict_detail = lib_tempo.get_detailresults(df_detail)
                      
    return json.dumps(dict_detail)
  
    
@app.callback(
    Output('tpm_dtable_time', 'data'),
    [Input('tpm_json_detail', 'children')]
)
def update_tpm_dtable_time(json_detail):
    df_time = pd.DataFrame()
    dict_detail = json.loads(json_detail)
    
    if len(dict_detail) > 0:
        df_time = pd.read_json(dict_detail['df_time'], orient = 'split', convert_dates = False)

    return df_time.to_dict('records')
    
    
@app.callback(
    [
        Output('tpm_ddown_detailtime', 'options'),
        Output('tpm_ddown_detailtime', 'value')
    ],
    [Input('tpm_json_detail', 'children')]
)
def update_tpm_ddown_detailtime(json_detail):
    options = []
    value = None
    dict_detail = json.loads(json_detail)
    
    if len(dict_detail) > 0:
        df_time = pd.read_json(dict_detail['df_time'], orient = 'split', convert_dates = False)
        
        if df_time.loc[0, 'FREE_TIME'] != '0:00:00':
            df_note = pd.read_json(dict_detail['df_note'], orient = 'split')
            options = [{'label': i, 'value': i} for i in df_note['TIME']]
            value = df_note['TIME'].values[0]
    
    return options, value 
    
    
@app.callback(
    Output('tpm_text_result', 'children'),
    [
        Input('tpm_json_detail', 'children'),
        Input('tpm_ddown_detailtime', 'value')
    ]
)
def update_tpm_text_result(json_detail, ddown_detailtime):
    note = None
    dict_detail = json.loads(json_detail)
    
    if len(dict_detail) > 0:
        df_note = pd.read_json(dict_detail['df_note'], orient = 'split')
        if ddown_detailtime is not None:
            note = df_note.loc[df_note['TIME'] == ddown_detailtime, 'TEXT_RESULT'].values[0]

    return note   
    
        
@app.callback(
    [
        Output('tpm_img_before', 'src'),
        Output('tpm_img_after', 'src')
    ],
    [
        Input('tpm_json_detail', 'children'),
        Input('tpm_ddown_detailtime', 'value')
    ]
)
def update_tpm_images_detail(json_detail, ddown_detailtime):
    img_before = None
    img_after = None
    dict_detail = json.loads(json_detail)
    
    if len(dict_detail) > 0:
        df_note = pd.read_json(dict_detail['df_note'], orient = 'split')
        if ddown_detailtime is not None:
            img_before_b64 = df_note.loc[df_note['TIME'] == ddown_detailtime, 'IMG_BEFORE'].values[0]
            img_after_b64 = df_note.loc[df_note['TIME'] == ddown_detailtime, 'IMG_AFTER'].values[0]

            img_before = 'data:image/png;base64,{}'.format(img_before_b64)
            img_after = 'data:image/png;base64,{}'.format(img_after_b64)

    return img_before, img_after




                        