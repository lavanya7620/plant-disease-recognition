"""
Streamlit app: Plant Disease Recognition

Run with:
    streamlit run app.py
"""

import json
import os

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from class_names import CLASS_NAMES
from disease_info import DISEASE_INFO

IMG_SIZE = (128, 128)
MODEL_PATH = "outputs/trained_model.keras"
CONFIG_PATH = "outputs/config.json"
CONFIDENCE_THRESHOLD = 0.60  # below this, treat the prediction as unreliable


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
    return [(CLASS_NAMES[i], float(probs[i])) for i in top_indices]


def main():
    st.set_page_config(page_title="Plant Disease Recognition", page_icon="🌿", layout="centered")

    st.title("🌿 Plant Disease Recognition")
    st.write(
        "Upload a photo of a plant leaf and get an instant disease diagnosis "
        "with treatment guidance."
    )

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

    uploaded_file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded image", use_container_width=True)

        if st.button("Predict", type="primary"):
            try:
                model, backbone = load_model_and_config()
            except Exception:
                st.error(
                    "Model file not found. Train the model first with `python train.py`, "
                    "which saves `outputs/trained_model.keras`, then restart the app."
                )
                return

            with st.spinner("Analyzing image..."):
                results = predict(model, image, backbone)

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

            st.subheader(f"🩺 {info.get('condition', top_class)}")
            st.caption(f"Crop: {info.get('crop', '—')} · Confidence: {top_conf:.1%}")

            if "healthy" in top_class.lower():
                st.success(info.get("description", ""))
            else:
                st.warning(info.get("description", ""))
                st.markdown(f"**Suggested treatment / management:**\n\n{info.get('treatment', 'N/A')}")

            with st.expander("Other possible matches"):
                for name, conf in results[1:]:
                    other_info = DISEASE_INFO.get(name, {})
                    st.write(f"- {other_info.get('condition', name)} ({other_info.get('crop', '')}) — {conf:.1%}")

            st.caption(
                "⚠️ This is a machine-learning prediction, not a substitute for advice "
                "from a certified plant pathologist or local agricultural extension office."
            )


if __name__ == "__main__":
    main()
