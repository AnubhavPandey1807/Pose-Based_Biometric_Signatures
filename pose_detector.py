# pose_detector.py
import cv2
import math
import numpy as np
import mediapipe as mp

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options
from app.utils.logger import log_angle_to_csv


class PoseDetector:
    def __init__(self):
        options = vision.PoseLandmarkerOptions(
            base_options=base_options.BaseOptions(
                model_asset_path="pose_landmarker_lite.task"
            ),
            running_mode=vision.RunningMode.IMAGE,
            num_poses=1,
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)
        self.lmList = []

    # -------------------------------
    # Pose detection
    # -------------------------------
    def findPose(self, img, draw=False):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=img_rgb
        )

        result = self.detector.detect(mp_image)

        self.lmList = []

        if not result.pose_landmarks:
            return img

        h, w, _ = img.shape

        for idx, lm in enumerate(result.pose_landmarks[0]):
            cx, cy = int(lm.x * w), int(lm.y * h)
            self.lmList.append([idx, cx, cy])

            if draw:
                cv2.circle(img, (cx, cy), 4, (255, 0, 0), cv2.FILLED)

        return img

    # -------------------------------
    # Landmark list
    # -------------------------------
    def findPosition(self, img, draw=False):
        # lmList already populated in findPose
        return self.lmList
    
    

    # -------------------------------
    # Angle computation (UNCHANGED LOGIC)
    # -------------------------------
    def findAngle(self, img, p1, p2, p3, draw=True):
        if len(self.lmList) < max(p1, p2, p3) + 1:
            return None

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) -
            math.atan2(y1 - y2, x1 - x2)
        )

        if angle < 0:
            angle += 360

        # CSV logging (preserved)
        log_angle_to_csv(p1, p2, p3, angle)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 2)

            for x, y in [(x1, y1), (x2, y2), (x3, y3)]:
                cv2.circle(img, (x, y), 6, (0, 0, 255), cv2.FILLED)

            cv2.putText(
                img,
                f"{int(angle)}",
                (x2 - 40, y2 + 40),
                cv2.FONT_HERSHEY_PLAIN,
                1.5,
                (0, 0, 255),
                2
            )

        return angle


def extract_landmarks(self, img):
    """
    Returns a flattened pose landmark vector (x,y,z normalized)
    """
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = self.pose.process(imgRGB)

    if not results.pose_landmarks:
        return None

    landmarks = []
    for lm in results.pose_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])

    return landmarks
