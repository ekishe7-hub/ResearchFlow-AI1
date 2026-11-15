import streamlit as st
import os

st.set_page_config(page_title="ResearchFlow AI", page_icon="📚", layout="wide")

st.title("📚 ResearchFlow AI: Intelligent Academic Paper Generator")
st.write("Mfumo mahiri wa kuandaa karatasi kamili ya utafiti.")

# Sidebar ya kuweka taarifa
st.sidebar.header("Mipangilio ya Utafiti")
research_title = st.sidebar.text_input("Kichwa cha Utafiti:", "AI-Driven Flood Modeling")
sheets_link = st.sidebar.text_input("Kiungo cha Google Sheets (Hiari):", "")
citation_style = st.sidebar.selectbox("Mtindo wa Marejeleo:", ["APA 7th", "IEEE", "Harvard"])

# Kitufe cha Submit kilichokosekana
if st.sidebar.button("Tengeneza Karatasi ya Utafiti"):
    with st.spinner("Inachakata na kutengeneza karatasi yako... Subiri kidogo."):
        # Hapa ndipo uchakataji wa AI utafanyika
        st.success(f"Utafiti wenye kichwa: '{research_title}' umeanza kuandaliwa!")
        st.write("### Muhtasari wa Sehemu za Utafiti:")
        st.markdown("1. **Utangulizi (Introduction)** - Umekamilika.")
        st.markdown("2. **Mapitio ya Fasihi (Literature Review)** - Umekamilika.")
        st.markdown("3. **Mbinu za Utafiti (Methodology)** - Umekamilika.")
        st.info("Mfumo unaendelea kukamilisha sehemu zilizobaki...")
else:
    st.info("Weka kichwa cha utafiti upande wa kushoto kisha bonyeza kitufe cha **Tengeneza Karatasi ya Utafiti** ili kuanza.")
