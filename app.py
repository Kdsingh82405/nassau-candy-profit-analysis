import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    layout="wide"
)
# -------------------------------------------------
# Custom Styling
# -------------------------------------------------
import numpy as np

# ✅ ADD HERE
def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(size=13),
    )
    fig.update_traces(marker_line_width=0)
    return fig

st.markdown("""
<style>

/* ----------- Main Background ----------- */
.main {
    background: linear-gradient(135deg, #f8fafc, #eef2ff);
}

/* ----------- Titles ----------- */
h1 {
    color: #1e293b;
    font-weight: 700;
}

h2, h3 {
    color: #334155;
    font-weight: 600;
}

/* ----------- KPI Cards ----------- */
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #6366f1;
    transition: 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.12);
}

/* KPI Value */
[data-testid="stMetricValue"] {
    font-size: 22px;
    font-weight: bold;
    color: #111827;
}

/* KPI Label */
[data-testid="stMetricLabel"] {
    color: #6b7280;
}

/* ----------- Sidebar ----------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1f2937);
    border-right: 1px solid #374151;
}

section[data-testid="stSidebar"] label {
    color: #e5e7eb !important;
    font-weight: 500;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f9fafb;
}
/* ===== PREMIUM SLIDER DESIGN ===== */

/* Only fix text visibility */
div[data-baseweb="slider"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Fix min/max labels */
div[data-testid="stTickBarMin"],
div[data-testid="stTickBarMax"] {
    color: #ffffff !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Slider hover effect */
div[data-baseweb="slider"] div[role="slider"]:hover {
    transform: scale(1.2);
    transition: 0.2s ease;
}

/* Slider value text (69) */
div[data-baseweb="slider"] span {
    color: #f87171 !important;
    font-weight: 700 !important;
}
/* ----------- Buttons ----------- */
.stDownloadButton > button {
    background: linear-gradient(90deg, #6366f1, #4f46e5);
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
    border: none;
    transition: 0.3s;
}

.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #4338ca);
    transform: scale(1.05);
}

/* ----------- Tables ----------- */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

/* ----------- Alerts ----------- */
.stAlert {
    border-radius: 12px;
}

/* ----------- Section Spacing ----------- */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ----------- Divider ----------- */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #c7d2fe, transparent);
    margin: 25px 0;
}
            
/* ===== Tabs Container ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 30px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 10px;
}

/* ===== Individual Tabs ===== */
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
    color: #6b7280;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

/* ===== Hover Effect ===== */
.stTabs [data-baseweb="tab"]:hover {
    color: #4f46e5;
    background-color: #eef2ff;
}

/* ===== Active Tab ===== */
.stTabs [aria-selected="true"] {
    color: #4f46e5 !important;
    border-bottom: 3px solid #4f46e5;
    background-color: #eef2ff;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/Nassau Candy Distributor.csv")
    return df

df = load_data()

# -------------------------------------------------
# Data Cleaning
# -------------------------------------------------

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

for col in ["Sales","Gross Profit","Units","Cost"]:
    df[col] = pd.to_numeric(df[col],errors="coerce")

df = df[df["Sales"] > 0]
df = df[df["Gross Profit"].notna()]

df["Units"] = df["Units"].replace(0,np.nan)
df["Units"] = df["Units"].fillna(1)

df["Product Name"] = df["Product Name"].astype(str).str.strip()
df["Division"] = df["Division"].astype(str).str.strip()

# -------------------------------------------------
# KPI Calculations
# -------------------------------------------------

df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()

df["Revenue Contribution %"] = df["Sales"] / total_sales * 100
df["Profit Contribution %"] = df["Gross Profit"] / total_profit * 100

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.title("🔎 Filter Controls")
st.sidebar.caption("Use filters to explore product profitability and margin performance.")

date_range = st.sidebar.date_input(
"Select Date Range",
value=(df["Order Date"].min(),df["Order Date"].max())
)

division = st.sidebar.selectbox(
"Division",
["All"] + sorted(df["Division"].dropna().unique())
)

region = st.sidebar.selectbox(
"Region",
["All"] + sorted(df["Region"].dropna().unique())
)

margin_threshold = st.sidebar.slider("Minimum Margin %",0,100,0)

product_search = st.sidebar.text_input("Search Product")

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------

df_filtered = df.copy()

if len(date_range)==2:
    start,end=date_range
    df_filtered = df_filtered[
        (df_filtered["Order Date"]>=pd.to_datetime(start)) &
        (df_filtered["Order Date"]<=pd.to_datetime(end))
    ]

if division!="All":
    df_filtered=df_filtered[df_filtered["Division"]==division]

if region!="All":
    df_filtered=df_filtered[df_filtered["Region"]==region]

df_filtered = df_filtered[df_filtered["Gross Margin %"]>=margin_threshold]

if product_search:
    df_filtered=df_filtered[
        df_filtered["Product Name"].str.contains(product_search,case=False,na=False)
    ]

if df_filtered.empty:
    st.error("❌ No data matches your filters. Try adjusting filters.")
    st.stop()

if df_filtered["Sales"].sum() == 0:
    st.warning("No sales data available for selected filters")


# -------------------------------------------------
# Dashboard Title
# -------------------------------------------------

st.title("🍬 Nassau Candy Profitability Dashboard")

st.markdown("""
This dashboard analyzes **product profitability and margin performance**
for Nassau Candy Distributor. It identifies profitable products,
margin risks, and division-level financial efficiency.
""")

# -------------------------------------------------
# KPI Metrics
# -------------------------------------------------

total_sales_filtered = df_filtered["Sales"].sum()
total_profit_filtered = df_filtered["Gross Profit"].sum()

gross_margin = (total_profit_filtered / total_sales_filtered * 100) if total_sales_filtered != 0 else 0
profit_per_unit = (total_profit_filtered / df_filtered["Units"].sum()) if df_filtered["Units"].sum() != 0 else 0
revenue_contribution = df_filtered["Sales"].sum()/df["Sales"].sum()*100
profit_contribution = df_filtered["Gross Profit"].sum()/df["Gross Profit"].sum()*100
margin_volatility = df_filtered["Gross Margin %"].std()

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("Gross Margin (%)",f"{gross_margin:.2f}%",delta="Excellent" if gross_margin > 60 else "Good" if gross_margin > 40 else "Low")
k2.metric("Profit per Unit",f"${profit_per_unit:,.2f}",delta="High" if profit_per_unit > 5 else "Average" if profit_per_unit > 2 else "Low")
k3.metric("Revenue Contribution",f"{revenue_contribution:.2f}%",delta="High Impact" if revenue_contribution > 50 else "Moderate" if revenue_contribution > 20 else "Low")
k4.metric("Profit Contribution",f"{profit_contribution:.2f}%",delta="Strong" if profit_contribution > 50 else "Moderate" if profit_contribution > 20 else "Weak")
k5.metric("Margin Volatility",f"{margin_volatility:.2f}",delta="High Risk" if margin_volatility > 20 else "Moderate" if margin_volatility > 10 else "Stable")
st.divider()

# -------------------------------------------------
# TABS SECTIONS
# -------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Product Profitability Overview",
    "🏭 Division Performance Dashboard",
    "💸 Cost & Margin Diagnostics",
    "📊 Profit Concentration Analysis"
])
# -------------------------------------------------
# Product Profitability
# -------------------------------------------------
with tab1:
    st.subheader("📦 Product-level Margin & Profitability Analysis")

    product_perf = (
    df_filtered.groupby("Product Name")
    .agg(
    Sales=("Sales","sum"),
    Profit=("Gross Profit","sum"),
    Units=("Units","sum"),
    Margin=("Gross Margin %","mean")
    )
    .reset_index()
    )

    top_profit = product_perf.sort_values("Profit",ascending=False)

    fig1 = px.bar(
        top_profit.head(20),
        x="Product Name",
        y="Profit",
        title=None,
        color="Profit",
        text_auto=True,
        labels={"Profit": "Total Profit ($)"},
        color_continuous_scale="greens",
        hover_data={"Sales": ":,.0f", "Margin": ":.2f%"}
    )
    fig1 = style_chart(fig1)
    st.plotly_chart(fig1,use_container_width=True)
    st.divider()
# -------------------------------------------------
# 🏆 Top 5 vs 🚨 Bottom 5 Products (FINAL)
# -------------------------------------------------

    st.subheader("🏆 Top 5 vs 🚨 Bottom 5 Products")

    product_perf = (
        df_filtered.groupby("Product Name")
        .agg(
            Sales=("Sales","sum"),
            Profit=("Gross Profit","sum"),
            Units=("Units","sum"),
            Margin=("Gross Margin %","mean")
        )
        .reset_index()
    )
    top5 = product_perf.sort_values("Profit", ascending=False).head(5)
    bottom5 = product_perf.sort_values("Profit", ascending=True).head(5)

    c1, c2 = st.columns(2)

    # --------- TOP 5 ------------
    with c1:
        fig_top = px.bar(
            top5.sort_values("Profit"),
            y="Product Name",
            x="Profit",
            orientation="h",
            color="Profit",
            text="Profit",
            color_continuous_scale="Greens"
        )

        fig_top.update_layout(
            title=None,
            margin=dict(l=80, r=80, t=30, b=30)
        )

        fig_top.update_traces(
            textposition="outside",
            texttemplate='%{x:.0f}'
        )

        # Fix scaling
        fig_top.update_xaxes(range=[0, top5["Profit"].max() * 1.2])

        fig_top = style_chart(fig_top)
        st.plotly_chart(fig_top, use_container_width=True)

    # ------------ BOTTOM 5 -----------
    with c2:
        fig_bottom = px.bar(
            bottom5.sort_values("Profit"),
            y="Product Name",
            x="Profit",
            orientation="h",
            color="Profit",
            text="Profit",
            color_continuous_scale=["#fee2e2","#f87171","#dc2626"]
        )

        fig_bottom.update_layout(
            title=None,
            margin=dict(l=80, r=80, t=30, b=30)
        )

        fig_bottom.update_traces(
            textposition="outside",
            texttemplate='%{x:.2f}'
        )
        fig_bottom.update_xaxes(range=[0, bottom5["Profit"].max() * 1.5])
        fig_bottom = style_chart(fig_bottom)
        st.plotly_chart(fig_bottom, use_container_width=True)
    st.warning("Bottom products are dragging overall profitability. Review pricing or discontinue.")
    st.divider()
# -------------------------------------------------
# Profit Contribution Pie
# -------------------------------------------------

    st.subheader("Profit Contribution Analysis")

    fig_pie = px.pie(
    top_profit.head(10),
    values="Profit",
    names="Product Name",
    hole=0.5,
    title=None
    )
    st.plotly_chart(fig_pie,use_container_width=True)
    st.divider()
# -------------------------------------------------
# Product Category Segmentation
# -------------------------------------------------

    high_profit_high_margin = product_perf[
    (product_perf["Profit"]>product_perf["Profit"].median()) &
    (product_perf["Margin"]>product_perf["Margin"].median())
    ]

    high_sales_low_margin = product_perf[
    (product_perf["Sales"]>product_perf["Sales"].median()) &
    (product_perf["Margin"]<product_perf["Margin"].median())
    ]

    st.subheader("💰 High Profit & High Margin Products")

    fig_high = px.bar(
        high_profit_high_margin.sort_values("Profit", ascending=True),
        y="Product Name",
        x="Profit",
        orientation="h",
        title=None,
        color="Profit",
        color_continuous_scale="Greens",
        text="Profit"
    )

    fig_high.update_layout(
        yaxis_title="",
        xaxis_title="Profit ($)"
    )

    st.plotly_chart(fig_high, use_container_width=True)
    st.divider()
# ---------------------------------------
    st.subheader("⚠️ High Sales but Low Margin Products (Risk Analysis)")

    fig_low = px.bar(
        high_sales_low_margin.sort_values("Margin"),
        y="Product Name",
        x="Margin",
        orientation="h",
        title=None,
        color="Margin",
        color_continuous_scale=["#fee2e2","#f87171","#dc2626","#7f1d1d"],
        text="Margin"
    )

    fig_low.update_layout(
        yaxis_title="",
        xaxis_title="Margin (%)"
    )

    st.plotly_chart(fig_low, use_container_width=True)
# -------------------------------------------------
# Division Performance Dashboard
# -------------------------------------------------
with tab2:
    st.divider()
    st.subheader("🏭 Revenue vs Profit Comparison by Division")

    division_perf = (
    df_filtered.groupby("Division")
    .agg(
    Revenue=("Sales","sum"),
    Profit=("Gross Profit","sum"),
    Avg_Margin=("Gross Margin %","mean")
    )
    .reset_index()
    )

    fig2 = px.bar(
        division_perf,
        x="Division",
        y=["Revenue","Profit"],
        barmode="group",
        title=None,
        labels={
            "value": "Amount ($)",
            "variable": "Metric"
        }
    )

    fig2 = style_chart(fig2)
    st.plotly_chart(fig2,use_container_width=True)
    st.divider()
# -------------------------------------------------
# Average Margin by Division
# -------------------------------------------------
    st.subheader("📊 Average Margin by Division")
    fig3 = px.bar(
    division_perf,
    x="Division",
    y="Avg_Margin",
    title=None
    )
    fig3 = style_chart(fig3)
    st.plotly_chart(fig3,use_container_width=True)
    st.divider()
# -------------------------------------------------
# Margin Distribution by Division
# -------------------------------------------------
    st.subheader("📈 Margin Distribution by Division")
    fig_margin_div = px.box(
        df_filtered,
        x="Division",
        y="Gross Margin %",
        title=None
    )
    st.plotly_chart(fig_margin_div, use_container_width=True)
    st.divider()
# -------------------------------------------------
# Region Analysis
# -------------------------------------------------
    st.subheader("Regional Revenue & Profit Analysis")
    region_perf = (
    df_filtered.groupby("Region")
    .agg(
    Revenue=("Sales","sum"),
    Profit=("Gross Profit","sum")
    )
    .reset_index()
    )

    fig4 = px.bar(
    region_perf,
    x="Region",
    y=["Revenue","Profit"],
    barmode="group",
    title=None
    )
    fig4 = style_chart(fig4)
    st.plotly_chart(fig4,use_container_width=True)
    st.divider()
# -------------------------------------------------
# Profitability Quadrant
# -------------------------------------------------

    st.subheader("Product Profitability Quadrant")

    fig5 = px.scatter(
    product_perf,
    x="Sales",
    y="Margin",
    title=None,
    color="Margin",
    size="Profit",
    hover_name="Product Name"
    )

    fig5 = style_chart(fig5)
    st.plotly_chart(fig5,use_container_width=True)
    st.divider()
# -------------------------------------------------
# 🏭 Factory Performance Analysis
# -------------------------------------------------

    st.subheader("🏭 Factory Performance Analysis")

    factory_map = {
        "Chocolate": "Lot's O' Nuts",
        "Sugar": "Sugar Shack",
        "Other": "Secret Factory"
    }

    df_filtered["Factory"] = df_filtered["Division"].map(factory_map)

    factory_perf = df_filtered.groupby("Factory").agg(
        Profit=("Gross Profit", "sum"),
        Revenue=("Sales", "sum"),
        Units=("Units", "sum")
    ).reset_index()

    factory_coords = pd.DataFrame({
        "Factory": ["Lot's O' Nuts","Wicked Choccy's","Sugar Shack","Secret Factory","The Other Factory"],
        "Latitude": [32.881893,32.076176,48.11914,41.446333,35.1175],
        "Longitude": [-111.768036,-81.088371,-96.18115,-90.565487,-89.971107]
    })

    factory_perf = factory_perf.merge(factory_coords, on="Factory", how="left")

    factory_perf = factory_perf.dropna(subset=["Latitude"])

    fig_map = px.scatter_geo(
        factory_perf,
        lat="Latitude",
        lon="Longitude",
        size="Profit", 
        color="Profit",
        hover_name="Factory",
        hover_data={
            "Revenue": ":,.0f",
            "Profit": ":,.0f",
            "Units": ":,.0f"
        },
        color_continuous_scale="Blues"
    )

    fig_map.update_layout(
        template="plotly_dark",
        geo=dict(
            showland=True,
            landcolor="#1f2937",
            showcountries=True,
            countrycolor="gray",
            coastlinecolor="gray"
        ),
        height=500,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig_map, use_container_width=True)

    if not factory_perf.empty:
        best_factory = factory_perf.sort_values("Profit", ascending=False).iloc[0]["Factory"]
        worst_factory = factory_perf.sort_values("Profit", ascending=True).iloc[0]["Factory"]

        st.success(f"🏆 Best Performing Factory: {best_factory}")
        st.warning(f"⚠️ Lowest Performing Factory: {worst_factory}")
        st.markdown("""
        ### 🧠 Factory Insight
        - Profit is concentrated in a few factories
        - Some factories underperform relative to revenue
        - Cost optimization and efficiency improvements are recommended
        """)
        st.divider()
# -------------------------------------------------
# Margin Distribution
# -------------------------------------------------
with tab3:
    st.subheader("📉 Margin Distribution")

    fig6 = px.histogram(
    df_filtered,
    x="Gross Margin %",
    nbins=30
    )
    fig6 = style_chart(fig6)
    st.plotly_chart(fig6,use_container_width=True)
    
# -------------------------------------------------
# Cost vs Sales Diagnostics
# -------------------------------------------------
    st.divider()
    st.subheader("💸 Cost vs Sales Diagnostics")

    fig7 = px.scatter(
        df_filtered,
        x="Cost",
        y="Sales",
        color="Division",
        size="Gross Profit",
        hover_name="Product Name",
        title=None
    )
    fig7 = style_chart(fig7)
    st.plotly_chart(fig7,use_container_width=True)
    st.divider()
# -------------------------------------------------
# Margin Risk Products
# -------------------------------------------------
    st.subheader("🚨 Margin Risk Products")

    risk_products = df_filtered[
        (df_filtered["Gross Margin %"] < 15) &
        (df_filtered["Profit per Unit"] < 2)
    ]
    st.warning("These products have high cost but low margins. Review pricing or sourcing.")

    st.dataframe(risk_products.style.background_gradient(cmap="Reds"))
    st.divider()

# -------------------------------------------------
# Download DataSet
# -------------------------------------------------
    csv = df_filtered.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="nassau_filtered_data.csv",
        mime="text/csv",
    )

# -------------------------------------------------
# Monthly Trend
# -------------------------------------------------
with tab4:
    st.subheader("📅 Revenue & Profit Trend")

    df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"], errors="coerce")
    df_filtered = df_filtered.dropna(subset=["Order Date"])
    df_filtered.columns = df_filtered.columns.str.strip()
    df_temp = df_filtered.set_index("Order Date")

    monthly = df_temp.resample("MS").agg(
        Revenue=("Sales","sum"),
        Profit=("Gross Profit","sum")
    ).reset_index()

    fig8 = px.line(
    monthly,
    x="Order Date",
    y=["Revenue","Profit"]
    )
    fig8 = style_chart(fig8)
    st.plotly_chart(fig8,use_container_width=True)
    st.divider()
# -------------------------------------------------
# Margin Trend Over Time
# -------------------------------------------------
    st.subheader("📊 Monthly Margin Trend")

    margin_trend = df_temp.resample("ME").agg(
        Margin=("Gross Margin %", "mean")
    ).reset_index()

    fig_margin = px.line(
        margin_trend,
        x="Order Date",
        y="Margin",
        title=None
    )

    st.plotly_chart(fig_margin, use_container_width=True)
    
# -------------------------------------------------
# Profit Pareto
# -------------------------------------------------
    st.divider()
    st.subheader("📊 Pareto Analysis of Profit Contribution (80/20 Rule)")

    pareto = product_perf.sort_values("Profit", ascending=False)

    pareto["Cumulative Profit"] = pareto["Profit"].cumsum()
    pareto["Cumulative %"] = pareto["Cumulative Profit"] / pareto["Profit"].sum() * 100
    pareto["Rank"] = range(1, len(pareto) + 1)

    fig9 = px.line(
        pareto.head(50),
        x="Rank",
        y="Cumulative %",
        title=None,
        labels={
            "Rank": "Products (Sorted by Profit)",
            "Cumulative %": "Cumulative Profit (%)"
        }
    )
    fig9.update_traces(mode="lines+markers")
    fig9.add_hline(y=80, line_dash="dash", line_color="red")

    fig9 = style_chart(fig9)
    st.plotly_chart(fig9, use_container_width=True)
    st.info("A small number of products generate the majority of profit (Pareto principle).")
    st.divider()
# -------------------------------------------------
# Products Driving 80% Profit
# -------------------------------------------------
    st.subheader("🔥 Products Driving 80% Profit")
    top_80 = pareto[pareto["Cumulative %"] <= 80]
    st.dataframe(top_80.head(10))
    st.success("✔ Around 80% of total profit comes from a small number of products.")
    dependency_ratio = len(top_80) / len(product_perf) * 100

    st.metric(
        label="Products Driving 80% Profit",
        value=f"{len(top_80)} products",
        delta=f"{dependency_ratio:.1f}% of total products"
    )
    st.metric(
        label="Profit Concentration Level",
        value="High" if dependency_ratio < 20 else "Moderate" if dependency_ratio < 40 else "Low"
    )
    st.divider()

# -------------------------------------------------
# Executive Insights & Recommendations
# -------------------------------------------------

    st.subheader("📌 Executive Summary")

    top_products = df_filtered.groupby("Product Name")["Gross Profit"].sum().nlargest(3)
    low_products = df_filtered.groupby("Product Name")["Gross Profit"].sum().nsmallest(3)
    top_div = df_filtered.groupby("Division")["Gross Profit"].sum().idxmax()

    st.info(f"""
    🔹 Top Profit Drivers: {", ".join(top_products.index.tolist())}  
    🔹 Low Performing Products: {", ".join(low_products.index.tolist())}  
    🔹 Best Division: {top_div}  
    🔹 Focus should be on improving low-margin, high-sales products  
    """)

    st.subheader("📌 Final Business Summary")
    st.success("""
    ✔ A small group of products drives most of the profit (Pareto Principle)

    ✔ High-margin products should be prioritized for marketing and sales

    ✔ Low-margin, high-volume products need pricing or cost optimization

    ✔ Factory performance varies — efficiency improvements can increase profitability

    ✔ Business should shift focus from sales-driven to profit-driven strategy
    """)