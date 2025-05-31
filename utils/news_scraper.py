from browser_use import Agent
from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta

llm = ChatOpenAI(temperature=0, model="gpt-4o")

async def get_recent_news(company_name: str) -> str:
    since = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    query = (
        f"Search ONLY site:moneycontrol.com and site:economictimes.indiatimes.com "
        f"for 5 news articles about '{company_name}' published after {since} that are likely to IMPACT the company's stock price. "
        f"Exclude general market summaries or scraped news. Only include impactful news like earnings, acquisitions, management changes, government actions, major deals, etc.\n\n"
        f"For each article, return:\n"
        f"- Title\n- URL\n- Source (Moneycontrol or Economic Times)\n- A short summary (2-3 sentences).\n\n"
        f"Format the results as a Markdown bullet list like:\n"
        f"- **Title** (Source) [Link](URL)\n  Summary text"
    )

    agent = Agent(task=query, llm=llm)
    result = await agent.run()

    return result