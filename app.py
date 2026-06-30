import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="📊Business Sales Performance Analytics",
    layout="wide"
)


# -------------------------------
# Load Data
# -------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "dataset/cleaned1_superstore.csv"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"]
    )

    return df


df = load_data()



# -------------------------------
# Title
# -------------------------------
st.title("📊 Business Sales Performance Analytics Dashboard")
st.markdown(
    "Analyze Sales, Profit, Customers, Products, Shipping Performance, and Business Insights using interactive visualizations."
)
df.columns = df.columns.str.strip()

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.header("🔍 Filters")


region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)


category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)


year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Order Date"].dt.year.unique()),
    default=sorted(df["Order Date"].dt.year.unique())
)



# -------------------------------
# Filter Dataset
# -------------------------------

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order Date"].dt.year.isin(year))
]

# -------------------------------
# KPI Calculation
# -------------------------------

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()


profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)


avg_order_value = (
    total_sales / total_orders
    if total_orders != 0
    else 0
)

total_loss = filtered_df[filtered_df["Profit"]<0]['Profit'].sum()



# -------------------------------
# KPI Cards
# -------------------------------

col1, col2, col3, col4, col5, col6 = st.columns([1.3,1.3,1,1.2,1.2,1.3])

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "🛒 Total Orders",
    total_orders
)

col4.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

col5.metric(
    "💵 Average Order Value",
    f"${avg_order_value:,.2f}"
)

col6.metric(
    "📉 Total Loss",
    f"-${abs(total_loss):,.2f}"
)




# st.divider()

# -------------------------------
# Sales vs Profit Performance
# -------------------------------

st.markdown("---")

st.header(" Revenue vs Profit Performance")


monthly_compare = (
    filtered_df
    .groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )[["Sales", "Profit"]]
    .sum()
    .reset_index()
)


monthly_compare["Order Date"] = (
    monthly_compare["Order Date"]
    .astype(str)
)


fig = px.line(
    monthly_compare,
    x="Order Date",
    y=["Sales", "Profit"],
    markers=True,
    title="Monthly Sales and Profit Comparison"
)

fig.update_layout(
    hovermode="x unified"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# Sales & Profit Contribution Analysis
# -------------------------------

st.divider()

st.header("Sales & Profit Contribution Analysis")

# ==========================
# Row 1 : Region Charts
# ==========================

col1, col2 = st.columns(2)

# Sales Contribution by Region
with col1:

    st.subheader("Sales Contribution by Region (%)")

    sales_region = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        sales_region,
        names="Region",
        values="Sales",
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Profit Contribution by Region
with col2:

    st.subheader("Profit Contribution by Region (%)")

    profit_region = (
        filtered_df
        .groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        profit_region,
        names="Region",
        values="Profit",
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================
# Row 2 : Category Charts
# ==========================

col3, col4 = st.columns(2)

# Sales Contribution by Category
with col3:

    st.subheader("Sales Contribution by Category (%)")

    sales_category = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        sales_category,
        names="Category",
        values="Sales",
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Profit Contribution by Category
with col4:

    st.subheader("Profit Contribution by Category (%)")

    profit_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        profit_category,
        names="Category",
        values="Profit",
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
# -------------------------------
# Product Analysis
# -------------------------------

st.divider()

st.header(" Product Performance Analysis")


col1, col2 = st.columns(2)


# Top Products by Sales

with col1:

    top_products = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


top_products["Product Name"] = top_products["Product Name"].apply(
    lambda x: "<br>".join(textwrap.wrap(str(x), 20))
)



fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales"
    )

fig.update_layout(
    height=750,
    yaxis={'categoryorder': 'total ascending'}
)

st.plotly_chart(
        fig,
        use_container_width=True
    )



# Loss Making Products

with col2:

    loss_products = (
        filtered_df
        .groupby("Product Name")["Profit"]
        .sum()
        .sort_values()
        .head(10)
        .reset_index()
    )
loss_products["Product Name"] = loss_products["Product Name"].apply(
    lambda x: "<br>".join(textwrap.wrap(str(x), 20))
)

fig = px.bar(
        loss_products,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Loss Making Products"
    )

fig.update_layout(
    height=650,
    yaxis={'categoryorder': 'total ascending'}
)
st.plotly_chart(
        fig,
        use_container_width=True
    )



# -------------------------------
# Customer Analysis
# -------------------------------

st.divider()

st.header(" Customer Analysis")


col1, col2 = st.columns(2)



# Top Customers by Sales

with col1:

    st.subheader("Top 10 Customers by Sales")


    customer_sales = (
        filtered_df
        .groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


    fig = px.bar(
        customer_sales,
        x="Sales",
        y="Customer Name",
        orientation="h"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# Top Customers by Profit

with col2:

    st.subheader("Top 10 Customers by Profit")


    customer_profit = (
        filtered_df
        .groupby("Customer Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


    fig = px.bar(
        customer_profit,
        x="Profit",
        y="Customer Name",
        orientation="h"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# -------------------------------
# Customer Segment Analysis
# -------------------------------

st.subheader(" Customer Segment Contribution (%)")


segment_sales = (
    filtered_df
    .groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)


fig = px.pie(
    segment_sales,
    names="Segment",
    values="Sales",
    hole=0.4
)


fig.update_traces(
   textinfo="label+percent",
textposition="inside"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -------------------------------
# Sales & Profit Trend Analysis
# -------------------------------

st.divider()

st.header("📈 Sales & Profit Trend Analysis")

col1, col2 = st.columns(2)

# ==========================
# Monthly Sales Trend
# ==========================
with col1:

    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        filtered_df
        .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# Monthly Profit Trend
# ==========================
with col2:

    st.subheader("Monthly Profit Trend")

    monthly_profit = (
        filtered_df
        .groupby(filtered_df["Order Date"].dt.to_period("M"))["Profit"]
        .sum()
        .reset_index()
    )

    monthly_profit["Order Date"] = monthly_profit["Order Date"].astype(str)

    fig = px.line(
        monthly_profit,
        x="Order Date",
        y="Profit",
        markers=True,
        title="Monthly Profit Trend"
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -------------------------------
# Shipping Analysis
# -------------------------------

st.divider()

st.header("Shipping Performance Analysis")


shipping = (
    filtered_df
    .groupby("Ship Mode")["Delivery Time"]
    .mean()
    .reset_index()
)



fig = px.pie(
    shipping,
    names="Ship Mode",
    values="Delivery Time",
    hole=0.4,
    title="Average Delivery Time Contribution (%)"
)


fig.update_traces(
   textinfo="label+percent",
textposition="inside"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -------------------------------
# Dynamic Business Insights
# -------------------------------

st.divider()

st.header(" Business Insights")



# Best Category

best_category = (
    filtered_df
    .groupby("Category")["Profit"]
    .sum()
    .idxmax()
)


best_category_profit = (
    filtered_df
    .groupby("Category")["Profit"]
    .sum()
    .max()
)

# Best Region

best_region = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .idxmax()
)


best_region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .max()
)



# Worst Product

worst_product = (
    filtered_df
    .groupby("Product Name")["Profit"]
    .sum()
    .idxmin()
)


worst_product_loss = (
    filtered_df
    .groupby("Product Name")["Profit"]
    .sum()
    .min()
)



# Best Customer

best_customer = (
    filtered_df
    .groupby("Customer Name")["Profit"]
    .sum()
    .idxmax()
)


best_customer_profit = (
    filtered_df
    .groupby("Customer Name")["Profit"]
    .sum()
    .max()
)



best_product = filtered_df.groupby("Product Name")["Sales"].sum()
best_product_name = best_product.idxmax()
best_product_sales = best_product.max()

profit_region = filtered_df.groupby("Region")["Profit"].sum()
profit_region_name = profit_region.idxmax()
profit_region_value = profit_region.max()

fastest_ship = filtered_df.groupby("Ship Mode")["Delivery Time"].mean()
fastest_ship_mode = fastest_ship.idxmin()
fastest_ship_days = fastest_ship.min()

avg_discount = filtered_df["Discount"].mean() * 100


# st.divider()
# st.header(" Business Insights")
best_profit_region = (
    filtered_df
    .groupby("Region")["Profit"]
    .sum()
)

best_profit_region_name = best_profit_region.idxmax()

best_profit_region_value = best_profit_region.max()

st.markdown(f"""
- **{best_category}** is the most profitable category, generating ${best_category_profit:,.2f} in profit.

- **{best_product_name}** is the highest-selling product with total sales of ${best_product_sales:,.2f}.

- **{best_profit_region_name}** emerged as the most profitable region, contributing a total profit of **${best_profit_region_value:,.2f}**.
- **{best_customer}** is the most valuable customer, contributing ${best_customer_profit:,.2f} in profit.

- **{worst_product}** incurred the highest loss (**${abs(worst_product_loss):,.2f}**), indicating a need to review pricing, discounting, or inventory decisions.

- The business achieved an overall **profit margin of {profit_margin:.2f}%**.

- **{fastest_ship_mode}** is the fastest shipping method with an average delivery time of **{fastest_ship_days:.1f} days**.

- The average discount offered across all orders is **{avg_discount:.2f}%**, which should be monitored to maintain healthy profit margins.

- High-performing products and regions should receive priority in inventory allocation and marketing investments.

- Regular analysis of monthly sales and profit trends can support better forecasting and strategic decision-making.
""")


st.divider()

st.caption(
    "Business Sales Performance Analytics Dashboard | Built using Python, Streamlit, Pandas, and Plotly"
)



