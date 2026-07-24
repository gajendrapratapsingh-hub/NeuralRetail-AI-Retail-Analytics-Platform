import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Business Recommendation",
    page_icon="💡",
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
                rgba(250, 204, 21, 0.22),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 20%,
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
                #eff6ff 80%,
                #ecfeff 100%
            );

        background-attachment: fixed;
    }

    /* Main page container */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #78350f 0%,
            #9d174d 48%,
            #312e81 100%
        );

        border-right: 1px solid rgba(255, 255, 255, 0.20);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] .stTextInput div,
    section[data-testid="stSidebar"] .stMultiSelect div {
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
        font-size: 29px;
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

    /* Chart containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.80);
        border-radius: 18px;
        padding: 8px;

        border: 1px solid rgba(255, 255, 255, 0.86);

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

    /* Insight cards */
    .insight-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);

        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 12px;

        border-left: 6px solid #7c3aed;

        box-shadow:
            0 8px 22px rgba(30, 41, 59, 0.08);

        color: #1e293b;
        font-size: 15px;
        font-weight: 600;
    }

    .high-insight {
        border-left-color: #ef4444;
    }

    .medium-insight {
        border-left-color: #f59e0b;
    }

    .low-insight {
        border-left-color: #10b981;
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

    /* Divider */
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
            💡 Business Recommendation Dashboard
        </p>

        <p class="dashboard-subtitle">
            Explore AI-generated business recommendations,
            priority levels, and actionable retail insights.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_recommendation_data():
    return pd.read_csv(
        "data/processed/business_recommendations.csv"
    )


try:
    recommendation = load_recommendation_data()

except FileNotFoundError:
    st.error(
        "❌ business_recommendations.csv was not found "
        "inside data/processed."
    )
    st.stop()

except Exception as error:
    st.error(
        f"❌ Error loading business_recommendations.csv:"
        f"\n\n{error}"
    )
    st.stop()

# ==========================================================
# CHECK AND CLEAN PRIORITY COLUMN
# ==========================================================

if "Priority" not in recommendation.columns:
    recommendation["Priority"] = "Medium"

recommendation["Priority"] = (
    recommendation["Priority"]
    .fillna("Medium")
    .astype(str)
    .str.strip()
    .str.title()
)

valid_priorities = ["High", "Medium", "Low"]

recommendation.loc[
    ~recommendation["Priority"].isin(valid_priorities),
    "Priority"
] = "Medium"

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

with st.sidebar:

    st.markdown("## 🎛️ Recommendation Filters")

    st.markdown(
        "Use these filters to explore specific recommendations."
    )

    selected_priorities = st.multiselect(
        "Select Priority",
        options=valid_priorities,
        default=valid_priorities
    )

    search_text = st.text_input(
        "Search Recommendation",
        placeholder="Enter keyword"
    )

    st.markdown("---")

    st.markdown(
        """
        ### 📌 Priority Meaning

        **High:** Requires immediate business attention

        **Medium:** Important but can be planned

        **Low:** Useful improvement with lower urgency
        """
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = recommendation[
    recommendation["Priority"].isin(
        selected_priorities
    )
].copy()

if search_text:

    search_text = search_text.strip()

    searchable_columns = [
        column
        for column in recommendation.columns
        if recommendation[column].dtype == "object"
    ]

    search_mask = pd.Series(
        False,
        index=filtered.index
    )

    for column in searchable_columns:
        search_mask = (
            search_mask
            |
            filtered[column]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        )

    filtered = filtered[search_mask]

if filtered.empty:
    st.warning(
        "No recommendations match the selected filters."
    )

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_recommendations = len(filtered)

high_priority = len(
    filtered[
        filtered["Priority"] == "High"
    ]
)

medium_priority = len(
    filtered[
        filtered["Priority"] == "Medium"
    ]
)

low_priority = len(
    filtered[
        filtered["Priority"] == "Low"
    ]
)

if total_recommendations > 0:
    high_priority_percentage = (
        high_priority / total_recommendations
    ) * 100
else:
    high_priority_percentage = 0

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Recommendation Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💡</div>
            <div class="kpi-label">Recommendations</div>
            <div class="kpi-value">
                {total_recommendations:,}
            </div>
            <div class="kpi-description">
                Recommendations currently displayed
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-label">High Priority</div>
            <div class="kpi-value">
                {high_priority:,}
            </div>
            <div class="kpi-description">
                Immediate business attention
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Medium Priority</div>
            <div class="kpi-value">
                {medium_priority:,}
            </div>
            <div class="kpi-description">
                Important planned actions
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">✅</div>
            <div class="kpi-label">Low Priority</div>
            <div class="kpi-value">
                {low_priority:,}
            </div>
            <div class="kpi-description">
                Lower urgency improvements
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
            <div class="kpi-label">High Priority Rate</div>
            <div class="kpi-value">
                {high_priority_percentage:.1f}%
            </div>
            <div class="kpi-description">
                Share of urgent recommendations
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# PRIORITY DISTRIBUTION
# ==========================================================

priority_count = (
    filtered["Priority"]
    .value_counts()
    .reindex(
        valid_priorities,
        fill_value=0
    )
    .reset_index()
)

priority_count.columns = [
    "Priority",
    "Count"
]

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.markdown(
        '<div class="section-title">🥧 Priority Distribution</div>',
        unsafe_allow_html=True
    )

    pie_chart = px.pie(
        priority_count,
        names="Priority",
        values="Count",
        hole=0.50,
        title="Recommendation Priority Distribution",
        color="Priority",
        color_discrete_map={
            "High": "#ef4444",
            "Medium": "#f59e0b",
            "Low": "#10b981"
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
            "Recommendations: %{value:,}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    pie_chart.update_layout(
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.02,
        legend_title="Priority",
        annotations=[
            dict(
                text=(
                    f"{total_recommendations:,}"
                    "<br>Recommendations"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font_size=15
            )
        ]
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

# ==========================================================
# PRIORITY BAR CHART
# ==========================================================

with chart_col2:

    st.markdown(
        '<div class="section-title">📊 Recommendation Summary</div>',
        unsafe_allow_html=True
    )

    bar_chart = px.bar(
        priority_count,
        x="Priority",
        y="Count",
        color="Priority",
        text="Count",
        title="Recommendations by Priority",
        color_discrete_map={
            "High": "#ef4444",
            "Medium": "#f59e0b",
            "Low": "#10b981"
        }
    )

    bar_chart.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1.5,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Recommendations: %{y:,}"
            "<extra></extra>"
        )
    )

    bar_chart.update_layout(
        height=430,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.65)",
        title_x=0.02,
        xaxis_title="Priority",
        yaxis_title="Number of Recommendations"
    )

    bar_chart.update_yaxes(
        gridcolor="rgba(148,163,184,0.22)"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

# ==========================================================
# BUSINESS RECOMMENDATIONS TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Business Recommendations</div>',
    unsafe_allow_html=True
)

if filtered.empty:

    st.info(
        "No business recommendations are available "
        "for the selected filters."
    )

else:

    priority_order = pd.CategoricalDtype(
        categories=[
            "High",
            "Medium",
            "Low"
        ],
        ordered=True
    )

    filtered["Priority"] = filtered[
        "Priority"
    ].astype(priority_order)

    filtered = filtered.sort_values(
        "Priority"
    )

    filtered["Priority"] = filtered[
        "Priority"
    ].astype(str)

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=450,
        column_config={
            "Priority": st.column_config.TextColumn(
                "Priority",
                help=(
                    "High means urgent, Medium means planned, "
                    "and Low means lower urgency."
                )
            )
        }
    )

# ==========================================================
# AI BUSINESS INSIGHTS
# ==========================================================

st.markdown(
    '<div class="section-title">🤖 AI Business Insights</div>',
    unsafe_allow_html=True
)

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.markdown(
        """
        <div class="insight-card high-insight">
            🚨 <b>Inventory Strategy:</b>
            Increase inventory levels for fast-moving and
            high-demand products to avoid stock shortages.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card medium-insight">
            🏷️ <b>Discount Strategy:</b>
            Offer targeted discounts on slow-moving products
            to improve sales and reduce excess stock.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card high-insight">
            🔄 <b>Customer Retention:</b>
            Contact high-risk churn customers with
            personalised offers and loyalty benefits.
        </div>
        """,
        unsafe_allow_html=True
    )

with insight_col2:

    st.markdown(
        """
        <div class="insight-card medium-insight">
            💰 <b>Price Optimization:</b>
            Use recommended prices and discount predictions
            to improve revenue and profitability.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card low-insight">
            📈 <b>Demand Forecasting:</b>
            Review forecasted sales regularly to improve
            purchasing and inventory planning.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card low-insight">
            🎯 <b>Customer Marketing:</b>
            Focus premium campaigns on high-value customers
            and personalised campaigns on other segments.
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# DOWNLOAD DATA
# ==========================================================

st.markdown(
    '<div class="section-title">⬇️ Download Recommendations</div>',
    unsafe_allow_html=True
)

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Recommendations CSV",
    data=csv,
    file_name="business_recommendations.csv",
    mime="text/csv"
)

# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

st.success(
    "✅ Business Recommendation Dashboard Loaded Successfully"
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

        AI Business Recommendation and Decision Support Module

    </div>
    """,
    unsafe_allow_html=True
)