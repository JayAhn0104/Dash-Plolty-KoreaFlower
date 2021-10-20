import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
from app import app
import plot_fn as pf
import plotly.express as px

def df_top(df, var, top_limit):
    sorted_df = df.sort_values(by=var, ascending=False)
    target_df = sorted_df[:top_limit]
    target_other_df = pd.DataFrame(sorted_df[top_limit:].sum()).transpose()
    out_df = pd.concat([target_df, target_other_df], axis=0)
    out_df.rename({0:'Others'}, inplace=True)
    return out_df


def df_top_years(df, var, top_limit, others_drop=True):
    df_list = []
    for year in df.unstack().index:
        year_df = df.xs(year)
        df_list.append(df_top(year_df, var, top_limit)[var])
    out_df = pd.concat(df_list, axis=1)
    out_df.set_axis(df.unstack().index, axis=1, inplace=True)
    if others_drop: out_df.drop('Others', axis=0, inplace=True)
    return out_df


def df_top_reduce(df, top_list):
    top_df = df[df['pumName'].isin(top_list)]
    other_df = df[df['pumName'].isin(top_list)].groupby('Year').sum()
    other_df['pumName'] = 'others'
    other_df['Year'] = other_df.index

    return pd.concat([top_df, other_df], axis=0)

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr', index_col=0)

year_pum_df = df.groupby(['saleYear', 'pumName'])[['totAmt', 'totQty', 'avgAmt']].sum()
year_pum_df['pumName'], year_pum_df['Year'] = None, None
for year in year_pum_df.unstack().index:
    year_pum_df.loc[year, 'Year'] = str(year)
    year_pum_df.loc[year, 'pumName'] = year_pum_df.loc[year].index

layout = html.Div([
    html.H1('top sales', style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Pre(children="변수", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='input-var',
                options=[{'label': i, 'value': i} for i in ['totQty', 'avgAmt']],
                value='totQty',
                clearable=False,
                persistence=True, persistence_type='session'
            )
        ], className='six columns'),
        html.Div([
            html.Pre(children="top limit", style={"fontSize": "150%"}),
            dcc.RadioItems(
                id='input-top-limit',
                options=[{'label': i, 'value': i} for i in [10, 20, 30, 'all']],
                value=20,
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '35%', 'display': 'inline-block'})

    ]),

    html.Div([
        dcc.Graph(
            id='out-fig-top-bar'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'}),
])


@app.callback(
    Output(component_id='out-fig-top-bar', component_property='figure'),
    [Input(component_id='input-top-var', component_property='value'),
     Input(component_id='input-top-limit', component_property='value')]
)
def update_graph(var, top_limit):
    top_list = df_top_years(year_pum_df, var, top_limit, others_drop=False).index
    fin_df = df_top_reduce(year_pum_df, top_list)
    fig = px.bar(fin_df.sort_values(by=var, ascending=False), x='Year', y=var, color='pumName')
    return fig
