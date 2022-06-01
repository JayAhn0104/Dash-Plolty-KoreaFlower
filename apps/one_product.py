import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
from app import app
import plot_fn as pf

# get relative data folder
PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../Deploy/datasets").resolve()
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfg = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr', index_col=0)
pum_list = sorted(dfg['pumName'].unique())
year_list = sorted(dfg['saleYear'].unique())
year_list.append('전체기간')
time_list_en = ['saleDate', 'Year_Month', 'saleMonth']
time_list_kr = ['일자별', '월별', '월별 합계']

layout = html.Div([
    html.H1('개별 품종의 거래정보', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="품종", style={"fontSize":"150%"}),
            dcc.Dropdown(
                id='input-1',
                options=[{'label': i, 'value': i} for i in pum_list],
                value=pum_list[0],
                clearable=False,
                persistence=True, persistence_type='session'
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="기간", style={"fontSize":"150%"}),
            dcc.Dropdown(
                id='input-3',
                options=[{'label': i, 'value': i} for i in year_list],
                value=year_list[-1],
                clearable=False,
                persistence=True, persistence_type='session'
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="시간 단위", style={"fontSize":"150%"}),
            dcc.RadioItems(
                id='input-2',
                options=[{'label': time_list_kr[i], 'value': time_list_en[i]} for i in range(0, len(time_list_en))],
                value='Year_Month',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '35%', 'display': 'inline-block'})

    ]),

    html.Div([
        dcc.Graph(
            id='out-fig-one'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'})

])

@app.callback(
    Output(component_id='out-fig-one', component_property='figure'),
    [Input(component_id='input-1', component_property='value'),
     Input(component_id='input-2', component_property='value'),
     Input(component_id='input-3', component_property='value')]
)
def update_graph(name, time_unit, year):
    a = pf.target_fn(dfg, name, time_unit, year)
    fig = a.plot_target(a.df_target(year))
    return fig

