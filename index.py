import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import global_sales, one_product, market, top_sales

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('전체 시장|', href='/apps/market'),
        dcc.Link('top sales|', href='/apps/top_sales'),
        dcc.Link('개별 품목', href='/apps/one_product')
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/market':
        return market.layout
    elif pathname == '/apps/top_sales':
        return top_sales.layout
    elif pathname == '/apps/one_product':
        return one_product.layout
    else:
        return market.layout


if __name__ == '__main__':
    app.run_server(debug=True)