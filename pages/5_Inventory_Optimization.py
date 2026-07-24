import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* Main colorful background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 15%,
                rgba(37, 99, 235, 0.22),
                transparent 34%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(168, 85, 247, 0.20),
                transparent 34%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(16, 185, 129, 0.18),
                transparent 40%
            ),
            linear-gradient(
                135deg,
                #eff6ff 0%,
                #f5f3ff 35%,
                #fdf2f8 65%,
                #ecfdf5 100%
            );

        background-attachment: fixed;
    }

    /* Page spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554 0%,
            #312e81 50%,
            #581c87 100%
        );

        border-right: 1px solid rgba(255, 255, 255, 0.20);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] .stTextInput div {
        color: #111827;
    }

    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(
            120deg,
            #2563eb,
            #7c3aed,
            #ec4899
        );

        padding: 28px 30px;
        border-radius: 22px;
        color: white;
        margin-bottom: 24px;

        box-shadow:
            0 15px 35px rgba(79, 70, 229, 0.25);
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
        background: rgba(255, 255, 255, 0.84);
        backdrop-filter: blur(11px);
        -webkit-backdrop-filter: blur(11px);

        border-radius: 18px;
        padding: 20px 18px;
        min-height: 138px;

        border: 1px solid rgba(255, 255, 255, 0.85);

        box-shadow:
            0 10px 27px rgba(30, 41, 59, 0.10);

        transition: all 0.25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);

        box-shadow:
            0 16px 35px rgba(124, 58, 237, 0.20);
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
        color: #7c3aed;
        margin-top: 4px;
    }

    /* Section heading */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #312e81;

        border-left: 6px solid #7c3aed;
        padding-left: 12px;

        margin-top: 27px;
        margin-bottom: 14px;
    }

    /* Plotly chart containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.78);
        border-radius: 18px;
        padding: 8px;

        border: 1px solid rgba(255, 255, 255, 0.85);

        box-shadow:
            0 8px 24px rgba(30, 41, 59, 0.09);
    }

    /* Dataframe */
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
            #2563eb,
            #7c3aed,
            #ec4899
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
            0 10px 23px rgba(124, 58, 237, 0.27);
    }

    /* Horizontal line */
    hr {
        border: none;
        height: 1px;

        background: linear-gradient(
            90deg,
            transparent,
            rgba(124, 58, 237, 0.45),
            transparent
        );

        margin: 25px 0;
    }

    /* Hide default footer */
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
            📦 Inventory Optimization Dashboard
        </p>

        <p class="dashboard-subtitle">
            Monitor product movement, identify top-performing products,
            and manage reorder requirements efficiently.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_inventory_data():
    return pd.read_csv(
        "data/processed/inventory_status.csv"
    )


try:
    inventory = load_inventory_data()

except FileNotFoundError:
    st.error(
        "❌ inventory_status.csv was not found inside "
        "data/processed."
    )
    st.stop()

except Exception as error:
    st.error(
        f"❌ Error loading inventory_status.csv:\n\n{error}"
    )
    st.stop()

# ==========================================================
# VALIDATE REQUIRED COLUMNS
# ==========================================================

required_columns = {
    "InventoryStatus",
    "Revenue",
    "Description",
    "ReorderAlert"
}

missing_columns = required_columns.difference(
    inventory.columns
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

inventory["InventoryStatus"] = (
    inventory["InventoryStatus"]
    .astype(str)
    .str.strip()
)

inventory["ReorderAlert"] = (
    inventory["ReorderAlert"]
    .astype(str)
    .str.strip()
    .str.upper()
)

inventory["Description"] = (
    inventory["Description"]
    .fillna("Unknown Product")
    .astype(str)
    .str.strip()
)

inventory["Revenue"] = pd.to_numeric(
    inventory["Revenue"],
    errors="coerce"
)

inventory = inventory.dropna(
    subset=["Revenue"]
).copy()

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

with st.sidebar:

    st.markdown("## 🎛️ Inventory Filters")

    st.markdown(
        "Use these filters to explore specific inventory records."
    )

    available_status = sorted(
        inventory["InventoryStatus"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_status = st.multiselect(
        "Select Inventory Status",
        options=available_status,
        default=available_status
    )

    selected_reorder = st.selectbox(
        "Select Reorder Alert",
        options=[
            "All",
            "YES",
            "NO"
        ]
    )

    product_search = st.text_input(
        "Search Product",
        placeholder="Enter product name"
    )

    st.markdown("---")

    st.markdown(
        """
        ### 📌 Status Meaning

        **Fast Moving:** Products with high sales movement

        **Medium Moving:** Products with moderate sales movement

        **Slow Moving:** Products with low sales movement

        **Reorder Alert:** Products requiring stock replenishment
        """
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_inventory = inventory[
    inventory["InventoryStatus"].isin(
        selected_status
    )
].copy()

if selected_reorder != "All":
    filtered_inventory = filtered_inventory[
        filtered_inventory["ReorderAlert"]
        == selected_reorder
    ]

if product_search:
    filtered_inventory = filtered_inventory[
        filtered_inventory["Description"]
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]

if filtered_inventory.empty:
    st.warning(
        "No inventory records match the selected filters."
    )
    st.stop()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_products = len(filtered_inventory)

fast_products = len(
    filtered_inventory[
        filtered_inventory["InventoryStatus"]
        == "Fast Moving"
    ]
)

medium_products = len(
    filtered_inventory[
        filtered_inventory["InventoryStatus"]
        == "Medium Moving"
    ]
)

slow_products = len(
    filtered_inventory[
        filtered_inventory["InventoryStatus"]
        == "Slow Moving"
    ]
)

reorder_products = len(
    filtered_inventory[
        filtered_inventory["ReorderAlert"]
        == "YES"
    ]
)

total_revenue = filtered_inventory["Revenue"].sum()

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Inventory Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Total Products</div>
            <div class="kpi-value">{total_products:,}</div>
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
            <div class="kpi-icon">🚀</div>
            <div class="kpi-label">Fast Moving</div>
            <div class="kpi-value">{fast_products:,}</div>
            <div class="kpi-description">
                High-performing products
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-label">Medium Moving</div>
            <div class="kpi-value">{medium_products:,}</div>
            <div class="kpi-description">
                Moderately performing products
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🐢</div>
            <div class="kpi-label">Slow Moving</div>
            <div class="kpi-value">{slow_products:,}</div>
            <div class="kpi-description">
                Low-performing products
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-label">Reorder Alerts</div>
            <div class="kpi-value">{reorder_products:,}</div>
            <div class="kpi-description">
                Products requiring reorder
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">₹{total_revenue:,.0f}</div>
            <div class="kpi-description">
                Revenue from displayed products
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# INVENTORY STATUS CHART
# ==========================================================

status = (
    filtered_inventory["InventoryStatus"]
    .value_counts()
    .reset_index()
)

status.columns = [
    "Status",
    "Products"
]

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.markdown(
        '<div class="section-title">🥧 Inventory Status</div>',
        unsafe_allow_html=True
    )

    pie_chart = px.pie(
        status,
        names="Status",
        values="Products",
        title="Inventory Classification",
        hole=0.50,
        color="Status",
        color_discrete_map={
            "Fast Moving": "#10b981",
            "Medium Moving": "#f59e0b",
            "Slow Moving": "#ef4444"
        }
    )

    pie_chart.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color="white",
                width=2
            )
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Products: %{value:,}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    pie_chart.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.02,
        legend_title="Inventory Status",
        annotations=[
            dict(
                text=f"{total_products:,}<br>Products",
                x=0.5,
                y=0.5,
                showarrow=False,
                font_size=16
            )
        ]
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

# ==========================================================
# STATUS BAR CHART
# ==========================================================

with chart_col2:

    st.markdown(
        '<div class="section-title">📊 Product Movement</div>',
        unsafe_allow_html=True
    )

    status_bar = px.bar(
        status,
        x="Status",
        y="Products",
        color="Status",
        text="Products",
        color_discrete_map={
            "Fast Moving": "#10b981",
            "Medium Moving": "#f59e0b",
            "Slow Moving": "#ef4444"
        },
        title="Products by Inventory Status"
    )

    status_bar.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1.5,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Products: %{y:,}"
            "<extra></extra>"
        )
    )

    status_bar.update_layout(
        height=440,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.65)",
        title_x=0.02,
        xaxis_title="Inventory Status",
        yaxis_title="Number of Products"
    )

    status_bar.update_yaxes(
        gridcolor="rgba(148,163,184,0.22)"
    )

    st.plotly_chart(
        status_bar,
        use_container_width=True
    )

# ==========================================================
# TOP SELLING PRODUCTS
# ==========================================================

st.markdown(
    '<div class="section-title">🏆 Top Revenue Products</div>',
    unsafe_allow_html=True
)

top_products = (
    filtered_inventory
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
    color="InventoryStatus",
    text="Revenue",
    color_discrete_map={
        "Fast Moving": "#10b981",
        "Medium Moving": "#f59e0b",
        "Slow Moving": "#ef4444"
    },
    title="Top 10 Products Based on Revenue"
)

top_products_chart.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Revenue: ₹%{x:,.2f}"
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
    legend_title="Inventory Status",
    margin=dict(
        l=70,
        r=40,
        t=70,
        b=40
    )
)

top_products_chart.update_xaxes(
    tickprefix="₹",
    gridcolor="rgba(148,163,184,0.22)"
)

st.plotly_chart(
    top_products_chart,
    use_container_width=True
)

# ==========================================================
# REORDER ALERTS
# ==========================================================

st.markdown(
    '<div class="section-title">🚨 Products Requiring Reorder</div>',
    unsafe_allow_html=True
)

reorder = filtered_inventory[
    filtered_inventory["ReorderAlert"]
    == "YES"
].copy()

if reorder.empty:

    st.success(
        "✅ No products currently require reorder."
    )

else:

    st.warning(
        f"⚠️ {len(reorder):,} products require reorder."
    )

    reorder_display_columns = [
        column
        for column in [
            "StockCode",
            "Description",
            "QuantitySold",
            "Revenue",
            "InventoryStatus",
            "ReorderAlert"
        ]
        if column in reorder.columns
    ]

    st.dataframe(
        reorder[reorder_display_columns]
        .sort_values(
            "Revenue",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True,
        height=350,
        column_config={
            "StockCode": st.column_config.TextColumn(
                "Stock Code"
            ),
            "Description": st.column_config.TextColumn(
                "Product Description"
            ),
            "QuantitySold": st.column_config.NumberColumn(
                "Quantity Sold",
                format="%d"
            ),
            "Revenue": st.column_config.NumberColumn(
                "Revenue",
                format="₹%.2f"
            ),
            "InventoryStatus": st.column_config.TextColumn(
                "Inventory Status"
            ),
            "ReorderAlert": st.column_config.TextColumn(
                "Reorder Alert"
            )
        }
    )

# ==========================================================
# INVENTORY DETAILS TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Inventory Details</div>',
    unsafe_allow_html=True
)

display_columns = [
    column
    for column in [
        "StockCode",
        "Description",
        "QuantitySold",
        "Revenue",
        "InventoryStatus",
        "ReorderAlert"
    ]
    if column in filtered_inventory.columns
]

st.dataframe(
    filtered_inventory[display_columns]
    .sort_values(
        "Revenue",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
    height=470,
    column_config={
        "StockCode": st.column_config.TextColumn(
            "Stock Code"
        ),
        "Description": st.column_config.TextColumn(
            "Product Description"
        ),
        "QuantitySold": st.column_config.NumberColumn(
            "Quantity Sold",
            format="%d"
        ),
        "Revenue": st.column_config.NumberColumn(
            "Revenue",
            format="₹%.2f"
        ),
        "InventoryStatus": st.column_config.TextColumn(
            "Inventory Status"
        ),
        "ReorderAlert": st.column_config.TextColumn(
            "Reorder Alert"
        )
    }
)

# ==========================================================
# DOWNLOAD CSV
# ==========================================================

st.markdown(
    '<div class="section-title">⬇️ Download Inventory Data</div>',
    unsafe_allow_html=True
)

csv = filtered_inventory.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Inventory CSV",
    data=csv,
    file_name="inventory_status.csv",
    mime="text/csv"
)

# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

st.success(
    "✅ Inventory Dashboard Loaded Successfully"
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
        <b>NeuralRetail – AI-Powered Retail Analytics Platform</b>
        <br>
        Inventory Optimization and Reorder Management Module
    </div>
    """,
    unsafe_allow_html=True
)