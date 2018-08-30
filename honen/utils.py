import numpy as np
import torch


def to_numpy(tensor) -> np.array:
    if isinstance(tensor, torch.Tensor):
        return tensor.to("cpu").numpy()
    elif isinstance(tensor, list):
        return np.array(tensor)
    else:
        # if numpy array or None
        return tensor


def length_check(x, y) -> None:
    if x is not None and len(x) != len(y):
        raise RuntimeError(f"length of x and y should be same but {len(x)} and {len(y)}")
