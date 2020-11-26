from datetime import timedelta
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Card import Card
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url_raspi = '/home/gabriel/dev/planta_monitor/app/dataset/clotilde_v1.csv'

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
        
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='umidade_indicator', animate=True), 
                ]), md=4
            ), 
            dbc.Col(
                html.Div([
                    #html.H2('TESTE')
                ]), md=4
            ),
            dbc.Col(
                html.Div([
                    #html.H2('TESTE')
                ]), md=4
            ),
        ], align="center", 
            justify="center", 
            style={'margin-top': '4px',
            'margin-left': '4px',}),  

        dbc.Row(dbc.Col(
            html.Div([
                dcc.Graph(id='live-graph', animate=True),
                dcc.Interval(
                    id='graph-update',
                    interval=1*2000 # 2 seg
                ),
            ]), md=12,  
        ), 
        align="right", 
        justify="center", 
        style={'margin-top': '4px',
            'margin-left': '4px',
            'margin-right': '4px'})

    ]
)


@app.callback(Output('live-graph', 'figure'),
                Output('umidade_indicator', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    
    # ToDo: Qnd der erro, como proceder? Tentar colocar o dataframe como atributo numa classe instanciada
    df = pd.read_csv(url_raspi) 
    # df.sort_values('data', inplace=True)

    data = go.Scatter(
            x=df['data'],
            y=df['umidade'],
            name='Scatter',
            mode= 'lines', 
            line=dict(color='green', width=1.8), 
            line_shape='spline',
            # marker=dict(size=4)
            )
    xaxis_max_date = pd.to_datetime(max(df['data'])) + timedelta(minutes=1)
    scatter_fig = {'data': [data],
                    'layout' : go.Layout(xaxis=dict(range=[min(df['data']),xaxis_max_date]),
                                                yaxis=dict(range=[min(df['umidade'])-2,max(df['umidade'])+2]),), }


    data_umidade_indicator = go.Indicator(
        mode = 'gauge+number+delta', 
        gauge = {'shape': "bullet"},
        delta = {'reference': 500, 'relative': False}, 
        value = int(df.tail(1)['umidade'].values),
        domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
        #title = {'text': "Indicator de Umidade:"}
    )

    indicator_fig = {'data': [data_umidade_indicator],
                    'layout' : go.Layout(height=300, 
                                        width=600, 
                                        title='Indicador de Úmidade:', 
                                        template='plotly_white')}


    return scatter_fig, indicator_fig
    




if __name__ == "__main__":
    app.run_server(debug=True)