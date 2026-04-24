import requests
import pandas as pd
import mysql.connector
import time
from datetime import datetime

# ---------------------------------
# MYSQL CONNECTION FUNCTION
# ---------------------------------

def connect_db():

    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ifdxrmf4j9#123",
        database="crypto_project"
    )


conn = connect_db()
cursor = conn.cursor()

print("Connected to MySQL")

# ---------------------------------
# API SETTINGS
# ---------------------------------

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

headers = {
    "User-Agent": "crypto-dashboard"
}

# ---------------------------------
# MAIN PIPELINE LOOP
# ---------------------------------

while True:

    try:

        print("Fetching crypto data...")

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if isinstance(data, list):

            df = pd.DataFrame(data)

            required_cols = [
                "name",
                "symbol",
                "current_price",
                "market_cap",
                "total_volume"
            ]

            if all(col in df.columns for col in required_cols):

                df = df[required_cols]

                df.columns = [
                    "coin_name",
                    "symbol",
                    "price",
                    "market_cap",
                    "volume"
                ]

                df["timestamp"] = datetime.now()

                # Insert rows
                for _, row in df.iterrows():

                    query = """
                    INSERT INTO crypto_prices
                    (coin_name, symbol, price, market_cap, volume, timestamp)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    """

                    values = (
                        row["coin_name"],
                        row["symbol"],
                        row["price"],
                        row["market_cap"],
                        row["volume"],
                        row["timestamp"]
                    )

                    cursor.execute(query, values)

                conn.commit()

                print("Data inserted at:", datetime.now())

            else:

                print("API columns changed:", df.columns)

        else:

            print("API returned unexpected data:", data)

    except mysql.connector.Error as db_error:

        print("Database error:", db_error)

        # reconnect database
        conn = connect_db()
        cursor = conn.cursor()

    except requests.exceptions.RequestException as api_error:

        print("API connection error:", api_error)

    except Exception as e:

        print("Unexpected error:", e)

    # ---------------------------------
    # WAIT BEFORE NEXT FETCH
    # ---------------------------------

    print("Waiting 5 minutes...\n")

    time.sleep(300)