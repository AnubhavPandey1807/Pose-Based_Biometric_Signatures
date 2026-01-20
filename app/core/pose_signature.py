import numpy as np
import math

def angle(a, b, c):
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cos_angle = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6
    )
    return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

def extract_signature(lm):
    """
    lm: landmark list from PoseDetector
    """

    right_elbow = angle(lm[12][1:], lm[14][1:], lm[16][1:])
    left_elbow  = angle(lm[11][1:], lm[13][1:], lm[15][1:])

    shoulder_width = np.linalg.norm(
        np.array(lm[11][1:]) - np.array(lm[12][1:])
    )

    arm_extension = np.linalg.norm(
        np.array(lm[16][1:]) - np.array(lm[12][1:])
    ) / shoulder_width

    return np.array([
        right_elbow,
        left_elbow,
        arm_extension
    ])
