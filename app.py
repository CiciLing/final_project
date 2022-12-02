import pickle
import pandas as pd
import numpy as np
from dash import Dash,dcc, html, Input, Output, dash_table
import plotly.express as px
import dash_daq as daq
import json


with open('solutions.dat', 'rb') as file:
        result = pickle.load(file)
        print(result)


app = Dash(__name__)

# fig = px.scatter()
# app.layout = html.Div([
#         # put section title on first graph
#         html.H4('Northeastern TA Assignment',style={'font-size': '27px', 'textAlign': 'center'}),
#         html.P('Evolution Framework'),
#         # upload options
#         html.Div([
#         dcc.Upload(
#             id='upload-data',
#             children=html.Div([
#                 'Drag and Drop or ',
#                 html.A('Select TA file')
#             ]),
#             style={
#                 'width': '100%',
#                 'height': '60px',
#                 'lineHeight': '60px',
#                 'borderWidth': '1px',
#                 'borderStyle': 'dashed',
#                 'borderRadius': '5px',
#                 'textAlign': 'center',
#                 'margin': '10px'
#             },
#             # Allow multiple files to be uploaded
#             multiple=True
#         ),
#         html.Div(id='output-data-upload'),
#     ]),
#
#         # ## 1. decide where to put all these/ 2. make the size larger /3. add instructions
#         # dcc.Input(
#         # id="run_time", type="number", placeholder="Input your expected run time for evo(in sec)",
#         # min=5, max=600, step=3, size = '100'),
#         # ## change the x and y axis
#
#         dcc.Graph(id="scatter-plot", style={'width':'60vw', 'height':'60vh'}, figure=fig),
#         daq.Slider(id='df_row', min=0, max=len(result), size = 1000, value = 10)
# ])
#
#
#
#
# def data_selector(df):
#     columns=df.columns
#     data_options= [{'label' :k, 'value' :k} for k in columns]
#     return dcc.Dropdown(
#         id='selector',
#         options=data_options,
#
#
#
# app.run_server(debug=True)
#
