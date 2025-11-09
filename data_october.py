# Written by Kevin Eldho
# Formatted by Kyle Berzett

import pandas as pd
import plotly.express as px
import os

def createOctoberPlots():

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "october.csv")

    octDF = pd.read_csv(csv_path)
    # Clean up dollar signs and commas in Amount
    octDF['Amount'] = octDF['Amount'].replace('[\$,]', '', regex=True).astype(float)

    # Clean up commas in Count before converting to int
    octDF['Count'] = octDF['Count'].replace(',', '', regex=True).astype(int)

    # === Top Selling Categories (by Count) ===
    sales_sorted = octDF.sort_values('Count', ascending=False)

    fig1 = px.bar(
        sales_sorted,
        x='Count',
        y='Category',
        orientation='h',
        title='Top Selling Categories in October',
        labels={'Count': 'Quantity Sold', 'Category': 'Category'},
        color='Count',
        color_continuous_scale='Reds'
    )
    fig1.update_layout(
        template='plotly_white',
        height=600,
        yaxis=dict(categoryorder='total ascending')
    )


    # === Top Revenue Categories (by Amount) ===
    revenue_sorted = octDF.sort_values('Amount', ascending=False)

    fig2 = px.bar(
        revenue_sorted,
        x='Amount',
        y='Category',
        orientation='h',
        title='Top Revenue Categories in October',
        labels={'Amount': 'Revenue ($)', 'Category': 'Category'},
        color='Amount',
        color_continuous_scale='Reds'
    )
    fig2.update_layout(
        template='plotly_white',
        height=600,
        yaxis=dict(categoryorder='total ascending')
    )

    return fig1, fig2



