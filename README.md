# 🌿 Plant Disease Recognition

A CNN-based web app that identifies plant leaf diseases from a photo and
suggests treatment steps — built with TensorFlow/Keras and deployed with
Streamlit, with a deliberate focus on **real-world generalization**, not just
lab-condition accuracy (see [Limitations](#limitations--real-world-generalization) below).

## Features
- Two architectures trained and compared head-to-head — a from-scratch CNN
  baseline vs. transfer learning — with the better one selected on evidence,
  not assumption (see [Model Comparison](#model-comparison-custom-cnn-vs-transfer-learning))
- Transfer-learning CNN (MobileNetV3Small, ImageNet-pretrained) across
  **38 disease classes** and 14 crop species (Apple, Corn, Grape, Potato,
  Tomato, and more)
- Field-conditioned data augmentation (flip, rotation, zoom, translation,
  brightness, contrast) to reduce overfitting to plain lab backgrounds
- Two-phase training: frozen feature extraction, then optional fine-tuning
  of the backbone's top layers
- **Grad-CAM explainability**: every prediction shows a heatmap of which
  region of the leaf the model actually focused on
- Streamlit UI: tabbed layout (Diagnose / Model Performance), styled result
  cards, session history, and a downloadable text diagnosis report
- **Confidence gating**: low-confidence predictions are flagged as uncertain
  instead of shown as a false-confident diagnosis
- Honest evaluation on both the lab-condition validation set AND an
  independent real-world dataset (PlantDoc), for both architectures

## Dataset
[New Plant Diseases Dataset (Augmented)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
— ~87,000 RGB leaf images across 38 classes, pre-split into `train/` and `valid/`.

## Limitations & real-world generalization

This dataset (like the original PlantVillage it's built from) consists of
leaf images photographed individually against plain, uniform backgrounds
in controlled conditions. This is a well-documented issue in the plant
disease classification literature — models trained on it can achieve
99%+ accuracy internally but generalize poorly to field photos:

- One widely-cited study found accuracy dropping from 99% to 31% when a
  PlantVillage-trained model was tested on images collected from other
  online sources.
- A more recent study found a model that scored 99.6% internally dropped
  to 66.8% on an independent field-acquired test set.
- A bias analysis found a model trained on **just 8 background pixels**
  (no leaf at all) achieved 49% accuracy vs. a 2.6% random baseline —
  evidence that models can partly learn background/lighting shortcuts
  instead of real disease features.

This project doesn't pretend that problem is solved, but it does actively
work against it:
1. **Field-conditioned augmentation** during training (see `train.py`)
2. **Transfer learning** from ImageNet features, which generalize better
   than a CNN trained from scratch on a narrow, uniform dataset
3. **Confidence gating** in the app, so uncertain predictions are labeled
   as such rather than presented as confident diagnoses
4. **External validation on PlantDoc** (`evaluate_plantdoc.py`) — a separate
   dataset of real, cluttered-background field photos — to honestly measure
   and report the internal-vs-field accuracy gap rather than hiding it

**Measured on this project:**
- Internal validation accuracy (PlantVillage): **87.4%**
- External real-world accuracy (PlantDoc): **16.9%**

That ~70-point gap is real, and it's larger than what some published studies
report — likely because several PlantDoc classes here have very few images
(4-12), making per-class accuracy noisy, and because some PlantDoc "leaf"
categories mix healthy and diseased photos ambiguously. Reporting it honestly,
rather than only citing the 87.4%, is the point.

## Model comparison: custom CNN vs. transfer learning

Rather than assume transfer learning would win, both architectures were
actually trained and evaluated on identical data, preprocessing, and
augmentation:

| | MobileNetV3 (transfer learning) | Custom CNN (from scratch) |
|---|---|---|
| Lab validation accuracy | **87.4%** | 85.8%* |
| Real-world (PlantDoc) accuracy | **16.9%** | 13.6%* |
| Params trained | ~22K (frozen backbone) → full net after fine-tuning | 15.05M (all trained from epoch 1) |
| Time per epoch (CPU) | ~4-5 min | ~33 min |
| Total training time | ~94 min (20 epochs: 15 frozen + 5 fine-tune) | ~165 min (only 5 epochs — see note) |

\* *The custom CNN was stopped after 5 epochs (train accuracy still climbing:
0.44 → 0.86) due to the ~6-8x slower per-epoch cost on CPU with no pretrained
head start. Even under-trained, MobileNetV3 already beats it on both lab and
real-world accuracy while training faster in total — the gap would likely
widen further if the custom CNN were trained to full convergence, given how
much more slowly it improves per unit of compute.*

**Conclusion:** MobileNetV3Small was selected as the production model — it
generalizes better to real-world photos, trains substantially faster per
epoch, and starts from ImageNet features rather than learning basic visual
patterns from scratch on a narrow, single-domain dataset.

Reproduce this comparison:
```bash
python train.py --data_dir data --backbone custom --epochs 5 --output_dir outputs_custom
python evaluate_plantdoc.py --plantdoc_dir PlantDoc-Dataset/test --model_path outputs_custom/trained_model.keras --output_dir outputs_custom
```

## Project structure
```
plant-disease-app/
├── app.py                  # Streamlit app (tabs, Grad-CAM, history, confidence gating)
├── gradcam.py               # Grad-CAM heatmap generation
├── train.py                # Training script (augmentation + transfer learning)
├── evaluate_plantdoc.py    # External real-world evaluation
├── class_names.py          # 38 class labels (order-sensitive)
├── disease_info.py         # Descriptions + treatment guidance per class
├── plantdoc_mapping.py     # Maps PlantDoc folders -> our 38 classes
├── .streamlit/config.toml   # App color theme
├── requirements.txt
├── outputs/                 # Active model: trained_model.keras, metrics, plots (generated)
└── outputs_custom/          # Custom-CNN comparison run (generated, optional)
```

## Setup

```bash
git clone <your-repo-url>
cd plant-disease-app
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Download the dataset from Kaggle and arrange it as:
```
data/
├── train/<class_name>/*.jpg
└── valid/<class_name>/*.jpg
```

## Train the model
```bash
python train.py --data_dir data --backbone mobilenet --epochs 15 --fine_tune_epochs 5
```
Saves `outputs/trained_model.keras`, `outputs/config.json`, training curves,
a confusion matrix, and a classification report.

Use `--backbone custom` instead for a from-scratch CNN (faster to train,
but generalizes worse to real photos — see Limitations above).

## Evaluate on real-world images (PlantDoc)
```bash
git clone https://github.com/pratikkayal/PlantDoc-Dataset.git
python evaluate_plantdoc.py --plantdoc_dir PlantDoc-Dataset/test
```
Prints per-class and overall real-world accuracy, and saves a report +
confusion matrix to `outputs/`.

## Run the app
```bash
streamlit run app.py
```

## Model architecture
MobileNetV3Small (ImageNet-pretrained, frozen initially) as a feature
extractor, with a dropout + dense softmax classification head over 38
classes. An optional fine-tuning phase unfreezes the backbone's top layers
at a low learning rate for a further accuracy boost.

## Results
- Lab validation accuracy: **87.4%** (`outputs/training_curves.png`, `outputs/confusion_matrix.png`)
- Real-world (PlantDoc) accuracy: **16.9%** (`outputs/plantdoc_confusion_matrix.png`)
- Full per-class precision/recall/F1 for both: see the "Model Performance"
  tab in the running app, or `outputs/classification_report.txt` and
  `outputs/plantdoc_classification_report.txt`
- See [Model comparison](#model-comparison-custom-cnn-vs-transfer-learning)
  above for how this compares to a from-scratch CNN baseline

## Acknowledgements
Dataset by [vipoooool on Kaggle](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset).
Real-world evaluation set: [PlantDoc](https://github.com/pratikkayal/PlantDoc-Dataset)
(Singh et al., 2019). Project architecture inspired by common plant-disease
CNN tutorials, rebuilt and extended (transfer learning, field-conditioned
augmentation, confidence gating, treatment-info layer, external validation)
as an independent implementation.