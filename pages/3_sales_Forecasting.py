import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📈",
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
            radial-gradient(circle at 10% 15%, rgba(14, 165, 233, 0.22), transparent 35%),
            radial-gradient(circle at 90% 20%, rgba(124, 58, 237, 0.20), transparent 35%),
            radial-gradient(circle at 50% 90%, rgba(16, 185, 129, 0.16), transparent 40%),
            linear-gradient(
                135deg,
                #ecfeff 0%,
                #eff6ff 30%,
                #f5f3ff 65%,
                #ecfdf5 100%
            );
        background-attachment: fixed;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0f172a 0%,
            #0c4a6e 45%,
            #312e81 100%
        );
        border-right: 1px solid rgba(255, 255, 255, 0.20);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] .stMultiSelect div,
    section[data-testid="stSidebar"] .stDateInput div {
        color: #111827;
    }

    /* Header */
    .dashboard-header {
        background: linear-gradient(
            120deg,
            #0284c7,
            #2563eb,
            #7c3aed,
            #059669
        );
        padding: 28px 30px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 15px 38px rgba(37, 99, 235, 0.25);
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
        opacity: 0.93;
    }

    /* Section heading */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #1e3a8a;
        margin-top: 20px;
        margin-bottom: 12px;
        padding-left: 12px;
        border-left: 6px solid #0ea5e9;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.84);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px 18px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.80);
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.10);
        min-height: 138px;
        margin-bottom: 10px;
        transition: all 0.25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 17px 36px rgba(37, 99, 235, 0.20);
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
        color: #0f172a;
        font-size: 27px;
        font-weight: 800;
        margin-top: 4px;
    }

    .kpi-description {
        color: #2563eb;
        font-size: 12px;
        font-weight: 600;
        margin-top: 3px;
    }

    /* Insight cards */
    .insight-card {
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.90),
            rgba(239, 246, 255, 0.88)
        );
        padding: 20px;
        border-radius: 17px;
        border: 1px solid rgba(14, 165, 233, 0.20);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        margin-top: 8px;
        margin-bottom: 12px;
    }

    .insight-title {
        color: #1d4ed8;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .insight-text {
        color: #334155;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Plotly containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.75);
        border-radius: 18px;
        padding: 7px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.82);
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    }

    /* Download buttons */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(
            90deg,
            #0284c7,
            #2563eb,
            #7c3aed
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
        box-shadow: 0 10px 22px rgba(37, 99, 235, 0.25);
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(37, 99, 235, 0.40),
            transparent
        );
        margin: 24px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class="dashboard-header">
        <p class="dashboard-title">📈 Sales Forecasting Dashboard</p>
        <p class="dashboard-subtitle">
            Analyze predicted sales trends, compare actual and forecasted
            performance, and support future business planning.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_forecast_data():
    return pd.read_csv("data/processed/forecasted_sales.csv")


try:
    forecast = load_forecast_data()

except FileNotFoundError:
    st.error(
        "❌ `forecasted_sales.csv` was not found in "
        "`data/processed/forecasted_sales.csv`."
    )
    st.stop()

except Exception as error:
    st.error(f"❌ Unable to load forecast data: {error}")
    st.stop()

# ==========================================================
# VALIDATE DATA
# ==========================================================

required_columns = {"Date", "PredictedSales"}

missing_columns = required_columns.difference(forecast.columns)

if missing_columns:
    st.error(
        "The following required columns are missing: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

forecast["Date"] = pd.to_datetime(
    forecast["Date"],
    errors="coerce"
)

forecast["PredictedSales"] = pd.to_numeric(
    forecast["PredictedSales"],
    errors="coerce"
)

if "ActualSales" in forecast.columns:
    forecast["ActualSales"] = pd.to_numeric(
        forecast["ActualSales"],
        errors="coerce"
    )

forecast = forecast.dropna(
    subset=["Date", "PredictedSales"]
).copy()

forecast = forecast.sort_values("Date").reset_index(drop=True)

if forecast.empty:
    st.warning("No valid sales forecasting records are available.")
    st.stop()

# Additional columns
forecast["Month"] = forecast["Date"].dt.strftime("%b %Y")
forecast["MonthNumber"] = forecast["Date"].dt.to_period("M")
forecast["DayName"] = forecast["Date"].dt.day_name()
forecast["Week"] = forecast["Date"].dt.isocalendar().week.astype(int)
forecast["Year"] = forecast["Date"].dt.year

forecast["DailyChange"] = forecast["PredictedSales"].diff()
forecast["GrowthPercent"] = (
    forecast["PredictedSales"].pct_change() * 100
).replace([float("inf"), -float("inf")], pd.NA)

forecast["MovingAverage"] = (
    forecast["PredictedSales"]
    .rolling(window=7, min_periods=1)
    .mean()
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

with st.sidebar:
    st.markdown("## 🎛️ Forecast Filters")
    st.markdown(
        "Use these filters to analyse a selected forecasting period."
    )

    minimum_date = forecast["Date"].min().date()
    maximum_date = forecast["Date"].max().date()

    selected_dates = st.date_input(
        "Select date range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date
    )

    available_years = sorted(
        forecast["Year"].unique().tolist()
    )

    selected_years = st.multiselect(
        "Select year",
        options=available_years,
        default=available_years
    )

    chart_style = st.selectbox(
        "Main trend chart style",
        options=[
            "Line Chart",
            "Area Chart",
            "Bar Chart"
        ]
    )

    show_moving_average = st.checkbox(
        "Show 7-day moving average",
        value=True
    )

    st.markdown("---")

    st.markdown(
        """
        ### 📌 Dashboard Guide

        **Predicted Sales:** Forecasted future sales value  
        **Actual Sales:** Original observed sales value  
        **Moving Average:** Smoothed seven-day trend  
        **Growth Rate:** Percentage change between periods  
        """
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])
else:
    start_date = pd.Timestamp(minimum_date)
    end_date = pd.Timestamp(maximum_date)

filtered_forecast = forecast[
    (forecast["Date"] >= start_date)
    & (forecast["Date"] <= end_date)
    & (forecast["Year"].isin(selected_years))
].copy()

if filtered_forecast.empty:
    st.warning(
        "No forecasting records match the selected filters."
    )
    st.stop()

# Recalculate filtered changes
filtered_forecast["DailyChange"] = (
    filtered_forecast["PredictedSales"].diff()
)

filtered_forecast["GrowthPercent"] = (
    filtered_forecast["PredictedSales"].pct_change() * 100
).replace([float("inf"), -float("inf")], pd.NA)

filtered_forecast["MovingAverage"] = (
    filtered_forecast["PredictedSales"]
    .rolling(window=7, min_periods=1)
    .mean()
)

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_days = len(filtered_forecast)
total_forecast_sales = filtered_forecast["PredictedSales"].sum()
average_sales = filtered_forecast["PredictedSales"].mean()
highest_sales = filtered_forecast["PredictedSales"].max()
lowest_sales = filtered_forecast["PredictedSales"].min()

highest_sales_date = filtered_forecast.loc[
    filtered_forecast["PredictedSales"].idxmax(),
    "Date"
]

first_sales = filtered_forecast["PredictedSales"].iloc[0]
last_sales = filtered_forecast["PredictedSales"].iloc[-1]

if first_sales != 0:
    overall_growth = (
        (last_sales - first_sales) / first_sales
    ) * 100
else:
    overall_growth = 0

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Forecast Overview</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📅</div>
            <div class="kpi-label">Forecast Days</div>
            <div class="kpi-value">{total_days:,}</div>
            <div class="kpi-description">Selected forecast records</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Forecast</div>
            <div class="kpi-value">${total_forecast_sales:,.0f}</div>
            <div class="kpi-description">Combined predicted sales</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Average Sales</div>
            <div class="kpi-value">${average_sales:,.2f}</div>
            <div class="kpi-description">Average forecast value</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚀</div>
            <div class="kpi-label">Highest Sales</div>
            <div class="kpi-value">${highest_sales:,.2f}</div>
            <div class="kpi-description">
                {highest_sales_date.strftime("%d %b %Y")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📉</div>
            <div class="kpi-label">Lowest Sales</div>
            <div class="kpi-value">${lowest_sales:,.2f}</div>
            <div class="kpi-description">Minimum predicted value</div>
        </div>
        """,
        unsafe_allow_html=True
    )

growth_icon = "⬆️" if overall_growth >= 0 else "⬇️"

with kpi6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{growth_icon}</div>
            <div class="kpi-label">Overall Growth</div>
            <div class="kpi-value">{overall_growth:,.2f}%</div>
            <div class="kpi-description">First to latest forecast</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# MAIN FORECAST TREND
# ==========================================================

st.markdown(
    '<div class="section-title">📈 Forecast Sales Trend</div>',
    unsafe_allow_html=True
)

if chart_style == "Line Chart":

    trend_chart = go.Figure()

    trend_chart.add_trace(
        go.Scatter(
            x=filtered_forecast["Date"],
            y=filtered_forecast["PredictedSales"],
            mode="lines+markers",
            name="Predicted Sales",
            line=dict(width=3),
            marker=dict(size=7),
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Predicted Sales: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    if show_moving_average:
        trend_chart.add_trace(
            go.Scatter(
                x=filtered_forecast["Date"],
                y=filtered_forecast["MovingAverage"],
                mode="lines",
                name="7-Day Moving Average",
                line=dict(width=3, dash="dash"),
                hovertemplate=(
                    "<b>%{x|%d %b %Y}</b><br>"
                    "Moving Average: $%{y:,.2f}"
                    "<extra></extra>"
                )
            )
        )

elif chart_style == "Area Chart":

    trend_chart = go.Figure()

    trend_chart.add_trace(
        go.Scatter(
            x=filtered_forecast["Date"],
            y=filtered_forecast["PredictedSales"],
            mode="lines",
            fill="tozeroy",
            name="Predicted Sales",
            line=dict(width=3),
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Predicted Sales: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    if show_moving_average:
        trend_chart.add_trace(
            go.Scatter(
                x=filtered_forecast["Date"],
                y=filtered_forecast["MovingAverage"],
                mode="lines",
                name="7-Day Moving Average",
                line=dict(width=3, dash="dash")
            )
        )

else:

    trend_chart = go.Figure()

    trend_chart.add_trace(
        go.Bar(
            x=filtered_forecast["Date"],
            y=filtered_forecast["PredictedSales"],
            name="Predicted Sales",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Predicted Sales: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    if show_moving_average:
        trend_chart.add_trace(
            go.Scatter(
                x=filtered_forecast["Date"],
                y=filtered_forecast["MovingAverage"],
                mode="lines",
                name="7-Day Moving Average",
                line=dict(width=3)
            )
        )

trend_chart.update_layout(
    title="Predicted Sales Performance Over Time",
    title_x=0.02,
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.68)",
    xaxis_title="Forecast Date",
    yaxis_title="Predicted Sales",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(t=90, l=55, r=30, b=50)
)

trend_chart.update_xaxes(
    gridcolor="rgba(148,163,184,0.20)"
)

trend_chart.update_yaxes(
    gridcolor="rgba(148,163,184,0.20)",
    tickprefix="$"
)

st.plotly_chart(trend_chart, use_container_width=True)

# ==========================================================
# MONTHLY SALES AND DISTRIBUTION
# ==========================================================

monthly_summary = (
    filtered_forecast.groupby(
        ["MonthNumber", "Month"],
        as_index=False
    )["PredictedSales"]
    .sum()
    .sort_values("MonthNumber")
)

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown(
        '<div class="section-title">📊 Monthly Forecast</div>',
        unsafe_allow_html=True
    )

    monthly_chart = px.bar(
        monthly_summary,
        x="Month",
        y="PredictedSales",
        text="PredictedSales",
        color="PredictedSales",
        color_continuous_scale="Blues",
        title="Total Predicted Sales by Month"
    )

    monthly_chart.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Predicted Sales: $%{y:,.2f}"
            "<extra></extra>"
        )
    )

    monthly_chart.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        xaxis_title="Month",
        yaxis_title="Predicted Sales",
        coloraxis_showscale=False
    )

    monthly_chart.update_yaxes(tickprefix="$")

    st.plotly_chart(monthly_chart, use_container_width=True)

with chart2:
    st.markdown(
        '<div class="section-title">🥧 Monthly Sales Share</div>',
        unsafe_allow_html=True
    )

    monthly_pie = px.pie(
        monthly_summary,
        names="Month",
        values="PredictedSales",
        hole=0.52,
        title="Contribution of Each Month to Forecast Sales"
    )

    monthly_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(color="white", width=2)
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Sales: $%{value:,.2f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    monthly_pie.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.02,
        annotations=[
            dict(
                text=f"${total_forecast_sales:,.0f}<br>Total",
                x=0.5,
                y=0.5,
                font_size=16,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(monthly_pie, use_container_width=True)

# ==========================================================
# ACTUAL VS PREDICTED SALES
# ==========================================================

if (
    "ActualSales" in filtered_forecast.columns
    and filtered_forecast["ActualSales"].notna().any()
):

    st.markdown(
        '<div class="section-title">⚖️ Actual vs Predicted Sales</div>',
        unsafe_allow_html=True
    )

    comparison_chart = go.Figure()

    comparison_chart.add_trace(
        go.Scatter(
            x=filtered_forecast["Date"],
            y=filtered_forecast["ActualSales"],
            mode="lines+markers",
            name="Actual Sales",
            line=dict(width=3),
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Actual Sales: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    comparison_chart.add_trace(
        go.Scatter(
            x=filtered_forecast["Date"],
            y=filtered_forecast["PredictedSales"],
            mode="lines+markers",
            name="Predicted Sales",
            line=dict(width=3, dash="dash"),
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Predicted Sales: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    comparison_chart.update_layout(
        title="Comparison Between Actual and Predicted Sales",
        title_x=0.02,
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    comparison_chart.update_yaxes(tickprefix="$")

    st.plotly_chart(
        comparison_chart,
        use_container_width=True
    )

    # ======================================================
    # FORECAST ERROR ANALYSIS
    # ======================================================

    error_data = filtered_forecast.dropna(
        subset=["ActualSales"]
    ).copy()

    error_data["ForecastError"] = (
        error_data["ActualSales"]
        - error_data["PredictedSales"]
    )

    error_data["AbsoluteError"] = (
        error_data["ForecastError"].abs()
    )

    error_data["PercentageError"] = (
        error_data["AbsoluteError"]
        / error_data["ActualSales"].replace(0, pd.NA)
    ) * 100

    average_absolute_error = error_data["AbsoluteError"].mean()
    average_percentage_error = (
        error_data["PercentageError"].mean()
    )

    error1, error2 = st.columns(2)

    with error1:
        error_chart = px.bar(
            error_data,
            x="Date",
            y="ForecastError",
            color="ForecastError",
            color_continuous_scale="RdBu",
            title="Forecast Error by Date"
        )

        error_chart.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.68)",
            title_x=0.02,
            xaxis_title="Date",
            yaxis_title="Actual − Predicted"
        )

        st.plotly_chart(
            error_chart,
            use_container_width=True
        )

    with error2:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    🎯 Forecast Accuracy Summary
                </div>
                <div class="insight-text">
                    Average absolute forecast error:
                    <b>${average_absolute_error:,.2f}</b>
                    <br><br>
                    Average percentage error:
                    <b>{average_percentage_error:,.2f}%</b>
                    <br><br>
                    Lower values indicate that predicted sales are
                    closer to actual sales.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# SALES DISTRIBUTION AND GROWTH
# ==========================================================

st.markdown(
    '<div class="section-title">📉 Sales Distribution and Growth</div>',
    unsafe_allow_html=True
)

distribution1, distribution2 = st.columns(2)

with distribution1:
    sales_histogram = px.histogram(
        filtered_forecast,
        x="PredictedSales",
        nbins=30,
        marginal="box",
        title="Distribution of Predicted Sales",
        labels={
            "PredictedSales": "Predicted Sales",
            "count": "Number of Days"
        },
        color_discrete_sequence=["#2563eb"]
    )

    sales_histogram.update_layout(
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        bargap=0.07
    )

    sales_histogram.update_xaxes(tickprefix="$")

    st.plotly_chart(
        sales_histogram,
        use_container_width=True
    )

with distribution2:
    growth_data = filtered_forecast.dropna(
        subset=["GrowthPercent"]
    )

    growth_chart = px.bar(
        growth_data,
        x="Date",
        y="GrowthPercent",
        color="GrowthPercent",
        color_continuous_scale="RdYlGn",
        title="Period-to-Period Sales Growth"
    )

    growth_chart.update_layout(
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        xaxis_title="Date",
        yaxis_title="Growth Rate (%)",
        coloraxis_showscale=False
    )

    growth_chart.update_yaxes(ticksuffix="%")

    st.plotly_chart(
        growth_chart,
        use_container_width=True
    )

# ==========================================================
# DAY-WISE SALES ANALYSIS
# ==========================================================

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_summary = (
    filtered_forecast.groupby("DayName")["PredictedSales"]
    .agg(["mean", "sum", "count"])
    .reset_index()
)

day_summary["DayName"] = pd.Categorical(
    day_summary["DayName"],
    categories=day_order,
    ordered=True
)

day_summary = day_summary.sort_values("DayName")

st.markdown(
    '<div class="section-title">📅 Day-wise Forecast Analysis</div>',
    unsafe_allow_html=True
)

day_chart = px.bar(
    day_summary,
    x="DayName",
    y="mean",
    color="mean",
    text="mean",
    color_continuous_scale="Viridis",
    title="Average Predicted Sales by Day of the Week",
    labels={
        "DayName": "Day",
        "mean": "Average Predicted Sales"
    }
)

day_chart.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

day_chart.update_layout(
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.68)",
    title_x=0.02,
    coloraxis_showscale=False
)

day_chart.update_yaxes(tickprefix="$")

st.plotly_chart(day_chart, use_container_width=True)

# ==========================================================
# TOP AND LOWEST FORECAST DAYS
# ==========================================================

st.markdown(
    '<div class="section-title">🏆 Highest and Lowest Forecast Days</div>',
    unsafe_allow_html=True
)

top_days = filtered_forecast.nlargest(
    10,
    "PredictedSales"
)[["Date", "PredictedSales"]].copy()

top_days["DateLabel"] = top_days["Date"].dt.strftime(
    "%d %b %Y"
)

lowest_days = filtered_forecast.nsmallest(
    10,
    "PredictedSales"
)[["Date", "PredictedSales"]].copy()

lowest_days["DateLabel"] = lowest_days["Date"].dt.strftime(
    "%d %b %Y"
)

top_col, low_col = st.columns(2)

with top_col:
    top_chart = px.bar(
        top_days.sort_values("PredictedSales"),
        x="PredictedSales",
        y="DateLabel",
        orientation="h",
        text="PredictedSales",
        title="Top 10 Forecast Sales Days",
        color="PredictedSales",
        color_continuous_scale="Greens"
    )

    top_chart.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    top_chart.update_layout(
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        xaxis_title="Predicted Sales",
        yaxis_title="Date",
        coloraxis_showscale=False
    )

    top_chart.update_xaxes(tickprefix="$")

    st.plotly_chart(top_chart, use_container_width=True)

with low_col:
    lowest_chart = px.bar(
        lowest_days.sort_values(
            "PredictedSales",
            ascending=False
        ),
        x="PredictedSales",
        y="DateLabel",
        orientation="h",
        text="PredictedSales",
        title="Lowest 10 Forecast Sales Days",
        color="PredictedSales",
        color_continuous_scale="Oranges"
    )

    lowest_chart.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    lowest_chart.update_layout(
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        title_x=0.02,
        xaxis_title="Predicted Sales",
        yaxis_title="Date",
        coloraxis_showscale=False
    )

    lowest_chart.update_xaxes(tickprefix="$")

    st.plotly_chart(
        lowest_chart,
        use_container_width=True
    )

# ==========================================================
# AUTOMATIC BUSINESS INSIGHTS
# ==========================================================

best_day_name = day_summary.loc[
    day_summary["mean"].idxmax(),
    "DayName"
]

best_day_average = day_summary.loc[
    day_summary["mean"].idxmax(),
    "mean"
]

best_month = monthly_summary.loc[
    monthly_summary["PredictedSales"].idxmax(),
    "Month"
]

best_month_sales = monthly_summary.loc[
    monthly_summary["PredictedSales"].idxmax(),
    "PredictedSales"
]

trend_direction = (
    "increasing"
    if overall_growth > 0
    else "decreasing"
    if overall_growth < 0
    else "stable"
)

st.markdown(
    '<div class="section-title">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

insight1, insight2 = st.columns(2)

with insight1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                🚀 Highest Forecast Period
            </div>
            <div class="insight-text">
                The highest predicted sales value is
                <b>${highest_sales:,.2f}</b> on
                <b>{highest_sales_date.strftime("%d %b %Y")}</b>.
                The business should prepare sufficient stock and staff
                for this period.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">
                📅 Strongest Day of the Week
            </div>
            <div class="insight-text">
                <b>{best_day_name}</b> has the highest average predicted
                sales of <b>${best_day_average:,.2f}</b>.
                Marketing campaigns can be concentrated around this day.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with insight2:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                🗓️ Best Forecast Month
            </div>
            <div class="insight-text">
                <b>{best_month}</b> has the highest total forecast sales
                of <b>${best_month_sales:,.2f}</b>.
                Inventory and promotional planning should be strengthened
                for this month.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">
                📈 Overall Sales Direction
            </div>
            <div class="insight-text">
                The selected forecast period shows an
                <b>{trend_direction}</b> trend with an overall change of
                <b>{overall_growth:,.2f}%</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# FORECAST TABLE
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Forecast Data</div>',
    unsafe_allow_html=True
)

display_columns = [
    "Date",
    "PredictedSales",
    "MovingAverage",
    "DailyChange",
    "GrowthPercent"
]

if "ActualSales" in filtered_forecast.columns:
    display_columns.insert(2, "ActualSales")

st.dataframe(
    filtered_forecast[display_columns],
    use_container_width=True,
    hide_index=True,
    height=440,
    column_config={
        "Date": st.column_config.DateColumn(
            "Forecast Date",
            format="DD MMM YYYY"
        ),
        "ActualSales": st.column_config.NumberColumn(
            "Actual Sales",
            format="$%.2f"
        ),
        "PredictedSales": st.column_config.NumberColumn(
            "Predicted Sales",
            format="$%.2f"
        ),
        "MovingAverage": st.column_config.NumberColumn(
            "7-Day Moving Average",
            format="$%.2f"
        ),
        "DailyChange": st.column_config.NumberColumn(
            "Daily Change",
            format="$%.2f"
        ),
        "GrowthPercent": st.column_config.NumberColumn(
            "Growth",
            format="%.2f%%"
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

filtered_csv = filtered_forecast.to_csv(
    index=False
).encode("utf-8")

monthly_csv = monthly_summary.to_csv(
    index=False
).encode("utf-8")

with download1:
    st.download_button(
        label="⬇️ Download Filtered Forecast Data",
        data=filtered_csv,
        file_name="filtered_forecasted_sales.csv",
        mime="text/csv"
    )

with download2:
    st.download_button(
        label="⬇️ Download Monthly Forecast Summary",
        data=monthly_csv,
        file_name="monthly_forecast_summary.csv",
        mime="text/csv"
    )

# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

st.success(
    "✅ Sales Forecasting Dashboard Loaded Successfully"
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
        Sales Forecasting using historical sales data and Linear Regression
    </div>
    """,
    unsafe_allow_html=True
)