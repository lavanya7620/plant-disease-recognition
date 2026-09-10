import json
import os

import numpy as np
import streamlit as st

from core import try_load_model

st.title("📊 Model Performance")

model, backbone, model_loaded = try_load_model()

if not model_loaded:
    st.error(
        "Model file not found. Train the model first with `python train.py`, "
        "which saves `outputs/trained_model.keras`, then restart the app."
    )
    st.stop()

st.subheader("Model Information")

arch_names = {
    "mobilenet": "MobileNetV3Small (ImageNet-pretrained transfer learning)",
    "custom": "Custom CNN (trained from scratch, no pretrained weights)",
}
total_params = model.count_params()
trainable_params = sum(int(np.prod(w.shape)) for w in model.trainable_weights)

c1, c2, c3 = st.columns(3)
c1.metric("Architecture", arch_names.get(backbone, backbone or "—"))
c2.metric("Total parameters", f"{total_params:,}")
c3.metric("Input image size", "128 × 128 px")

if backbone == "mobilenet":
    st.caption(
        f"**Training strategy:** two-phase transfer learning — Phase 1 trains only the "
        f"classification head ({trainable_params:,} params) with the pretrained MobileNetV3 "
        "backbone frozen; Phase 2 unfreezes the backbone's top layers and fine-tunes the "
        "full network at a low learning rate (1e-5). Field-conditioned data augmentation "
        "(flip, rotation, zoom, translation, brightness, contrast) is applied throughout to "
        "improve real-world generalization — see the About page for details."
    )
elif backbone == "custom":
    st.caption(
        f"**Training strategy:** trained end-to-end from randomly-initialized weights "
        f"(all {trainable_params:,} parameters trainable from epoch 1), with the same "
        "field-conditioned data augmentation applied. See the About page's Model Comparison "
        "section for why MobileNetV3 was selected as the production model instead."
    )

st.divider()
st.subheader("Accuracy: Lab vs. Real-World")

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
        "(see the About page for details) — reported here rather than hidden."
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
    st.info("Run `python train.py` and `python evaluate_plantdoc.py` first to populate this page.")
