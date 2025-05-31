import streamlit as st
import requests
import pandas as pd
import json

st.title("Stock Report Viewer")

company_name = st.text_input("Enter Company Name", value="Ixigo")

# Session state for loading, data, and error
if "loading" not in st.session_state:
    st.session_state.loading = False
if "data" not in st.session_state:
    st.session_state.data = None
if "error" not in st.session_state:
    st.session_state.error = None

def fetch_data():
    try:
        st.session_state.loading = True

        response = requests.post("http://127.0.0.1:8000/report", json={"company_name": company_name})
        response.raise_for_status()
        data = response.json()
        
        st.session_state.data = data
        st.session_state.error = None
    except requests.exceptions.RequestException as e:
        st.session_state.error = f"Error fetching data from API: {e}"
        st.session_state.data = None
    finally:
        st.session_state.loading = False

generate = st.button("Generate Report")

if generate and company_name and not st.session_state.loading:
    # Clear old data/error
    st.session_state.data = None
    st.session_state.error = None

    fetch_data()

if st.session_state.loading:
    st.info("Loading... Please wait.")

if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.data:
    data = st.session_state.data

    st.subheader(f"Metrics for {data.get('ticker', company_name)}")
    metrics = data.get("metrics", {})
    if metrics:
        metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
        st.table(metrics_df)
    else:
        st.write("No metrics data available.")

    history = data.get("history", [])
    if history:
        st.subheader("Historical Prices (Last 7 Days)")
        df_history = pd.DataFrame(history)
        df_history['Date'] = pd.to_datetime(df_history['Date'])
        df_history = df_history.set_index('Date')
        st.line_chart(df_history['Close'])
    else:
        st.write("No historical price data available.")

    news = data.get("news", [])
    if news:
        if isinstance(news, str):
            news_str = news.strip()
            if news_str.startswith("```"):
                news_str = "\n".join(news_str.split("\n")[1:-1])
            news = json.loads(news_str)

        st.subheader("News")
        for article in news:
            st.markdown(f"**[{article['title']}]({article['url']})**")
            st.markdown(f"*Source:* {article['source']}")
            st.markdown(f"{article['summary']}")
            st.markdown("---")
    else:
        st.write("No news available.")

    sentiment = data.get("sentiment", "")
    if sentiment:
        st.subheader("AI Analysis about the Stock")
        st.write(sentiment)
    else:
        st.write("No sentiment data available.")
