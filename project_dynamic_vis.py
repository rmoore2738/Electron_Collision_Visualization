# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# load data
df = pd.read_csv("dielectron.csv")

# create list for dropdowns, change Run to string to not color using color bar
drop_list = df.columns.to_list()
df["Run"] = df["Run"].astype(str)

# create list of unique runs to use for changing second chart based on hover/click action in first chart
run_list = df["Run"].unique()

# Create the options list dynamically based on the columns in the DataFrame
options = [{'label': col, 'value': col} for col in df.columns]

# design/layout portion
app.layout = html.Div([
    html.H1('Interactive Visual'),
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value=df.columns[0]
    ),
    dcc.Graph(id='histogram'),
    html.Div('Energy of Eletron 1 vs Run Number.'),
    html.Div([
            dcc.Graph(id='pie')

        ]),
    html.Div('Energy of Eletron 2 vs Run Number.'),
    html.Div([
            dcc.Graph(id='pie2')
        ]),
    html.Div('Interactive Scatterplot.'),

    # add dropdowns to select columns for axes
    html.Div([
        html.Label('X-axis'),
        dcc.Dropdown(
            id="xvalue",
            options=drop_list,
            value=drop_list[2]),
        html.Label('Y-axis'),
        dcc.Dropdown(
            id="yvalue",
            options=drop_list,
            value=drop_list[10])
    ]),                       
    
    # create div for graphs
    html.Div([
        dcc.Graph(id='interactive_graph',
            hoverData={'points': [{'curveNumber': 0}]}),
        dcc.Graph(id='limit_graph')
        ]),

    
])

#@callback - when input changes (xaxis or yaxis column), update output (scatter)
@app.callback(
    Output('interactive_graph', 'figure'),
    Input('xvalue', 'value'),
    Input('yvalue', 'value'))

def update_scatter(xvalue_col, yvalue_col):

    fig = px.scatter(df, x=xvalue_col, y=yvalue_col, color="Run", title=xvalue_col + " vs " + yvalue_col,
                     color_discrete_sequence=px.colors.qualitative.Light24)
    
    fig.update_xaxes(title=xvalue_col)
    fig.update_yaxes(title=yvalue_col)
    fig.update_layout(transition_duration=500)

    return fig

#@callback to update second graph to show unique Run values
@app.callback(
    Output('limit_graph', 'figure'),
    Input('interactive_graph', 'hoverData'),
    Input('xvalue', 'value'),
    Input('yvalue', 'value'))
def update_insight(hover_id, xvalue_col, yvalue_col):

    # get value for Run from curveNumber in hover data
    run_id = hover_id['points'][0]['curveNumber']

    # filter data based on run_id from hover data
    df_new = df[df["Run"].isin([run_list[run_id]])]
    
    fig = px.scatter(df_new, x=xvalue_col, y=yvalue_col, color='Event',
                     title=xvalue_col + " vs " + yvalue_col + " for Run " + run_list[run_id])
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
    Output(component_id='histogram', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def update_histogram(selected_column):
    fig = px.histogram(df, x=selected_column)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)