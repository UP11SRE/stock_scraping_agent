import requests

def get_ticker_from_name(company_name: str) -> str | None:
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36"
    }
    params = {
        "q": company_name,
        "quotes_count": 1,
        "country": "India",
        "lang": "en-IN"
    }

    try:
        res = requests.get(url=url, params=params, headers=headers, timeout=5)
        res.raise_for_status()
        data = res.json()
    except (requests.RequestException, ValueError):
        return None

    if not data.get("quotes"):
        return None

    company_code = data["quotes"][0].get("symbol")
    if company_code and not company_code.endswith(".NS"):
        company_code += ".NS"
    return company_code
