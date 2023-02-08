import numpy as np

def collect_info(array):
    return "Shape: {}; dimensions: {}; length: {}; size: {}".format(array.shape, array.ndim, len(array), array.size)
