# Description: random code for testing 
        dbc.Row(
            [
                html.H5('Settings',
                        style={'margin-top': '12px', 'margin-left': '24px'})
                ],
            style={"height": "5vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Categorical Variable',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cat-picker', multi=False, value='cat0',
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cat],
                                 style={'width': '320px'}
                                 ),
                    html.P('Continuous Variable',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cont-picker', multi=False, value='cont0',
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cont],
                                 style={'width': '320px'}
                                 ),
                    html.P('Continuous Variables for Correlation Matrix',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-corr-picker', multi=True,
                                 value=vars_cont + ['Run'],
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cont + ['target']],
                                 style={'width': '320px'}
                                 ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px'},
                                className='bg-dark text-white'),
                    html.Hr()
                ]
                )
            ],
            style={'height': '50vh', 'margin': '8px'}),
   
   

@app.callback(Output('bar-chart', 'figure'),
              Output('bar-title', 'children'),
              Input('my-button', 'n_clicks'),
              State('my-cat-picker', 'value'))
def update_bar(n_clicks, cat_pick):
    bar_df = df.groupby(['target', cat_pick]).count()['id'].reset_index()
    bar_df['target'] = bar_df['target'].replace({0: 'target=0', 1: 'target=1'})

    fig_bar = px.bar(bar_df,
                     x=cat_pick,
                     y="id",
                     color="target",
                     color_discrete_sequence=['#bad6eb', '#2b7bba'])

    fig_bar.update_layout(width=500,
                          height=340,
                          margin=dict(l=40, r=20, t=20, b=30),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend_title=None,
                          yaxis_title=None,
                          xaxis_title=None,
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              )
                          )

    title_bar = 'Distribution of Categorical Variable: ' + cat_pick

    return fig_bar, title_bar


@app.callback(Output('dist-chart', 'figure'),
              Output('dist-title', 'children'),
              Input('my-button', 'n_clicks'),
              State('my-cont-picker', 'value'))
def update_dist(n_clicks, cont_pick):
    num0 = df[df['target'] == 0][cont_pick].values.tolist()
    num1 = df[df['target'] == 1][cont_pick].values.tolist()

    fig_dist = ff.create_distplot(hist_data=[num0, num1],
                                  group_labels=['target=0', 'target=1'],
                                  show_hist=False,
                                  colors=['#bad6eb', '#2b7bba'])

    fig_dist.update_layout(width=500,
                           height=340,
                           margin=dict(t=20, b=20, l=40, r=20),
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           legend=dict(
                               orientation="h",
                               yanchor="bottom",
                               y=1.02,
                               xanchor="right",
                               x=1
                               )
                           )

    title_dist = 'Distribution of Continuous Variable: ' + cont_pick

    return fig_dist, title_dist