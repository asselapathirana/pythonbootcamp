import plotly.express as px
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

countries = pd.read_pickle("./data/country_profile_variables.csv.pickle")
col_options = [dict(label=x, value=x) for x in countries.columns]
dimensions = ["x", "y", "color"]#, "facet_col", "facet_row"]

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.H1("Demo: Plotly Express in Dash with countries Dataset"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
    ]
)


@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure(x, y, color, ): #facet_col, facet_row):
    return px.scatter(
        countries,
        x=x,
        y=y,
        color=color,
        #facet_col=facet_col,
        #facet_row=facet_row,
        height=700,
        hover_name='country',
    )


app.run_server(debug=True)