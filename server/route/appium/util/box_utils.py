from typing import List, Union

import numpy as np


def merge_box(box: Union[List[List[float]], np.ndarray]) -> List[float]:
    if len(box) == 0:
        return [0, 0, 0, 0]

    box = np.asarray(box)

    x_min, y_min = np.min(box[:, 0]), np.min(box[:, 1])
    x_max, y_max = np.max(box[:, 2]), np.max(box[:, 3])

    return [float(x_min), float(y_min), float(x_max), float(y_max)]

def get_occluded_indices(box: Union[List[List[float]], np.ndarray], drawing_order: List[int]) -> List[int]:
    if len(box) == 0:
        return []

    box = np.asarray(box) # [n, 4]
    drawing_order = np.asarray(drawing_order) # [n,]

    # broadcasting
    box_i = box[:, np.newaxis, :] # [n, 1, 4]
    box_j = box[np.newaxis, :, :] # [1, n, 4]

    # split min max
    min_i, max_i = box_i[:, :, :2], box_i[:, :, 2:] # [n, 1, 2]
    min_j, max_j = box_j[:, :, :2], box_j[:, :, 2:] # [1, n, 2]

    # create relationship
    contains = np.all(min_i <= min_j, axis=2) & np.all(max_i >= max_j, axis=2)
    # exclude self x self
    np.fill_diagonal(contains, False)

    # broadcasting
    order_i = drawing_order[:, np.newaxis] # [n, 1]
    order_j = drawing_order[np.newaxis, :]  # [1, n]

    order = order_i > order_j
    occlusion = contains & order
    occluded = np.any(occlusion, axis=0)
    return np.where(occluded)[0].tolist()
