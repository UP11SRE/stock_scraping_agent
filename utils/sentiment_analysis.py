from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(temperature=0, model="gpt-4o")

extract_prompt = ChatPromptTemplate.from_template("""
You will be given raw text data containing news articles about a company. 
Extract a JSON array of articles with fields: title, source, url, summary.

Input:
{text}

Output JSON:
""")

extract_chain = LLMChain(llm=llm, prompt=extract_prompt, output_key="articles_json")

analyze_prompt = ChatPromptTemplate.from_template("""
You are a financial analyst.

Given the following news articles about a stock:

{articles_json}

Please provide:
- An overall sentiment about the stock (Positive, Negative, or Neutral)
- A brief explanation for your sentiment
- Your investment recommendation (Buy, Hold, or Sell) with reasoning

Output in a clear, concise paragraph.
""")

analyze_chain = LLMChain(llm=llm, prompt=analyze_prompt, output_key="analysis")

def analyze_stock_news(raw_agent_output_text: str) -> tuple[str, str]:
    extraction_result = extract_chain.run(text=raw_agent_output_text)
    try:
        articles = json.loads(extraction_result)
        articles_json_str = json.dumps(articles, indent=2)
    except json.JSONDecodeError:
        articles_json_str = extraction_result

    analysis_result = analyze_chain.run(articles_json=articles_json_str)

    return articles_json_str, analysis_result
