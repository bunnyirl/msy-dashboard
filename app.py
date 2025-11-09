# Written by Kyle Berzett
# Formatted by Kyle Berzett

from dash import Dash, html, dcc, Input, Output, State
from data_revenue import createRevenuePlot
from data_meatVariance import createMeatPlots
from data_ingredients import createIngredientPlots
from data_october import createOctoberPlots
import plotly.io as pio

app = Dash(__name__)

# Default theme
default_theme = "light"

# Source files of monthly data
month_sources = ["may.csv",
                 "june.csv",
                 "july.csv",
                 "august.csv",
                 "september.csv",
                 "october.csv",]

# PLOTS
incomePlot = createRevenuePlot(month_sources)
(meatEstimationPlot,
 beefVariancePlot,
 chickenVariancePlot,
 _,
 _) = createMeatPlots(0.6, 0.2, 0.2, month_sources)
(ingredientFrequencyPlot,
 quantityPerIngredientPlot) = createIngredientPlots()
(topSellingCatsPlot,
 topRevenueCatsPlot) = createOctoberPlots()


# WEBSITE LAYOUT
app.layout = html.Div(
    id="page-container",
    style={
        "backgroundColor": "#FFFFFF",
        "color": "#000000",
        "minHeight": "100vh",
        "padding": "20px",
    },
    children=[
        # Header
        html.H1("Mai Shan Yun Dashboard", id="header-title", style={"textAlign": "center"}),

        # Theme toggle
        html.Div([
            html.Label("Theme:"),
            dcc.RadioItems(
                id="theme-toggle",
                options=[
                    {"label": "Light Mode", "value": "light"},
                    {"label": "Dark Mode", "value": "dark"},
                ],
                value=default_theme,
                inline=True,
            )
        ], style={"textAlign": "center", "marginBottom": "20px"}),

        # Dropdown for month selection for the revenue graph
        dcc.Dropdown(
            id='month-dropdown',
            options=[
                {'label': 'All Months', 'value': 'all'},
                {'label': 'May', 'value': 'may'},
                {'label': 'June', 'value': 'june'},
                {'label': 'July', 'value': 'july'},
                {'label': 'August', 'value': 'august'},
                {'label': 'September', 'value': 'september'},
                {'label': 'October', 'value': 'october'}
            ],
            value='all',
            clearable=False,
        ),
        dcc.Graph(id="income-plot", figure=incomePlot),

        # Sliders
        html.Label("Beef %"),
        dcc.Slider(
            id='slider-beef',
            min=0.0, max=1.0, step=0.01, value=0.5,
            marks=None, tooltip={"always_visible": False, "placement": "bottom"},
        ),
        html.Label("Chicken %"),
        dcc.Slider(
            id='slider-chicken',
            min=0.0, max=1.0, step=0.01, value=0.3,
            marks=None, tooltip={"always_visible": False, "placement": "bottom"},
        ),
        html.Label("Pork %"),
        dcc.Slider(
            id='slider-pork',
            min=0.0, max=1.0, step=0.01, value=0.3,
            marks=None, tooltip={"always_visible": False, "placement": "bottom"},
        ),

        # Graphs
        dcc.Graph(id="meat-estimation-plot", figure=meatEstimationPlot),
        dcc.Graph(id="beef-variance-plot", figure=beefVariancePlot),
        dcc.Graph(id="chicken-variance-plot", figure=chickenVariancePlot),
        dcc.Graph(id="ingredient-frequency-plot", figure=ingredientFrequencyPlot),
        dcc.Graph(id="quantity-per-ingredient-plot", figure=quantityPerIngredientPlot),
        dcc.Graph(id="top-selling-cats-plot", figure=topSellingCatsPlot),
        dcc.Graph(id="top-revenue-cats-plot", figure=topRevenueCatsPlot)
    ]
)


# CALLBACK: Update income plot
@app.callback(
    Output('income-plot', 'figure'),
    Input('month-dropdown', 'value'),
    Input('theme-toggle', 'value'),
)
def update_income_plot(selected_month, theme):
    if selected_month == 'all':
        month_sources = [
            "may.csv", "june.csv", "july.csv",
            "august.csv", "september.csv", "october.csv"
        ]
    else:
        month_sources = [f"{selected_month}.csv"]

    fig = createRevenuePlot(month_sources)
    fig.update_layout(template="plotly_dark" if theme == "dark" else "plotly_white")
    return fig


# CALLBACK: Update meat plots
@app.callback(
    [
        Output('slider-beef', 'value'),
        Output('slider-chicken', 'value'),
        Output('slider-pork', 'value'),
        Output('meat-estimation-plot', 'figure'),
        Output('beef-variance-plot', 'figure'),
        Output('chicken-variance-plot', 'figure'),
    ],
    [
        Input('slider-beef', 'value'),
        Input('slider-chicken', 'value'),
        Input('slider-pork', 'value'),
        Input('theme-toggle', 'value'),
    ]
)
def update_plots(beef_val, chicken_val, pork_val, theme):
    values = [beef_val, chicken_val, pork_val]
    total = sum(values)
    if total > 1.0:
        values = [v / total for v in values]
    beef_val, chicken_val, pork_val = values

    fig_meat, fig_beef, fig_chicken, _, _ = createMeatPlots(
        beefPercent=beef_val,
        chickenPercent=chicken_val,
        porkPercent=pork_val,
        month_sources=month_sources
    )

    # Apply theme to all graphs
    for fig in [fig_meat, fig_beef, fig_chicken]:
        fig.update_layout(template="plotly_dark" if theme == "dark" else "plotly_white")

    return beef_val, chicken_val, pork_val, fig_meat, fig_beef, fig_chicken


# CALLBACK: Global page styling
@app.callback(
    Output("page-container", "style"),
    Output("header-title", "style"),
    Input("theme-toggle", "value"),
)
def update_theme_styles(theme):
    if theme == "dark":
        page_style = {
            "backgroundColor": "#111111",
            "color": "#FFFFFF",
            "minHeight": "100vh",
            "padding": "20px",
        }
        header_style = {"textAlign": "center", "color": "#FFFFFF"}
    else:
        page_style = {
            "backgroundColor": "#FFFFFF",
            "color": "#000000",
            "minHeight": "100vh",
            "padding": "20px",
        }
        header_style = {"textAlign": "center", "color": "#000000"}

    return page_style, header_style


if __name__ == '__main__':
    app.run(debug=True)
