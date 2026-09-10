"""
Streamlit app: Plant Disease Recognition (multi-page)

Run with:
    streamlit run app.py
"""

import streamlit as st

from theme import CUSTOM_CSS

st.set_page_config(page_title="Plant Disease Recognition", page_icon="🌿", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

home = st.Page("views/home.py", title="Home", icon="🏠", default=True)
diagnose = st.Page("views/diagnose.py", title="Diagnose", icon="🔍")
library = st.Page("views/disease_library.py", title="Disease Library", icon="📖")
performance = st.Page("views/model_performance.py", title="Model Performance", icon="📊")
about = st.Page("views/about.py", title="About", icon="ℹ️")

pg = st.navigation([home, diagnose, library, performance, about])

with st.sidebar:
    st.markdown("### 🌿 Plant Disease Recognition")
    st.caption("AI-powered leaf disease diagnosis")
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