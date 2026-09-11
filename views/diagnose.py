from datetime import datetime

import streamlit as st
from PIL import Image

from class_names import CLASS_NAMES
from core import CONFIDENCE_THRESHOLD, build_report_text, predict, try_load_model
from disease_info import DISEASE_INFO
from gradcam import make_gradcam_heatmap, overlay_heatmap

st.title("🔍 Diagnose a Leaf")
st.write(
    "Upload a photo of a plant leaf and get an instant disease diagnosis, "
    "a Grad-CAM explanation of the model's reasoning, and treatment guidance."
)

if "history" not in st.session_state:
    st.session_state.history = []

model, backbone, model_loaded = try_load_model()

if not model_loaded:
    st.error(
        "Model file not found. Train the model first with `python train.py`, "
        "which saves `outputs/trained_model.keras`, then restart the app."
    )
    st.stop()

uploaded_file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded image", use_container_width=True)

    if st.button("🔍 Predict", type="primary"):
        with st.status("Analyzing leaf image...", expanded=True) as status:
            st.write("🔎 Preprocessing image...")
            results, arr = predict(model, image, backbone)
            top_class, top_conf = results[0]
            info = DISEASE_INFO.get(top_class, {})

            st.write("🧠 Running model prediction...")
            heatmap_overlay = None
            if top_conf >= CONFIDENCE_THRESHOLD:
                st.write("🔥 Generating Grad-CAM explanation...")
                try:
                    heatmap = make_gradcam_heatmap(model, backbone, arr, pred_index=CLASS_NAMES.index(top_class))
                    heatmap_overlay = overlay_heatmap(image, heatmap)
                except Exception:
                    heatmap_overlay = None

            status.update(label="Analysis complete ✅", state="complete", expanded=False)

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
        else:
            is_healthy = "healthy" in top_class.lower()
            card_class = "result-card" if is_healthy else "result-card disease"

            if is_healthy:
                st.balloons()
                st.toast(f"Good news — {info.get('crop', 'this plant')} looks healthy!", icon="🌿")
            else:
                st.toast(f"Diagnosis complete: {info.get('condition', top_class)}", icon="🩺")

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
                if heatmap_overlay is not None:
                    st.image(heatmap_overlay, caption="Grad-CAM: where the model looked", use_container_width=True)
                else:
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