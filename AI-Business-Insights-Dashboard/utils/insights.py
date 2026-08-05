import pandas as pd


def generate_insights(df):

    insights = []

    # Total Sales
    if "Sales" in df.columns:
        total_sales = df["Sales"].sum()
        insights.append(f"💰 Total Sales : ${total_sales:,.2f}")

    # Highest Category
    if "Category" in df.columns and "Sales" in df.columns:
        category = (
            df.groupby("Category")["Sales"]
            .sum()
            .idxmax()
        )
        insights.append(f"🏆 Highest Selling Category : {category}")

    # Highest Region
    if "Region" in df.columns and "Sales" in df.columns:
        region = (
            df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )
        insights.append(f"🌍 Highest Revenue Region : {region}")

    # Best Product
    if "Product Name" in df.columns and "Sales" in df.columns:
        product = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .idxmax()
        )
        insights.append(f"🔥 Best Selling Product : {product}")

    # Total Orders
    insights.append(f"📦 Total Records : {len(df)}")

    # Missing Values
    missing = df.isnull().sum().sum()
    insights.append(f"⚠ Missing Values : {missing}")

    return insights