import json
import os

import streamlit as st

st.markdown(
    """<div class="hero-banner">
    <h1>🌿 Plant Disease Recognition</h1>
    <p>Upload a photo of a plant leaf and get an instant AI diagnosis — complete with
    a confidence score, a Grad-CAM explanation of what the model actually looked at,
    and practical treatment guidance. Built and evaluated end-to-end, including honest
    testing on real-world field photos, not just lab images.</p>
    </div>""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    st.page_link("views/diagnose.py", label="🔍  Try it now", use_container_width=True)
with col2:
    st.page_link("views/disease_library.py", label="📖  Browse Disease Library", use_container_width=True)

st.write("")

# ---------- Quick stats, read live from training outputs ----------
val_acc, real_acc = None, None
try:
    with open("outputs/training_history.json") as f:
        val_acc = json.load(f).get("val_accuracy", [None])[-1]
except Exception:
    pass
try:
    with open("outputs/plantdoc_accuracy.json") as f:
        real_acc = json.load(f).get("overall_accuracy")
except Exception:
    pass

stats = [
    ("38", "Disease classes"),
    ("14", "Crop species"),
    (f"{val_acc:.1%}" if val_acc else "—", "Lab validation accuracy"),
    (f"{real_acc:.1%}" if real_acc else "—", "Real-world (PlantDoc) accuracy"),
]
cols = st.columns(4)
for c, (big, label) in zip(cols, stats):
    with c:
        st.markdown(
            f'<div class="stat-box"><div class="big">{big}</div>'
            f'<div class="label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.write("")

# ---------- How it works ----------
st.subheader("How it works")
steps = [
    ("📸", "1. Upload", "Take or upload a photo of a single leaf, ideally against a plain background."),
    ("🧠", "2. AI Analysis", "A MobileNetV3 model (transfer learning) classifies it across 38 disease classes."),
    ("🔥", "3. Grad-CAM", "See a heatmap of exactly which part of the leaf drove the prediction."),
    ("💊", "4. Guidance", "Get the diagnosis, confidence score, and crop-specific treatment advice."),
]
cols = st.columns(4)
for c, (icon, title, desc) in zip(cols, steps):
    with c:
        st.markdown(
            f'<div class="feature-card"><div class="icon">{icon}</div>'
            f'<h4>{title}</h4><p>{desc}</p></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.write("")

# ---------- Feature highlights ----------
st.subheader("What makes this different")
features = [
    ("🔍", "Explainable AI", "Every prediction comes with a Grad-CAM heatmap, not just a black-box label."),
    ("⚠️", "Confidence gating", "Uncertain predictions are flagged as such, instead of confidently guessing."),
    ("🌍", "Real-world tested", "Evaluated on independent field photos (PlantDoc), not only lab images — and the gap is reported honestly."),
    ("⚖️", "Model comparison", "A from-scratch CNN and a transfer-learning model were both trained and compared before picking one."),
]
cols = st.columns(4)
for c, (icon, title, desc) in zip(cols, features):
    with c:
        st.markdown(
            f'<div class="feature-card"><div class="icon">{icon}</div>'
            f'<h4>{title}</h4><p>{desc}</p></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.info(
    "⚠️ **Note on accuracy:** this model is trained on lab-condition images with plain "
    "backgrounds, so real-world field photos are harder and accuracy is meaningfully lower. "
    "See the **About** page for the full, honest breakdown."
)
