import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Customer Churn",
    page_icon="🔄",
    layout="wide"
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
                circle at 10% 20%,
                rgba(255, 99, 132, 0.22),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(124, 58, 237, 0.22),
                transparent 34%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(14, 165, 233, 0.20),
                transparent 38%
            ),
            linear-gradient(
                135deg,
                #fff1f2 0%,
                #f5f3ff 35%,
                #eff6ff 70%,
                #ecfeff 100%
            );

        background-attachment: fixed;
    }

    /* Main page spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(
            120deg,
            #e11d48,
            #7c3aed,
            #2563eb
        );

        padding: 27px 30px;
        border-radius: 22px;
        color: white;
        margin-bottom: 24px;

        box-shadow:
            0 15px 35px rgba(124, 58, 237, 0.25);
    }

    .dashboard-title {
        font-size: 37px;
        font-weight: 800;
        margin: 0;
    }

    .dashboard-subtitle {
        font-size: 16px;
        margin-top: 8px;
        margin-bottom: 0;
        opacity: 0.92;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);

        border-radius: 18px;
        padding: 21px 18px;
        min-height: 135px;

        border: 1px solid rgba(255, 255, 255, 0.85);

        box-shadow:
            0 10px 27px rgba(30, 41, 59, 0.10);

        transition: all 0.25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);

        box-shadow:
            0 15px 35px rgba(124, 58, 237, 0.20);
    }

    .kpi-icon {
        font-size: 28px;
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

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #312e81;

        border-left: 6px solid #e11d48;
        padding-left: 12px;

        margin-top: 27px;
        margin-bottom: 14px;
    }

    /* Chart containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.77);
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

    /* Text input */
    div[data-baseweb="input"] {
        border-radius: 12px;
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;

        background: linear-gradient(
            90deg,
            #e11d48,
            #7c3aed,
            #2563eb
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

    /* Search section card */
    .search-card {
        background: rgba(255, 255, 255, 0.78);
        padding: 18px;
        border-radius: 16px;

        border: 1px solid rgba(255, 255, 255, 0.85);

        box-shadow:
            0 8px 24px rgba(30, 41, 59, 0.08);

        margin-bottom: 12px;
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
            🔄 Customer Churn Prediction Dashboard
        </p>

        <p class="dashboard-subtitle">
            Identify active and churned customers and analyse the overall
            customer retention status.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_churn_data():
    return pd.read_csv(
        "data/processed/churn_prediction.csv"
    )


try:
    churn = load_churn_data()

except FileNotFoundError:
    st.error(
        "❌ churn_prediction.csv was not found inside "
        "data/processed."
    )
    st.stop()

except Exception as error:
    st.error(
        f"❌ Error loading churn_prediction.csv:\n\n{error}"
    )
    st.stop()

# ==========================================================
# VALIDATE REQUIRED COLUMN
# ==========================================================

if "Churn" not in churn.columns:
    st.error(
        "❌ The required `Churn` column is missing from the CSV file."
    )
    st.stop()

# Ensure Churn is numeric
churn["Churn"] = pd.to_numeric(
    churn["Churn"],
    errors="coerce"
)

churn = churn.dropna(subset=["Churn"]).copy()

churn["Churn"] = churn["Churn"].astype(int)

# ==========================================================
# CLEAN CUSTOMER ID
# ==========================================================

if "CustomerID" in churn.columns:

    churn["CustomerID"] = (
        churn["CustomerID"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

# ==========================================================
# CREATE CUSTOMER STATUS
# ==========================================================

churn["CustomerStatus"] = churn["Churn"].replace(
    {
        0: "Active",
        1: "Churn"
    }
)

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_customers = len(churn)

churn_customers = len(
    churn[churn["Churn"] == 1]
)

active_customers = len(
    churn[churn["Churn"] == 0]
)

if total_customers > 0:
    churn_rate = (
        churn_customers / total_customers
    ) * 100

    retention_rate = (
        active_customers / total_customers
    ) * 100

else:
    churn_rate = 0
    retention_rate = 0

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Customer Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-description">
                Customer records analysed
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Churn Customers</div>
            <div class="kpi-value">{churn_customers:,}</div>
            <div class="kpi-description">
                Customers predicted to churn
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">✅</div>
            <div class="kpi-label">Active Customers</div>
            <div class="kpi-value">{active_customers:,}</div>
            <div class="kpi-description">
                Customers currently active
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📉</div>
            <div class="kpi-label">Churn Rate</div>
            <div class="kpi-value">{churn_rate:.2f}%</div>
            <div class="kpi-description">
                Percentage of churn customers
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Retention Rate</div>
            <div class="kpi-value">{retention_rate:.2f}%</div>
            <div class="kpi-description">
                Percentage of active customers
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# CHURN DISTRIBUTION
# ==========================================================

churn_count = (
    churn["CustomerStatus"]
    .value_counts()
    .reset_index()
)

churn_count.columns = [
    "Status",
    "Customers"
]

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.markdown(
        '<div class="section-title">🥧 Churn Distribution</div>',
        unsafe_allow_html=True
    )

    pie_chart = px.pie(
        churn_count,
        names="Status",
        values="Customers",
        hole=0.48,
        color="Status",
        color_discrete_map={
            "Active": "#10b981",
            "Churn": "#ef4444"
        },
        title="Active and Churn Customer Distribution"
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
            "Customers: %{value:,}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    pie_chart.update_layout(
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.02,
        legend_title="Customer Status",
        margin=dict(
            t=65,
            l=25,
            r=25,
            b=30
        ),
        annotations=[
            dict(
                text=f"{total_customers:,}<br>Customers",
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
        '<div class="section-title">📊 Customer Status</div>',
        unsafe_allow_html=True
    )

    bar_chart = px.bar(
        churn_count,
        x="Status",
        y="Customers",
        color="Status",
        text="Customers",
        color_discrete_map={
            "Active": "#10b981",
            "Churn": "#ef4444"
        },
        title="Number of Active and Churn Customers"
    )

    bar_chart.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1.5,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Customers: %{y:,}"
            "<extra></extra>"
        )
    )

    bar_chart.update_layout(
        height=430,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.65)",
        title_x=0.02,
        xaxis_title="Customer Status",
        yaxis_title="Number of Customers",
        margin=dict(
            t=65,
            l=45,
            r=30,
            b=40
        )
    )

    bar_chart.update_yaxes(
        gridcolor="rgba(148,163,184,0.22)"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

# ==========================================================
# SEARCH CUSTOMER
# ==========================================================

st.markdown(
    '<div class="section-title">🔍 Search Customer</div>',
    unsafe_allow_html=True
)

if "CustomerID" in churn.columns:

    customer_id = st.text_input(
        "Enter Customer ID",
        placeholder="Example: 17850"
    )

    if customer_id:

        customer_id = customer_id.strip()

        filtered_customer = churn[
            churn["CustomerID"] == customer_id
        ]

        if not filtered_customer.empty:

            customer_status = (
                filtered_customer["CustomerStatus"]
                .iloc[0]
            )

            if customer_status == "Active":
                st.success(
                    "✅ Customer found and the customer is active."
                )
            else:
                st.warning(
                    "⚠️ Customer found and predicted as churn."
                )

            st.dataframe(
                filtered_customer,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.error("❌ Customer not found.")

            with st.expander(
                "View sample Customer IDs"
            ):
                st.write(
                    churn["CustomerID"]
                    .head(20)
                    .tolist()
                )

else:
    st.info(
        "The CustomerID column is not available, "
        "so customer search cannot be displayed."
    )

# ==========================================================
# CUSTOMER STATUS FILTER
# ==========================================================

st.markdown(
    '<div class="section-title">🎛️ Filter Customer Records</div>',
    unsafe_allow_html=True
)

selected_status = st.multiselect(
    "Select Customer Status",
    options=["Active", "Churn"],
    default=["Active", "Churn"]
)

filtered_churn = churn[
    churn["CustomerStatus"].isin(
        selected_status
    )
].copy()

if filtered_churn.empty:
    st.warning(
        "No records are available for the selected status."
    )

# ==========================================================
# CHURN TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Customer Churn Prediction</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_churn,
    use_container_width=True,
    hide_index=True,
    height=450,
    column_config={
        "CustomerID": st.column_config.TextColumn(
            "Customer ID"
        ),
        "Churn": st.column_config.NumberColumn(
            "Churn Prediction",
            help="0 means Active and 1 means Churn",
            format="%d"
        ),
        "CustomerStatus": st.column_config.TextColumn(
            "Customer Status"
        )
    }
)

# ==========================================================
# DOWNLOAD CSV
# ==========================================================

st.markdown(
    '<div class="section-title">⬇️ Download Data</div>',
    unsafe_allow_html=True
)

csv = filtered_churn.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Churn Prediction CSV",
    data=csv,
    file_name="churn_prediction.csv",
    mime="text/csv"
)

# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

st.success(
    "✅ Customer Churn Dashboard Loaded Successfully"
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 15px;
        color: #475569;
        font-size: 14px;
    ">
        <b>NeuralRetail – AI-Powered Retail Analytics Platform</b>
        <br>
        Customer Churn Prediction and Retention Analysis
    </div>
    """,
    unsafe_allow_html=True
)