from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.ticker_lookup import get_ticker_from_name
from utils.stock_info import get_stock_info
from utils.news_scraper import get_recent_news
from utils.sentiment_analysis import analyze_stock_news
import uvicorn

app = FastAPI(title="Stock Insight API")

class CompanyRequest(BaseModel):
    company_name: str

@app.post("/report")
async def generate_stock_report(request: CompanyRequest):
    company_name = request.company_name
    ticker = get_ticker_from_name(company_name)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found.")

    stock_metrics = get_stock_info(ticker)
    news_data = await get_recent_news(company_name)
    news_sources, sentiment_summary = analyze_stock_news(news_data)

    return {
        "ticker": ticker,
        "metrics": stock_metrics["metrics"],
        "history": stock_metrics["history_df"],
        "news": news_sources,
        "sentiment": sentiment_summary,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
