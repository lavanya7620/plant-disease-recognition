"""
Streamlit app: Plant Disease Recognition

Run with:
    streamlit run app.py
"""

import json
import os
from datetime import datetime

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from class_names import CLASS_NAMES
from disease_info import DISEASE_INFO
from gradcam import make_gradcam_heatmap, overlay_heatmap

IMG_SIZE = (128, 128)
MODEL_PATH = "outputs/trained_model.keras"
CONFIG_PATH = "outputs/config.json"
CONFIDENCE_THRESHOLD = 0.60  # below this, treat the prediction as unreliable

CUSTOM_CSS = """
<style>
.result-card {
    padding: 1.25rem 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid #C8E6C9;
    background-color: #F1F8E9;
    margin-bottom: 1rem;
}
.result-card.disease {
    border-color: #FFCC80;
    background-color: #FFF8E1;
}
.confidence-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 1rem;
    background-color: #2E7D32;
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
}
.hero {
    padding: 1.5rem 0 0.5rem 0;
}
.history-item {
    padding: 0.4rem 0.6rem;
    border-radius: 0.5rem;
    background-color: #F1F8E9;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
}
</style>
"""


@st.cache_resource
def load_model_and_config():
    model = tf.keras.models.load_model(MODEL_PATH)
    backbone = "mobilenet"  # default assumption if config.json is missing
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            backbone = json.load(f).get("backbone", backbone)
    return model, backbone


def preprocess_image(image: Image.Image, backbone: str) -> np.ndarray:
    image = image.convert("RGB").resize(IMG_SIZE)
    arr = tf.keras.preprocessing.image.img_to_array(image)  # float32, [0, 255]
    arr = np.expand_dims(arr, axis=0)
    if backbone == "custom":
        arr = arr / 255.0  # the mobilenet backbone normalizes internally
    return arr


def predict(model, image: Image.Image, backbone: str):
    arr = preprocess_image(image, backbone)
    probs = model.predict(arr, verbose=0)[0]
    top_indices = np.argsort(probs)[::-1][:3]
    return [(CLASS_NAMES[i], float(probs[i])) for i in top_indices], arr


def build_report_text(info, top_class, top_conf, results):
    lines = [
        "PLANT DISEASE RECOGNITION — DIAGNOSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "-" * 50,
        f"Crop: {info.get('crop', '—')}",
        f"Condition: {info.get('condition', top_class)}",
        f"Confidence: {top_conf:.1%}",
        "",
        f"Symptoms: {info.get('symptoms', '')}",
        f"Likely cause: {info.get('causes', '')}",
    ]
    if "healthy" not in top_class.lower():
        lines += ["", f"Suggested treatment / management: {info.get('treatment', 'N/A')}"]
    lines += ["", "Other possible matches:"]
    for name, conf in results[1:]:
        c_info = DISEASE_INFO.get(name, {})
        lines.append(f"  - {c_info.get('condition', name)} ({c_info.get('crop', '')}) — {conf:.1%}")
    lines += [
        "",
        "-" * 50,
        "This is a machine-learning prediction, not a substitute for advice from a",
        "certified plant pathologist or local agricultural extension office.",
    ]
    return "\n".join(lines)


def render_diagnose_tab(model, backbone):
    uploaded_file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

    if uploaded_file is None:
        return

    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded image", use_container_width=True)

    if not st.button("🔍 Predict", type="primary"):
        return

    with st.spinner("Analyzing image..."):
        results, arr = predict(model, image, backbone)

    top_class, top_conf = results[0]
    info = DISEASE_INFO.get(top_class, {})

    if top_conf < CONFIDENCE_THRESHOLD:
        st.warning(
            f"⚠️ Low confidence ({top_conf:.0%}) — the model isn't sure about this image. "
            "This often happens with cluttered backgrounds, poor lighting, multiple leaves "
            "in frame, or a plant/disease outside the 38 classes this model was trained on. "
            "Try a clearer photo of a single leaf against a plain background."
        )
        with st.expander("Best guesses anyway (low confidence)"):
            for name, conf in results:
                c_info = DISEASE_INFO.get(name, {})
                st.write(f"- {c_info.get('condition', name)} ({c_info.get('crop', '')}) — {conf:.1%}")
        return

    is_healthy = "healthy" in top_class.lower()
    card_class = "result-card" if is_healthy else "result-card disease"
    st.markdown(
        f"""<div class="{card_class}">
        <h3>🩺 {info.get('condition', top_class)}</h3>
        <p>Crop: <b>{info.get('crop', '—')}</b> &nbsp;
        <span class="confidence-badge">{top_conf:.1%} confidence</span></p>
        <p><b>Symptoms:</b> {info.get('symptoms', '')}</p>
        {'' if is_healthy else f"<p><b>Likely cause:</b> {info.get('causes', '')}</p>"}
        {'' if is_healthy else f"<p><b>Suggested treatment / management:</b><br>{info.get('treatment', 'N/A')}</p>"}
        </div>""",
        unsafe_allow_html=True,
    )

    with col2:
        try:
            heatmap = make_gradcam_heatmap(model, backbone, arr, pred_index=CLASS_NAMES.index(top_class))
            overlay = overlay_heatmap(image, heatmap)
            st.image(overlay, caption="Grad-CAM: where the model looked", use_container_width=True)
        except Exception:
            st.caption("Grad-CAM visualization unavailable for this model.")

    with st.expander("Other possible matches"):
        for name, conf in results[1:]:
            other_info = DISEASE_INFO.get(name, {})
            st.write(f"- {other_info.get('condition', name)} ({other_info.get('crop', '')}) — {conf:.1%}")

    report_text = build_report_text(info, top_class, top_conf, results)
    st.download_button(
        "⬇️ Download diagnosis report (.txt)",
        data=report_text,
        file_name=f"diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )

    st.caption(
        "⚠️ This is a machine-learning prediction, not a substitute for advice "
        "from a certified plant pathologist or local agricultural extension office."
    )

    st.session_state.history.insert(
        0, {"condition": info.get("condition", top_class), "crop": info.get("crop", ""), "confidence": top_conf}
    )
    st.session_state.history = st.session_state.history[:10]


def render_performance_tab():
    st.subheader("Model Performance")

    val_acc, real_acc = None, None
    try:
        with open("outputs/training_history.json") as f:
            hist = json.load(f)
            val_acc = hist.get("val_accuracy", [None])[-1]
    except Exception:
        pass
    try:
        with open("outputs/plantdoc_accuracy.json") as f:
            real_acc = json.load(f).get("overall_accuracy")
    except Exception:
        pass

    c1, c2 = st.columns(2)
    c1.metric("Validation accuracy (lab images)", f"{val_acc:.1%}" if val_acc else "—")
    c2.metric("Real-world accuracy (PlantDoc)", f"{real_acc:.1%}" if real_acc else "—")
    if val_acc and real_acc:
        st.caption(
            f"The {val_acc - real_acc:.0%} gap between these two numbers reflects the "
            "well-documented lab-to-field generalization challenge for this dataset "
            "(see README for details) — reported here rather than hidden."
        )

    st.divider()

    if os.path.exists("outputs/training_curves.png"):
        st.image("outputs/training_curves.png", caption="Training accuracy & loss curves")

    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("outputs/confusion_matrix.png"):
            st.image("outputs/confusion_matrix.png", caption="Confusion matrix (validation set)")
    with col2:
        if os.path.exists("outputs/plantdoc_confusion_matrix.png"):
            st.image("outputs/plantdoc_confusion_matrix.png", caption="Confusion matrix (real-world PlantDoc set)")

    if os.path.exists("outputs/classification_report.txt"):
        with st.expander("Full validation classification report"):
            st.text(open("outputs/classification_report.txt").read())
    if os.path.exists("outputs/plantdoc_classification_report.txt"):
        with st.expander("Full real-world (PlantDoc) classification report"):
            st.text(open("outputs/plantdoc_classification_report.txt").read())

    if not any(os.path.exists(p) for p in ["outputs/training_curves.png", "outputs/confusion_matrix.png"]):
        st.info("Run `python train.py` and `python evaluate_plantdoc.py` first to populate this tab.")


def main():
    st.set_page_config(page_title="Plant Disease Recognition", page_icon="🌿", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.title("🌿 Plant Disease Recognition")
    st.write(
        "Upload a photo of a plant leaf and get an instant disease diagnosis, "
        "a Grad-CAM explanation of the model's reasoning, and treatment guidance."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("About")
        st.write(
            "Dataset: New Plant Diseases Dataset (Kaggle) — ~87K images, "
            "14 crop species, 38 classes."
        )
        st.write("[Dataset source](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)")
        st.divider()
        st.caption(
            "⚠️ **Known limitation:** this model is trained on lab-condition "
            "images with plain backgrounds. Real-world field photos (cluttered "
            "background, uneven lighting) are harder and accuracy will be lower. "
            "For best results: one leaf, filling most of the frame, on a plain "
            "background, in good light."
        )
        if st.session_state.history:
            st.divider()
            st.subheader("Recent checks")
            for item in st.session_state.history:
                st.markdown(
                    f'<div class="history-item">🌿 {item["condition"]} '
                    f'({item["crop"]}) — {item["confidence"]:.0%}</div>',
                    unsafe_allow_html=True,
                )

    tab1, tab2 = st.tabs(["🔍 Diagnose", "📊 Model Performance"])

    try:
        model, backbone = load_model_and_config()
        model_loaded = True
    except Exception:
        model, backbone, model_loaded = None, None, False

    with tab1:
        if not model_loaded:
            st.error(
                "Model file not found. Train the model first with `python train.py`, "
                "which saves `outputs/trained_model.keras`, then restart the app."
            )
        else:
            render_diagnose_tab(model, backbone)

    with tab2:
        render_performance_tab()


if __name__ == "__main__":
    main()