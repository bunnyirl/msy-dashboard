# Written by Kyle Berzett

from dash import Dash, html, dcc, Input, Output
from incomeBarChart import createIncomeBarChart
from msy2 import meatVarianceCharts
from keMSY import ingredientPlots, octPlots

app = Dash(__name__)

# Custom HTML template — ensures no white border/background
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Mai Shan Yun Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                background-color: #ffffff;
                transition: background-color 0.5s, color 0.5s;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Source files
month_sources = ["may.csv", "june.csv", "july.csv", "august.csv", "september.csv", "october.csv"]

# Jeremiah's
fig1, fig2, fig3, beef, chicken = meatVarianceCharts(0.0, 0.5, 0.5, month_sources)

# Kevin's
fig4, fig5 = ingredientPlots()
fig6, fig7 = octPlots()

# Layout
app.layout = html.Div(
    [
        html.H1("Mai Shan Yun Dashboard", id="page-title"),

        # Light/Dark toggle
        html.Div([
            html.Label("Theme:", id="theme-label"),
            dcc.RadioItems(
                id="theme-toggle",
                options=[
                    {"label": "Light", "value": "light"},
                    {"label": "Dark", "value": "dark"}
                ],
                value="light",
                inline=True,
                style={"margin": "10px"}
            )
        ], style={"textAlign": "center"}),

        html.Div(id="graphs-container")
    ],
    id="page-container",
    style={
        "backgroundColor": "#ffffff",
        "color": "#000000",
        "minHeight": "100vh",
        "padding": "20px",
        "margin": "0",
    }
)


@app.callback(
    Output("graphs-container", "children"),
    Output("page-container", "style"),
    Output("page-title", "style"),
    Output("theme-label", "style"),
    Input("theme-toggle", "value")
)
def update_theme(theme):
    """Switch between light and dark themes dynamically."""
    if theme == "light":
        bg_color = "#_
