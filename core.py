"""
Shared logic used across every page of the app: model loading, prediction,
and diagnosis report generation. Kept separate from any single page so it
has one source of truth.
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


def try_load_model():
    """Returns (model, backbone, loaded_ok). Never raises — callers check loaded_ok."""
    try:
        model, backbone = load_model_and_config()
        return model, backbone, True
    except Exception:
        return None, None, False


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
