import pickle
import pandas as pd
import numpy as np
from dash import Dash,dcc, html, Input, Output, dash_table
import plotly.express as px
import dash_daq as daq
import json


result = []
with (open("solutions.dat", "rb")) as openfile:
    while True:
        try:
            result.append(pickle.load(openfile))
        except EOFError:
            break

objective_num = list(result[0].keys())
print(objective_num[0])



objectives = ['overallocation','conflicts','undersupport','unwilling','unpreferred']



app = Dash(__name__)

app.layout = html.Div([
        # put section title on first graph
        html.H4('Northeastern TA Assignment',style={'font-size': '27px', 'textAlign': 'center'}),
        html.P('Evolution Framework'),
        # upload options

        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select TA file')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dcc.Dropdown(id='objective_x',
        options=objectives,clearable = False),
        dcc.Dropdown(id='objective_y',
        options=objectives,clearable = False),
        # ## 1. decide where to put all these/ 2. make the size larger /3. add instructions
        # dcc.Input(
        # id="run_time", type="number", placeholder="Input your expected run time for evo(in sec)",
        # min=5, max=600, step=3, size = '100'),
        # ## change the x and y axis

        dcc.Graph(id="scatter", style={'width':'60vw', 'height':'60vh'}),
])

@app.callback(
    Output("scatter", "figure"),
    Input("objective_x", "value"),
    Input("objective_y", "value"),
)


def data_selector(objective_x,objective_y):
    score_x = []
    score_y = []
    for ob_tu in range(len(objective_num)):
        for ob in range(len(objective_num[ob_tu])):
            if objective_num[ob_tu][ob][0] == objective_x:
                score_x.append(objective_num[ob_tu][ob][1])
            if objective_num[ob_tu][ob][0] == objective_y:
                score_y.append(objective_num[ob_tu][ob][1])
    fig = px.scatter(x = score_x, y = score_y)
    return fig



app.run_server(debug=True)

