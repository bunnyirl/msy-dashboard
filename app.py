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


# --- WEBSITE LAYOUT (MODIFIED FOR SIDE-BY-SIDE GRAPHS) ---
app.layout = html.Div(
    style={'fontFamily': 'Visby Round, sans-serif', 'padding': '20px', 'backgroundColor': '#f4f4f9'},
    children=[

        html.H1(),

        #this Div will be controlled by assets/style.css and assets/script.js
        html.Div([
            #add the logo using html.Img.
            html.Img(
                src='/assets/麦_画板-1.png',
                id='app-logo'
                #all styles are now in assets/style.css
            ),
        ], id='app-header'),

        # ----------------- SECTION 1: REVENUE -----------------
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'center'}, children=[
            # Dropdown for month selection for the revenue graph
            html.Div(style={'width': '93%', 'padding': '10px', 'minWidth': '300px', 'align-items': 'center', 'justify-content': 'center'}, children=[
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
                    clearable=False,
                    style={'marginBottom': '15px'})
            ]),
            html.Div(style={'width': '93%', 'padding': '10px', 'minWidth': '300px', 'align-items': 'center', 'justify-content': 'center'}, children=[
                dcc.Graph(id="income-plot", figure=incomePlot)
            ]),
        ]),

        # ----------------- SECTION 2: MEAT ESTIMATION & VARIANCE -----------------
        html.H1(),
        html.H1(),

        # Sliders Container (3-Column Layout)
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap', 'align-content': 'center', 'justify-content': 'center', 'marginBottom': '20px', 'margin': 'auto'},
            children=[
                # Slider for beef
                html.Div(style={'width': 'calc(33% - 20px)', 'minWidth': '200px', 'padding': '10px'}, children=[
                    html.Label("Beef %", style={'fontWeight': 'bold'}),
                    dcc.Slider(
                        id='slider-beef', min=0.0, max=1.0, step=0.01, value=0.5,
                        marks=None, tooltip={"always_visible": False, "placement": "bottom"},
                    ),
                ]),

                # Slider for chicken
                html.Div(style={'width': 'calc(33% - 20px)', 'minWidth': '200px', 'padding': '10px'}, children=[
                    html.Label("Chicken %", style={'fontWeight': 'bold'}),
                    dcc.Slider(
                        id='slider-chicken', min=0.0, max=1.0, step=0.01, value=0.3,
                        marks=None, tooltip={"always_visible": False, "placement": "bottom"},
                    ),
                ]),

                # Slider for pork
                html.Div(style={'width': 'calc(33% - 20px)', 'minWidth': '200px', 'padding': '10px'}, children=[
                    html.Label("Pork %", style={'fontWeight': 'bold'}),
                    dcc.Slider(
                        id='slider-pork', min=0.0, max=1.0, step=0.01, value=0.2,
                        marks=None, tooltip={"always_visible": False, "placement": "bottom"},
                    ),
                ]),
            ]
        ),



        # Beef and Chicken Variance Plots (Side-by-Side)
        html.H3(),
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'center'},
            children=[
                html.Div(style={'width': '30%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="meat-estimation-plot", figure=meatEstimationPlot)
                ]),
                html.Div(style={'width': '30%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="beef-variance-plot", figure=beefVariancePlot)
                ]),
                html.Div(style={'width': '30%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="chicken-variance-plot", figure=chickenVariancePlot)
                ]),
            ]
        ),


        # ----------------- SECTION 3: INGREDIENTS -----------------
        html.H2(),

        # Ingredient Frequency and Quantity Plots (Side-by-Side)
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'center'},
            children=[
                html.Div(style={'width': '46%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="ingredient-frequency-plot", figure=ingredientFrequencyPlot)
                ]),
                html.Div(style={'width': '46%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="quantity-per-ingredient-plot", figure=quantityPerIngredientPlot)
                ]),
            ]
        ),


        # ----------------- SECTION 4: OCTOBER SALES -----------------
        html.H2(),

        # October Top Selling and Top Revenue Plots (Side-by-Side)
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'center'},
            children=[
                html.Div(style={'width': '46%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="top-selling-cats-plot", figure=topSellingCatsPlot)
                ]),
                html.Div(style={'width': '46%', 'padding': '10px', 'minWidth': '300px'}, children=[
                    dcc.Graph(id="top-revenue-cats-plot", figure=topRevenueCatsPlot)
                ]),
            ]
        ),

    ]
)









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
