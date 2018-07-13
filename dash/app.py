import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv("../data/dash_data.csv", parse_dates=["Ride Date"])

vals = list(df.columns)
vals.remove('Ride Duration')
vals.remove('Ride Date')


app.layout = html.Div([
    html.H1(children="Cycling Data Cross-Filter Chart"),
    html.Div([

        html.Div([
            html.Div(children="X-Axis"),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in vals],
                value='Average Cadence'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Div(children="Y-Axis"),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in vals],
                value='Average Speed'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='scatter-graphic'),

], style={"fontFamily":"sans-serif"})

@app.callback(
    dash.dependencies.Output('scatter-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):

    xs = df[xaxis_column_name]
    ys = df[yaxis_column_name]

    trace = go.Scatter(
        x=xs,
        y=ys,
        text="<em>Ride Date: </em>" + df["Ride Date"].astype(str) + 
            "<br><em>Ride Duration: </em>" + (df["Ride Duration"]/60/60).round(2).astype(str) + " Hours",
        mode='markers',
        marker=dict(
            opacity=0.5,
            size = df["Ride Duration"],
            sizemode="area",
            sizeref=2.*max(df["Ride Duration"])/(40.**2),
            sizemin=4
            )
        )

    layout = go.Layout(
        xaxis={'title':xaxis_column_name},
        yaxis={'title':yaxis_column_name},
        hovermode='closest'
        )

    return {
        'data': [trace],
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server(debug=True)
