import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
from app import app

from plotly.subplots import make_subplots
import plotly.graph_objects as go

def bar_line_fn(target_df, time_unit):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=target_df[time_unit], y=target_df['totQty'], name="totQty"),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=target_df[time_unit], y=target_df['avgAmt'], name="avgAmt",
                   mode='lines'),
        secondary_y=True
    )
    fig.update_layout(
        title_text='totQty & avgAmt from {} to {}'.format(target_df[time_unit].iloc[0],
                                                          target_df[time_unit].iloc[-1])
    )
    fig.update_xaxes(title_text=time_unit)
    fig.update_yaxes(title_text="<b>totQty</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>avgAmt</b>", secondary_y=True)

    return fig

# get relative data folder
PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../Deploy/datasets").resolve()
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfg = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr', index_col=0)
time_list_en = ['saleYear', 'Year_Month', 'saleMonth']
time_list_kr = ['년도별', '월별', '월별 합계']

layout = html.Div([
    html.H1('개별 품목의 거래정보', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="시간 단위", style={"fontSize":"150%"}),
            dcc.RadioItems(
                id='input-1',
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
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'})

])

@app.callback(
    Output(component_id='out-fig-market', component_property='figure'),
    [Input(component_id='input-1', component_property='value')]
)
def update_graph(time_unit):
    target_df = dfg.groupby([time_unit])[['totAmt','totQty', 'avgAmt']].sum().reset_index()
    fig = bar_line_fn(target_df, time_unit)
    return fig
