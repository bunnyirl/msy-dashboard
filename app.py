# Written by Kyle Berzett

from dash import Dash, html, dcc
from incomeBarChart import createIncomeBarChart
from msy2 import meatVarianceCharts
from keMSY import ingredientPlots, octPlots

app = Dash()

# Source files of monthly data
month_sources = ["may.csv",
                 "june.csv",
                 "july.csv",
                 "august.csv",
                 "september.csv",
                 "october.csv",]

# Jeremiah's
fig1, fig2, fig3, beef, chicken = meatVarianceCharts(0.0, 0.5, 0.5, month_sources)


# Kevin's
fig4, fig5 = ingredientPlots()
fig6, fig7 = octPlots()


app.layout = [html.Div([
    html.H1("Mai Shan Yun Dashboard"),
    dcc.Graph(id="income-bar-chart", figure=createIncomeBarChart(month_sources)),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7)

])]

if __name__ == '__main__':
    app.run(debug=True)
