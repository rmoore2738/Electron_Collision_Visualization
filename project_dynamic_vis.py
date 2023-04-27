# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

app = Dash(__name__)

# load data
df = pd.read_csv("dielectron.csv")

# create list for dropdowns, change Run to string to not color using color bar
drop_list = df.columns.to_list()
df["Run"] = df["Run"].astype(str)

# add None to drop_list for 3d scatter option
drop_list3d = ['None'] + drop_list

# create list of unique runs to use for changing second chart based on hover/click action in first chart
run_list = df["Run"].unique()

# Create the options list dynamically based on the columns in the DataFrame
options = [{'label': col, 'value': col} for col in df.columns]

# design/layout portion
app.layout = html.Div([
    html.H1('Electron Collision Interactive Visualizations'),
    html.H4("Histogram and Heatmap of Attributes"),
    html.Div([
        html.Label("Select a Run"),
        dcc.Dropdown(
            id='Run_Category-dropdown',
            options=[{'label': i, 'value': i} for i in df['Run'].unique()],
            value=df['Run'].unique()[0]
        ),
        html.Br(),
        html.Label("Select the Attribute"),
        dcc.Dropdown(
            id='attribute-dropdown',
            options=[{'label': i, 'value': i} for i in df.columns[1:]],
            value=df.columns[1]
        ),
        html.Br(),
        dcc.Graph(id='histogram', figure={}),
        dcc.Graph(id='heatmap', figure={})])
    ,
    html.Div('Energy of Eletron 1 vs Run Number.'),
    html.Div([
            dcc.Graph(id='pie')

        ]),
    html.Div('Energy of Eletron 2 vs Run Number.'),
    html.Div([
            dcc.Graph(id='pie2')
        ]),
    html.Div('Interactive Scatterplot.'),
    html.Div([
        # add dropdowns to select columns for axes
        html.Div([
            html.Label('X-axis'),
            dcc.Dropdown(
                id="xvalue",
                options=drop_list,
                value=drop_list[2])], 
                style={"width" : "30%", "display" : "inline-block", "padding" : "10px"}
            ),
        html.Div([
            html.Label('Y-axis'),
            dcc.Dropdown(
                id="yvalue",
                options=drop_list,
                value=drop_list[10])
            ], style={"width" : "30%", "display" : "inline-block", "padding" : "10px"}),
        html.Div([    
            html.Label('Z-axis (select to enable 3D scatter)'),
            dcc.Dropdown(
                id="zvalue",
                options=drop_list3d,
                value=drop_list3d[0])
            ], style={"width" : "30%", "display" : "inline-block", "padding" : "10px"}),                       
    ]),    
    # create divs for graphs
    html.Div([
        dcc.Graph(
            id='interactive_graph',
            clickData={'points': [{'curveNumber': 0}]} # set default to avoid initial load error
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(
            id='limit_graph'
            )
        ], style={'display': 'inline-block', 'width': '49%'})

])

#@callback - when input changes (x, y, or z-axis column), update output (scatter)
@app.callback(
    Output('interactive_graph', 'figure'),
    Input('xvalue', 'value'),
    Input('yvalue', 'value'),
    Input('zvalue', 'value'))
def update_scatter(xvalue_col, yvalue_col, zvalue_col):
    if zvalue_col == 'None': # 2d plot

        fig = px.scatter(df, x=xvalue_col, y=yvalue_col, color="Run", title=xvalue_col + " vs " + yvalue_col,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        
        fig.update_xaxes(title=xvalue_col)
        fig.update_yaxes(title=yvalue_col)
        fig.update_layout(transition_duration=500)
    
    else: # 3d plot
        fig = px.scatter_3d(df, x=xvalue_col, y=yvalue_col, z=zvalue_col, color="Run", title=xvalue_col + " vs " + yvalue_col + " vs " + zvalue_col,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        
        fig.update_xaxes(title=xvalue_col)
        fig.update_yaxes(title=yvalue_col)
        fig.update_layout(transition_duration=500)

    return fig

#@callback to update second graph to show unique Run values
@app.callback(
    Output('limit_graph', 'figure'),
    Input('interactive_graph', 'clickData'),
    Input('xvalue', 'value'),
    Input('yvalue', 'value'),
    Input('zvalue', 'value'))
def update_insight(clickData, xvalue_col, yvalue_col, zvalue_col):

    # get value for Run from curveNumber in hover data
    run_id = clickData['points'][0]['curveNumber']

    # filter data based on run_id from hover data
    df_new = df[df["Run"].isin([run_list[run_id]])]
    
    if zvalue_col == 'None':
        fig = px.scatter(df_new, x=xvalue_col, y=yvalue_col, color='Event',
                        title=xvalue_col + " vs " + yvalue_col + " for Run " + run_list[run_id])
        fig.update_layout(transition_duration=500)
    else:
        fig = px.scatter_3d(df_new, x=xvalue_col, y=yvalue_col, z=zvalue_col, color='Event',
                        title=xvalue_col + " vs " + yvalue_col + " vs " + zvalue_col + " for Run " + run_list[run_id])
        fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('pie', 'figure'),
    Input('interactive_graph', 'hoverData')
    )
def update_pie(hover_id):
        fig = px.pie(df, values = "E1", names = "Run")
        return fig

@app.callback(
    Output('pie2', 'figure'),
    Input('interactive_graph', 'hoverData')
    )
def update_pie(hover_id):
        fig = px.pie(df, values = "E2", names = "Run")
        return fig

@app.callback(
    [Output(component_id='histogram', component_property='figure'),
     Output(component_id='heatmap', component_property='figure')],
    [Input(component_id='Run_Category-dropdown', component_property='value'),
     Input(component_id='attribute-dropdown', component_property='value')]
    )
def update_figure(Run_Category, attribute):
    filterd_df = df[df['Run'] == Run_Category]

    # Create the histogram
    fig_histt = px.histogram(filterd_df, x=attribute, nbins=10, title=f"Histogram of {attribute} for Run {Run_Category}")
    # corr_matrix = filterd_df.corr()
    corr_matrix = filterd_df.drop('Run', axis=1).corr()

    # Create the heatmap
    heatmap = go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
    )
    htmp_lyt = go.Layout(title=f'Heatmap Showing Correlation for Attributes in Run {Run_Category}',
                           xaxis=dict(title='Variable'),
                           yaxis=dict(title='Variable'))

    fig_htmp=go.Figure(data=[heatmap], layout=htmp_lyt)

    return fig_histt, fig_htmp

#commented out when running on flask website
if __name__ == '__main__':
    app.run_server(debug=True)
