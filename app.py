"""
============================================================
NeuralRetail AI Retail Analytics Platform
Premium Streamlit Home Application
============================================================
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NeuralRetail AI Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
FEATURED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "featured_data.csv"
LOGO_PATH = PROJECT_ROOT / "images" / "logo.png"
BANNER_PATH = PROJECT_ROOT / "images" / "banner.jpg"

PAGES = {
    "home": "app.py",
    "segmentation": "pages/2_Customer_Segmentation.py",
    "forecasting": "pages/3_Sales_Forecasting.py",
    "churn": "pages/4_Customer_Churn.py",
    "inventory": "pages/5_Inventory_Optimization.py",
    "pricing": "pages/6_Price_Optimization.py",
    "recommendation": "pages/7_Business_Recommendation.py",
}


# ==========================================================
# PREMIUM COLORFUL CSS
# ==========================================================

st.markdown(
    """
    <style>
    :root {
        --navy: #071426;
        --blue: #2563eb;
        --violet: #7c3aed;
        --pink: #db2777;
        --orange: #f97316;
        --green: #10b981;
        --cyan: #06b6d4;
        --text: #0f172a;
        --muted: #64748b;
    }

    html {
        scroll-behavior: smooth;
    }

    .stApp {
        background:
            radial-gradient(circle at 7% 8%, rgba(37, 99, 235, 0.34), transparent 25%),
            radial-gradient(circle at 92% 9%, rgba(249, 115, 22, 0.35), transparent 25%),
            radial-gradient(circle at 10% 88%, rgba(124, 58, 237, 0.30), transparent 29%),
            radial-gradient(circle at 91% 87%, rgba(16, 185, 129, 0.28), transparent 27%),
            radial-gradient(circle at 51% 47%, rgba(219, 39, 119, 0.18), transparent 37%),
            linear-gradient(
                135deg,
                #dbeafe 0%,
                #ede9fe 18%,
                #fce7f3 37%,
                #ffedd5 58%,
                #cffafe 78%,
                #dcfce7 100%
            );
        background-attachment: fixed;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 1.6rem;
        padding-bottom: 2.5rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #061226 0%,
                #172554 38%,
                #312e81 67%,
                #4c1d95 82%,
                #431407 100%
            );
        border-right: 1px solid rgba(255, 255, 255, 0.12);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.18);
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        margin: 0.22rem 0;
        padding: 0.68rem 0.82rem;
        border-radius: 13px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        font-weight: 750;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
        background:
            linear-gradient(
                90deg,
                rgba(37, 99, 235, 0.86),
                rgba(124, 58, 237, 0.86),
                rgba(249, 115, 22, 0.86)
            );
        transform: translateX(5px);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.22);
    }

    .hero-container {
        position: relative;
        overflow: hidden;
        padding: 54px 52px;
        margin-bottom: 28px;
        border-radius: 30px;
        color: white;
        background:
            linear-gradient(
                120deg,
                rgba(7, 20, 38, 0.99),
                rgba(37, 99, 235, 0.94),
                rgba(124, 58, 237, 0.93),
                rgba(219, 39, 119, 0.90),
                rgba(249, 115, 22, 0.91)
            );
        box-shadow:
            0 24px 58px rgba(15, 23, 42, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.18);
    }

    .hero-container::before,
    .hero-container::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.13);
        filter: blur(1px);
    }

    .hero-container::before {
        width: 285px;
        height: 285px;
        right: -92px;
        top: -100px;
    }

    .hero-container::after {
        width: 185px;
        height: 185px;
        right: 155px;
        bottom: -120px;
        background: rgba(253, 230, 138, 0.18);
    }

    .hero-badge {
        position: relative;
        z-index: 2;
        display: inline-block;
        margin-bottom: 17px;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.30);
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.4px;
    }

    .hero-title {
        position: relative;
        z-index: 2;
        margin: 0;
        font-size: clamp(40px, 5vw, 60px);
        line-height: 1.06;
        font-weight: 900;
        letter-spacing: -1.3px;
    }

    .hero-highlight {
        color: #fde68a;
        text-shadow: 0 5px 20px rgba(253, 230, 138, 0.25);
    }

    .hero-subtitle {
        position: relative;
        z-index: 2;
        max-width: 950px;
        margin-top: 18px;
        margin-bottom: 0;
        color: #f8fafc;
        font-size: 18px;
        line-height: 1.72;
    }

    .section-heading {
        display: inline-block;
        margin-top: 22px;
        margin-bottom: 7px;
        padding: 11px 19px;
        border-radius: 15px;
        color: var(--text);
        font-size: 30px;
        font-weight: 900;
        background:
            linear-gradient(
                90deg,
                rgba(37, 99, 235, 0.16),
                rgba(124, 58, 237, 0.16),
                rgba(219, 39, 119, 0.15),
                rgba(249, 115, 22, 0.18)
            );
        border: 1px solid rgba(255, 255, 255, 0.62);
        box-shadow: 0 7px 18px rgba(15, 23, 42, 0.06);
    }

    .section-description {
        margin: 4px 0 21px;
        color: #475569;
        font-size: 16px;
    }

    .kpi-card {
        min-height: 150px;
        padding: 23px 20px;
        border-radius: 22px;
        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.98),
                rgba(239, 246, 255, 0.95),
                rgba(253, 244, 255, 0.92)
            );
        border: 1px solid rgba(255, 255, 255, 0.82);
        box-shadow:
            0 14px 34px rgba(37, 99, 235, 0.14),
            0 5px 14px rgba(219, 39, 119, 0.07);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }

    .kpi-card:hover {
        transform: translateY(-7px);
        box-shadow:
            0 24px 48px rgba(124, 58, 237, 0.20),
            0 10px 24px rgba(249, 115, 22, 0.12);
    }

    .kpi-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 0.58px;
    }

    .kpi-value {
        margin-top: 7px;
        color: var(--text);
        font-size: 29px;
        font-weight: 900;
    }

    .clickable-module-card {
        min-height: 228px;
        padding: 28px;
        border-radius: 25px;
        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.99),
                rgba(239, 246, 255, 0.95),
                rgba(250, 245, 255, 0.95),
                rgba(255, 247, 237, 0.94)
            );
        border: 1px solid rgba(255, 255, 255, 0.84);
        box-shadow:
            0 15px 36px rgba(37, 99, 235, 0.14),
            0 7px 18px rgba(249, 115, 22, 0.08);
        transition: transform 0.24s ease, box-shadow 0.24s ease;
    }

    .clickable-module-card:hover {
        transform: translateY(-9px) scale(1.01);
        box-shadow:
            0 26px 52px rgba(124, 58, 237, 0.22),
            0 12px 28px rgba(249, 115, 22, 0.15);
    }

    .module-icon {
        font-size: 43px;
    }

    .module-title {
        margin-top: 10px;
        color: var(--text);
        font-size: 22px;
        font-weight: 900;
    }

    .module-description {
        margin-top: 9px;
        color: var(--muted);
        font-size: 15px;
        line-height: 1.58;
    }

    .module-tag {
        display: inline-block;
        margin-top: 13px;
        padding: 6px 12px;
        border-radius: 999px;
        color: #3730a3;
        font-size: 12px;
        font-weight: 850;
        background:
            linear-gradient(
                90deg,
                rgba(37, 99, 235, 0.13),
                rgba(124, 58, 237, 0.13),
                rgba(219, 39, 119, 0.10)
            );
    }

    /* Strong, dark, highly visible main-page buttons */
    .main [data-testid="stPageLink"] a,
    section.main [data-testid="stPageLink"] a,
    div[data-testid="stPageLink"] a {
        justify-content: center;
        width: 100%;
        margin-top: 0.12rem;
        margin-bottom: 1.25rem;
        padding: 0.78rem 1.05rem;
        border-radius: 14px;
        color: #ffffff !important;
        font-size: 15px;
        font-weight: 900;
        text-decoration: none;
        background:
            linear-gradient(
                90deg,
                #061226 0%,
                #172554 26%,
                #4c1d95 58%,
                #9d174d 79%,
                #7c2d12 100%
            ) !important;
        border: 2px solid rgba(255, 255, 255, 0.90) !important;
        box-shadow:
            0 11px 25px rgba(7, 20, 38, 0.34),
            0 4px 10px rgba(124, 58, 237, 0.20);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .main [data-testid="stPageLink"] a:hover,
    section.main [data-testid="stPageLink"] a:hover,
    div[data-testid="stPageLink"] a:hover {
        transform: translateY(-3px) scale(1.01);
        color: #ffffff !important;
        background:
            linear-gradient(
                90deg,
                #0f172a,
                #1d4ed8,
                #6d28d9,
                #be185d,
                #ea580c
            ) !important;
        box-shadow:
            0 17px 34px rgba(15, 23, 42, 0.37),
            0 8px 18px rgba(219, 39, 119, 0.20);
    }

    .workflow-step {
        min-height: 128px;
        padding: 18px;
        text-align: center;
        border-radius: 18px;
        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.97),
                rgba(239, 246, 255, 0.92),
                rgba(255, 247, 237, 0.90)
            );
        border: 1px solid rgba(255, 255, 255, 0.82);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.09);
    }

    .workflow-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        margin-bottom: 9px;
        border-radius: 50%;
        color: white;
        font-weight: 900;
        background:
            linear-gradient(
                135deg,
                #2563eb,
                #7c3aed,
                #db2777,
                #f97316
            );
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.22);
    }

    .workflow-title {
        color: var(--text);
        font-weight: 900;
    }

    .insight-box {
        padding: 27px;
        border-radius: 22px;
        color: #334155;
        line-height: 1.82;
        border-left: 8px solid #f97316;
        background:
            linear-gradient(
                120deg,
                rgba(255, 255, 255, 0.99),
                rgba(239, 246, 255, 0.95),
                rgba(250, 245, 255, 0.94),
                rgba(255, 247, 237, 0.94)
            );
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.10);
    }

    .footer {
        margin-top: 40px;
        padding: 30px;
        border-radius: 23px;
        text-align: center;
        color: #ffffff;
        line-height: 1.75;
        background:
            linear-gradient(
                90deg,
                #061226,
                #172554,
                #4c1d95,
                #9d174d,
                #c2410c
            );
        box-shadow: 0 19px 42px rgba(15, 23, 42, 0.26);
    }

    .footer strong {
        color: #ffffff;
    }

    @media (max-width: 900px) {
        .hero-container {
            padding: 36px 27px;
        }

        .hero-subtitle {
            font-size: 16px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_featured_data(file_path: Path) -> pd.DataFrame:
    """Load processed retail data used by the home page."""
    return pd.read_csv(file_path)


featured_data: pd.DataFrame | None = None
data_error: str | None = None

if FEATURED_DATA_PATH.exists():
    try:
        featured_data = load_featured_data(FEATURED_DATA_PATH)
    except Exception as error:
        data_error = str(error)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def find_first_column(
    dataframe: pd.DataFrame,
    possible_names: list[str],
) -> str | None:
    """Return the first matching column name."""
    for name in possible_names:
        if name in dataframe.columns:
            return name
    return None


def format_currency(value: float) -> str:
    """Format KPI values using the Indian number system."""
    if abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:,.2f} Cr"

    if abs(value) >= 100_000:
        return f"₹{value / 100_000:,.2f} L"

    return f"₹{value:,.2f}"


def render_kpi(icon: str, label: str, value: str) -> None:
    """Render one KPI card."""
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


def render_clickable_module(
    page_path: str,
    icon: str,
    title: str,
    description: str,
    tag: str,
) -> None:
    """Render a module card and a working page-navigation link."""
    st.markdown(
        f"""
        <div class="clickable-module-card">
            <div class="module-icon">{icon}</div>
            <div class="module-title">{title}</div>
            <div class="module-description">{description}</div>
            <div class="module-tag">{tag}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link(
        page_path,
        label=f"Open {title}",
        icon="➡️",
        use_container_width=True,
    )


# ==========================================================
# SIDEBAR
# ==========================================================

if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), width=145)
else:
    st.sidebar.markdown(
        """
        <div style="
            text-align:center;
            font-size:62px;
            margin-bottom:4px;
        ">
            🛒
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.title("NeuralRetail AI")
st.sidebar.caption("Intelligent Retail Decision Platform")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Dashboard Modules")

st.sidebar.page_link(PAGES["home"], label="Home", icon="🏠")
st.sidebar.page_link(
    PAGES["segmentation"],
    label="Customer Segmentation",
    icon="👥",
)
st.sidebar.page_link(
    PAGES["forecasting"],
    label="Sales Forecasting",
    icon="📈",
)
st.sidebar.page_link(
    PAGES["churn"],
    label="Customer Churn",
    icon="🔄",
)
st.sidebar.page_link(
    PAGES["inventory"],
    label="Inventory Optimization",
    icon="📦",
)
st.sidebar.page_link(
    PAGES["pricing"],
    label="Price Optimization",
    icon="💰",
)
st.sidebar.page_link(
    PAGES["recommendation"],
    label="Business Recommendation",
    icon="💡",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 AI Capabilities")

st.sidebar.markdown(
    """
    - Machine Learning
    - Predictive Analytics
    - Customer Intelligence
    - Inventory Intelligence
    - Pricing Analytics
    - Business Recommendations
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Technology Stack")

st.sidebar.markdown(
    """
    `Python` · `Streamlit`  
    `Plotly` · `Pandas`  
    `Scikit-learn` · `Power BI`
    """
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "B.Tech CSE — Data Science & Artificial Intelligence"
)


# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">
            AI • MACHINE LEARNING • BUSINESS INTELLIGENCE
        </div>

        <h1 class="hero-title">
            Welcome to
            <span class="hero-highlight">NeuralRetail AI</span>
        </h1>

        <p class="hero-subtitle">
            Transform raw retail transactions into intelligent business
            decisions. Analyse customers, forecast sales, predict churn,
            optimise inventory and pricing, and receive actionable
            AI-powered recommendations from one integrated platform.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# OPTIONAL BANNER IMAGE
# ==========================================================

if BANNER_PATH.exists():
    st.image(
        str(BANNER_PATH),
        caption="AI-Powered Retail Analytics and Decision Intelligence",
        use_container_width=True,
    )


# ==========================================================
# BUSINESS KPIs
# ==========================================================

st.markdown(
    '<div class="section-heading">📊 Business Snapshot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        A quick overview calculated from the processed retail dataset.
    </div>
    """,
    unsafe_allow_html=True,
)

if featured_data is not None and not featured_data.empty:

    revenue_column = find_first_column(
        featured_data,
        ["TotalPrice", "Total Revenue", "Revenue"],
    )
    customer_column = find_first_column(
        featured_data,
        ["CustomerID", "Customer ID"],
    )
    product_column = find_first_column(
        featured_data,
        ["StockCode", "ProductID", "Product ID"],
    )
    order_column = find_first_column(
        featured_data,
        ["InvoiceNo", "OrderID", "Order ID"],
    )
    country_column = find_first_column(
        featured_data,
        ["Country", "Region"],
    )

    total_revenue = (
        pd.to_numeric(
            featured_data[revenue_column],
            errors="coerce",
        ).sum()
        if revenue_column
        else 0.0
    )

    total_customers = (
        featured_data[customer_column].nunique()
        if customer_column
        else 0
    )

    total_products = (
        featured_data[product_column].nunique()
        if product_column
        else 0
    )

    total_orders = (
        featured_data[order_column].nunique()
        if order_column
        else len(featured_data)
    )

    total_countries = (
        featured_data[country_column].nunique()
        if country_column
        else 0
    )

    average_order_value = (
        total_revenue / total_orders
        if total_orders
        else 0.0
    )

    kpi_1, kpi_2, kpi_3 = st.columns(3)

    with kpi_1:
        render_kpi("💰", "Total Revenue", format_currency(total_revenue))

    with kpi_2:
        render_kpi("👥", "Total Customers", f"{total_customers:,}")

    with kpi_3:
        render_kpi("🧾", "Total Orders", f"{total_orders:,}")

    st.write("")

    kpi_4, kpi_5, kpi_6 = st.columns(3)

    with kpi_4:
        render_kpi("📦", "Total Products", f"{total_products:,}")

    with kpi_5:
        render_kpi("🌍", "Countries", f"{total_countries:,}")

    with kpi_6:
        render_kpi(
            "📈",
            "Average Order Value",
            format_currency(average_order_value),
        )

else:
    st.warning(
        "The home dashboard is ready, but "
        "`data/processed/featured_data.csv` could not be loaded."
    )

    if data_error:
        with st.expander("View data-loading error"):
            st.code(data_error)


# ==========================================================
# CLICKABLE MODULE CARDS
# ==========================================================

st.markdown(
    '<div class="section-heading">🚀 Explore AI Modules</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Use the dark, high-contrast buttons to open each analytical module.
    </div>
    """,
    unsafe_allow_html=True,
)

row_1_col_1, row_1_col_2, row_1_col_3 = st.columns(3)

with row_1_col_1:
    render_clickable_module(
        PAGES["segmentation"],
        "👥",
        "Customer Segmentation",
        (
            "Group customers using RFM analysis and K-Means clustering "
            "to identify valuable, loyal and at-risk segments."
        ),
        "RFM + K-Means",
    )

with row_1_col_2:
    render_clickable_module(
        PAGES["forecasting"],
        "📈",
        "Sales Forecasting",
        (
            "Explore predicted future sales and historical trends "
            "for inventory, budgeting and revenue planning."
        ),
        "Predictive Analytics",
    )

with row_1_col_3:
    render_clickable_module(
        PAGES["churn"],
        "🔄",
        "Customer Churn",
        (
            "Find customers who may stop purchasing and support "
            "proactive retention and loyalty campaigns."
        ),
        "Classification",
    )

row_2_col_1, row_2_col_2, row_2_col_3 = st.columns(3)

with row_2_col_1:
    render_clickable_module(
        PAGES["inventory"],
        "📦",
        "Inventory Optimization",
        (
            "Identify fast-, medium- and slow-moving products and "
            "highlight products requiring reorder attention."
        ),
        "Inventory Intelligence",
    )

with row_2_col_2:
    render_clickable_module(
        PAGES["pricing"],
        "💰",
        "Price Optimization",
        (
            "Review current prices, recommended prices, revenue "
            "performance and product discount suggestions."
        ),
        "Pricing Intelligence",
    )

with row_2_col_3:
    render_clickable_module(
        PAGES["recommendation"],
        "💡",
        "Business Recommendation",
        (
            "Convert sales, customer, pricing and inventory analytics "
            "into practical business actions."
        ),
        "Decision Support",
    )


# ==========================================================
# ANALYTICS SHOWCASE
# ==========================================================

st.markdown(
    '<div class="section-heading">🖼️ Analytics Showcase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Selected visual outputs generated by the machine-learning pipeline.
    </div>
    """,
    unsafe_allow_html=True,
)

showcase_images = [
    ("images/monthly_sales.png", "Monthly Sales Analysis"),
    ("images/customer_segments.png", "Customer Segmentation"),
    ("images/forecast_sales.png", "Sales Forecast"),
]

available_showcase = [
    (PROJECT_ROOT / path, caption)
    for path, caption in showcase_images
    if (PROJECT_ROOT / path).exists()
]

if available_showcase:
    showcase_columns = st.columns(len(available_showcase))

    for column, (image_path, caption) in zip(
        showcase_columns,
        available_showcase,
    ):
        with column:
            st.image(
                str(image_path),
                caption=caption,
                use_container_width=True,
            )
else:
    st.info(
        "Run `python main.py` to generate the analytical images "
        "that will appear in this section."
    )


# ==========================================================
# PROJECT WORKFLOW
# ==========================================================

st.markdown(
    '<div class="section-heading">⚙️ How NeuralRetail Works</div>',
    unsafe_allow_html=True,
)

workflow_columns = st.columns(5)

workflow_data = [
    ("1", "Retail Data", "Transactions and customer activity"),
    ("2", "Data Science", "Cleaning, analysis and feature creation"),
    ("3", "Machine Learning", "Forecasting, clustering and prediction"),
    ("4", "AI Insights", "Pricing, inventory and recommendations"),
    ("5", "Dashboard", "Streamlit and Power BI decision support"),
]

for column, (number, title, description) in zip(
    workflow_columns,
    workflow_data,
):
    with column:
        st.markdown(
            f"""
            <div class="workflow-step">
                <div class="workflow-number">{number}</div>
                <div class="workflow-title">{title}</div>
                <div style="
                    color:#64748b;
                    font-size:13px;
                    margin-top:5px;
                ">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================================
# AI INSIGHTS
# ==========================================================

st.markdown(
    '<div class="section-heading">🤖 What the Platform Delivers</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="insight-box">
        <strong>NeuralRetail supports retail decision-makers by:</strong>
        <br><br>
        • Identifying valuable customer groups and behavioural patterns.<br>
        • Forecasting future sales for improved planning.<br>
        • Detecting customers who may stop purchasing.<br>
        • Highlighting fast-moving, slow-moving and reorder products.<br>
        • Recommending product prices and promotional discounts.<br>
        • Converting analytics into clear business actions.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# DATA PREVIEW
# ==========================================================

if featured_data is not None and not featured_data.empty:
    with st.expander("📄 View Sample Retail Data"):
        st.dataframe(
            featured_data.head(20),
            use_container_width=True,
            hide_index=True,
        )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        <strong>NeuralRetail AI Retail Analytics Platform</strong>
        <br>
        Developed by Gajendra Pratap Singh
        <br>
        B.Tech CSE — Data Science & Artificial Intelligence
        <br><br>
        Powered by Python • Streamlit • Plotly • Scikit-learn • Power BI
    </div>
    """,
    unsafe_allow_html=True,
)