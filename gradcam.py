"""
Grad-CAM: highlights which regions of the leaf image most influenced the
model's prediction. Works for both backbones trained by train.py.
"""

import numpy as np
import tensorflow as tf
from PIL import Image


def _find_last_conv_layer(m: tf.keras.Model):
    """Finds the last layer with a 4D (batch, H, W, C) output — i.e. the
    last spatial feature map before flattening/pooling."""
    for layer in reversed(m.layers):
        try:
            shape = layer.output.shape
        except (AttributeError, ValueError):
            continue
        if shape is not None and len(shape) == 4:
            return layer
    return None


def make_gradcam_heatmap(model: tf.keras.Model, backbone: str, img_array: np.ndarray, pred_index=None):
    """img_array: preprocessed batch of shape (1, H, W, 3), in the same
    format passed to model.predict() (raw [0,255] for mobilenet, [0,1] for
    the custom backbone). Returns a 2D numpy heatmap in [0, 1]."""
    img_tensor = tf.convert_to_tensor(img_array)

    if backbone == "mobilenet":
        base = model.layers[2]  # Input -> augmentation -> MobileNetV3Small base
        conv_layer = _find_last_conv_layer(base)
        grad_model = tf.keras.Model(base.input, [conv_layer.output, base.output])
        dropout_layer = model.layers[3]
        dense_layer = model.layers[4]

        with tf.GradientTape() as tape:
            conv_output, pooled_output = grad_model(img_tensor)
            tape.watch(conv_output)
            x = dropout_layer(pooled_output, training=False)
            preds = dense_layer(x)
            if pred_index is None:
                pred_index = int(tf.argmax(preds[0]))
            class_channel = preds[:, pred_index]
    else:
        conv_layer = _find_last_conv_layer(model)
        grad_model = tf.keras.Model(model.input, [conv_layer.output, model.output])

        with tf.GradientTape() as tape:
            conv_output, preds = grad_model(img_tensor)
            tape.watch(conv_output)
            if pred_index is None:
                pred_index = int(tf.argmax(preds[0]))
            class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_output = conv_output[0]
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()


def overlay_heatmap(original_image: Image.Image, heatmap: np.ndarray, alpha: float = 0.45) -> Image.Image:
    """Resizes the heatmap to the original image and blends it on as a
    red/yellow 'hot' overlay, without needing matplotlib's colormap module."""
    heatmap_img = Image.fromarray(np.uint8(255 * heatmap)).resize(original_image.size)
    intensity = np.array(heatmap_img).astype(np.float32)

    colored = np.zeros((*intensity.shape, 3), dtype=np.uint8)
    colored[..., 0] = np.clip(intensity * 2, 0, 255).astype(np.uint8)                  # red ramps up first
    colored[..., 1] = np.clip((intensity - 128) * 2, 0, 255).astype(np.uint8)          # green kicks in at high intensity (-> yellow/white hot)
    colored_img = Image.fromarray(colored).convert("RGB")

    base = original_image.convert("RGB")
    return Image.blend(base, colored_img, alpha=alpha)
