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
# DATA_PATH = PATH.joinpath("../Deploy/datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("2017_2021_flower.csv"), encoding='euc-kr', index_col=0)

year_pum_df = df.groupby(['saleYear', 'pumName'])[['totAmt', 'totQty', 'avgAmt']].sum()
year_pum_df['pumName'], year_pum_df['Year'] = None, None
for year in year_pum_df.unstack().index:
    year_pum_df.loc[year, 'Year'] = str(year)
    year_pum_df.loc[year, 'pumName'] = year_pum_df.loc[year].index

month_pum_df = df.groupby(['saleYear','saleMonth','pumName'])[['totAmt','totQty','avgAmt']].sum()
month_pum_df['pumName'], month_pum_df['Month'] = None, None
for year in month_pum_df.unstack().unstack().index:
    for month in month_pum_df.loc[year].unstack().index:
        month_pum_df.loc[(year, month), 'Month'] = str(month)
        month_pum_df.loc[(year, month), 'pumName'] = month_pum_df.loc[(year, month)].index

logic_label = ['O', 'X']
logic_value = [True, False]

layout = html.Div([
    html.H1('Top sales', style={"textAlign": "center"}),

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
            html.Pre(children="Top limit", style={"fontSize": "150%"}),
            dcc.Slider(
                id='input-top-limit',
                min=5,
                max=30,
                marks={i: 'Top{}'.format(i) for i in range(5, 31, 5)},
                value=10
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="Others 포함여부", style={"fontSize": "150%"}),
            dcc.RadioItems(
                id='input-logic',
                options=[{'label': logic_label[i], 'value': logic_value[i]} for i in range(len(logic_label)) ],
                value=logic_value[0],
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '35%', 'display': 'inline-block'})

    ]),

    html.Div([
        dcc.Graph(
            id='out-fig-top-bar'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'}),



    html.Div([

        html.Div([
            html.Pre(children="년도", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='input-year',
                options=[{'label': i, 'value': i} for i in df['saleYear'].unique()],
                value=df['saleYear'].unique()[-1],
                clearable=False,
                persistence=True, persistence_type='session'
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="변수", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='input-year-var',
                options=[{'label': i, 'value': i} for i in ['totQty', 'avgAmt']],
                value='totQty',
                clearable=False,
                persistence=True, persistence_type='session'
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="Top limit", style={"fontSize": "150%"}),
            dcc.Slider(
                id='input-year-top-limit',
                min=5,
                max=30,
                marks={i: 'Top{}'.format(i) for i in range(5, 31, 5)},
                value=10
            ),
            html.Pre(children="Others 포함여부", style={"fontSize": "150%"}),
            dcc.RadioItems(
                id='input-year-logic',
                options=[{'label': logic_label[i], 'value': logic_value[i]} for i in range(len(logic_label)) ],
                value=logic_value[0],
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width':'99%', 'display':'inline-block'}),

        # html.Div([
        #     html.Pre(children="Top limit", style={"fontSize": "150%"}),
        #     dcc.Slider(
        #         id='input-year-top-limit',
        #         min=5,
        #         max=30,
        #         marks={i: 'Top{}'.format(i) for i in range(5, 31, 5)},
        #         value=10
        #     )
        # ], className='six columns')

    ]),

    html.Div([
        dcc.Graph(
            id='out-fig-year-pie'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(
            id='out-fig-year-bar'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'})


])


@app.callback(
    Output(component_id='out-fig-top-bar', component_property='figure'),
    [Input(component_id='input-var', component_property='value'),
     Input(component_id='input-top-limit', component_property='value'),
     Input(component_id='input-logic', component_property='value')]
)
def update_graph(var, top_limit, logic):
    top_list = pf.df_top_years(year_pum_df, var, top_limit).index
    fin_df = pf.df_top_reduce(year_pum_df, top_list, logic)
    fig = px.bar(fin_df.sort_values(by=var, ascending=False), x='Year', y=var, color='pumName',
                 title='Top {} {} 품목들'.format(top_limit, var))
    return fig


@app.callback(
    Output(component_id='out-fig-year-pie', component_property='figure'),
    [Input(component_id='input-year', component_property='value'),
     Input(component_id='input-year-var', component_property='value'),
     Input(component_id='input-year-top-limit', component_property='value'),
     Input(component_id='input-year-logic', component_property='value')]
)
def update_graph(year, var, top_limit, logic):
    top_df = pf.df_top_others(year_pum_df.xs(year), var, top_limit, logic)
    fig = px.pie(top_df, values=var, names=top_df.index, title='{} of {}'.format(var, year))
    return fig


@app.callback(
    Output(component_id='out-fig-year-bar', component_property='figure'),
    [Input(component_id='input-year', component_property='value'),
     Input(component_id='input-year-var', component_property='value'),
     Input(component_id='input-year-top-limit', component_property='value'),
     Input(component_id='input-year-logic', component_property='value')]
)
def update_graph(year, var, top_limit, logic):
    top_df = pf.month_top_df(month_pum_df, year, var, top_limit, logic)
    fig = px.bar(top_df.sort_values(by=var, ascending=False), x='Month', y=var, color='pumName', title='{} of {} by month'.format(var, year))
    return fig