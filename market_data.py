import yfinance as yf
import pandas as pd


TICKERS = {

    "NIFTY 50": "^NSEI",

    "SENSEX": "^BSESN",

    "S&P 500": "^GSPC",

    "NASDAQ": "^IXIC",

    "DOW JONES": "^DJI",

    "GOLD": "GC=F",

    "BRENT CRUDE": "BZ=F",

    "USD/INR": "INR=X",

    "10Y US TREASURY": "^TNX"

}


def get_market_data():

    results = []

    for name, ticker in TICKERS.items():

        try:

            data = yf.Ticker(ticker).history(
                period="5d"
            )

            if data.empty:
                continue

            latest = data.iloc[-1]

            close = float(
                latest["Close"]
            )

            previous = float(
                data.iloc[-2]["Close"]
            )

            change = (
                (close - previous)
                / previous
            ) * 100

            results.append({

                "name": name,

                "price": round(
                    close,
                    2
                ),

                "change": round(
                    change,
                    2
                )

            })

        except Exception as e:

            print(
                f"Market data error {name}: {e}"
            )

    return pd.DataFrame(results)