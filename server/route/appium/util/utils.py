import subprocess
from typing import Union

import numpy as np
import supervision as sv
from PIL import Image

from ..util.box_annotator import BoxAnnotator


def execute_command(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()

def create_annotated_image(image: Union[str, Image.Image], bboxes: np.ndarray) -> Image.Image:
    if isinstance(image, str):
        image = Image.open(image)

    image = image.convert('RGB')
    image = np.asarray(image)
    h, w, _ = image.shape

    overlay_ratio = h / 3200
    draw_bbox_config = {
        'text_scale': 0.8 * overlay_ratio,
        'text_thickness': max(int(2 * overlay_ratio), 1),
        'text_padding': max(int(3 * overlay_ratio), 1),
        'thickness': max(int(3 * overlay_ratio), 1),
    }

    bboxes = bboxes * np.array([1, 1, 1, 1])
    detections = sv.Detections(bboxes)

    labels = [str(i) for i, _ in enumerate(bboxes)]

    annotator = BoxAnnotator(**draw_bbox_config)
    annotated_frame = image.copy()
    annotated_frame = annotator.annotate(
        scene=annotated_frame,
        detections=detections,
        labels=labels,
        image_size=(w, h)
    )
    pil_image = Image.fromarray(annotated_frame)
    return pil_image