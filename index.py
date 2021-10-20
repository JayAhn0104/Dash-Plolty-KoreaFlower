import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import global_sales, one_product

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Other Products|', href='/apps/global_sales'),
        # dcc.Link('전체 시장|', href='/apps/market'),
        dcc.Link('개별 품목', href='/apps/one_product')
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/global_sales':
        return global_sales.layout
    # elif pathname == '/apps/market':
    #     return market.layout
    elif pathname == '/apps/one_product':
        return one_product.layout
    else:
        return one_product.layout


if __name__ == '__main__':
    app.run_server(debug=True)