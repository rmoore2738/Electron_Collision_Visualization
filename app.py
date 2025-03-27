import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
server = app.server

# Load data
df = pd.read_csv("dielectron.csv")
df["Run"] = df["Run"].astype(str)
drop_list = df.columns.to_list()
drop_list3d = ['None'] + drop_list
run_list = df["Run"].unique()

# Sidebar
sidebar = html.Div([
    html.H4("ELECTRON COLLISION DASHBOARD", className="text-white"),
    html.H6("By: Brian Gilmore, Rebecca Moore, Chiamaka Aghaizu", className="text-white"),
    html.Hr(),
    html.P("Select a Run"),
    dcc.Dropdown(id="Run_Category-dropdown", options=[{'label': 'Total', 'value': 'Total'}] + [{'label': i, 'value': i} for i in df['Run'].unique()], value="Total"),
    html.P("Choose an Attribute"),
    dcc.Dropdown(id="attribute-dropdown", options=[{'label': i, 'value': i} for i in df.columns[1:]], value=df.columns[1]),
    html.Hr(),
    html.P("3D Scatterplot Options"),
    dcc.Dropdown(id="xvalue", options=drop_list, value=drop_list[2], placeholder="X Variable"),
    dcc.Dropdown(id="yvalue", options=drop_list, value=drop_list[10], placeholder="Y Variable"),
    dcc.Dropdown(id="zvalue", options=drop_list3d, value=drop_list3d[0], placeholder="Z Variable")
], style={"padding": "1rem", "overflowY": "auto", "maxHeight": "90vh"}, className="bg-primary")

# Cards
card1 = dbc.Card(dbc.CardBody([html.H6("Total Instances"), html.H4("100,000")]), style={"margin": "1rem"})
card2 = dbc.Card(dbc.CardBody([html.H6("Avg Invariant Mass (M)"), html.H4("30.02 GeV")]), style={"margin": "1rem"})
card3 = dbc.Card(dbc.CardBody([html.H6("Avg Events Per Run"), html.H4("7692")]), style={"margin": "1rem"})

cards = dbc.Row([dbc.Col(card1, md=4), dbc.Col(card2, md=4), dbc.Col(card3, md=4)], className="mb-4")

# Content
content = html.Div([
    cards,
    html.Div([html.P("In this dashboard..."), html.P("Interact with the dropdowns...")], style={"margin": "1rem"}),
    dbc.Row([dbc.Col(dcc.Graph(id="pie", config={"responsive": True}), xs=12, md=6),
             dbc.Col(dcc.Graph(id="pie2", config={"responsive": True}), xs=12, md=6)]),
    dbc.Row([dbc.Col(dcc.Graph(id="histogram", config={"responsive": True}), xs=12)]),
    dbc.Row([dbc.Col(dcc.Graph(id="heatmap", config={"responsive": True}), xs=12)]),
    dbc.Row([dbc.Col(dcc.Graph(id="interactive_graph", config={"responsive": True}), xs=12)]),
    dbc.Row([dbc.Col(dcc.Graph(id="limit_graph", config={"responsive": True}), xs=12)])
], style={"padding": "1rem"})

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, xs=12, md=3),
        dbc.Col(content, xs=12, md=9)
    ])
], fluid=True)

# Callbacks
@app.callback(Output('interactive_graph', 'figure'), Input('xvalue', 'value'), Input('yvalue', 'value'), Input('zvalue', 'value'))
def update_scatter(xvalue_col, yvalue_col, zvalue_col):
    if zvalue_col == 'None':
        fig = px.scatter(df, x=xvalue_col, y=yvalue_col, color="Run", title=f"{xvalue_col} vs {yvalue_col}")
    else:
        fig = px.scatter_3d(df, x=xvalue_col, y=yvalue_col, z=zvalue_col, color="Run", title=f"{xvalue_col} vs {yvalue_col} vs {zvalue_col}")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

@app.callback(Output('limit_graph', 'figure'), Input('interactive_graph', 'clickData'), Input('xvalue', 'value'), Input('yvalue', 'value'), Input('zvalue', 'value'))
def update_insight(clickData, xvalue_col, yvalue_col, zvalue_col):
    run_id = clickData['points'][0]['curveNumber']
    df_new = df[df["Run"].isin([run_list[run_id]])]
    if zvalue_col == 'None':
        fig = px.scatter(df_new, x=xvalue_col, y=yvalue_col, color='Event')
    else:
        fig = px.scatter_3d(df_new, x=xvalue_col, y=yvalue_col, z=zvalue_col, color='Event')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

@app.callback([Output('histogram', 'figure'), Output('heatmap', 'figure')], [Input('Run_Category-dropdown', 'value'), Input('attribute-dropdown', 'value')])
def update_figure(Run_Category, attribute):
    val = 'All Runs' if Run_Category == 'Total' else f'Run {Run_Category}'
    filterd_df = df if Run_Category == 'Total' else df[df['Run'] == Run_Category]
    fig_histt = px.histogram(filterd_df, x=attribute, nbins=40, title=f"Histogram of {attribute} for {val}")
    corr_matrix = filterd_df.drop('Run', axis=1).corr()
    heatmap = go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns, colorscale='Blues', zmin=-1, zmax=1)
    fig_htmp = go.Figure(data=[heatmap])
    return fig_histt, fig_htmp

@app.callback(Output('pie', 'figure'), Input('interactive_graph', 'hoverData'))
def update_pie1(hover_id):
    return px.pie(df, values="E1", names="Run", color_discrete_sequence=['#bad6eb', '#2b7bba'])

@app.callback(Output('pie2', 'figure'), Input('interactive_graph', 'hoverData'))
def update_pie2(hover_id):
    return px.pie(df, values="E2", names="Run", color_discrete_sequence=['#bad6eb', '#2b7bba'])

if __name__ == "__main__":
    app.run_server(debug=True, port=1234)
