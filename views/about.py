import streamlit as st

st.title("ℹ️ About This Project")

st.write(
    "A CNN-based web app that identifies plant leaf diseases from a photo and "
    "suggests treatment steps — built with TensorFlow/Keras and Streamlit, with a "
    "deliberate focus on **real-world generalization**, not just lab-condition accuracy."
)

st.subheader("Dataset")
st.write(
    "[New Plant Diseases Dataset (Augmented)]"
    "(https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset) — "
    "~87,000 RGB leaf images across 38 classes and 14 crop species, pre-split into "
    "train/validation sets."
)

st.divider()
st.subheader("Model comparison: custom CNN vs. transfer learning")
st.write(
    "Rather than assume transfer learning would win, both architectures were actually "
    "trained and evaluated on identical data, preprocessing, and augmentation:"
)
st.table(
    {
        "": ["Lab validation accuracy", "Real-world (PlantDoc) accuracy", "Time per epoch (CPU)", "Total training time"],
        "MobileNetV3 (transfer learning)": ["87.4%", "16.9%", "~4-5 min", "~94 min (20 epochs)"],
        "Custom CNN (from scratch)": ["85.8%*", "13.6%*", "~33 min", "~165 min (5 epochs only)"],
    }
)
st.caption(
    "*The custom CNN was stopped after 5 epochs (still improving) due to its ~6-8x "
    "slower per-epoch cost with no pretrained head start. MobileNetV3 was selected as "
    "the production model — better accuracy on both benchmarks, and far faster to train."
)

st.divider()
st.subheader("Limitations & real-world generalization")
st.write(
    "This dataset (like the original PlantVillage it's built from) consists of leaf "
    "images photographed individually against plain, uniform backgrounds in controlled "
    "conditions. This is a well-documented issue in the plant disease classification "
    "literature — models trained on it can achieve 99%+ accuracy internally but "
    "generalize poorly to field photos."
)
st.markdown(
    """
- One widely-cited study found accuracy dropping from 99% to 31% when a
  PlantVillage-trained model was tested on images from other online sources.
- A more recent study found a model scoring 99.6% internally dropped to 66.8%
  on an independent field-acquired test set.
- A bias analysis found a model trained on just 8 background pixels (no leaf
  at all) achieved 49% accuracy vs. a 2.6% random baseline — evidence that
  models can partly learn background/lighting shortcuts instead of real
  disease features.
"""
)
st.write("This project actively works against that problem, rather than ignoring it:")
st.markdown(
    """
1. **Field-conditioned augmentation** during training
2. **Transfer learning** from ImageNet features, which generalize better than
   training from scratch on a narrow, single-domain dataset
3. **Confidence gating** in the app, so uncertain predictions are labeled as
   such instead of presented as confident diagnoses
4. **External validation on PlantDoc** — a separate dataset of real,
   cluttered-background field photos — to honestly measure and report the
   internal-vs-field accuracy gap rather than hiding it
"""
)

st.divider()
st.subheader("Links")
st.markdown(
    """
- 💻 [Source code on GitHub](https://github.com/lavanya7620/plant-disease-recognition)
- 📊 [Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- 🌍 [Real-world evaluation set: PlantDoc](https://github.com/pratikkayal/PlantDoc-Dataset)
"""
)

st.caption(
    "Project architecture inspired by common plant-disease CNN tutorials, rebuilt and "
    "extended (transfer learning, field-conditioned augmentation, confidence gating, "
    "Grad-CAM explainability, structured treatment info, external validation, and this "
    "multi-page UI) as an independent implementation."
)
