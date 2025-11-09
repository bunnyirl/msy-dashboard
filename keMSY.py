import pandas as pd
import plotly.express as px
import os

def ingredientPlots ():

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "ingredients.csv")

    intdf = pd.read_csv(csv_path, sep=None, engine='python')
    intdf = intdf.fillna(0)
    long_df = intdf.melt(
    id_vars=['Item name'],
    var_name='Ingredient',
    value_name='Quantity'
    )

    # Drop zero or null quantities
    long_df = long_df[long_df['Quantity'] > 0]

    # === Frequency of Ingredient Usage Across Menu Items ===
    ingredientCount = long_df['Ingredient'].value_counts().reset_index()
    ingredientCount.columns = ['Ingredient', 'UsageCount']

    fig1 = px.bar(
        ingredientCount,
        x='Ingredient',
        y='UsageCount',
        title="Frequency of Ingredient Usage Across Menu Items",
        labels={'UsageCount': 'Number of Menu Items Using It'},
    )
    fig1.update_layout(
        xaxis_tickangle=90,
        template='plotly_white',
        height=600
    )
    # === Total Quantity Used per Ingredient ===
    ingredient_totals = (
        long_df.groupby('Ingredient')['Quantity']
        .sum()
        .reset_index()
        .sort_values('Quantity', ascending=False)
    )

    fig2 = px.bar(
        ingredient_totals,
        x='Ingredient',
        y='Quantity',
        title="Total Quantity Used per Ingredient",
        labels={'Quantity': 'Total Quantity (sum across menu items)'},
    )
    fig2.update_layout(
        xaxis_tickangle=90,
        template='plotly_white',
        height=600
    )
    return fig1, fig2

def octPlots():

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



