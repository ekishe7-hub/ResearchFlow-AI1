import streamlit as st
import os
import google.generativeai as genai

# Sanidi ukurasa kuwa mpana
st.set_page_config(page_title="ResearchFlow AI", page_icon="📚", layout="wide")

st.title("📚 ResearchFlow AI: Intelligent Academic Paper Generator")
st.write("Mfumo kamili wa kuandaa, kuchambua na kuandika karatasi za kiakademia kwa kutumia Gemini AI.")

# Soma API Key
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
if api_key:
    genai.configure(api_key=api_key)

# ----------------- SIDEBAR (MIPANGILIO) -----------------
st.sidebar.header("⚙️ Mipangilio ya Utafiti")

research_title = st.sidebar.text_input("Kichwa cha Utafiti:", value="AI-Driven Flood Modeling")
sheets_link = st.sidebar.text_input("Kiungo cha Google Sheets (Data za Utafiti):", value="")
citation_style = st.sidebar.selectbox("Mtindo wa Marejeleo:", ["APA 7th", "IEEE", "Harvard", "Chicago"])

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Pakia Nyaraka / Muktasari")
uploaded_file = st.sidebar.file_uploader("Weka faili la Quick Read / PDF / Text", type=["txt", "pdf", "docx", "csv"])

# Kitufe cha Submit kuu kwenye Sidebar
submit_button = st.sidebar.button("🚀 Tengeneza Karatasi Kamili", type="primary")

# ----------------- UKURASA WA MBELE (MAIN UI) -----------------
tab1, tab2, tab3 = st.tabs(["📝 Utengenezaji wa Karatasi", "🔍 Search Strings", "📊 Uchambuzi wa Data & Documents"])

with tab1:
    st.subheader("Muhtasari na Hatua za Utafiti")
    
    if submit_button:
        if not api_key:
            st.error("⚠️ Tafadhali weka Gemini API Key kwanza kwenye Streamlit Secrets.")
        else:
            with st.spinner("AI inaandaa na kuchakata karatasi yako ya utafiti... Subiri kidogo."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    # Soma maelezo ya faili kama lipo
                    file_content_text = ""
                    if uploaded_file is not None:
                        file_content_text = uploaded_file.read().decode("utf-8", errors="ignore")
                    
                    prompt = f'''
                    Weka karatasi ya utafiti ya kitaalamu yenye kichwa: "{research_title}".
                    Mtindo wa Marejeleo: {citation_style}.
                    Kiungo cha Data: {sheets_link}.
                    Maelezo ya Ziada kutoka kwenye faili lililopakiwa: {file_content_text[:1000]}
                    
                    Tafadhali jumuisha sehemu zifuatazo kwa kina:
                    1. Utangulizi (Introduction)
                    2. Mapitio ya Fasihi (Literature Review)
                    3. Mbinu za Utafiti (Methodology)
                    4. Matokeo na Uchambuzi (Results & Discussion)
                    5. Hitimisho na Mapendekezo (Conclusion & Recommendations)
                    '''
                    
                    response = model.generate_content(prompt)
                    
                    st.success("🎉 Karatasi imekamilika kuzalishwa kikamilifu!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Imetokea kosa wakati wa kuwasiliana na AI: {e}")
    else:
        st.info("👈 Jaza taarifa za utafiti wako upande wa kushoto kisha ubofye kitufe cha **Tengeneza Karatasi Kamili** ili kuanza.")

with tab2:
    st.subheader("🔍 Jenereta ya Search Strings kwa Ajili ya Google Scholar / Hifadhi za Vifungu")
    if st.button("Tengeneza Search Strings za Mada Hii"):
        if api_key:
            model = genai.GenerativeModel("gemini-1.5-flash")
            s_prompt = f"Tengeneza boolean search strings 3 za kitaalamu za kutumia kwenye Google Scholar na Scopus kwa ajili ya mada hii: '{research_title}'."
            s_res = model.generate_content(s_prompt)
            st.code(s_res.text, language="text")
        else:
            st.warning("Weka API Key kwanza.")
    else:
        st.write("Bonyeza kitufe hapo juu ili mfumo ukutengenezee maneno sahihi ya kutafutia makala za kitaalamu kwenye Google Scholar.")

with tab3:
    st.subheader("📊 Uchambuzi wa Data na Nyaraka Zilizopakiwa")
    if uploaded_file is not None:
        st.write(f"Faili lililounganishwa: **{uploaded_file.name}**")
        st.success("Faili lipo tayari kutumiwa na mfumo kuchakata matokeo.")
    else:
        st.warning("Hakuna faili lililopakiwa bado. Tumia sehemu ya pembeni (sidebar) kupakia faili lako la muktasari au data.")
