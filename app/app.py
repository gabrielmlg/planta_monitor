import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import pandas as pd


app = dash.Dash(
    name='clotilde-monitor', 
    external_stylesheets=[dbc.themes.LITERA]
)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Detalhes", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Mais", header=True),
                dbc.DropdownMenuItem("Tese 1", href="#"),
                dbc.DropdownMenuItem("Testes 2", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="MONITOR DE SAÚDE DA CLOTILDE",
    brand_href="#",
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [

        dbc.Row(dbc.Col(html.Div(navbar))), 
        html.Br(), 

        dbc.Row(dbc.Col(
            html.Div([
                dcc.Graph(id='live-graph', animate=True),
                dcc.Interval(
                    id='graph-update',
                    interval=1*1000
                ),
            ])
        ))

    ]
)


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    
    df = pd.read_csv('/Users/gabriel/Documents/dev/planta_monitor/app/dataset/clotilde_v1.csv')

    data = go.Scatter(
            x=df['data'],
            y=df['umidade'],
            name='Scatter',
            mode= 'lines+markers', 
            line=dict(color='green', width=1.8), 
            marker=dict(size=4)
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(df['data']),max(df['data'])]),
                                                yaxis=dict(range=[min(df['umidade'])-2,max(df['umidade'])+2]),)}




if __name__ == "__main__":
    app.run_server(debug=True)