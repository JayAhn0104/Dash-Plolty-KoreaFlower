import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
from app import app
from target_fn import target_fn


# get relative data folder
PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../Deploy/datasets").resolve()
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfg = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr')
pum_list = sorted(dfg['pumName'].unique())
year_list = sorted(dfg['saleYear'].unique())
year_list.append('전체기간')
time_list_en = ['saleDate', 'Year_Month', 'saleMonth']
time_list_kr = ['일자별', '월별', '월별 합계']

layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='input-1',
                options=[{'label': i, 'value': i} for i in pum_list],
                value=pum_list[0]
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='input-3',
                options=[{'label': i, 'value': i} for i in year_list],
                value=year_list[-1]
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.RadioItems(
                id='input-2',
                options=[{'label': time_list_kr[i], 'value': time_list_en[i]} for i in range(0, len(time_list_en))],
                value='Year_Month',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ],
            style={'width': '49%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(
            id='out-fig'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'})
])

@app.callback(
    Output(component_id='out-fig', component_property='figure'),
    [Input(component_id='input-1', component_property='value'),
     Input(component_id='input-2', component_property='value'),
     Input(component_id='input-3', component_property='value')]
)
def update_graph(name, time_unit, year):
    a = target_fn(dfg, name, time_unit, year)
    fig = a.plot_target(a.df_target(year))
    return fig

