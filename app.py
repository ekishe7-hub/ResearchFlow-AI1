import streamlit as st
import os
import pandas as pd
import google.generativeai as genai

# Sanidi ukurasa kuwa mpana
st.set_page_config(page_title="ResearchFlow AI", page_icon="📚", layout="wide")

st.title("📚 ResearchFlow AI: Intelligent Academic Paper Generator")
st.write("Mfumo kamili wa kuandaa, kuchambua na kuandika karatasi za kiakademia kwa kutumia Gemini AI.")

# Soma API Key
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
if api_key:
    genai.configure(api_key=api_key)

# Kitendakazi cha kupata modeli kwa uhakika
def get_ai_model():
    # Tunatumia gemini-2.5-flash ambayo ndiyo pendekezo rasmi la API
    return genai.GenerativeModel("gemini-2.5-flash")

# ----------------- SIDEBAR (MIPANGILIO) -----------------
st.sidebar.header("⚙️ Mipangilio ya Utafiti")

research_title = st.sidebar.text_input("Kichwa cha Utafiti:", value="AI-Driven Flood Modeling")
citation_style = st.sidebar.selectbox("Mtindo wa Marejeleo:", ["APA 7th", "IEEE", "Harvard", "Chicago"])

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Pakia Data za Google Sheets (CSV / Excel)")
sheets_file = st.sidebar.file_uploader("Weka faili la Google Sheets", type=["csv", "xlsx"])

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Pakia Muktasari / Nyaraka")
uploaded_file = st.sidebar.file_uploader("Weka faili la Quick Read / PDF / Text", type=["txt", "pdf", "docx"])

# Kitufe cha Submit kuu kwenye Sidebar
submit_button = st.sidebar.button("🚀 Tengeneza Karatasi Kamili", type="primary")

# ----------------- UKURASA WA MBELE (MAIN UI) -----------------
tab1, tab2, tab3 = st.tabs(["📝 Utengenezaji wa Karatasi", "🔍 Search Strings", "📊 Uchambuzi wa Data"])

with tab1:
    st.subheader("Muhtasari na Hatua za Utafiti")
    
    if submit_button:
        if not api_key:
            st.error("⚠️ Tafadhali weka Gemini API Key kwanza kwenye Streamlit Secrets.")
        else:
            with st.spinner("AI inaandaa na kuchakata karatasi yako ya utafiti... Subiri kidogo."):
                try:
                    # Soma maelezo ya faili la Excel/CSV kama lipo
                    sheet_data_summary = ""
                    if sheets_file is not None:
                        if sheets_file.name.endswith('.csv'):
                            df = pd.read_csv(sheets_file)
                        else:
                            df = pd.read_excel(sheets_file)
                        sheet_data_summary = f"Muhtasari wa Data kutoka Google Sheets: {df.shape}. Maelezo ya awali: {df.head(5).to_string()}"
                    
                    # Soma maelezo ya faili la muktasari kama lipo
                    file_content_text = ""
                    if uploaded_file is not None:
                        file_content_text = uploaded_file.read().decode("utf-8", errors="ignore")
                    
                    prompt = f'''
                    Weka karatasi ya utafiti ya kitaalamu yenye kichwa: "{research_title}".
                    Mtindo wa Marejeleo: {citation_style}.
                    {sheet_data_summary}
                    Maelezo ya Ziada kutoka kwenye nyaraka: {file_content_text[:1000]}
                    
                    Tafadhali jumuisha sehemu zifuatazo kwa kina:
                    1. Utangulizi (Introduction)
                    2. Mapitio ya Fasihi (Literature Review)
                    3. Mbinu za Utafiti (Methodology)
                    4. Matokeo na Uchambuzi wa Data (Results & Discussion)
                    5. Hitimisho na Mapendekezo (Conclusion & Recommendations)
                    '''
                    
                    model = get_ai_model()
                    response = model.generate_content(prompt)
                    
                    st.success("🎉 Karatasi imekamilika kuzalishwa kikamilifu!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Imetokea kosa wakati wa kuchakata: {e}")
    else:
        st.info("👈 Jaza taarifa na upakie faili lako la Google Sheets au nyaraka upande wa kushoto kisha ubofye kitufe cha **Tengeneza Karatasi Kamili**.")

with tab2:
    st.subheader("🔍 Jenereta ya Search Strings kwa Ajili ya Google Scholar")
    if st.button("Tengeneza Search Strings za Mada Hii"):
        if api_key:
            try:
                model = get_ai_model()
                s_prompt = f"Tengeneza boolean search strings 3 za kitaalamu za kutumia kwenye Google Scholar na Scopus kwa ajili ya mada hii: '{research_title}'."
                s_res = model.generate_content(s_prompt)
                st.code(s_res.text, language="text")
            except Exception as e:
                st.error(f"Kosa: {e}")
        else:
            st.warning("Weka API Key kwanza.")

with tab3:
    st.subheader("📊 Uchambuzi wa Data za Google Sheets")
    if sheets_file is not None:
        if sheets_file.name.endswith('.csv'):
            df = pd.read_csv(sheets_file)
        else:
            df = pd.read_excel(sheets_file)
        st.write(f"Faili la Google Sheets: **{sheets_file.name}**")
        st.dataframe(df.head(10))
    else:
        st.warning("Hakuna faili la Google Sheets lililopakiwa bado. Tumia upande wa kushoto kupakia faili lako.")
