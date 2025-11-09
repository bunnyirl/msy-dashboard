# Written by Kyle Berzett
# Formatted by Kyle Berzett

import os
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
from typing import List, Optional

def createRevenuePlot(
    month_sources: Optional[List[str]] = None,
    title: str = "Various Revenue Totals from May to October"
    )-> Figure:

    base_dir = os.path.dirname(__file__)

    # Defining lists of months and their
    # respective categorical incomes
    months = []
    grossMonthlyIncomes = []
    lunchMenuMonthlyIncomes = []
    allDayMenuMonthlyIncomes = []


    for source in month_sources:

        # Creating a dataframe for each month to analyze
        # their incomes for each category
        csv_path = os.path.join(base_dir, source)
        df = pd.read_csv(csv_path)
        grossMonthlyIncome = 0

        for index, amount in enumerate(df['Amount']):

            # Converts each income to a float and adds it to the
            # month's gross income
            income = float(df['Amount'][index][1:].replace(",", ""))

            grossMonthlyIncome += income


            # The October .csv file has different categories, so
            # it must be treated differently than the rest
            if 'october' not in source:

                paymentGroup = df['Group'][index]

                if paymentGroup == 'Lunch Menu':
                    lunchMenuMonthlyIncomes.append(income)

                elif paymentGroup == 'All Day Menu':
                    allDayMenuMonthlyIncomes.append(income)


        # Special addition accounting for October since it has
        # no determinable lunch menu or all-day menu incomes,
        # so we claim its individual incomes are zero
        if 'october' in source:
            lunchMenuMonthlyIncomes.append(0)
            allDayMenuMonthlyIncomes.append(0)


        # Adds the gross income to the list of monthly incomes as
        # well as the name of the month for clarity in the graph
        grossMonthlyIncomes.append(grossMonthlyIncome)
        months.append(os.path.splitext(os.path.basename(source))[0].capitalize())


    # Creates a database of the months and their incomes
    # df_income = pd.DataFrame({"Month": months, "Total Monthly Income": allDayMenuMonthlyIncomes})
    # df_income = pd.DataFrame({"Month": months, "Total Monthly Income": lunchMenuMonthlyIncomes})
    df_income = pd.DataFrame({"Month": months,
                              "Gross Monthly Revenue": grossMonthlyIncomes,
                              "Lunch Menu Revenue": lunchMenuMonthlyIncomes,
                              "All-Day Menu Revenue": allDayMenuMonthlyIncomes})

    incomeGraph = px.bar(df_income,
                         x="Month",
                         y=["Lunch Menu Revenue", "All-Day Menu Revenue", "Gross Monthly Revenue"],
                         barmode='group')

    incomeGraph.update_layout(title=dict(text=title, font=dict(size=24)))

    return incomeGraph
