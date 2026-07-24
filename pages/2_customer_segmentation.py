import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* Main dashboard background */
    .stApp {
        background:
            radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.20), transparent 35%),
            radial-gradient(circle at 90% 20%, rgba(168, 85, 247, 0.18), transparent 35%),
            radial-gradient(circle at 50% 90%, rgba(236, 72, 153, 0.15), transparent 40%),
            linear-gradient(
                135deg,
                #eff6ff 0%,
                #f5f3ff 35%,
                #fdf2f8 70%,
                #ecfeff 100%
            );
        background-attachment: fixed;
    }

    /* Hide Streamlit default footer */
    footer {
        visibility: hidden;
    }

    /* Main page padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554 0%,
            #312e81 45%,
            #581c87 100%
        );
        border-right: 1px solid rgba(255,255,255,0.20);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stMultiSelect div,
    section[data-testid="stSidebar"] .stSelectbox div {
        color: #111827;
    }

    /* Dashboard title */
    .dashboard-header {
        background: linear-gradient(
            120deg,
            #1d4ed8,
            #7c3aed,
            #db2777
        );
        padding: 28px 30px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 15px 35px rgba(79, 70, 229, 0.25);
        margin-bottom: 22px;
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
        opacity: 0.92;
    }

    /* Section title */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #312e81;
        margin-top: 20px;
        margin-bottom: 12px;
        padding-left: 12px;
        border-left: 6px solid #7c3aed;
    }

    /* KPI card */
    .kpi-card {
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.75);
        box-shadow: 0 10px 28px rgba(30, 41, 59, 0.10);
        transition: all 0.25s ease;
        min-height: 135px;
        margin-bottom: 10px;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 35px rgba(79, 70, 229, 0.20);
    }

    .kpi-icon {
        font-size: 29px;
        margin-bottom: 4px;
    }

    .kpi-label {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #111827;
        font-size: 27px;
        font-weight: 800;
        margin-top: 4px;
    }

    .kpi-description {
        color: #7c3aed;
        font-size: 12px;
        font-weight: 600;
        margin-top: 3px;
    }

    /* Insight card */
    .insight-card {
        background: linear-gradient(
            135deg,
            rgba(255,255,255,0.88),
            rgba(245,243,255,0.88)
        );
        padding: 20px;
        border-radius: 17px;
        border: 1px solid rgba(124, 58, 237, 0.16);
        box-shadow: 0 8px 24px rgba(30, 41, 59, 0.08);
        margin-top: 8px;
        margin-bottom: 12px;
    }

    .insight-title {
        color: #5b21b6;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .insight-text {
        color: #334155;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Buttons */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(
            90deg,
            #2563eb,
            #7c3aed,
            #db2777
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 18px;
        font-weight: 650;
        transition: all 0.25s ease;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        color: white;
        box-shadow: 0 10px 22px rgba(124, 58, 237, 0.25);
    }

    /* Dataframe container */
    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(30, 41, 59, 0.08);
    }

    /* Plotly chart container */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.72);
        border-radius: 18px;
        padding: 7px;
        box-shadow: 0 8px 24px rgba(30, 41, 59, 0.08);
        border: 1px solid rgba(255,255,255,0.80);
    }

    /* Horizontal separator */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(124, 58, 237, 0.40),
            transparent
        );
        margin: 24px 0;
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
        <p class="dashboard-title">👥 Customer Segmentation Dashboard</p>
        <p class="dashboard-subtitle">
            Analyze customer behaviour using Recency, Frequency and Monetary
            values with K-Means Clustering.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_customer_data():
    return pd.read_csv("data/processed/customer_segments.csv")


try:
    rfm = load_customer_data()
except FileNotFoundError:
    st.error(
        "❌ `customer_segments.csv` was not found in "
        "`data/processed/customer_segments.csv`."
    )
    st.stop()
except Exception as error:
    st.error(f"❌ Unable to load customer segmentation data: {error}")
    st.stop()

# ==========================================================
# VALIDATE REQUIRED COLUMNS
# ==========================================================

required_columns = {
    "Recency",
    "Frequency",
    "Monetary",
    "Cluster"
}

missing_columns = required_columns.difference(rfm.columns)

if missing_columns:
    st.error(
        "The following required columns are missing from the CSV file: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

# Remove invalid records from important columns
rfm = rfm.dropna(
    subset=["Recency", "Frequency", "Monetary", "Cluster"]
).copy()

rfm["Cluster"] = rfm["Cluster"].astype(int)
rfm["Cluster Name"] = "Cluster " + rfm["Cluster"].astype(str)

# Detect the customer identifier column
customer_id_column = None

possible_customer_columns = [
    "CustomerID",
    "Customer ID",
    "customer_id",
    "Customer"
]

for column in possible_customer_columns:
    if column in rfm.columns:
        customer_id_column = column
        break

if customer_id_column is None:
    rfm.insert(0, "CustomerNumber", range(1, len(rfm) + 1))
    customer_id_column = "CustomerNumber"

# ==========================================================
# COLOUR PALETTE
# ==========================================================

cluster_colours = [
    "#2563EB",
    "#7C3AED",
    "#EC4899",
    "#F97316",
    "#10B981",
    "#06B6D4",
    "#EF4444",
    "#FACC15"
]

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

with st.sidebar:
    st.markdown("## 🎛️ Dashboard Filters")
    st.markdown(
        "Use these filters to explore specific customer groups."
    )

    available_clusters = sorted(rfm["Cluster"].unique().tolist())

    selected_clusters = st.multiselect(
        "Select customer clusters",
        options=available_clusters,
        default=available_clusters,
        format_func=lambda value: f"Cluster {value}"
    )

    minimum_monetary = float(rfm["Monetary"].min())
    maximum_monetary = float(rfm["Monetary"].max())

    if minimum_monetary == maximum_monetary:
        selected_monetary = (
            minimum_monetary,
            maximum_monetary
        )
    else:
        selected_monetary = st.slider(
            "Monetary value range",
            min_value=minimum_monetary,
            max_value=maximum_monetary,
            value=(minimum_monetary, maximum_monetary)
        )

    minimum_frequency = int(rfm["Frequency"].min())
    maximum_frequency = int(rfm["Frequency"].max())

    if minimum_frequency == maximum_frequency:
        selected_frequency = (
            minimum_frequency,
            maximum_frequency
        )
    else:
        selected_frequency = st.slider(
            "Purchase frequency range",
            min_value=minimum_frequency,
            max_value=maximum_frequency,
            value=(minimum_frequency, maximum_frequency)
        )

    customer_search = st.text_input(
        "Search customer",
        placeholder="Enter customer ID"
    )

    st.markdown("---")

    st.markdown(
        """
        ### 📌 RFM Meaning

        **Recency:** Days since the latest purchase  
        **Frequency:** Number of purchases  
        **Monetary:** Total customer spending  
        """
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_rfm = rfm[
    (rfm["Cluster"].isin(selected_clusters))
    & (
        rfm["Monetary"].between(
            selected_monetary[0],
            selected_monetary[1]
        )
    )
    & (
        rfm["Frequency"].between(
            selected_frequency[0],
            selected_frequency[1]
        )
    )
].copy()

if customer_search:
    filtered_rfm = filtered_rfm[
        filtered_rfm[customer_id_column]
        .astype(str)
        .str.contains(customer_search, case=False, na=False)
    ]

if filtered_rfm.empty:
    st.warning(
        "No customer records match the selected filters. "
        "Please change the filter values."
    )
    st.stop()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_customers = len(filtered_rfm)
total_clusters = filtered_rfm["Cluster"].nunique()
average_recency = filtered_rfm["Recency"].mean()
average_frequency = filtered_rfm["Frequency"].mean()
average_monetary = filtered_rfm["Monetary"].mean()
total_customer_value = filtered_rfm["Monetary"].sum()

highest_value_customer = filtered_rfm.loc[
    filtered_rfm["Monetary"].idxmax()
]

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Customer Overview</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-description">Filtered customer records</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🧩</div>
            <div class="kpi-label">Active Clusters</div>
            <div class="kpi-value">{total_clusters}</div>
            <div class="kpi-description">Customer segments</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🕒</div>
            <div class="kpi-label">Average Recency</div>
            <div class="kpi-value">{average_recency:,.1f}</div>
            <div class="kpi-description">Average days since purchase</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🛍️</div>
            <div class="kpi-label">Average Frequency</div>
            <div class="kpi-value">{average_frequency:,.1f}</div>
            <div class="kpi-description">Average purchase count</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💳</div>
            <div class="kpi-label">Average Monetary</div>
            <div class="kpi-value">${average_monetary:,.2f}</div>
            <div class="kpi-description">Average customer spending</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Customer Value</div>
            <div class="kpi-value">${total_customer_value:,.0f}</div>
            <div class="kpi-description">Total monetary value</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# CLUSTER DISTRIBUTION
# ==========================================================

cluster_count = (
    filtered_rfm.groupby(["Cluster", "Cluster Name"])
    .size()
    .reset_index(name="Customers")
    .sort_values("Cluster")
)

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown(
        '<div class="section-title">📊 Cluster Distribution</div>',
        unsafe_allow_html=True
    )

    cluster_bar = px.bar(
        cluster_count,
        x="Cluster Name",
        y="Customers",
        color="Cluster Name",
        text="Customers",
        color_discrete_sequence=cluster_colours,
        title="Number of Customers in Each Cluster"
    )

    cluster_bar.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1.5,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Customers: %{y:,}<extra></extra>"
        )
    )

    cluster_bar.update_layout(
        showlegend=False,
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.65)",
        title_x=0.02,
        xaxis_title="Customer Cluster",
        yaxis_title="Number of Customers",
        margin=dict(t=65, l=45, r=30, b=40)
    )

    st.plotly_chart(cluster_bar, use_container_width=True)

with chart2:
    st.markdown(
        '<div class="section-title">🥧 Customer Share</div>',
        unsafe_allow_html=True
    )

    cluster_pie = px.pie(
        cluster_count,
        names="Cluster Name",
        values="Customers",
        hole=0.52,
        color="Cluster Name",
        color_discrete_sequence=cluster_colours,
        title="Percentage Distribution of Customers"
    )

    cluster_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Customers: %{value:,}<br>"
            "Share: %{percent}<extra></extra>"
        ),
        marker=dict(
            line=dict(color="white", width=2)
        )
    )

    cluster_pie.update_layout(
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.02,
        legend_title="Clusters",
        margin=dict(t=65, l=25, r=25, b=30),
        annotations=[
            dict(
                text=f"{total_customers:,}<br>Customers",
                x=0.5,
                y=0.5,
                font_size=17,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(cluster_pie, use_container_width=True)

# ==========================================================
# CUSTOMER SEGMENTATION SCATTER PLOTS
# ==========================================================

st.markdown(
    '<div class="section-title">🔍 Customer Behaviour Analysis</div>',
    unsafe_allow_html=True
)

scatter1, scatter2 = st.columns(2)

with scatter1:
    recency_monetary_scatter = px.scatter(
        filtered_rfm,
        x="Recency",
        y="Monetary",
        color="Cluster Name",
        size="Frequency",
        hover_name=customer_id_column,
        hover_data={
            "Recency": ":,.0f",
            "Frequency": ":,.0f",
            "Monetary": ":,.2f",
            "Cluster Name": True
        },
        color_discrete_sequence=cluster_colours,
        title="Recency vs Monetary Value",
        labels={
            "Recency": "Recency (Days)",
            "Monetary": "Monetary Value",
            "Cluster Name": "Customer Cluster"
        },
        size_max=35
    )

    recency_monetary_scatter.update_layout(
        height=480,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        legend_title="Clusters",
        margin=dict(t=65, l=45, r=30, b=40)
    )

    recency_monetary_scatter.update_xaxes(
        gridcolor="rgba(148,163,184,0.20)"
    )
    recency_monetary_scatter.update_yaxes(
        gridcolor="rgba(148,163,184,0.20)"
    )

    st.plotly_chart(
        recency_monetary_scatter,
        use_container_width=True
    )

with scatter2:
    frequency_monetary_scatter = px.scatter(
        filtered_rfm,
        x="Frequency",
        y="Monetary",
        color="Cluster Name",
        size="Monetary",
        hover_name=customer_id_column,
        hover_data={
            "Recency": ":,.0f",
            "Frequency": ":,.0f",
            "Monetary": ":,.2f"
        },
        color_discrete_sequence=cluster_colours,
        title="Purchase Frequency vs Monetary Value",
        labels={
            "Frequency": "Purchase Frequency",
            "Monetary": "Monetary Value",
            "Cluster Name": "Customer Cluster"
        },
        size_max=35
    )

    frequency_monetary_scatter.update_layout(
        height=480,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        legend_title="Clusters",
        margin=dict(t=65, l=45, r=30, b=40)
    )

    frequency_monetary_scatter.update_xaxes(
        gridcolor="rgba(148,163,184,0.20)"
    )
    frequency_monetary_scatter.update_yaxes(
        gridcolor="rgba(148,163,184,0.20)"
    )

    st.plotly_chart(
        frequency_monetary_scatter,
        use_container_width=True
    )

# ==========================================================
# RFM DISTRIBUTIONS
# ==========================================================

st.markdown(
    '<div class="section-title">📈 RFM Value Distribution</div>',
    unsafe_allow_html=True
)

distribution_tab1, distribution_tab2, distribution_tab3 = st.tabs(
    [
        "🕒 Recency Distribution",
        "🛍️ Frequency Distribution",
        "💰 Monetary Distribution"
    ]
)

with distribution_tab1:
    recency_histogram = px.histogram(
        filtered_rfm,
        x="Recency",
        color="Cluster Name",
        nbins=30,
        barmode="overlay",
        opacity=0.72,
        color_discrete_sequence=cluster_colours,
        title="Distribution of Customer Recency",
        labels={
            "Recency": "Recency (Days)",
            "count": "Customers"
        }
    )

    recency_histogram.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        bargap=0.08
    )

    st.plotly_chart(recency_histogram, use_container_width=True)

with distribution_tab2:
    frequency_histogram = px.histogram(
        filtered_rfm,
        x="Frequency",
        color="Cluster Name",
        nbins=30,
        barmode="overlay",
        opacity=0.72,
        color_discrete_sequence=cluster_colours,
        title="Distribution of Customer Purchase Frequency",
        labels={
            "Frequency": "Purchase Frequency",
            "count": "Customers"
        }
    )

    frequency_histogram.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        bargap=0.08
    )

    st.plotly_chart(frequency_histogram, use_container_width=True)

with distribution_tab3:
    monetary_histogram = px.histogram(
        filtered_rfm,
        x="Monetary",
        color="Cluster Name",
        nbins=35,
        barmode="overlay",
        opacity=0.72,
        color_discrete_sequence=cluster_colours,
        title="Distribution of Customer Monetary Value",
        labels={
            "Monetary": "Monetary Value",
            "count": "Customers"
        }
    )

    monetary_histogram.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        bargap=0.08
    )

    st.plotly_chart(monetary_histogram, use_container_width=True)

# ==========================================================
# CLUSTER AVERAGE COMPARISON
# ==========================================================

cluster_summary = (
    filtered_rfm.groupby(["Cluster", "Cluster Name"])
    .agg(
        Customers=(customer_id_column, "count"),
        Average_Recency=("Recency", "mean"),
        Average_Frequency=("Frequency", "mean"),
        Average_Monetary=("Monetary", "mean"),
        Total_Monetary=("Monetary", "sum")
    )
    .reset_index()
)

cluster_summary[
    [
        "Average_Recency",
        "Average_Frequency",
        "Average_Monetary",
        "Total_Monetary"
    ]
] = cluster_summary[
    [
        "Average_Recency",
        "Average_Frequency",
        "Average_Monetary",
        "Total_Monetary"
    ]
].round(2)

st.markdown(
    '<div class="section-title">⚖️ Cluster Performance Comparison</div>',
    unsafe_allow_html=True
)

comparison1, comparison2 = st.columns(2)

with comparison1:
    cluster_monetary_chart = px.bar(
        cluster_summary,
        x="Cluster Name",
        y="Average_Monetary",
        color="Cluster Name",
        text="Average_Monetary",
        color_discrete_sequence=cluster_colours,
        title="Average Monetary Value by Cluster"
    )

    cluster_monetary_chart.update_traces(
        texttemplate="$%{text:,.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average Monetary: $%{y:,.2f}<extra></extra>"
        )
    )

    cluster_monetary_chart.update_layout(
        showlegend=False,
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        xaxis_title="Customer Cluster",
        yaxis_title="Average Monetary Value"
    )

    st.plotly_chart(
        cluster_monetary_chart,
        use_container_width=True
    )

with comparison2:
    cluster_frequency_chart = px.bar(
        cluster_summary,
        x="Cluster Name",
        y="Average_Frequency",
        color="Cluster Name",
        text="Average_Frequency",
        color_discrete_sequence=cluster_colours,
        title="Average Purchase Frequency by Cluster"
    )

    cluster_frequency_chart.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average Frequency: %{y:,.2f}<extra></extra>"
        )
    )

    cluster_frequency_chart.update_layout(
        showlegend=False,
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        xaxis_title="Customer Cluster",
        yaxis_title="Average Purchase Frequency"
    )

    st.plotly_chart(
        cluster_frequency_chart,
        use_container_width=True
    )

# ==========================================================
# RFM RADAR CHART
# ==========================================================

st.markdown(
    '<div class="section-title">🎯 Normalized RFM Cluster Profile</div>',
    unsafe_allow_html=True
)

radar_data = cluster_summary[
    [
        "Cluster Name",
        "Average_Recency",
        "Average_Frequency",
        "Average_Monetary"
    ]
].copy()

metrics = [
    "Average_Recency",
    "Average_Frequency",
    "Average_Monetary"
]

for metric in metrics:
    minimum = radar_data[metric].min()
    maximum = radar_data[metric].max()

    if maximum != minimum:
        radar_data[metric] = (
            (radar_data[metric] - minimum)
            / (maximum - minimum)
        ) * 100
    else:
        radar_data[metric] = 100

# Lower recency is generally better, so reverse its normalized value
radar_data["Average_Recency"] = 100 - radar_data["Average_Recency"]

radar_chart = go.Figure()

for index, row in radar_data.iterrows():
    values = [
        row["Average_Recency"],
        row["Average_Frequency"],
        row["Average_Monetary"]
    ]

    radar_chart.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=[
                "Recency Score",
                "Frequency Score",
                "Monetary Score",
                "Recency Score"
            ],
            fill="toself",
            name=row["Cluster Name"],
            opacity=0.62
        )
    )

radar_chart.update_layout(
    title="RFM Behaviour Profile of Customer Clusters",
    title_x=0.02,
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    polar=dict(
        bgcolor="rgba(255,255,255,0.68)",
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            gridcolor="rgba(148,163,184,0.35)"
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.16,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(radar_chart, use_container_width=True)

# ==========================================================
# TOP HIGH-VALUE CUSTOMERS
# ==========================================================

st.markdown(
    '<div class="section-title">🏆 Top High-Value Customers</div>',
    unsafe_allow_html=True
)

top_customers = (
    filtered_rfm.nlargest(10, "Monetary")
    [
        [
            customer_id_column,
            "Recency",
            "Frequency",
            "Monetary",
            "Cluster Name"
        ]
    ]
    .sort_values("Monetary", ascending=True)
)

top_customer_chart = px.bar(
    top_customers,
    x="Monetary",
    y=customer_id_column,
    orientation="h",
    color="Cluster Name",
    text="Monetary",
    color_discrete_sequence=cluster_colours,
    title="Top 10 Customers Based on Monetary Value"
)

top_customer_chart.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside",
    hovertemplate=(
        "<b>Customer: %{y}</b><br>"
        "Monetary Value: $%{x:,.2f}<extra></extra>"
    )
)

top_customer_chart.update_layout(
    height=510,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.68)",
    title_x=0.02,
    xaxis_title="Monetary Value",
    yaxis_title="Customer",
    legend_title="Cluster",
    margin=dict(l=70, r=40, t=65, b=40)
)

st.plotly_chart(top_customer_chart, use_container_width=True)

# ==========================================================
# AUTOMATIC BUSINESS INSIGHTS
# ==========================================================

largest_cluster = cluster_count.loc[
    cluster_count["Customers"].idxmax()
]

highest_monetary_cluster = cluster_summary.loc[
    cluster_summary["Average_Monetary"].idxmax()
]

most_frequent_cluster = cluster_summary.loc[
    cluster_summary["Average_Frequency"].idxmax()
]

most_recent_cluster = cluster_summary.loc[
    cluster_summary["Average_Recency"].idxmin()
]

st.markdown(
    '<div class="section-title">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

insight1, insight2 = st.columns(2)

with insight1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">👥 Largest Customer Group</div>
            <div class="insight-text">
                <b>{largest_cluster["Cluster Name"]}</b> is the largest
                segment with <b>{int(largest_cluster["Customers"]):,}
                customers</b>. This cluster represents the largest portion
                of the selected customer base.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">💰 Highest-Spending Segment</div>
            <div class="insight-text">
                <b>{highest_monetary_cluster["Cluster Name"]}</b> has the
                highest average monetary value of
                <b>${highest_monetary_cluster["Average_Monetary"]:,.2f}</b>.
                These customers may be suitable for premium offers and
                loyalty benefits.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with insight2:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🛍️ Most Frequent Buyers</div>
            <div class="insight-text">
                <b>{most_frequent_cluster["Cluster Name"]}</b> has the
                highest average purchase frequency of
                <b>{most_frequent_cluster["Average_Frequency"]:,.2f}</b>.
                Regular engagement can help retain this group.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">🕒 Most Recently Active Segment</div>
            <div class="insight-text">
                <b>{most_recent_cluster["Cluster Name"]}</b> has the lowest
                average recency value of
                <b>{most_recent_cluster["Average_Recency"]:,.2f} days</b>,
                indicating comparatively recent purchasing activity.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# CLUSTER STATISTICS TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Cluster Statistics</div>',
    unsafe_allow_html=True
)

display_summary = cluster_summary.rename(
    columns={
        "Cluster Name": "Customer Segment",
        "Average_Recency": "Average Recency",
        "Average_Frequency": "Average Frequency",
        "Average_Monetary": "Average Monetary",
        "Total_Monetary": "Total Monetary"
    }
)

st.dataframe(
    display_summary[
        [
            "Customer Segment",
            "Customers",
            "Average Recency",
            "Average Frequency",
            "Average Monetary",
            "Total Monetary"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Customers": st.column_config.NumberColumn(
            "Customers",
            format="%d"
        ),
        "Average Recency": st.column_config.NumberColumn(
            "Average Recency",
            format="%.2f days"
        ),
        "Average Frequency": st.column_config.NumberColumn(
            "Average Frequency",
            format="%.2f"
        ),
        "Average Monetary": st.column_config.NumberColumn(
            "Average Monetary",
            format="$%.2f"
        ),
        "Total Monetary": st.column_config.NumberColumn(
            "Total Monetary",
            format="$%.2f"
        )
    }
)

# ==========================================================
# CUSTOMER DATA TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">🗂️ Customer Segmentation Data</div>',
    unsafe_allow_html=True
)

table_columns = [
    customer_id_column,
    "Recency",
    "Frequency",
    "Monetary",
    "Cluster",
    "Cluster Name"
]

st.dataframe(
    filtered_rfm[table_columns].sort_values(
        "Monetary",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
    height=430,
    column_config={
        customer_id_column: st.column_config.TextColumn(
            "Customer ID"
        ),
        "Recency": st.column_config.NumberColumn(
            "Recency",
            format="%.0f days"
        ),
        "Frequency": st.column_config.NumberColumn(
            "Frequency",
            format="%.0f"
        ),
        "Monetary": st.column_config.NumberColumn(
            "Monetary",
            format="$%.2f"
        ),
        "Cluster": st.column_config.NumberColumn(
            "Cluster",
            format="%d"
        )
    }
)

# ==========================================================
# DOWNLOAD SECTION
# ==========================================================

st.markdown(
    '<div class="section-title">⬇️ Download Reports</div>',
    unsafe_allow_html=True
)

download1, download2 = st.columns(2)

filtered_csv = filtered_rfm.to_csv(index=False).encode("utf-8")
summary_csv = display_summary.to_csv(index=False).encode("utf-8")

with download1:
    st.download_button(
        label="⬇️ Download Filtered Customer Data",
        data=filtered_csv,
        file_name="filtered_customer_segments.csv",
        mime="text/csv"
    )

with download2:
    st.download_button(
        label="⬇️ Download Cluster Summary",
        data=summary_csv,
        file_name="customer_cluster_summary.csv",
        mime="text/csv"
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:16px;
        color:#475569;
        font-size:14px;
    ">
        <b>NeuralRetail – AI-Powered Retail Analytics Platform</b><br>
        Customer Segmentation using RFM Analysis and K-Means Clustering
    </div>
    """,
    unsafe_allow_html=True
)