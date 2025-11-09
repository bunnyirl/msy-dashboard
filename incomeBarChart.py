import pandas as pd
import plotly.express as px
import os

month_sources = ["Data/may.csv",
                 "Data/june.csv",
                 "Data/july.csv",
                 "Data/august.csv",
                 "Data/september.csv",
                 "Data/october.csv",]


# Defining lists of months and their
# respective categorical incomes
months = []
grossMonthlyIncomes = []
lunchMenuMonthlyIncomes = []
allDayMenuMonthlyIncomes = []


for source in month_sources:

    # Creating a dataframe for each month to analyze
    # their incomes for each category
    df = pd.read_csv(source)
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

    # Adds the gross income to the list of monthly incomes as
    # well as the name of the month for clarity in the graph
    grossMonthlyIncomes.append(grossMonthlyIncome)
    months.append(os.path.splitext(os.path.basename(source))[0].capitalize())


# Special addition accounting for October since it has
# no determinable lunch menu or all-day menu incomes,
# so we claim its individual incomes are zero
lunchMenuMonthlyIncomes.append(0)
allDayMenuMonthlyIncomes.append(0)



# Creates a database of the months and their incomes
# df_income = pd.DataFrame({"Month": months, "Total Monthly Income": allDayMenuMonthlyIncomes})
# df_income = pd.DataFrame({"Month": months, "Total Monthly Income": lunchMenuMonthlyIncomes})
df_income = pd.DataFrame({"Month": months,
                          "Gross Monthly Income": grossMonthlyIncomes,
                          "Lunch Menu Income": lunchMenuMonthlyIncomes,
                          "All-Day Menu Income": allDayMenuMonthlyIncomes})

incomeGraph = px.bar(df_income,
                     x="Month",
                     y=["Lunch Menu Income", "All-Day Menu Income", "Gross Monthly Income"],
                     barmode='group')

incomeGraph.update_layout(title=dict(text="Various Income Totals from May to October", font=dict(size=24)))

incomeGraph.show()
