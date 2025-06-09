import streamlit as st
from pandasai import SmartDataframe
from pandasai.connectors.yahoo_finance import YahooFinanceConnector
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
# Set your PandasAI API key
#os.environ['PANDASAI_API_KEY'] = "$2a$10$ejBcbjF2sOx4XaiHsGqMxOTutW/iu54/RpYefPHF8je7Vxz.BEHnq"
# Initialize the ChatGroq model
groq_api_key = st.secrets["GROQ_API_KEY"]
model = ChatGroq(temperature=0.8, model="llama-3.1-70b-versatile",groq_api_key=groq_api_key)
# Streamlit app
st.title("Market Analysis of Stock Price Chatbot")
#Create a prompt template
prompt = ChatPromptTemplate.from_messages([
("system", "You're a very knowledgeable Market analysis who provides accurate and eloquent answers to historical questions."),
("human", "{question}")
])
# Text input for the company symbol
company_symbol = st.text_input("Enter the company symbol (e.g., AAPL):")

if company_symbol:
    try:
        # Initialize the Yahoo Finance connector with the input symbol
        yahoo_connector = YahooFinanceConnector(company_symbol)
        df = SmartDataframe(yahoo_connector, config={"llm": model},description=prompt)

        # Text input for user queries
        user_query = st.chat_input("Ask a question about the market:")

        if user_query:
            # Get the chatbot's response
            response = df.chat(user_query)
            st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
