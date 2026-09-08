"""
Evaluate the trained model on PlantDoc — a small dataset of REAL field-condition
leaf photos (cluttered backgrounds, natural lighting) — to honestly measure
how much accuracy drops going from the lab-condition PlantVillage validation
set to real-world photos.

Setup:
    git clone https://github.com/pratikkayal/PlantDoc-Dataset.git

Usage:
    python evaluate_plantdoc.py --plantdoc_dir PlantDoc-Dataset/test \
        --model_path outputs/trained_model.keras
"""

import argparse
import json
import os

import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from class_names import CLASS_NAMES
from plantdoc_mapping import PLANTDOC_TO_OUR_CLASSES

IMG_SIZE = (128, 128)


def load_image(path: str) -> np.ndarray:
    img = Image.open(path).convert("RGB").resize(IMG_SIZE)
    return tf.keras.preprocessing.image.img_to_array(img)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plantdoc_dir", required=True, help="Path to PlantDoc-Dataset/test (or /train)")
    parser.add_argument("--model_path", default="outputs/trained_model.keras")
    parser.add_argument("--output_dir", default="outputs")
    args = parser.parse_args()

    model = tf.keras.models.load_model(args.model_path)
    os.makedirs(args.output_dir, exist_ok=True)

    y_true, y_pred, skipped_classes = [], [], []

    for folder_name in sorted(os.listdir(args.plantdoc_dir)):
        folder_path = os.path.join(args.plantdoc_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        our_class = PLANTDOC_TO_OUR_CLASSES.get(folder_name)
        if our_class is None:
            skipped_classes.append(folder_name)
            continue

        true_idx = CLASS_NAMES.index(our_class)
        images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        batch = np.array([load_image(os.path.join(folder_path, f)) for f in images])
        preds = model.predict(batch, verbose=0)
        pred_indices = np.argmax(preds, axis=1)

        y_true.extend([true_idx] * len(images))
        y_pred.extend(pred_indices.tolist())

        acc = np.mean(pred_indices == true_idx)
        print(f"{folder_name:40s} -> {our_class:45s} ({len(images):3d} imgs, acc={acc:.1%})")

    if skipped_classes:
        print(f"\nSkipped {len(skipped_classes)} PlantDoc classes with no mapping to our 38 classes:")
        print(", ".join(skipped_classes))

    overall_acc = np.mean(np.array(y_true) == np.array(y_pred))
    print(f"\n=== Overall real-world (PlantDoc) accuracy: {overall_acc:.1%} ===")
    print("Compare this to your validation accuracy on the PlantVillage set — "
          "the gap between them IS the lab-to-field generalization gap.")

    present_labels = sorted(set(y_true) | set(y_pred))
    target_names = [CLASS_NAMES[i] for i in present_labels]
    report = classification_report(y_true, y_pred, labels=present_labels, target_names=target_names, zero_division=0)
    with open(os.path.join(args.output_dir, "plantdoc_classification_report.txt"), "w") as f:
        f.write(f"Overall real-world accuracy: {overall_acc:.1%}\n\n")
        f.write(report)
    print(report)

    cm = confusion_matrix(y_true, y_pred, labels=present_labels)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=target_names, yticklabels=target_names, cmap="Oranges")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"PlantDoc (real-world) Confusion Matrix — {overall_acc:.1%} accuracy")
    plt.tight_layout()
    plt.savefig(os.path.join(args.output_dir, "plantdoc_confusion_matrix.png"), dpi=150)

    with open(os.path.join(args.output_dir, "plantdoc_accuracy.json"), "w") as f:
        json.dump({"overall_accuracy": overall_acc}, f)

    print(f"\nSaved report + confusion matrix to {args.output_dir}/")


if __name__ == "__main__":
    main()
