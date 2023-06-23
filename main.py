import os, dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('assets/kaggle_data.csv')

numerical_cols = data.select_dtypes(include='number').columns

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "HealVisuals: Discovering Health Through Data"

app.layout = html.Div([
    html.H1('HealVisuals: Discovering Health Through Data'),
    html.Span('A Health Data Visualization Dashboard'),
    html.P('By Devansh Tikariha and Raghav Sivakuru'),
    
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Severity of Illness', 'value': 'Severity of Illness'},
            {'label': 'Visitors with Patient', 'value': 'Visitors with Patient'}
            
        ],
        value='Severity of Illness'  
    ),
    dcc.Graph(id='metric-graph'),
    
    dcc.Graph(
    id='hospital-type-histogram',
    figure=px.histogram(data, x='Hospital_type_code', title='Number of Cases by Hospital Type Code')
    ),
    
    dcc.Graph(
    id='city-code-hospital-histogram',
    figure=px.histogram(data, x='City_Code_Hospital', title='Number of Cases by City Code Hospital')
    ),

    dcc.Graph(
        id='visitors-admission-scatter-plot',
        figure=px.scatter(data, x='Visitors with Patient', y='Admission_Deposit', color='Severity of Illness', title='Relationship between Visitors with Patient and Admission Deposit')
    ),
    
    dcc.Graph(
        id='admission-deposit-box-plot',
        figure=px.box(data, x='Severity of Illness', y='Admission_Deposit', title='Distribution of Admission Deposit by Severity of Illness')
    ),
    
    dcc.Graph(
        id='correlation-heatmap',
        figure=px.imshow(data[numerical_cols].corr(), title='Correlation Heatmap')
    ),

    dcc.Graph(
    id='age-histogram',
    figure=px.histogram(data, x='Age', title='Distribution of Age of Patients')
    ),

    dcc.Graph(
        id='admission-type-pie-chart',
        figure=px.pie(data, names='Type of Admission', title='Percentage of Patients in Each Type of Admission')
    )
])
color_mapping = {
    'Severity of Illness': {
        'Minor': 'green',
        'Moderate': 'yellow',
        'Extreme': 'red'
    },
    'Visitors with Patient': {
        'Low': 'blue',
        'Average': 'orange',
        'High': 'red'
    },
    'Admission_Deposit': {
        'Low': 'blue',
        'Medium': 'green',
        'High': 'red'
    }
}
@app.callback(
    dash.dependencies.Output('metric-graph', 'figure'),
    [dash.dependencies.Input('metric-dropdown', 'value')]
)
def update_graph(metric):
    figure = go.Figure(data=go.Scatter(
        x=data[metric],
        y=data['Available Extra Rooms in Hospital'],
        mode='markers',
        marker=dict(
            size=10,
            color=[color_mapping[metric].get(i, 'gray') for i in data[metric]],
            opacity= 0.8
        ),
        text=data['Department']
    ))
    
    figure.update_layout(
        title=f'{metric} vs. Available Extra Rooms in Hospital',
        xaxis_title=metric,
        yaxis_title='Available Extra Rooms in Hospital'
    )
    
    return figure

app = Dash(__name__)

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
