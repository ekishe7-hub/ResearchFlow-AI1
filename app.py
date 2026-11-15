import streamlit as st
import os
import google.generativeai as genai

# Sanidi ukurasa
st.set_page_config(page_title="ResearchFlow AI", page_icon="📚", layout="wide")

st.title("📚 ResearchFlow AI: Intelligent Academic Paper Generator")
st.write("Mfumo mahiri wa kuandaa karatasi kamili ya utafiti kwa kutumia Gemini AI.")

# Soma API Key kutoka kwenye Streamlit Secrets au Environment
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ Tafadhali weka GEMINI_API_KEY kwenye mfumo wa Streamlit Secrets.")

# Sidebar ya kuweka taarifa
st.sidebar.header("Mipangilio ya Utafiti")
research_title = st.sidebar.text_input("Kichwa cha Utafiti:", "AI-Driven Flood Modeling")
sheets_link = st.sidebar.text_input("Kiungo cha Google Sheets (Hiari):", "")
citation_style = st.sidebar.selectbox("Mtindo wa Marejeleo:", ["APA 7th", "IEEE", "Harvard"])

# Kitufe cha kuanzisha mchakato
if st.sidebar.button("Tengeneza Karatasi ya Utafiti", type="primary"):
    if not api_key:
        st.error("Tafadhali weka Gemini API Key kwanza kwenye Secrets!")
    else:
        with st.spinner("Inawasiliana na Gemini AI na kuandaa karatasi yako... Subiri kidogo."):
            try:
                # Tumia Gemini AI kuzalisha maudhui halisi
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"Andika muhtasari wa kitaalamu wa karatasi ya utafiti yenye kichwa: '{research_title}' kwa mtindo wa {citation_style}. Jumuisha Utangulizi, Mapitio ya Fasihi, na Mbinu za Utafiti."
                
                response = model.generate_content(prompt)
                
                st.success("🎉 Karatasi imekamilika kuzalishwa kwa mafanikio!")
                st.write("### Matokeo ya Utafiti Wako:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Imetokea kosa wakati wa kuwasiliana na AI: {e}")
else:
    st.info("👈 Weka kichwa cha utafiti upande wa kushoto kisha bonyeza kitufe cha **Tengeneza Karatasi ya Utafiti** ili kuanza.")
