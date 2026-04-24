🚀 Crypto Analytics Dashboard

An end-to-end cryptocurrency analytics project that collects real-time crypto market data using the CoinGecko API, stores it in a MySQL database, and visualizes insights through an interactive Streamlit dashboard.

This project demonstrates data pipeline development, database management, and real-time analytics visualization.

📊 Project Architecture

CoinGecko API

  ↓

Python Data Collector

  ↓

MySQL Database

  ↓

Streamlit Analytics Dashboard

⚙️ Features

📈 Market Analytics

-Cryptocurrency price comparison

-Market capitalization analysis

-Trading volume visualization

-Market dominance chart

📉 Time Series Analysis

-Crypto price trend charts

-Log-scale price comparison

-Historical price tracking

🔮 Price Forecasting

Uses Prophet (Facebook Prophet) to generate cryptocurrency price forecasts.

📊 Market Insights

-Top gainers

-Top losers

-Top coins by market capitalization

⚙️ Data Pipeline Monitoring

-Dashboard includes pipeline health metrics:

-Total records in database

-Unique cryptocurrencies tracked

-Latest data timestamp

-Data freshness indicator

🗄️ Database Schema

MySQL table used in this project:

CREATE TABLE crypto_prices (

  id INT AUTO_INCREMENT PRIMARY KEY,

  coin_name VARCHAR(50),

  symbol VARCHAR(10),

  price FLOAT,

  market_cap BIGINT,

  volume BIGINT,

  timestamp DATETIME

);

🛠️ Technologies Used

-Python

-Streamlit

-MySQL

-Pandas

-Plotly

-Prophet

-CoinGecko API

▶️ Installation

-Clone the repository:

git clone https://github.com/JYOTIRADITYA-web-bit/Crypto-Analytics

cd crypto-analytics

-Install dependencies:

pip install -r requirements.txt

🗃️ Setup Database

-Create MySQL database:

CREATE DATABASE crypto_project;

-Create table:

CREATE TABLE crypto_prices (

  id INT AUTO_INCREMENT PRIMARY KEY,

  coin_name VARCHAR(50),

  symbol VARCHAR(10),

  price FLOAT,

  market_cap BIGINT,

  volume BIGINT,

  timestamp DATETIME

);

🔄 Run Data Pipeline

Start the data collector script:

python crypto_data_collector.py

This script fetches cryptocurrency market data every 5 minutes.

📊 Run Dashboard

-Launch the Streamlit dashboard:

streamlit run crypto_dashboard.py
