import re
import numpy as np
import matplotlib.pyplot as plt

def eccentric_anomaly_binary_search(M: float, e: float, accuracy: float) -> float:
    left = 0
    right = np.pi * 2

    while right - left > accuracy:
        mid = (left + right) / 2
        predict = mid - e * np.sin(mid)

        if predict <= M:
            left = mid
        else:
            right = mid

    return left

def true_from_eccentric_anomaly(E: float, e: float) -> float:
    t = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))
    return t

def r_from_true_anomaly(t: float, e: float, a: float) -> float:
    return a * (1 - e * e) / (1 + e * np.cos(t))

def get_xy(t: float, r: float):
    x = r * np.cos(t)
    y = r * np.sin(t)
    return np.array([x, y])

