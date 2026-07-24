import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Price Optimization",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* Main colorful dashboard background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 15%,
                rgba(250, 204, 21, 0.24),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(236, 72, 153, 0.20),
                transparent 34%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(59, 130, 246, 0.20),
                transparent 38%
            ),
            linear-gradient(
                135deg,
                #fff7ed 0%,
                #fefce8 25%,
                #fdf2f8 55%,
                #eff6ff 78%,
                #ecfeff 100%
            );

        background-attachment: fixed;
    }

    /* Main container */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #713f12 0%,
            #9d174d 48%,
            #312e81 100%
        );

        border-right: 1px solid rgba(255, 255, 255, 0.20);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] .stMultiSelect div,
    section[data-testid="stSidebar"] .stTextInput div {
        color: #111827;
    }

    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(
            120deg,
            #f59e0b,
            #ec4899,
            #7c3aed,
            #2563eb
        );

        padding: 28px 30px;
        border-radius: 22px;
        color: white;
        margin-bottom: 24px;

        box-shadow:
            0 15px 36px rgba(124, 58, 237, 0.25);
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        margin: 0;
    }

    .dashboard-subtitle {
        font-size: 17px;
        margin-top: 8px;
        margin-bottom: 0;
        opacity: 0.93;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.86);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);

        border-radius: 18px;
        padding: 20px 18px;
        min-height: 140px;

        border: 1px solid rgba(255, 255, 255, 0.86);

        box-shadow:
            0 10px 28px rgba(30, 41, 59, 0.10);

        transition: all 0.25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);

        box-shadow:
            0 16px 35px rgba(236, 72, 153, 0.20);
    }

    .kpi-icon {
        font-size: 29px;
        margin-bottom: 4px;
    }

    .kpi-label {
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 5px;
    }

    .kpi-description {
        font-size: 12px;
        font-weight: 600;
        color: #be185d;
        margin-top: 4px;
    }

    /* Section titles */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #4c1d95;

        border-left: 6px solid #ec4899;
        padding-left: 12px;

        margin-top: 27px;
        margin-bottom: 14px;
    }

    /* Plotly chart containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.78);
        border-radius: 18px;
        padding: 8px;

        border: 1px solid rgba(255, 255, 255, 0.86);

        box-shadow:
            0 8px 24px rgba(30, 41, 59, 0.09);
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;

        box-shadow:
            0 8px 24px rgba(30, 41, 59, 0.09);
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;

        background: linear-gradient(
            90deg,
            #f59e0b,
            #ec4899,
            #7c3aed
        );

        color: white;
        border: none;
        border-radius: 12px;

        padding: 11px 18px;
        font-weight: 650;

        transition: all 0.25s ease;
    }

    .stDownloadButton > button:hover {
        color: white;
        transform: translateY(-2px);

        box-shadow:
            0 10px 23px rgba(236, 72, 153, 0.27);
    }

    /* Horizontal line */
    hr {
        border: none;
        height: 1px;

        background: linear-gradient(
            90deg,
            transparent,
            rgba(236, 72, 153, 0.45),
            transparent
        );

        margin: 25px 0;
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# DASHBOARD HEADER
# ==========================================================

st.markdown(
    """
    <div class="dashboard-header">

        <p class="dashboard-title">
            💰 Price Optimization Dashboard
        </p>

        <p class="dashboard-subtitle">
            Analyse product prices, revenue performance, recommended prices,
            profit categories, and discount opportunities.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_price_data():
    return pd.read_csv(
        "data/processed/price_optimization.csv"
    )


try:
    price = load_price_data()

except FileNotFoundError:
    st.error(
        "❌ price_optimization.csv was not found inside "
        "data/processed."
    )
    st.stop()

except Exception as error:
    st.error(
        f"❌ Error loading price_optimization.csv:\n\n{error}"
    )
    st.stop()

# ==========================================================
# VALIDATE REQUIRED COLUMNS
# ==========================================================

required_columns = {
    "CurrentPrice",
    "Revenue",
    "Discount(%)",
    "Description",
    "StockCode",
    "RecommendedPrice",
    "ProfitCategory"
}

missing_columns = required_columns.difference(
    price.columns
)

if missing_columns:
    st.error(
        "❌ The following required columns are missing: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

# ==========================================================
# CLEAN DATA
# ==========================================================

numeric_columns = [
    "CurrentPrice",
    "Revenue",
    "RecommendedPrice",
    "Discount(%)"
]

for column in numeric_columns:
    price[column] = pd.to_numeric(
        price[column],
        errors="coerce"
    )

price["Description"] = (
    price["Description"]
    .fillna("Unknown Product")
    .astype(str)
    .str.strip()
)

price["StockCode"] = (
    price["StockCode"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

price["ProfitCategory"] = (
    price["ProfitCategory"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

price = price.dropna(
    subset=[
        "CurrentPrice",
        "Revenue",
        "RecommendedPrice",
        "Discount(%)"
    ]
).copy()

if price.empty:
    st.warning(
        "No valid price optimization records are available."
    )
    st.stop()

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

with st.sidebar:

    st.markdown("## 🎛️ Price Filters")

    st.markdown(
        "Use these filters to explore product pricing records."
    )

    available_categories = sorted(
        price["ProfitCategory"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        "Select Profit Category",
        options=available_categories,
        default=available_categories
    )

    discount_filter = st.selectbox(
        "Discount Recommendation",
        options=[
            "All Products",
            "Discount Recommended",
            "No Discount"
        ]
    )

    product_search = st.text_input(
        "Search Product",
        placeholder="Enter product name or stock code"
    )

    st.markdown("---")

    st.markdown(
        """
        ### 📌 Price Information

        **Current Price:** Existing selling price

        **Recommended Price:** Suggested optimized price

        **Discount:** Recommended percentage reduction

        **Profit Category:** Product revenue classification
        """
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_price = price[
    price["ProfitCategory"].isin(
        selected_categories
    )
].copy()

if discount_filter == "Discount Recommended":

    filtered_price = filtered_price[
        filtered_price["Discount(%)"] > 0
    ]

elif discount_filter == "No Discount":

    filtered_price = filtered_price[
        filtered_price["Discount(%)"] <= 0
    ]

if product_search:

    search_text = product_search.strip()

    filtered_price = filtered_price[
        filtered_price["Description"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
        |
        filtered_price["StockCode"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

if filtered_price.empty:
    st.warning(
        "No products match the selected filters."
    )
    st.stop()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_products = len(filtered_price)

average_price = filtered_price[
    "CurrentPrice"
].mean()

average_recommended_price = filtered_price[
    "RecommendedPrice"
].mean()

average_revenue = filtered_price[
    "Revenue"
].mean()

total_revenue = filtered_price[
    "Revenue"
].sum()

recommended_discount = len(
    filtered_price[
        filtered_price["Discount(%)"] > 0
    ]
)

average_discount = filtered_price.loc[
    filtered_price["Discount(%)"] > 0,
    "Discount(%)"
].mean()

if pd.isna(average_discount):
    average_discount = 0

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Price Optimization Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">📦</div>

            <div class="kpi-label">
                Products
            </div>

            <div class="kpi-value">
                {total_products:,}
            </div>

            <div class="kpi-description">
                Products currently displayed
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🏷️</div>

            <div class="kpi-label">
                Average Price
            </div>

            <div class="kpi-value">
                ${average_price:,.2f}
            </div>

            <div class="kpi-description">
                Average current product price
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🎯</div>

            <div class="kpi-label">
                Recommended Price
            </div>

            <div class="kpi-value">
                ${average_recommended_price:,.2f}
            </div>

            <div class="kpi-description">
                Average optimized price
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">💵</div>

            <div class="kpi-label">
                Average Revenue
            </div>

            <div class="kpi-value">
                ${average_revenue:,.2f}
            </div>

            <div class="kpi-description">
                Average product revenue
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">💰</div>

            <div class="kpi-label">
                Total Revenue
            </div>

            <div class="kpi-value">
                ${total_revenue:,.0f}
            </div>

            <div class="kpi-description">
                Combined revenue value
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🎁</div>

            <div class="kpi-label">
                Discounted Products
            </div>

            <div class="kpi-value">
                {recommended_discount:,}
            </div>

            <div class="kpi-description">
                Average discount {average_discount:.2f}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# PRICE DISTRIBUTION
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Price Distribution</div>',
    unsafe_allow_html=True
)

price_histogram = px.histogram(
    filtered_price,
    x="CurrentPrice",
    nbins=30,
    color="ProfitCategory",
    title="Product Price Distribution",
    labels={
        "CurrentPrice": "Current Price",
        "count": "Number of Products"
    },
    color_discrete_sequence=px.colors.qualitative.Set2
)

price_histogram.update_layout(
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.65)",
    title_x=0.02,
    xaxis_title="Current Product Price",
    yaxis_title="Number of Products",
    bargap=0.06,
    legend_title="Profit Category"
)

price_histogram.update_xaxes(
    tickprefix="$",
    gridcolor="rgba(148,163,184,0.22)"
)

price_histogram.update_yaxes(
    gridcolor="rgba(148,163,184,0.22)"
)

st.plotly_chart(
    price_histogram,
    use_container_width=True
)

# ==========================================================
# REVENUE VS PRICE
# ==========================================================

st.markdown(
    '<div class="section-title">📈 Revenue vs Current Price</div>',
    unsafe_allow_html=True
)

revenue_scatter = px.scatter(
    filtered_price,
    x="CurrentPrice",
    y="Revenue",
    color="ProfitCategory",
    size="Revenue",
    hover_name="Description",
    hover_data={
        "StockCode": True,
        "CurrentPrice": ":.2f",
        "RecommendedPrice": ":.2f",
        "Discount(%)": ":.2f",
        "Revenue": ":.2f"
    },
    title="Relationship Between Product Price and Revenue",
    labels={
        "CurrentPrice": "Current Price",
        "Revenue": "Product Revenue",
        "ProfitCategory": "Profit Category"
    },
    size_max=35,
    color_discrete_sequence=px.colors.qualitative.Bold
)

revenue_scatter.update_layout(
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.65)",
    title_x=0.02,
    xaxis_title="Current Product Price",
    yaxis_title="Revenue",
    legend_title="Profit Category"
)

revenue_scatter.update_xaxes(
    tickprefix="$",
    gridcolor="rgba(148,163,184,0.22)"
)

revenue_scatter.update_yaxes(
    tickprefix="$",
    gridcolor="rgba(148,163,184,0.22)"
)

st.plotly_chart(
    revenue_scatter,
    use_container_width=True
)

# ==========================================================
# TOP PROFITABLE PRODUCTS
# ==========================================================

st.markdown(
    '<div class="section-title">🏆 Top 10 Revenue Products</div>',
    unsafe_allow_html=True
)

top_products = (
    filtered_price
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
    .sort_values(
        "Revenue",
        ascending=True
    )
)

top_products_chart = px.bar(
    top_products,
    x="Revenue",
    y="Description",
    orientation="h",
    color="ProfitCategory",
    text="Revenue",
    title="Top Products Based on Revenue",
    color_discrete_sequence=px.colors.qualitative.Set1
)

top_products_chart.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Revenue: $%{x:,.2f}"
        "<extra></extra>"
    )
)

top_products_chart.update_layout(
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.65)",
    title_x=0.02,
    xaxis_title="Revenue",
    yaxis_title="Product Description",
    legend_title="Profit Category",
    margin=dict(
        l=80,
        r=40,
        t=70,
        b=40
    )
)

top_products_chart.update_xaxes(
    tickprefix="$",
    gridcolor="rgba(148,163,184,0.22)"
)

st.plotly_chart(
    top_products_chart,
    use_container_width=True
)

# ==========================================================
# DISCOUNT RECOMMENDATIONS
# ==========================================================

st.markdown(
    '<div class="section-title">🎁 Discount Recommendations</div>',
    unsafe_allow_html=True
)

discount_products = filtered_price[
    filtered_price["Discount(%)"] > 0
].copy()

if discount_products.empty:

    st.success(
        "✅ No discount recommendations are available "
        "for the selected products."
    )

else:

    st.info(
        f"💡 {len(discount_products):,} products have "
        "recommended discounts."
    )

    discount_columns = [
        column
        for column in [
            "StockCode",
            "Description",
            "CurrentPrice",
            "RecommendedPrice",
            "Discount(%)",
            "Revenue",
            "ProfitCategory"
        ]
        if column in discount_products.columns
    ]

    st.dataframe(
        discount_products[
            discount_columns
        ].sort_values(
            "Discount(%)",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True,
        height=380,
        column_config={
            "StockCode": st.column_config.TextColumn(
                "Stock Code"
            ),
            "Description": st.column_config.TextColumn(
                "Product Description"
            ),
            "CurrentPrice": st.column_config.NumberColumn(
                "Current Price",
                format="$%.2f"
            ),
            "RecommendedPrice": st.column_config.NumberColumn(
                "Recommended Price",
                format="$%.2f"
            ),
            "Discount(%)": st.column_config.NumberColumn(
                "Discount",
                format="%.2f%%"
            ),
            "Revenue": st.column_config.NumberColumn(
                "Revenue",
                format="$%.2f"
            ),
            "ProfitCategory": st.column_config.TextColumn(
                "Profit Category"
            )
        }
    )

# ==========================================================
# SEARCH PRODUCT
# ==========================================================

st.markdown(
    '<div class="section-title">🔍 Search Product by Stock Code</div>',
    unsafe_allow_html=True
)

product_code = st.text_input(
    "Enter Stock Code",
    placeholder="Example: 85123A"
)

if product_code:

    product_code = product_code.strip()

    searched_product = price[
        price["StockCode"] == product_code
    ]

    if not searched_product.empty:

        st.success(
            "✅ Product found successfully."
        )

        st.dataframe(
            searched_product,
            use_container_width=True,
            hide_index=True,
            column_config={
                "CurrentPrice": st.column_config.NumberColumn(
                    "Current Price",
                    format="$%.2f"
                ),
                "RecommendedPrice": st.column_config.NumberColumn(
                    "Recommended Price",
                    format="$%.2f"
                ),
                "Discount(%)": st.column_config.NumberColumn(
                    "Discount",
                    format="%.2f%%"
                ),
                "Revenue": st.column_config.NumberColumn(
                    "Revenue",
                    format="$%.2f"
                )
            }
        )

    else:

        st.error(
            "❌ Product not found."
        )

        with st.expander(
            "View sample stock codes"
        ):
            st.write(
                price["StockCode"]
                .head(20)
                .tolist()
            )

# ==========================================================
# COMPLETE DATA TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Complete Price Optimization Data</div>',
    unsafe_allow_html=True
)

display_columns = [
    column
    for column in [
        "StockCode",
        "Description",
        "CurrentPrice",
        "RecommendedPrice",
        "Discount(%)",
        "Revenue",
        "ProfitCategory"
    ]
    if column in filtered_price.columns
]

st.dataframe(
    filtered_price[
        display_columns
    ].sort_values(
        "Revenue",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
    height=480,
    column_config={
        "StockCode": st.column_config.TextColumn(
            "Stock Code"
        ),
        "Description": st.column_config.TextColumn(
            "Product Description"
        ),
        "CurrentPrice": st.column_config.NumberColumn(
            "Current Price",
            format="$%.2f"
        ),
        "RecommendedPrice": st.column_config.NumberColumn(
            "Recommended Price",
            format="$%.2f"
        ),
        "Discount(%)": st.column_config.NumberColumn(
            "Discount",
            format="%.2f%%"
        ),
        "Revenue": st.column_config.NumberColumn(
            "Revenue",
            format="$%.2f"
        ),
        "ProfitCategory": st.column_config.TextColumn(
            "Profit Category"
        )
    }
)

# ==========================================================
# DOWNLOAD CSV
# ==========================================================

st.markdown(
    '<div class="section-title">⬇️ Download Price Optimization Data</div>',
    unsafe_allow_html=True
)

csv = filtered_price.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Price Optimization CSV",
    data=csv,
    file_name="price_optimization.csv",
    mime="text/csv"
)

# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

st.success(
    "✅ Price Optimization Dashboard Loaded Successfully"
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 16px;
        color: #475569;
        font-size: 14px;
    ">

        <b>
            NeuralRetail – AI-Powered Retail Analytics Platform
        </b>

        <br>

        Price Optimization and Discount Recommendation Module

    </div>
    """,
    unsafe_allow_html=True
)