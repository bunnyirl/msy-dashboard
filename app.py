# Written by Kyle Berzett
# Formatted by Kyle Berzett

from dash import Dash, html, dcc, Input, Output
from data_revenue import createRevenuePlot
from data_meatVariance import createMeatPlots
from data_ingredients import createIngredientPlots
from data_october import createOctoberPlots

# Initialize app
app = Dash(__name__)

# Ensure no white borders or background flashes
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

# Source files of monthly data
month_sources = [
    "may.csv",
    "june.csv",
    "july.csv",
    "august.csv",
    "september.csv",
    "october.csv",
]

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
    [
        html.H1("Mai Shan Yun Dashboard", id="page-title"),

        # Theme toggle (Light/Dark)
        html.Div(
            [
                html.Label("Theme:", id="theme-label"),
                dcc.RadioItems(
                    id="theme-toggle",
                    options=[
                        {"label": "Light", "value": "light"},
                        {"label": "Dark", "value": "dark"},
                    ],
                    value="light",
                    inline=True,
                    style={"margin": "10px"},
                ),
            ],
            style={"textAlign": "center"},
        ),

        # Month selection dropdown
        dcc.Dropdown(
            id="month-dropdown",
            options=[
                {"label": "All Months", "value": "all"},
                {"label": "May", "value": "may"},
                {"label": "June", "value": "june"},
                {"label": "July", "value": "july"},
                {"label": "August", "value": "august"},
                {"label": "September", "value": "september"},
                {"label": "October", "value": "october"},
            ],
            value="all",
            clearable=False,
        ),
        dcc.Graph(id="income-plot", figure=incomePlot),

        # Sliders for meat proportions
        html.Label("Beef %"),
        dcc.Slider(
            id="slider-beef",
            min=0.0,
            max=1.0,
            step=0.01,
            value=0.5,
            marks=None,
            tooltip={"always_visible": False, "placement": "bottom"},
        ),

        html.Label("Chicken %"),
        dcc.Slider(
            id="slider-chicken",
            min=0.0,
            max=1.0,
            step=0.01,
            value=0.3,
            marks=None,
            tooltip={"always_visible": False, "placement": "bottom"},
        ),

        html.Label("Pork %"),
        dcc.Slider(
            id="slider-pork",
            min=0.0,
            max=1.0,
            step=0.01,
            value=0.3,
            marks=None,
            tooltip={"always_visible": False, "placement": "bottom"},
        ),

        # All graphs
        html.Div(
            id="graphs-container",
            children=[
                dcc.Graph(id="meat-estimation-plot", figure=meatEstimationPlot),
                dcc.Graph(id="beef-variance-plot", figure=beefVariancePlot),
                dcc.Graph(id="chicken-variance-plot", figure=chickenVariancePlot),
                dcc.Graph(id="ingredient-frequency-plot", figure=ingredientFrequencyPlot),
                dcc.Graph(id="quantity-per-ingredient-plot", figure=quantityPerIngredientPlot),
                dcc.Graph(id="top-selling-cats-plot", figure=topSellingCatsPlot),
                dcc.Graph(id="top-revenue-cats-plot", figure=topRevenueCatsPlot),
            ],
        ),
    ],
    id="page-container",
    style={
        "backgroundColor": "#ffffff",
        "color": "#000000",
        "minHeight": "100vh",
        "padding": "20px",
        "margin": "0",
    },
)

# -------------------------------
# THEME CALLBACK
# -------------------------------
@app.callback(
    Output("page-container", "style"),
    Output("page-title", "style"),
    Output("theme-label", "style"),
    Output("income-plot", "figure"),
    Output("meat-estimation-plot", "figure"),
    Output("beef-variance-plot", "figure"),
    Output("chicken-variance-plot", "figure"),
    Output("ingredient-frequency-plot", "figure"),
    Output("quantity-per-ingredient-plot", "figure"),
    Output("top-selling-cats-plot", "figure"),
    Output("top-revenue-cats-plot", "figure"),
    Input("theme-toggle", "value"),
)
def update_theme(theme):
    """Switch between light and dark themes dynamically."""

    # Colors and templates
    if theme == "light":
        bg_color = "#ffffff"
        text_color = "#000000"
        plotly_template = "plotly_white"
    else:
        bg_color = "#121212"
        text_color = "#ffffff"
        plotly_template = "plotly_dark"

    # Update existing figures with new theme
    figs = [
        createRevenuePlot(month_sources),
        createMeatPlots(0.6, 0.2, 0.2, month_sources)[0],
        createMeatPlots(0.6, 0.2, 0.2, month_sources)[1],
        createMeatPlots(0.6, 0.2, 0.2, month_sources)[2],
        createIngredientPlots()[0],
        createIngredientPlots()[1],
        createOctoberPlots()[0],
        createOctoberPlots()[1],
    ]

    for f in figs:
        f.update_layout(
            template=plotly_template,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font_color=text_color,
        )

    page_style = {
        "backgroundColor": bg_color,
        "color": text_color,
        "minHeight": "100vh",
        "padding": "20px",
        "margin": "0",
        "transition": "background-color 0.5s, color 0.5s",
    }

    title_style = {"textAlign": "center", "color": text_color}
    label_style = {"color": text_color}

    return (
        page_style,
        title_style,
        label_style,
        *figs,  # Unpacks all 8 updated figures
    )

# -------------------------------
# EXISTING CALLBACKS (untouched)
# -------------------------------

@app.callback(
    Output("income-plot", "figure"),
    [Input("month-dropdown", "value")],
)
def update_income_plot(selected_month):
    """Update income plot based on selected month."""
    if selected_month == "all":
        month_sources = [
            "may.csv",
            "june.csv",
            "july.csv",
            "august.csv",
            "september.csv",
            "october.csv",
        ]
    else:
        month_sources = [f"{selected_month}.csv"]
    return createRevenuePlot(month_sources)


@app.callback(
    [
        Output("slider-beef", "value"),
        Output("slider-chicken", "value"),
        Output("slider-pork", "value"),
        Output("meat-estimation-plot", "figure"),
        Output("beef-variance-plot", "figure"),
        Output("chicken-variance-plot", "figure"),
    ],
    [
        Input("slider-beef", "value"),
        Input("slider-chicken", "value"),
        Input("slider-pork", "value"),
    ],
)
def update_plots(beef_val, chicken_val, pork_val):
    """Ensure meat % sliders sum to ≤ 1.0 and update plots."""
    values = [beef_val, chicken_val, pork_val]
    total = sum(values)
    if total > 1.0:
        values = [v / total for v in values]

    beef_val, chicken_val, pork_val = values
    fig_meat, fig_beef, fig_chicken, _, _ = createMeatPlots(
        beefPercent=beef_val,
        chickenPercent=chicken_val,
        porkPercent=pork_val,
        month_sources=month_sources,
    )
    return beef_val, chicken_val, pork_val, fig_meat, fig_beef, fig_chicken


if __name__ == "__main__":
    app.run(debug=True)
