"""
Streamlit app: Plant Disease Recognition (multi-page)

Run with:
    streamlit run app.py
"""

import streamlit as st

from theme import get_custom_css

st.set_page_config(page_title="Plant Disease Recognition", page_icon="🌿", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.markdown(get_custom_css(st.session_state.dark_mode), unsafe_allow_html=True)

home = st.Page("views/home.py", title="Home", icon="🏠", default=True)
diagnose = st.Page("views/diagnose.py", title="Diagnose", icon="🔍")
library = st.Page("views/disease_library.py", title="Disease Library", icon="📖")
performance = st.Page("views/model_performance.py", title="Model Performance", icon="📊")
about = st.Page("views/about.py", title="About", icon="ℹ️")

pg = st.navigation([home, diagnose, library, performance, about])

with st.sidebar:
    st.markdown("### 🌿 Plant Disease Recognition")
    st.caption("AI-powered leaf disease diagnosis")
    st.toggle("🌙 Dark mode", key="dark_mode")
    st.divider()
    if st.session_state.history:
        st.subheader("Recent checks")
        for item in st.session_state.history:
            st.markdown(
                f'<div class="history-item">🌿 {item["condition"]} '
                f'({item["crop"]}) — {item["confidence"]:.0%}</div>',
                unsafe_allow_html=True,
            )
        st.divider()
    st.caption("[Dataset: New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)")

pg.run()