# Written by Jeremiah Johnson
# Formatted by Kyle Berzett

import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
from typing import List, Optional

# Created by Jeremiah Johnson

def createMeatPlots(beefPercent,
                    chickenPercent,
                    porkPercent,
                    month_sources: Optional[List[str]] = None):

    pio.templates.default = "plotly_white"

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, month_sources[5])

    octoberDF = pd.read_csv(csv_path)

    meatItems = ["Tossed Rice Noodle", "Tossed Ramen", "Ramen", "Rice Noodle"]

    totalCount = 0

    friedRiceCount = 0
    for idx, row in octoberDF.iterrows():
        if row["Category"] == "Fried Rice":
            friedRiceCount = float(row["Count"].replace(",", ""))
        
        if row["Category"] in meatItems:
            count = float(row["Count"].replace(",", ""))
            totalCount += count

    beefCount = totalCount * beefPercent
    chickenCount = totalCount * chickenPercent
    porkCount = totalCount * porkPercent
            
    beefCountFR = friedRiceCount * beefPercent
    chickenCountFR = friedRiceCount * chickenPercent
    porkCountFR = friedRiceCount * porkPercent

    # Hardcoded from ingredient data, 140g per ingredient (fried rice 100g)
    beefLbsSold = (beefCount * 140 / 453.6) + (beefCountFR * 100 / 453.6)
    chickenLbsSold = (chickenCount * 140 / 453.6) + (chickenCountFR * 100 / 453.6)
    porkLbsSold = (porkCount * 140 / 453.6) + (porkCountFR * 100 / 453.6)

    # Hardcoded from shipments data (120lbs weekly for beef, 80lbs weekly for chicken)
    beefPurchasedLbsWeekly = 120
    beefPurchasedLbsDaily = beefPurchasedLbsWeekly / 7
    beefPurchasedLbsMonthly = beefPurchasedLbsDaily * 31

    chickenPurchasedLbsWeekly = 80
    chickenPurchasedLbsDaily = chickenPurchasedLbsWeekly / 7
    chickenPurchasedLbsMonthly = chickenPurchasedLbsDaily * 31

    beefVariance = beefPurchasedLbsMonthly - beefLbsSold
    chickenVariance = chickenPurchasedLbsMonthly - chickenLbsSold

    meatValues = [beefLbsSold, chickenLbsSold, porkLbsSold]
    meatLabels = ["Beef", "Chicken", "Pork"]

    fig1 = px.pie(values=meatValues, labels=meatLabels, color=meatLabels)

    fig1.update_layout(
        title="Estimated Meat Sold (lbs)",
        xaxis_title="Meat",
        yaxis_title="Meat Sold (lbs)"
    )

    labelsBeef = ["Purchased Beef", "Sold Beef"]
    valuesBeef = [beefPurchasedLbsMonthly, beefLbsSold]

    fig2 = px.bar(x=labelsBeef, y=valuesBeef, color=labelsBeef)


    fig2.update_layout(
        title="Beef Variance Visualization (lbs)",
        xaxis_title="Category",
        yaxis_title="Beef (lbs)"
    )

    labelsChicken = ["Purchased Chicken", "Sold Chicken"]
    valuesChicken = [chickenPurchasedLbsMonthly, chickenLbsSold]

    fig3 = px.bar(x=labelsChicken, y=valuesChicken, color=labelsChicken)

    fig3.update_layout(
        title="Chicken Variance Visualization (lbs)",
        xaxis_title="Category",
        yaxis_title="Chicken (lbs)"
    )

    # fig 1 (plot) is meat sold per type
    # fig 2 (plot) shows surplus/deficit in beef
    # fig 3 (plot) shows surplus/deficit in chicken
    # beefVariance (image) is surplus/deficit of beef in lbs
    # chickenVariance (image) is surplus/deficit of chicken in lbs
    return fig1, fig2, fig3, beefVariance, chickenVariance