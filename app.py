import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from collections import OrderedDict


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

df2 = pd.DataFrame(
    OrderedDict([(name, col_data * 10) for (name, col_data) in df.items()])
)
'''
df = pd.read_csv('data/data_sample.csv')
vars_cat = [var for var in df.columns if var.startswith('cat')]
vars_cont = [var for var in df.columns if var.startswith('cont')]
'''
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# pie chart
pie = df.groupby('E1').count()['Run'] / len(df)

fig_pie1 = px.pie(df, values = "E1", names = "Run",
                 color_discrete_sequence=['#bad6eb', '#2b7bba'])
fig_pie2 = px.pie(df, values = "E2", names = "Run",
                 color_discrete_sequence=['#bad6eb', '#2b7bba'])



sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H4('Electron Collision Visualization Dashboard',
                        style={'margin-top': '20px', 'margin-left': '22px'}),
                html.H6('By: Brian Gilmore, Rebecca Moore and Chiamaka Aghaizu',
                        style={'margin-left': '16px'})
                ],
            style={"height": "130vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('"Select a Run"',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(
                        id='Run_Category-dropdown',
                        options=[{'label': i, 'value': i} for i in df['Run'].unique()],
                        value=df['Run'].unique()[0],
                    
                    ),
                    html.P('Continuous Variable',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(
                        id='attribute-dropdown',
                        options=[{'label': i, 'value': i} for i in df.columns[1:]],
                        value=df.columns[1],
                        style={'width': '320px'}
                    ),
                ]
                )
            ],
            style={'height': '170vh', 'margin': '8px'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([
                            html.P('3D Scatterplot',
                                   className='font-weight-bold'),
                            html.P('X Variable'),
                            dcc.Dropdown(
                                id="xvalue",
                                options=drop_list,
                                value=drop_list[2]),
                                html.P('Y Variable'),
                                dcc.Dropdown(
                                    id="yvalue",
                                    options=drop_list,
                                    value=drop_list[10]),
                                    html.P('Z Variable'),
                                    dcc.Dropdown(
                                        id="zvalue",
                                        options=drop_list3d,
                                        value=drop_list3d[0]),], 
                                style={'height': '110vh','width': '320px'}
                                )
                           
                            ])
                        ])
                ],
)
content = html.Div(
    [
        dbc.Row(
            [
                html.Div([
                            html.P('DESCRIPTION AND SUCH HERE'),
                            dash_table.DataTable(data = df.to_dict('records'),
                            columns = [{'id': c, 'name': c} for c in df.columns],
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_data={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            },
                            style_table={'overflowX': 'scroll'},
                            page_size=10)
            ]),
                dbc.Col(
                    [
                        html.Div([
                            html.P('Energy of Eletron 1 vs Run Number.',
                                   className='font-weight-bold'),
                            dcc.Graph(id="pie")])
                        ]),
                dbc.Col(
                    [
                        html.Div([
                            html.P('Energy of Eletron 2 vs Run Number.',
                                   className='font-weight-bold'),
                            dcc.Graph(id="pie2")])
                        ])
                ],
            style={'height': '130vh',
                   'margin-top': '16px', 'margin-left': '8px',
                    'margin-right': '8px'}),
        dbc.Row(
            [
                html.Br(),
                html.Br(),
                dbc.Col(
                    [
                        html.Div([
                            html.P('Histogram of Attributes',
                                   className='font-weight-bold'),
                            dcc.Graph(id='histogram')])
                        ]),
                        html.Div([
                                        html.P('DESCRIPTION AND SUCH HERE')
                        ])
                ],
            style={'height': '70vh'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([
                            dcc.Graph(id='heatmap')])
                        ]),
                        


                ],
            style={'height': '90vh',
                     'margin-top': '16px', 'margin-left': '8px',
                     'margin-bottom': '1px', 'margin-right': '8px'}),
        dbc.Row(
            [
                    
                        html.Div([
                                        html.P('Interactive Scatterplots',
                                            className='font-weight-bold'),
                                        dcc.Graph(
                                        id='interactive_graph',
                                        clickData={'points': [{'curveNumber': 0}]} # set default to avoid initial load error
                                        ),

                                        ],
                    style={'height': '50vh', 'margin-left': '8px',
                    'margin-right': '8px'})
                        ]),
                        html.Div([
                                        dcc.Graph(
                                            id='limit_graph')
                                        ],
                    style={'height': '30vh',
                   'margin-top': '10px', 'margin-left': '8px',
                    'margin-right': '8px'})

            ])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
                ]
            ),
        ],
    fluid=True
    )


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
        fig.update_layout(transition_duration=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    else: # 3d plot
        fig = px.scatter_3d(df, x=xvalue_col, y=yvalue_col, z=zvalue_col, color="Run", title=xvalue_col + " vs " + yvalue_col + " vs " + zvalue_col,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        
        fig.update_xaxes(title=xvalue_col)
        fig.update_yaxes(title=yvalue_col)
        fig.update_layout(transition_duration=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

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
        fig.update_layout(transition_duration=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        width=1080,
        height=500)
    else:
        fig = px.scatter_3d(df_new, x=xvalue_col, y=yvalue_col, z=zvalue_col, color='Event',
                        title=xvalue_col + " vs " + yvalue_col + " vs " + zvalue_col + " for Run " + run_list[run_id])
        fig.update_layout(transition_duration=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        width=1080,
        height=500)

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
    fig_histt.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)'
            
        })
    # corr_matrix = filterd_df.corr()
    corr_matrix = filterd_df.drop('Run', axis=1).corr()

    # Create the heatmap
    heatmap = go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Blues',
        zmin=-1,
        zmax=1,
    )
    htmp_lyt = go.Layout(title=f'Heatmap Showing Correlation for Attributes in Run {Run_Category}',
                           xaxis=dict(title='Variable'),
                           yaxis=dict(title='Variable'),
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           width=1080,
                           height=600,
                           )

    fig_htmp=go.Figure(data=[heatmap], layout=htmp_lyt)

    return fig_histt, fig_htmp

@app.callback(
    Output('pie', 'figure'),
    Input('interactive_graph', 'hoverData')
    )
def update_pie(hover_id):
        fig = px.pie(df, values = "E1", names = "Run", color_discrete_sequence=['#bad6eb', '#2b7bba'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        width=500,
        height=500)
        return fig

@app.callback(
    Output('pie2', 'figure'),
    Input('interactive_graph', 'hoverData')
    )
def update_pie(hover_id):
        fig = px.pie(df, values = "E2", names = "Run", color_discrete_sequence=['#bad6eb', '#2b7bba'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        width=500,
        height=500)
        return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=1234)