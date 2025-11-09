import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"

beefPercent = 0.6
chickenPercent = 0.2
porkPercent = 0.2

octoberDF = pd.read_csv("october.csv")
shipmentDF = pd.read_csv("shipments.csv")
ingredientDF = pd.read_csv("ingredients.csv")

for idx, row in octoberDF.iterrows():
    count = float(row["Count"].replace(",", ""))
    sales = float(row["Amount"].replace("$", "").replace(",", ""))

meatItems = ["Tossed Rice Noodle", "Tossed Ramen", "Ramen", "Rice Noodle"]

beefCount = 0
chickenCount = 0
porkCount = 0
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

beefLbsSold = (beefCount * 140 / 453.6) + (beefCountFR * 100 / 453.6)
chickenLbsSold = (chickenCount * 140 / 453.6) + (chickenCountFR * 100 / 453.6)
porkLbsSold = (porkCount * 140 / 453.6) + (porkCountFR * 100 / 453.6)

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

fig1 = go.Figure(data=[
    go.Bar(x=meatLabels, y=meatValues, marker_color=['red', 'orange', 'pink'])
])

fig1.update_layout(
    title="Estimated Meat Sold (lbs)",
    xaxis_title="Meat",
    yaxis_title="Meat Sold (lbs)"
)
fig1.write_image("meatsold.png", scale=3)

labelsBeef = ["Purchased Beef", "Sold Beef"]
valuesBeef = [beefPurchasedLbsMonthly, beefLbsSold]

fig2 = go.Figure(data=[
    go.Bar(x=labelsBeef, y=valuesBeef, marker_color=['red', 'blue'])
])

fig2.update_layout(
    title="Beef Variance Visualization (lbs)",
    xaxis_title="Category",
    yaxis_title="Beef (lbs)"
)

fig2.write_image("beefvariance.png", scale=3)

labelsChicken = ["Purchased Chicken", "Sold Chicken"]
valuesChicken = [chickenPurchasedLbsMonthly, chickenLbsSold]

fig3 = go.Figure(data=[
    go.Bar(x=labelsChicken, y=valuesChicken, marker_color=['green', 'orange'])
])

fig3.update_layout(
    title="Chicken Variance Visualization (lbs)",
    xaxis_title="Category",
    yaxis_title="Chicken (lbs)"
)


fig3.write_image("chickenvariance.png", scale=3)
