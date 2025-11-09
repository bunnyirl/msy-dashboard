# Written by Kyle Berzett
# Formatted by Kyle Berzett

from dash import Dash, html, dcc, Input, Output
from data_revenue import createRevenuePlot
from data_meatVariance import createMeatPlots
from data_ingredients import createIngredientPlots
from data_october import createOctoberPlots

app = Dash(__name__)

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


#website layout
app.layout = [html.Div([
    #this Div will be controlled by assets/style.css and assets/script.js
    html.Div([
        #add the logo using html.Img.
        html.Img(
            src='/assets/麦_画板-1.png',
            id='app-logo'
            #all styles are now in assets/style.css
        ),
    ], id='app-header'), 
  
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
        value='all',  # default value
        clearable=False
    ),
    dcc.Graph(id="income-plot", figure=incomePlot),


    # Slider for beef
    html.Label("Beef %"),
    dcc.Slider(
        id='slider-beef',
        min=0.0,
        max=1.0,
        step=0.01,
        value=0.5,
        marks=None,
        tooltip={"always_visible": False, "placement": "bottom"},
    ),

    # Slider for chicken
    html.Label("Chicken %"),
    dcc.Slider(
        id='slider-chicken',
        min=0.0,
        max=1.0,
        step=0.01,
        value=0.3,
        marks=None,
        tooltip={"always_visible": False, "placement": "bottom"},
    ),

    html.Label("Pork %"),
    dcc.Slider(
        id='slider-pork',
        min=0.0,
        max=1.0,
        step=0.01,
        value=0.3,
        marks=None,
        tooltip={"always_visible": False, "placement": "bottom"},
    ),

    dcc.Graph(id="meat-estimation-plot", figure=meatEstimationPlot),
    dcc.Graph(id="beef-variance-plot", figure=beefVariancePlot),
    dcc.Graph(id="chicken-variance-plot", figure=chickenVariancePlot),
    dcc.Graph(id="ingredient-frequency-plot", figure=ingredientFrequencyPlot),
    dcc.Graph(id="quantity-per-ingredient-plot", figure=quantityPerIngredientPlot),
    dcc.Graph(id="top-selling-cats-plot", figure=topSellingCatsPlot),
    dcc.Graph(id="top-revenue-cats-plot", figure=topRevenueCatsPlot)

])]


@app.callback(
    Output('income-plot', 'figure'),
    [Input('month-dropdown', 'value')]
)
def update_income_plot(selected_month):
    # Decide which CSV file(s) to include based on the selected_month
    if selected_month == 'all':
        month_sources = [
            "may.csv",
            "june.csv",
            "july.csv",
            "august.csv",
            "september.csv",
            "october.csv"
        ]
    else:
        # single CSV: e.g. "august.csv" if selected_month == "august"
        month_sources = [f"{selected_month}.csv"]

    # Use your existing function to generate the plot:
    fig = createRevenuePlot(month_sources)
    return fig




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
    ]
)
def update_plots(beef_val, chicken_val, pork_val):
    values = [beef_val, chicken_val, pork_val]
    total = sum(values)

    # If the sum exceeds 1.0, proportionally reduce them so total becomes 1.0
    if total > 1.0:
        # Rescale each so sum = 1.0
        values = [v / total for v in values]

    # Unpack the rescaled values
    beef_val, chicken_val, pork_val = values

    # Generate the updated figures
    fig_meat, fig_beef, fig_chicken, _, _ = createMeatPlots(
        beefPercent=beef_val,
        chickenPercent=chicken_val,
        porkPercent=pork_val,
        month_sources=month_sources
    )

    return beef_val, chicken_val, pork_val, fig_meat, fig_beef, fig_chicken





if __name__ == '__main__':
    app.run(debug=True)



