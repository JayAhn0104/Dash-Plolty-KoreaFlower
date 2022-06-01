import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
from app import app
import plot_fn as pf
import plotly.express as px

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfg = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr', index_col=0)
time_list_en = ['saleYear', 'Year_Month', 'saleMonth']
time_list_kr = ['년도별', '월별', '월별 합계']
year_month_df = dfg.groupby(['saleYear', 'saleMonth'])[['totAmt', 'totQty', 'avgAmt', 'saleYear', 'saleMonth']].sum()
year_unique = year_month_df.index.get_level_values(0).unique()
for year in year_unique:
    year_month_df.loc[year]['saleYear'] = year
    year_month_df.loc[year]['saleMonth'] = list(range(1, year_month_df.loc[year].shape[0] + 1))

layout = html.Div([
    html.H1('전체 시장의 거래정보', style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Pre(children="시간 단위", style={"fontSize": "150%"}),
            dcc.RadioItems(
                id='input-timeunit',
                options=[{'label': time_list_kr[i], 'value': time_list_en[i]} for i in range(0, len(time_list_en))],
                value='saleYear',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '35%', 'display': 'inline-block'})

    ]),

    html.Div([
        dcc.Graph(
            id='out-fig-market'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'}),

    html.H3('전체 시장 년도별 비교 by 월별 합계', style={"textAlign": "left"}),

    html.Div([
        html.Div([
            html.Pre(children="지표", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='input-var',
                options=[{'label': i, 'value': j} for i, j in zip(['거래량', '평균가격'], ['totQty', 'avgAmt'])],
                value='totQty',
                clearable=False,
                persistence=True, persistence_type='session'
            )
        ], className='six columns')
    ]),

    html.Div([
        dcc.Graph(
            id='out-fig-market-2'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'})
])


@app.callback(
    Output(component_id='out-fig-market', component_property='figure'),
    [Input(component_id='input-timeunit', component_property='value')]
)
def update_graph(time_unit):
    target_df = dfg.groupby([time_unit])[['totAmt', 'totQty', 'avgAmt']].sum().reset_index()
    fig = pf.bar_line_fn(target_df, time_unit)
    return fig


@app.callback(
    Output(component_id='out-fig-market-2', component_property='figure'),
    [Input(component_id='input-var', component_property='value')]
)
def update_graph_2(var):
    fig = px.line(year_month_df, x='saleMonth', y=var, color='saleYear')
    fig.update_xaxes(title_text='월')
    fig.update_layout(legend_title_text="년도")
    if var == 'totQty':
        fig.update_yaxes(title_text='거래량')
    elif var == 'avgAmt':
        fig.update_yaxes(title_text='평균가격')
    else:
        pass
    return fig
