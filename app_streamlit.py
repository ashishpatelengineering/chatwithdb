# app.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
import pathlib

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Setup database
db_path = pathlib.Path("Chinook.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# Setup LLM and agent
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(llm=llm, toolkit=toolkit)

# Streamlit UI
st.title("Simple SQL Query Agent")
user_query = st.text_input("Enter your question:")

if user_query.strip() != "":
    response = agent.invoke(user_query)
    st.subheader("Response:")
    st.write(response['output'])