"""
NeuralRetail AI
Modern Home Dashboard
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NeuralRetail Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# PROJECT PATHS
# ==========================================================

def resolve_project_root() -> Path:
    """Find the project root whether this file is in the root or pages folder."""
    current_file = Path(__file__).resolve()

    candidates = [
        current_file.parent,
        current_file.parent.parent,
        Path.cwd(),
    ]

    for candidate in candidates:
        expected_file = candidate / "data" / "processed" / "featured_data.csv"
        if expected_file.exists():
            return candidate

    return current_file.parent.parent


PROJECT_ROOT = resolve_project_root()
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "featured_data.csv"
BANNER_PATH = PROJECT_ROOT / "images" / "banner.jpg"


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>
    :root {
        --blue: #2563eb;
        --purple: #7c3aed;
        --pink: #db2777;
        --orange: #f97316;
        --green: #10b981;
        --red: #ef4444;
        --navy: #0f172a;
        --muted: #64748b;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 12%, rgba(37, 99, 235, 0.28), transparent 25%),
            radial-gradient(circle at 92% 10%, rgba(249, 115, 22, 0.28), transparent 24%),
            radial-gradient(circle at 12% 88%, rgba(124, 58, 237, 0.25), transparent 28%),
            radial-gradient(circle at 90% 86%, rgba(16, 185, 129, 0.22), transparent 27%),
            linear-gradient(135deg, #dbeafe 0%, #ede9fe 24%, #fce7f3 48%, #ffedd5 72%, #dcfce7 100%);
        background-attachment: fixed;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.3rem;
        padding-bottom: 2.5rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071426 0%, #172554 45%, #312e81 73%, #431407 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.15);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #0f172a !important;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 46px 48px;
        border-radius: 28px;
        color: white;
        background: linear-gradient(120deg, #071426, #2563eb, #7c3aed, #db2777, #f97316);
        box-shadow: 0 24px 58px rgba(15, 23, 42, 0.28);
        margin-bottom: 24px;
    }

    .hero::before,
    .hero::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.13);
    }

    .hero::before {
        width: 280px;
        height: 280px;
        right: -90px;
        top: -105px;
    }

    .hero::after {
        width: 175px;
        height: 175px;
        right: 150px;
        bottom: -112px;
        background: rgba(253, 230, 138, 0.18);
    }

    .hero-badge {
        position: relative;
        z-index: 2;
        display: inline-block;
        padding: 7px 15px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.28);
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .hero-title {
        position: relative;
        z-index: 2;
        margin: 0;
        font-size: clamp(38px, 5vw, 58px);
        line-height: 1.08;
        font-weight: 900;
        letter-spacing: -1px;
    }

    .hero-highlight {
        color: #fde68a;
    }

    .hero-text {
        position: relative;
        z-index: 2;
        max-width: 930px;
        margin-top: 16px;
        margin-bottom: 0;
        font-size: 18px;
        line-height: 1.7;
        color: #f8fafc;
    }

    .section-title {
        display: inline-block;
        margin-top: 22px;
        margin-bottom: 8px;
        padding: 10px 18px;
        border-radius: 15px;
        color: var(--navy);
        font-size: 27px;
        font-weight: 900;
        background: linear-gradient(90deg, rgba(37,99,235,.15), rgba(124,58,237,.15), rgba(219,39,119,.14), rgba(249,115,22,.17));
        border: 1px solid rgba(255, 255, 255, 0.72);
    }

    .section-subtitle {
        color: #475569;
        font-size: 15px;
        margin-bottom: 18px;
    }

    .kpi-card {
        min-height: 145px;
        padding: 22px 19px;
        border-radius: 22px;
        background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(239,246,255,.95), rgba(250,245,255,.94));
        border: 1px solid rgba(255, 255, 255, 0.84);
        box-shadow: 0 14px 34px rgba(37,99,235,.13), 0 6px 16px rgba(249,115,22,.08);
        transition: transform .22s ease, box-shadow .22s ease;
    }

    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 24px 48px rgba(124,58,237,.20), 0 10px 24px rgba(249,115,22,.13);
    }

    .kpi-icon {
        font-size: 31px;
        margin-bottom: 7px;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .55px;
    }

    .kpi-value {
        margin-top: 7px;
        color: var(--navy);
        font-size: 27px;
        font-weight: 900;
    }

    .overview-card {
        min-height: 190px;
        padding: 24px;
        border-radius: 22px;
        background: linear-gradient(145deg, rgba(255,255,255,.97), rgba(239,246,255,.93), rgba(255,247,237,.93));
        border: 1px solid rgba(255, 255, 255, 0.82);
        box-shadow: 0 13px 30px rgba(15,23,42,.09);
        transition: transform .22s ease;
    }

    .overview-card:hover {
        transform: translateY(-5px);
    }

    .overview-icon { font-size: 38px; }
    .overview-title { margin-top: 8px; color: var(--navy); font-size: 20px; font-weight: 900; }
    .overview-text { margin-top: 8px; color: var(--muted); font-size: 14px; line-height: 1.55; }

    .insight-box {
        padding: 26px;
        border-radius: 22px;
        color: #334155;
        line-height: 1.85;
        border-left: 8px solid #f97316;
        background: linear-gradient(120deg, rgba(255,255,255,.98), rgba(239,246,255,.94), rgba(250,245,255,.94), rgba(255,247,237,.94));
        box-shadow: 0 14px 34px rgba(15,23,42,.10);
    }

    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.80);
        border-radius: 20px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.85);
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.10);
    }

    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 10px 28px rgba(15,23,42,.10);
    }

    .stDownloadButton > button {
        width: 100%;
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 700;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777, #f97316);
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .stDownloadButton > button:hover {
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(124,58,237,.25);
    }

    .footer {
        margin-top: 36px;
        padding: 28px;
        border-radius: 22px;
        text-align: center;
        color: white;
        line-height: 1.72;
        background: linear-gradient(90deg, #071426, #172554, #4c1d95, #9d174d, #c2410c);
        box-shadow: 0 18px 40px rgba(15,23,42,.24);
    }

    footer { visibility: hidden; }

    @media (max-width: 900px) {
        .hero { padding: 34px 25px; }
        .hero-text { font-size: 16px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data(file_path: Path) -> pd.DataFrame:
    """Load processed retail data."""
    return pd.read_csv(file_path)


if not DATA_PATH.exists():
    st.error(
        "❌ The file `data/processed/featured_data.csv` was not found. "
        "Run `python main.py` first."
    )
    st.stop()

try:
    original_df = load_data(DATA_PATH)
except Exception as error:
    st.error(f"❌ Unable to load featured_data.csv: {error}")
    st.stop()

if original_df.empty:
    st.warning("The featured dataset is empty.")
    st.stop()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def find_column(data: pd.DataFrame, possible_names: list[str]) -> str | None:
    """Return the first available matching column."""
    for column_name in possible_names:
        if column_name in data.columns:
            return column_name
    return None


def format_currency(value: float) -> str:
    """Format currency using Indian lakh/crore notation."""
    if abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:,.2f} Cr"
    if abs(value) >= 100_000:
        return f"₹{value / 100_000:,.2f} L"
    return f"₹{value:,.2f}"


def render_kpi(icon: str, label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview_card(icon: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="overview-card">
            <div class="overview-icon">{icon}</div>
            <div class="overview-title">{title}</div>
            <div class="overview-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(figure, height: int = 430) -> None:
    figure.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=65, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.58)",
        title_font=dict(size=20),
        font=dict(color="#334155"),
    )
    figure.update_xaxes(gridcolor="rgba(148,163,184,0.22)")
    figure.update_yaxes(gridcolor="rgba(148,163,184,0.22)")


# ==========================================================
# COLUMN DISCOVERY
# ==========================================================

revenue_column = find_column(original_df, ["TotalPrice", "Total Revenue", "Revenue"])
customer_column = find_column(original_df, ["CustomerID", "Customer ID"])
product_column = find_column(original_df, ["StockCode", "ProductID", "Product ID"])
order_column = find_column(original_df, ["InvoiceNo", "OrderID", "Order ID"])
country_column = find_column(original_df, ["Country", "Region"])
description_column = find_column(original_df, ["Description", "ProductName", "Product Name"])
month_column = find_column(original_df, ["Month", "MonthName", "Month Name"])
date_column = find_column(original_df, ["InvoiceDate", "Date", "OrderDate", "Order Date"])

working_df = original_df.copy()

if revenue_column:
    working_df[revenue_column] = pd.to_numeric(
        working_df[revenue_column], errors="coerce"
    ).fillna(0)

if date_column:
    working_df[date_column] = pd.to_datetime(
        working_df[date_column], errors="coerce"
    )


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.title("🛒 NeuralRetail AI")
st.sidebar.caption("Retail Intelligence Dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Dashboard Filters")

selected_country = "All Countries"

if country_column:
    country_values = sorted(
        working_df[country_column].dropna().astype(str).unique().tolist()
    )
    selected_country = st.sidebar.selectbox(
        "🌍 Country",
        ["All Countries"] + country_values,
    )

    if selected_country != "All Countries":
        working_df = working_df[
            working_df[country_column].astype(str) == selected_country
        ].copy()

search_text = st.sidebar.text_input(
    "🔍 Search product",
    placeholder="Product name or stock code",
)

if search_text:
    search_mask = pd.Series(False, index=working_df.index)

    if description_column:
        search_mask |= working_df[description_column].astype(str).str.contains(
            search_text.strip(), case=False, na=False
        )

    if product_column:
        search_mask |= working_df[product_column].astype(str).str.contains(
            search_text.strip(), case=False, na=False
        )

    working_df = working_df[search_mask].copy()

if date_column and working_df[date_column].notna().any():
    minimum_date = working_df[date_column].min().date()
    maximum_date = working_df[date_column].max().date()

    selected_dates = st.sidebar.date_input(
        "📅 Date range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date,
    )

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        working_df = working_df[
            working_df[date_column].dt.date.between(start_date, end_date)
        ].copy()

st.sidebar.markdown("---")
st.sidebar.info(
    "Use the page navigation to explore segmentation, forecasting, churn, "
    "inventory, pricing and recommendations."
)

if working_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI • MACHINE LEARNING • BUSINESS INTELLIGENCE</div>
        <h1 class="hero-title">
            NeuralRetail <span class="hero-highlight">Business Overview</span>
        </h1>
        <p class="hero-text">
            Monitor revenue, customers, products, orders and geographical
            performance through one modern retail intelligence dashboard.
            Use filters and visual analytics to understand business performance
            and support faster data-driven decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if BANNER_PATH.exists():
    st.image(
        str(BANNER_PATH),
        caption="AI-Powered Retail Analytics",
        use_container_width=True,
    )


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = working_df[revenue_column].sum() if revenue_column else 0.0
total_customers = working_df[customer_column].nunique() if customer_column else 0
total_products = working_df[product_column].nunique() if product_column else 0
total_orders = working_df[order_column].nunique() if order_column else len(working_df)
total_countries = working_df[country_column].nunique() if country_column else 0


# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown('<div class="section-title">📊 Business Snapshot</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-subtitle">Current view: <strong>{selected_country}</strong> • {len(working_df):,} records</div>',
    unsafe_allow_html=True,
)

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

with kpi_1:
    render_kpi("🧾", "Total Orders", f"{total_orders:,}")
with kpi_2:
    render_kpi("💰", "Total Revenue", format_currency(total_revenue))
with kpi_3:
    render_kpi("👥", "Customers", f"{total_customers:,}")
with kpi_4:
    render_kpi("📦", "Products", f"{total_products:,}")
with kpi_5:
    render_kpi("🌍", "Countries", f"{total_countries:,}")


# ==========================================================
# REVENUE ANALYTICS
# ==========================================================

st.markdown('<div class="section-title">📈 Revenue Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Compare monthly performance and geographical revenue contribution.</div>',
    unsafe_allow_html=True,
)

chart_left, chart_right = st.columns(2)
monthly_sales = pd.DataFrame()
country_sales = pd.DataFrame()

with chart_left:
    if revenue_column and (date_column or month_column):
        if date_column and working_df[date_column].notna().any():
            chart_data = working_df.dropna(subset=[date_column]).copy()
            chart_data["MonthPeriod"] = chart_data[date_column].dt.to_period("M")
            monthly_sales = (
                chart_data.groupby("MonthPeriod")[revenue_column]
                .sum()
                .reset_index()
            )
            monthly_sales["Month"] = monthly_sales["MonthPeriod"].astype(str)
            x_column = "Month"
        else:
            monthly_sales = (
                working_df.groupby(month_column, dropna=False)[revenue_column]
                .sum()
                .reset_index()
            )
            x_column = month_column

        figure = px.bar(
            monthly_sales,
            x=x_column,
            y=revenue_column,
            title="Monthly Revenue",
            text_auto=".2s",
            color=revenue_column,
            color_continuous_scale="Blues",
        )
        figure.update_traces(hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.2f}<extra></extra>")
        figure.update_layout(coloraxis_showscale=False)
        style_chart(figure)
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("Monthly chart requires a date/month column and a revenue column.")

with chart_right:
    if country_column and revenue_column:
        country_sales = (
            working_df.groupby(country_column, dropna=False)[revenue_column]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        figure = px.pie(
            country_sales,
            values=revenue_column,
            names=country_column,
            title="Top 10 Countries by Revenue",
            hole=0.50,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        figure.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.2f}<br>%{percent}<extra></extra>",
        )
        figure.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=65, b=25),
            paper_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=20),
            showlegend=False,
        )
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("Country chart requires country and revenue columns.")


# ==========================================================
# PRODUCT PERFORMANCE
# ==========================================================

st.markdown('<div class="section-title">🏆 Product Performance</div>', unsafe_allow_html=True)
top_products = pd.DataFrame()

if description_column and revenue_column:
    top_products = (
        working_df.groupby(description_column, dropna=False)[revenue_column]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .sort_values(revenue_column, ascending=True)
    )

    figure = px.bar(
        top_products,
        x=revenue_column,
        y=description_column,
        orientation="h",
        title="Top 10 Revenue-Generating Products",
        text=revenue_column,
        color=revenue_column,
        color_continuous_scale="Sunset",
    )
    figure.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.2f}<extra></extra>",
    )
    figure.update_layout(coloraxis_showscale=False, xaxis_title="Revenue", yaxis_title="Product")
    style_chart(figure, height=520)
    st.plotly_chart(figure, use_container_width=True)
else:
    st.info("Product chart requires product description and revenue columns.")


# ==========================================================
# PLATFORM CAPABILITIES
# ==========================================================

st.markdown('<div class="section-title">🚀 Platform Capabilities</div>', unsafe_allow_html=True)

overview_1, overview_2, overview_3 = st.columns(3)

with overview_1:
    render_overview_card(
        "👥",
        "Customer Intelligence",
        "Understand customer value, purchasing behaviour, segments and potential churn risk.",
    )
with overview_2:
    render_overview_card(
        "📈",
        "Predictive Analytics",
        "Use historical retail data to estimate future sales and improve demand planning.",
    )
with overview_3:
    render_overview_card(
        "📦",
        "Retail Optimization",
        "Improve inventory decisions, pricing, discounts and business recommendations.",
    )


# ==========================================================
# AI BUSINESS INSIGHTS
# ==========================================================

st.markdown('<div class="section-title">🤖 AI Business Insights</div>', unsafe_allow_html=True)

best_product = (
    str(top_products.iloc[-1][description_column])
    if not top_products.empty and description_column
    else "Not available"
)

best_country = (
    str(country_sales.iloc[0][country_column])
    if not country_sales.empty and country_column
    else "Not available"
)

average_order_value = total_revenue / total_orders if total_orders else 0

st.markdown(
    f"""
    <div class="insight-box">
        <strong>Current dashboard observations</strong><br><br>
        • Total revenue in the selected view is <strong>{format_currency(total_revenue)}</strong>.<br>
        • Average order value is <strong>{format_currency(average_order_value)}</strong>.<br>
        • The current view includes <strong>{total_customers:,}</strong> customers and
          <strong>{total_products:,}</strong> products.<br>
        • Highest-revenue country: <strong>{best_country}</strong>.<br>
        • Highest-revenue product: <strong>{best_product}</strong>.<br>
        • Use the remaining pages for segmentation, forecasting, churn, inventory,
          pricing and recommendation analysis.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# RECENT TRANSACTIONS
# ==========================================================

st.markdown('<div class="section-title">🧾 Recent Transactions</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Latest records available in the currently filtered dataset.</div>',
    unsafe_allow_html=True,
)

recent_transactions = (
    working_df.sort_values(date_column, ascending=False).head(20)
    if date_column and working_df[date_column].notna().any()
    else working_df.tail(20)
)

st.dataframe(
    recent_transactions,
    use_container_width=True,
    hide_index=True,
    height=430,
)


# ==========================================================
# DOWNLOAD
# ==========================================================

st.markdown('<div class="section-title">⬇️ Download Current View</div>', unsafe_allow_html=True)

csv_data = working_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Retail Data",
    data=csv_data,
    file_name="neuralretail_home_filtered_data.csv",
    mime="text/csv",
)

st.success("✅ NeuralRetail Home Dashboard Loaded Successfully")


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        <strong>NeuralRetail AI Retail Analytics Platform</strong><br>
        Business Overview Dashboard<br><br>
        Powered by Python • Streamlit • Plotly • Machine Learning • Power BI
    </div>
    """,
    unsafe_allow_html=True,
)