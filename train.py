"""
Train a CNN to classify plant leaf diseases (38 classes).

Dataset: "New Plant Diseases Dataset (Augmented)" on Kaggle
https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

Expected folder layout after downloading/extracting:
    data/
        train/<class_name>/*.jpg
        valid/<class_name>/*.jpg

Two backbone options:
    --backbone custom     A CNN trained from scratch (faithful to the original
                           tutorial architecture). Fast to train, but tends to
                           overfit to the plain lab backgrounds in this dataset.
    --backbone mobilenet  MobileNetV3Small pretrained on ImageNet, with a new
                           classification head. RECOMMENDED — pretrained
                           features generalize much better to real-world
                           photos (see README "Limitations" section).

Usage:
    python train.py --data_dir data --backbone mobilenet --epochs 15
"""

import argparse
import json
import os

import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras import layers, models

from class_names import CLASS_NAMES

IMG_SIZE = (128, 128)


def build_datasets(data_dir: str, batch_size: int):
    """Returns raw float32 images in [0, 255] — preprocessing/normalization
    happens inside build_model() so it matches whichever backbone is used."""
    train_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "train"),
        labels="inferred",
        label_mode="categorical",
        color_mode="rgb",
        batch_size=batch_size,
        image_size=IMG_SIZE,
        shuffle=True,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "valid"),
        labels="inferred",
        label_mode="categorical",
        color_mode="rgb",
        batch_size=batch_size,
        image_size=IMG_SIZE,
        shuffle=False,
    )
    assert train_ds.class_names == CLASS_NAMES, (
        "Dataset class order does not match class_names.py — "
        "update CLASS_NAMES to match train_ds.class_names."
    )

    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
    return train_ds, val_ds


def build_augmentation() -> tf.keras.Sequential:
    """Field-conditioned augmentation: goes beyond simple flips/zooms to
    simulate the messiness of a real phone photo (uneven lighting, off-center
    leaf, blur/noise) — not just clean lab-style variations. This directly
    targets the lab-to-field generalization gap."""
    return models.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.15),
            layers.RandomZoom(0.2),
            layers.RandomTranslation(0.15, 0.15),
            layers.RandomContrast(0.25),
            layers.RandomBrightness(0.25, value_range=(0, 255)),
        ],
        name="field_augmentation",
    )


def build_model(num_classes: int, backbone: str) -> tf.keras.Model:
    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = build_augmentation()(inputs)

    if backbone == "custom":
        x = layers.Rescaling(1.0 / 255)(x)
        x = layers.Conv2D(32, 3, padding="same", activation="relu")(x)
        x = layers.Conv2D(32, 3, activation="relu")(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
        x = layers.Conv2D(64, 3, activation="relu")(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
        x = layers.Conv2D(128, 3, activation="relu")(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(256, 3, padding="same", activation="relu")(x)
        x = layers.Conv2D(256, 3, activation="relu")(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Dropout(0.25)(x)
        x = layers.Flatten()(x)
        x = layers.Dense(1500, activation="relu")(x)
        x = layers.Dropout(0.4)(x)
        outputs = layers.Dense(num_classes, activation="softmax")(x)

    elif backbone == "mobilenet":
        # include_preprocessing=True lets us feed raw [0, 255] floats directly —
        # the base model handles its own normalization internally.
        base = tf.keras.applications.MobileNetV3Small(
            input_shape=(*IMG_SIZE, 3),
            include_top=False,
            weights="imagenet",
            pooling="avg",
            include_preprocessing=True,
        )
        base.trainable = False  # Phase 1: feature extraction only
        x = base(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(num_classes, activation="softmax")(x)

    else:
        raise ValueError(f"Unknown backbone: {backbone}")

    model = models.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3 if backbone == "mobilenet" else 1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def unfreeze_for_fine_tuning(model: tf.keras.Model, num_layers: int = 30):
    """Phase 2 (optional): unfreeze the last N layers of the MobileNet base
    and continue training at a low learning rate. Improves accuracy further
    but is optional — skip if training time is limited."""
    base = model.layers[2]  # Input -> augmentation -> base model
    base.trainable = True
    for layer in base.layers[:-num_layers]:
        layer.trainable = False
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def evaluate_and_save(model, val_ds, output_dir):
    y_true, y_pred = [], []
    for x_batch, y_batch in val_ds:
        preds = model.predict(x_batch, verbose=0)
        y_pred.extend(tf.argmax(preds, axis=1).numpy())
        y_true.extend(tf.argmax(y_batch, axis=1).numpy())

    report = classification_report(y_true, y_pred, target_names=CLASS_NAMES)
    print(report)
    with open(os.path.join(output_dir, "classification_report.txt"), "w") as f:
        f.write(report)

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(20, 20))
    sns.heatmap(cm, annot=False, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix (PlantVillage validation set)")
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"), dpi=150)
    plt.close()


def plot_history(history_dict, output_dir, filename="training_curves.png"):
    epochs_range = range(1, len(history_dict["accuracy"]) + 1)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(epochs_range, history_dict["accuracy"], label="Train")
    axes[0].plot(epochs_range, history_dict["val_accuracy"], label="Validation")
    axes[0].set_title("Accuracy")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()
    axes[1].plot(epochs_range, history_dict["loss"], label="Train")
    axes[1].plot(epochs_range, history_dict["val_loss"], label="Validation")
    axes[1].set_title("Loss")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()
    fig.savefig(os.path.join(output_dir, filename), dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data", help="Folder containing train/ and valid/ subfolders")
    parser.add_argument("--backbone", choices=["custom", "mobilenet"], default="mobilenet")
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--fine_tune_epochs", type=int, default=5, help="0 to skip fine-tuning phase (mobilenet only)")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--output_dir", default="outputs")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    train_ds, val_ds = build_datasets(args.data_dir, args.batch_size)
    model = build_model(len(CLASS_NAMES), args.backbone)
    model.summary()

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            os.path.join(args.output_dir, "best_model.keras"),
            monitor="val_accuracy",
            save_best_only=True,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=4, restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6
        ),
    ]

    history = model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)
    full_history = dict(history.history)

    # Optional phase 2: fine-tune the last layers of the pretrained backbone.
    if args.backbone == "mobilenet" and args.fine_tune_epochs > 0:
        print("\n--- Fine-tuning phase: unfreezing top layers of MobileNetV3 ---\n")
        model = unfreeze_for_fine_tuning(model)
        ft_history = model.fit(
            train_ds, validation_data=val_ds, epochs=args.fine_tune_epochs, callbacks=callbacks
        )
        for k, v in ft_history.history.items():
            full_history[k] = full_history.get(k, []) + v

    model.save(os.path.join(args.output_dir, "trained_model.keras"))
    with open(os.path.join(args.output_dir, "training_history.json"), "w") as f:
        json.dump(full_history, f)
    with open(os.path.join(args.output_dir, "config.json"), "w") as f:
        json.dump({"backbone": args.backbone, "img_size": IMG_SIZE}, f)

    plot_history(full_history, args.output_dir)
    evaluate_and_save(model, val_ds, args.output_dir)

    print(f"\nDone. Artifacts saved to: {args.output_dir}/")


if __name__ == "__main__":
    main()
