import yfinance as yf
import pandas as pd

def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)

    history_df = stock.history(period="7d", interval="1d").reset_index()
    history = history_df.astype(object).where(pd.notnull(history_df), None).to_dict(orient="records")

    info = stock.info
    metrics = {
        "Current Price": info.get("currentPrice"),
        "52 Week High": info.get("fiftyTwoWeekHigh"),
        "52 Week Low": info.get("fiftyTwoWeekLow"),
        "Market Cap": info.get("marketCap"),
        "PE Ratio (TTM)": info.get("trailingPE"),
        "Forward PE Ratio": info.get("forwardPE"),
        "PEG Ratio": info.get("pegRatio"),
        "Price to Book Ratio": info.get("priceToBook"),
        "Dividend Yield": info.get("dividendYield"),
        "Dividend Rate": info.get("dividendRate"),
        "Revenue (TTM)": info.get("totalRevenue"),
        "Net Income (TTM)": info.get("netIncomeToCommon"),
        "EPS (TTM)": info.get("trailingEps"),
        "Beta": info.get("beta"),
        "Volume": info.get("volume"),
        "Average Volume (3 months)": info.get("averageVolume3Month"),
        "Shares Outstanding": info.get("sharesOutstanding"),
        "Float Shares": info.get("floatShares"),
        "Short Ratio": info.get("shortRatio"),
        "Return on Assets (ROA)": info.get("returnOnAssets"),
        "Return on Equity (ROE)": info.get("returnOnEquity"),
        "Debt to Equity Ratio": info.get("debtToEquity"),
        "Sector": info.get("sector"),
        "Industry": info.get("industry"),
    }

    return {
        "metrics": metrics,
        "history_df": history,
    }
