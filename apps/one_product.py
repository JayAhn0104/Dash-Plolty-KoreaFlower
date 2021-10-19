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

# owner: shivp Kaggle. Source: https://data.mendeley.com/datasets
# dataset was modified. Original data: https://www.kaggle.com/shivkp/customer-behaviour
dfg = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr')

layout = html.Div([
    html.H1('General Product Sales', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Payment type", style={"fontSize":"150%"}),
            dcc.Dropdown(
                id='pymnt-dropdown', value='카랑코에', clearable=False,
                persistence=True, persistence_type='session',
                options=[{'label': x, 'value': x} for x in sorted(dfg["pumName"].unique())]
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="Country of destination", style={"fontSize": "150%"}),
            dcc.RadioItems(
                id='country-dropdown', value='Year_Month',
                persistence=True, persistence_type='local',
                options=[{'label': x, 'value': x} for x in ['saleDate', 'saleMonth', 'Year_Month']]
            )
        ], className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-map', figure={}),
])

@app.callback(
    Output(component_id='my-map', component_property='figure'),
    [Input(component_id='pymnt-dropdown', component_property='value'),
     Input(component_id='country-dropdown', component_property='value')]
)
def update_graph(name, time_unit):
    a = target_fn(dfg, name, time_unit, year='whole_range')
    fig = a.plot_target(a.df_target(), width=800)
    return fig
