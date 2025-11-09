# Written by Kevin Eldho
# Formatted by Kyle Berzett

import pandas as pd
import plotly.express as px
import os

def createIngredientPlots ():

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
    # === Total Quantity Used per Ingredient (convert all to grams) ===
    conv_map = {
        'egg': 50,               # each egg ≈ 50g
        'chicken wing': 100,     # each wing ≈ 100g
        'chicken wings': 100,
        'ramen': 400,            # one ramen serving ≈ 400g
        'chicken thigh': 200,    # each thigh ≈ 200g
    }

    long_df['Ingredient_lower'] = long_df['Ingredient'].str.lower()

    def to_grams(row):
        for key, factor in conv_map.items():
            if key in row['Ingredient_lower']:
                return row['Quantity'] * factor
        return row['Quantity']

    def rename_with_g(row):
        name = row['Ingredient']
        # Replace any existing "(...)" with "(g)"
        name = pd.Series(name).str.replace(r"\s*\(.*?\)", "", regex=True).iloc[0]
        for key in conv_map.keys():
            if key in row['Ingredient_lower']:
                return f"{name.strip()} (g)"
        return name.strip()

    long_df['Quantity_grams'] = long_df.apply(to_grams, axis=1)
    long_df['Ingredient_grams'] = long_df.apply(rename_with_g, axis=1)

    ingredient_totals = (
        long_df.groupby('Ingredient_grams')['Quantity_grams']
        .sum()
        .reset_index()
        .sort_values('Quantity_grams', ascending=False)
    )

    fig2 = px.bar(
        ingredient_totals,
        x='Ingredient_grams',
        y='Quantity_grams',
        title="Total Quantity Used per Ingredient (All in Grams)",
        labels={'Quantity_grams': 'Total (grams)', 'Ingredient_grams': 'Ingredient'},
    )
    fig2.update_layout(
        xaxis_tickangle=90,
        template='plotly_white',
        height=600
    )

    return fig1, fig2