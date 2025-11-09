# Written by Kyle Berzett

from dash import Dash, html, dcc, Input, Output
from incomeBarChart import createIncomeBarChart
from msy2 import meatVarianceCharts
from keMSY import ingredientPlots, octPlots

# Initialize Dash app
app = Dash(__name__)

# Source files of monthly data
month_sources = ["may.csv", "june.csv", "july.csv", "august.csv", "september.csv", "october.csv"]

# Jeremiah's
fig1, fig2, fig3, beef, chicken = meatVarianceCharts(0.0, 0.5, 0.5, month_sources)

# Kevin's
fig4, fig5 = ingredientPlots()
fig6, fig7 = octPlots()

# Set initial theme (light)
initial_theme = "light"

# Layout
app.layout = html.Div(
    [
        html.H1("Mai Shan Yun Dashboard", style={"textAlign": "center"}),

        # Light/Dark mode toggle
        html.Div([
            html.Label("Theme:"),
            dcc.RadioItems(
                id="theme-toggle",
                options=[
                    {"label": "🌞 Light", "value": "light"},
                    {"label": "🌙 Dark", "value": "dark"}
                ],
                value=initial_theme,
                inline=True,
                style={"margin": "10px"}
            )
        ], style={"textAlign": "center"}),

        # Graph container
        html.Div(id="graphs-container")
    ]
)

# Callback to update the graphs based on selected theme
@app.callback(
    Output("graphs-container", "children"),
    Input("theme-toggle", "value")
)
def update_theme(theme):
    """Switch between light and dark themes dynamically."""

    # Plotly themes
    plotly_template = "plotly_white" if theme == "light" else "plotly_dark"
    bg_color = "#ffffff" if theme == "light" else "#1e1e1e"
    text_color = "#000000" if theme == "light" else "#ffffff"

    # Generate all figures using the theme
    figs = [
        createIncomeBarChart(month_sources),
        fig1, fig2, fig3, fig4, fig5, fig6, fig7
    ]

    # Apply the selected theme to all figures
    for f in figs:
        f.update_layout(
            template=plotly_template,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font_color=text_color
        )

    # Return updated graphs
    return [dcc.Graph(figure=f) for f in figs]


if __name__ == "__main__":
    app.run(debug=True)
