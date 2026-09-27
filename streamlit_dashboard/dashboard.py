import os
import sys

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from dashboard_style import (
    PRIMARY, CYAN, AMBER, ROSE, EMERALD,
    REGION_COLORS, CATEGORY_COLORS, GRADIENT_INDIGO,
    TEXT_SECONDARY, GRID, style_fig,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPO_ROOT)
DATA_PATH = os.path.join(REPO_ROOT, 'data', 'supermarket_sales.csv')

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide", page_icon="📊")

# ---------- Global styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0F172A; }

.hero {
    background: linear-gradient(135deg, #4338CA 0%, #7C3AED 100%);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 20px;
    color: white;
}
.hero h1 { margin: 0; font-size: 28px; font-weight: 700; color: white; }
.hero .subtitle { margin: 6px 0 0 0; opacity: 0.85; font-size: 14px; }
.hero .intro { margin: 12px 0 0 0; opacity: 0.8; font-size: 13px; max-width: 720px; line-height: 1.5; }

.kpi-card {
    background: #1E293B;
    border-radius: 16px;
    padding: 18px 20px;
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 4px solid var(--accent);
}
.kpi-icon { font-size: 20px; }
.kpi-value { font-size: 24px; font-weight: 700; color: #F1F5F9; margin-top: 6px; }
.kpi-label { font-size: 13px; color: #94A3B8; margin-top: 2px; }

.chart-card {
    background: #1E293B;
    border-radius: 16px;
    padding: 20px 20px 8px 20px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 20px;
}
.chart-title { font-size: 15px; font-weight: 600; color: #F1F5F9; margin-bottom: 4px; }
.chart-sub { font-size: 12px; color: #94A3B8; margin-bottom: 12px; }

section[data-testid="stSidebar"] { background: #0B1120; border-right: 1px solid rgba(255,255,255,0.06); }

div[data-baseweb="tab-list"] { gap: 28px; }
button[data-baseweb="tab"] { font-weight: 600; padding-left: 4px; padding-right: 4px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
    return df


def kpi_card(col, icon, value, label, accent):
    col.markdown(f"""
    <div class="kpi-card" style="--accent: {accent};">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def chart_card_open(title, subtitle=None):
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-title">{title}</div>
        {f'<div class="chart-sub">{subtitle}</div>' if subtitle else ''}
    """, unsafe_allow_html=True)


def chart_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


sales_data = load_data()

# ---------- Sidebar filters ----------
st.sidebar.markdown("### 🔎 Filters")
regions = sorted(sales_data['Region'].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(sales_data['Category'].unique())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

filtered = sales_data[
    sales_data['Region'].isin(selected_regions) &
    sales_data['Category'].isin(selected_categories)
]

# ---------- Hero header ----------
n_orders = sales_data['Order ID'].nunique()
n_customers = sales_data['Customer ID'].nunique()
n_regions = sales_data['Region'].nunique()
n_subcats = sales_data['Sub-Category'].nunique()

st.markdown(f"""
<div class="hero">
    <h1>Superstore Sales Dashboard</h1>
    <div class="subtitle">Sales performance, segmentation, and trends · 2015-2018</div>
    <div class="intro">
        <b>Superstore</b> is a sample dataset representing a fictional US retail chain selling Furniture, Office Supplies, and Technology products. This dashboard covers <b>{n_orders:,} orders</b> from <b>{n_customers:,} customers</b> across <b>{n_regions} US regions</b> and <b>{n_subcats} product sub-categories</b>, from January 2015 to December 2018.
    </div>
</div>
""", unsafe_allow_html=True)

if filtered.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ---------- KPI row ----------
col1, col2, col3, col4 = st.columns(4, gap="medium")
kpi_card(col1, "💰", f"${filtered['Sales'].sum():,.0f}", "Total Sales", PRIMARY)
kpi_card(col2, "🧾", f"{filtered['Order ID'].nunique():,}", "Total Orders", CYAN)
kpi_card(col3, "👥", f"{filtered['Customer ID'].nunique():,}", "Total Customers", AMBER)
kpi_card(col4, "📦", f"${filtered.groupby('Order ID')['Sales'].sum().mean():,.2f}", "Avg Order Value", EMERALD)

st.write("")

# ---------- Tabs ----------
tab_overview, tab_regions, tab_products, tab_customers, tab_season = st.tabs(
    ["Overview", "Regions", "Products", "Customers", "Seasonality"]
)

# ===== Overview =====
with tab_overview:
    chart_card_open("Monthly Sales Trend", "Total sales per month, with a linear trend line")

    monthly_sales = filtered.groupby(
        filtered['Order Date'].dt.to_period('M')
    )['Sales'].sum()
    monthly_sales.index = monthly_sales.index.to_timestamp()

    x = np.arange(len(monthly_sales))
    trend = np.poly1d(np.polyfit(x, monthly_sales.values, 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_sales.index, y=monthly_sales.values,
        mode='lines+markers', name='Monthly Sales',
        line=dict(color=PRIMARY, width=3, shape='spline'),
        marker=dict(size=6, color=PRIMARY),
        fill='tozeroy', fillcolor='rgba(129,140,248,0.15)',
    ))
    fig.add_trace(go.Scatter(
        x=monthly_sales.index, y=trend(x),
        mode='lines', name='Trend',
        line=dict(color=ROSE, width=2, dash='dash'),
    ))
    fig = style_fig(fig, height=380, showlegend=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    chart_card_close()

# ===== Regions =====
with tab_regions:
    left, right = st.columns(2, gap="medium")

    with left:
        chart_card_open("Sales by Region")
        regional_sales = filtered.groupby('Region')['Sales'].sum().reindex(regions).dropna()
        fig = go.Figure(go.Bar(
            x=regional_sales.index, y=regional_sales.values,
            marker_color=[REGION_COLORS[r] for r in regional_sales.index],
        ))
        fig = style_fig(fig, height=340)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        chart_card_close()

    with right:
        chart_card_open("Monthly Sales by Region")
        regional_monthly = {}
        fig = go.Figure()
        for r in regions:
            if r not in selected_regions:
                continue
            rm = filtered[filtered['Region'] == r].groupby(
                filtered['Order Date'].dt.to_period('M')
            )['Sales'].sum()
            rm.index = rm.index.to_timestamp()
            fig.add_trace(go.Scatter(
                x=rm.index, y=rm.values, mode='lines', name=r,
                line=dict(color=REGION_COLORS[r], width=2, shape='spline'),
            ))
        fig = style_fig(fig, height=340, showlegend=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        chart_card_close()

# ===== Products =====
with tab_products:
    left, right = st.columns([1, 1.4], gap="medium")

    with left:
        chart_card_open("Sales by Category")
        category_sales = filtered.groupby('Category')['Sales'].sum()
        fig = go.Figure(go.Bar(
            x=category_sales.index, y=category_sales.values,
            marker_color=[CATEGORY_COLORS[c] for c in category_sales.index],
        ))
        fig = style_fig(fig, height=380)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        chart_card_close()

    with right:
        chart_card_open("Sales by Sub-Category", "Ranked, light to dark = higher sales")
        subcategory_sales = filtered.groupby('Sub-Category')['Sales'].sum().sort_values().reset_index()
        fig = px.bar(
            subcategory_sales, x='Sales', y='Sub-Category', orientation='h',
            color='Sales', color_continuous_scale=GRADIENT_INDIGO,
        )
        fig.update_layout(coloraxis_showscale=False)
        fig = style_fig(fig, height=480)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        chart_card_close()

# ===== Customers =====
with tab_customers:
    chart_card_open("Top 10 Customers by Total Sales")
    top_customers = filtered.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
    top_customers = top_customers.sort_values().reset_index()
    fig = px.bar(
        top_customers, x='Sales', y='Customer Name', orientation='h',
        color='Sales', color_continuous_scale=GRADIENT_INDIGO,
    )
    fig.update_layout(coloraxis_showscale=False)
    fig = style_fig(fig, height=420)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    chart_card_close()

    top10_share = top_customers['Sales'].sum() / filtered['Sales'].sum() * 100
    st.caption(f"The top 10 customers shown account for {top10_share:.1f}% of total sales in the current filter.")

# ===== Seasonality =====
with tab_season:
    chart_card_open("Seasonal Pattern", "Total sales by calendar month, all years combined")
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    seasonal_sales = filtered.groupby(filtered['Order Date'].dt.month)['Sales'].sum()
    seasonal_sales = seasonal_sales.reindex(range(1, 13))
    seasonal_df = pd.DataFrame({
        'Month': [month_names[m] for m in seasonal_sales.index],
        'Sales': seasonal_sales.values,
    })
    fig = px.bar(
        seasonal_df, x='Month', y='Sales',
        color='Sales', color_continuous_scale=GRADIENT_INDIGO,
    )
    fig.update_layout(coloraxis_showscale=False)
    fig = style_fig(fig, height=380)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    chart_card_close()

st.caption(
    "Built with Streamlit + Plotly · data: Kaggle Superstore sales dataset (2015-2018). "
    "See REPORT.md in the repo for the full written analysis and recommendations."
)
