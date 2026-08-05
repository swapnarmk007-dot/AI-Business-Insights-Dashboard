import pandas as pd
import plotly.express as px


# =====================================================
# Sales by Category
# =====================================================
def sales_by_category(df):

    if "Category" not in df.columns or "Sales" not in df.columns:
        return None

    data = df.groupby("Category")["Sales"].sum().reset_index()

    fig = px.bar(
        data,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    return fig.to_html(full_html=False)


# =====================================================
# Sales Trend
# =====================================================
def sales_trend(df):

    if "Order Date" not in df.columns or "Sales" not in df.columns:
        return None

    temp = df.copy()

    temp["Order Date"] = pd.to_datetime(
        temp["Order Date"],
        errors="coerce"
    )

    temp = temp.dropna(subset=["Order Date"])

    trend = temp.groupby("Order Date")["Sales"].sum().reset_index()

    fig = px.line(
        trend,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Sales Trend"
    )

    return fig.to_html(full_html=False)


# =====================================================
# Region-wise Sales
# =====================================================
def region_sales(df):

    if "Region" not in df.columns or "Sales" not in df.columns:
        return None

    data = df.groupby("Region")["Sales"].sum().reset_index()

    fig = px.pie(
        data,
        names="Region",
        values="Sales",
        title="Region-wise Sales"
    )

    return fig.to_html(full_html=False)


# =====================================================
# Top Products
# =====================================================
def top_products(df):

    if "Product Name" not in df.columns or "Sales" not in df.columns:
        return None

    data = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        title="Top 10 Products"
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )

    return fig.to_html(full_html=False)


# =====================================================
# Sales by Segment
# =====================================================
def sales_by_segment(df):

    if "Segment" not in df.columns:
        return None

    data = df.groupby("Segment").size().reset_index(name="Count")

    fig = px.pie(
        data,
        names="Segment",
        values="Count",
        title="Sales by Segment"
    )

    return fig.to_html(full_html=False)


# =====================================================
# Profit by Category
# =====================================================
def profit_by_category(df):

    if "Category" not in df.columns:
        return None

    if "Profit" not in df.columns:
        return None

    data = df.groupby("Category")["Profit"].sum().reset_index()

    fig = px.bar(
        data,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category"
    )

    return fig.to_html(full_html=False)


# =====================================================
# Top Customers
# =====================================================
def top_customers(df):

    if "Customer Name" not in df.columns:
        return None

    if "Sales" not in df.columns:
        return None

    data = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Sales",
        y="Customer Name",
        orientation="h",
        color="Sales",
        title="Top 10 Customers"
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )

    return fig.to_html(full_html=False)
def correlation_heatmap(df):

    import plotly.express as px

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap"
    )

    return fig.to_html(full_html=False)