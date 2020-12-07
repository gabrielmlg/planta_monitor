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
from pymongo import MongoClient

url_raspi = '/home/pi/dev/planta_monitor/app/dataset/clotilde_v1.csv'
url_mac = '/Users/gabriel/Documents/dev/planta_monitor/app/dataset/clotilde_v1.csv'

# Mongodb
string_conn_raspi = 'mongodb://admin:v73jMSPw9EQI@192.168.68.116:27017/admin'
string_conn_mac = 'mongodb://root:example@localhost:27017/admin'

string_conn = string_conn_mac

client = MongoClient(string_conn)
db = client.clotilde
collection_arduino = db.arduino

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
                    dcc.Graph(id='temperatura_indicator', animate=True), 
                ]), md=4
            ),
            dbc.Col(
                html.Div([
                    # dcc.Graph(id='temp', animate=True), 
                    #html.H2('TESTE')
                ]), md=4
            ),
        ], align="center", 
            justify="center", 
            style={'margin-top': '4px',
            'margin-left': '2px',
            'margin-right': '2px'}),  

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
                Output('temperatura_indicator', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    
    # ToDo: Qnd der erro, como proceder? Tentar colocar o dataframe como atributo numa classe instanciada
    #df = pd.read_csv(url_raspi) 
    # df.sort_values('data', inplace=True)
    cursor = collection_arduino.find({})
    df = pd.DataFrame(list(cursor))

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
                                        yaxis=dict(range=[min(df['umidade'])-2,max(df['umidade'])+2]),
                                        template='plotly_white'
                                ), }


    data_umidade_indicator = go.Indicator(
        mode = "number+delta",
        value = float(df.tail(1)['umidade'].values),
        title = {"text": "Úmidade<br><span style='font-size:0.8em;color:gray'>Solo</span><br>"},
        delta = {'reference': 500, 'relative': True},
        domain = {'x': [0, 1], 'y': [0, 1]}
    )

    kpi_umidade_fig = {
        'data': [data_umidade_indicator],
        'layout' : go.Layout(
            template='plotly_white', 
            height=300, 
            width=400, 
        )
    }

    # Termperatura KPI
    data_temperatura_indicator = go.Indicator(
        mode = "number+delta",
        value = float(df.tail(1)['temperatura'].values),
        title = {"text": "Temperatura<br><span style='font-size:0.8em;color:gray'>Ambiente</span><br>"},
        delta = {'reference': 25, 'relative': True},
        domain = {'x': [0, 1], 'y': [0, 1]}
    )

    kpi_temperatura_fig = {
        'data': [data_temperatura_indicator],
        'layout' : go.Layout(
            template='plotly_white', 
            height=300, 
            width=400, 
        )
    }

    return scatter_fig, kpi_umidade_fig, kpi_temperatura_fig
    


if __name__ == "__main__":
    app.run_server(debug=True)