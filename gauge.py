import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_daq as daq
import plotly.io as pio
from datetime import date, timedelta

df = pd.read_csv('week_data.csv')
labels = ['市场','权益市场','期货']
periods = ['一周','两周','一月']
num_of_day = (df['date']).unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style = dict(backgroundImage='url("assets/logo_04.jpg")',backgroundPosition='bottom left',backgroundRepeat='no-repeat',position='absolute',zIndex='auto',backgroundSize='80px'),
    children=[
        html.Div([
            dcc.Slider(
                id='date_slider',
                min=0,
                max=len(num_of_day)-1,
                value=len(num_of_day)-2,
                marks={i: j for i,j in enumerate(num_of_day)},
                step=None
            ),
            dcc.Dropdown(
                id='labels_list',
                options=[{'label':i,'value':i} for i in labels],
                value = '市场'
            ),
            dcc.RadioItems(
                id='period',
                options=[{'label':i,'value':i} for i in periods],
                value='一周'
            )
        ],
        style={'width':'100%','display':'inline-block'}
        ),
        html.Div(
            daq.Gauge(
                id = 'gauge1',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                value=float(df[(df['date']==num_of_day[-2])&(df['label']=='市场')&(df['period']=='一周')&(df['name']=='上证50')]['prob'])*100,
                label='上证50',
                max=100,
                min=0
            ),
            style=dict(float='left',height='500px',width='900px') 
        ),
        html.Div(
            daq.Gauge(
                id = 'gauge2',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                value=float(df[(df['date']==num_of_day[-2])&(df['label']=='市场')&(df['period']=='一周')&(df['name']=='沪深300')]['prob'])*100,
                label='沪深300',
                max=100,
                min=0,
            ),
            style=dict(float='left',height='500px',width='900px')
        ),
        html.Div(
            daq.Gauge(
                id = 'gauge3',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                value=float(df[(df['date']==num_of_day[-2])&(df['label']=='市场')&(df['period']=='一周')&(df['name']=='中证500')]['prob'])*100,
                label='中证500',
                max=100,
                min=0,
            ),
            style=dict(float='left',clear='left',height='500px',width='900px')
        ),
        html.Div(
            daq.Gauge(
                id = 'gauge4',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                value=float(df[(df['date']==num_of_day[-2])&(df['label']=='市场')&(df['period']=='一周')&(df['name']=='中证1000')]['prob'])*100,
                label='中证1000',
                max=100,
                min=0,
            ),
            style=dict(float='left',height='500px',width='900px')
        )
    ]
)

@app.callback(
    [Output('gauge1','value'),
    Output('gauge1','label'),
    Output('gauge2','value'),
    Output('gauge2','label'),
    Output('gauge3','value'),
    Output('gauge3','label'),
    Output('gauge4','value'),
    Output('gauge4','label')],
    [Input('labels_list','value'),
    Input('period','value'),
    Input('date_slider','value')]
)
# class_label ['市场','权益市场','期货']
# period_value ['一周','两周','一月']
# date_value 
def update_date(class_label,period_value,date_value):
    filtered_df = df[(df['date']==num_of_day[date_value])&(df['label']==class_label)&(df['period']==period_value)]

    g1_title = list(filtered_df['name'])[0]
    g2_title = list(filtered_df['name'])[1]
    g3_title = list(filtered_df['name'])[2]
    g4_title = list(filtered_df['name'])[3]
    g1_value = list(filtered_df['prob'])[0]*100
    g2_value = list(filtered_df['prob'])[1]*100
    g3_value = list(filtered_df['prob'])[2]*100
    g4_value = list(filtered_df['prob'])[3]*100
    return g1_value,g1_title,g2_value,g2_title,g3_value,g3_title,g4_value,g4_title
    

app.run_server(debug=True,port=8502)

