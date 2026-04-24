import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from prophet import Prophet

# ---------------------------------
# AUTO REFRESH
# ---------------------------------
st_autorefresh(interval=60000, key="refresh")

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Crypto Analytics Dashboard", layout="wide")

st.title("🚀 Crypto Analytics Dashboard")

# ---------------------------------
# SQL QUERIES
# ---------------------------------
latest_query = """
SELECT *
FROM crypto_prices
WHERE timestamp = (
    SELECT MAX(timestamp)
    FROM crypto_prices
)
"""

trend_query = """
SELECT coin_name, price, timestamp
FROM crypto_prices
WHERE timestamp >= NOW() - INTERVAL 1 DAY
ORDER BY timestamp
"""

# ---------------------------------
# LOAD DATA (CACHED)
# ---------------------------------
@st.cache_data(ttl=60)
def load_latest_data():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ifdxrmf4j9#123",
        database="crypto_project"
    )
    return pd.read_sql(latest_query, connection)


@st.cache_data(ttl=60)
def load_trend_data():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ifdxrmf4j9#123",
        database="crypto_project"
    )
    return pd.read_sql(trend_query, connection)


df = load_latest_data()
trend_df = load_trend_data()

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("Dashboard Filters")

coin_list = df["coin_name"].unique()

selected_coins = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    coin_list,
    default=coin_list
)

forecast_coin = st.sidebar.selectbox(
    "Select Coin for Forecast",
    coin_list
)

filtered_df = df[df["coin_name"].isin(selected_coins)]
trend_df = trend_df[trend_df["coin_name"].isin(selected_coins)]

# ---------------------------------
# KPI SECTION
# ---------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Coins", filtered_df["coin_name"].nunique())

col2.metric(
    "Highest Price",
    filtered_df.loc[filtered_df["price"].idxmax()]["coin_name"]
)

col3.metric(
    "Highest Market Cap",
    filtered_df.loc[filtered_df["market_cap"].idxmax()]["coin_name"]
)

col4.metric(
    "Highest Volume",
    filtered_df.loc[filtered_df["volume"].idxmax()]["coin_name"]
)

# ---------------------------------
# MARKET CAP + VOLUME CHARTS
# ---------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Market Cap by Cryptocurrency")

    fig1 = px.bar(
        filtered_df,
        x="coin_name",
        y="market_cap",
        color="coin_name"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Trading Volume")

    fig2 = px.bar(
        filtered_df,
        x="coin_name",
        y="volume",
        color="coin_name"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------
# PRICE COMPARISON
# ---------------------------------
st.subheader("Cryptocurrency Price Comparison")

fig3 = px.bar(
    filtered_df,
    x="coin_name",
    y="price",
    color="coin_name"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------
# MARKET DOMINANCE PIE CHART
# ---------------------------------
st.subheader("Crypto Market Dominance")

dominance_df = filtered_df[["coin_name", "market_cap"]]

fig4 = px.pie(
    dominance_df,
    names="coin_name",
    values="market_cap"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------
# PRICE TREND LINE CHART
# ---------------------------------
st.subheader("Crypto Price Trend Over Time")

fig5 = px.line(
    trend_df,
    x="timestamp",
    y="price",
    color="coin_name",
    markers=True,
    log_y=True
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------
# FORECAST SECTION
# ---------------------------------
st.subheader(f"{forecast_coin} Price Forecast")

coin_df = trend_df[trend_df["coin_name"] == forecast_coin]

if len(coin_df) > 20:

    prophet_df = coin_df[["timestamp", "price"]].rename(
        columns={"timestamp": "ds", "price": "y"}
    )

    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=24, freq="5min")
    forecast = model.predict(future)

    fig_forecast = px.line(
        forecast,
        x="ds",
        y="yhat",
        title=f"{forecast_coin} Predicted Price"
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

else:
    st.info("Not enough data yet for forecasting. Let the data collector run longer.")

# ---------------------------------
# PRICE CHANGE CALCULATION
# ---------------------------------
trend_df = trend_df.sort_values(["coin_name", "timestamp"])

trend_df["price_change"] = trend_df.groupby("coin_name")["price"].diff()

trend_df["pct_change"] = trend_df.groupby("coin_name")["price"].pct_change() * 100

trend_df["pct_change"] = trend_df["pct_change"].round(2)

latest_changes = trend_df.groupby("coin_name").tail(1)

# ---------------------------------
# TOP GAINERS & LOSERS
# ---------------------------------
st.subheader("Top Gainers & Top Losers")

top_gainers = latest_changes.sort_values(
    by="pct_change",
    ascending=False
).head(5)

top_losers = latest_changes.sort_values(
    by="pct_change"
).head(5)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 Top Gainers")

    st.dataframe(
        top_gainers[["coin_name", "price", "pct_change"]]
    )

with col2:
    st.markdown("### 🔴 Top Losers")

    st.dataframe(
        top_losers[["coin_name", "price", "pct_change"]]
    )

# ---------------------------------
# MARKET INSIGHTS
# ---------------------------------
st.subheader("Market Insights")

top_marketcap = filtered_df.sort_values(
    by="market_cap",
    ascending=False
).head(5)

st.write("Top 5 Coins by Market Cap")

st.dataframe(
    top_marketcap[["coin_name", "price", "market_cap", "volume"]]
)

# ---------------------------------
# FULL DATASET
# ---------------------------------
st.subheader("Full Cryptocurrency Dataset")

st.dataframe(filtered_df)

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("---")
st.caption("Crypto Analytics Dashboard | Built with Python, MySQL & Streamlit")

st.subheader("⚙️ Data Pipeline Metrics")

total_records = len(trend_df)

latest_timestamp = trend_df["timestamp"].max()

data_freshness = (
    pd.Timestamp.now() - pd.to_datetime(latest_timestamp)
).total_seconds() / 60

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", total_records)

col2.metric("Unique Coins", trend_df["coin_name"].nunique())

col3.metric(
    "Latest Data",
    latest_timestamp.strftime("%Y-%m-%d %H:%M")
)
col4.metric("Data Freshness (minutes)", round(data_freshness, 2))