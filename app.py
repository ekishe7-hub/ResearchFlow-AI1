import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
import docx
from io import BytesIO

st.set_page_config(page_title="ResearchFlow AI", page_icon="📚", layout="wide")

API_KEY = os.getenv("GEMINI_API_KEY", "WEKA_API_KEY_YAKO_HAPA")
if API_KEY != "WEKA_API_KEY_YAKO_HAPA":
    genai.configure(api_key=API_KEY)

st.title("📚 ResearchFlow AI: Intelligent Academic Paper Generator")
st.markdown("Mfumo mahiri wa kuandaa karatasi kamili za utafiti.")

research_title = st.sidebar.text_input("Kichwa cha Utafiti:", value="AI-Driven Flood Modeling")
sheets_link = st.sidebar.text_input("Kiungo cha Google Sheets:", placeholder="https://...")
citation_style = st.sidebar.selectbox("Mtindo wa Marejeleo:", ["APA 7th", "IEEE"])

if st.sidebar.button("1. Tengeneza Search Strings"):
    st.session_state['search_string'] = '("Artificial Intelligence") AND ("Urban Flooding")'

if 'search_string' in st.session_state:
    st.code(st.session_state['search_string'])

st.success("Tunaendelea kujenga mfumo...")
