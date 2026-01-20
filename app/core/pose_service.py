import numpy as np
import cv2


def detect_pose_signature(frames):
    """
    frames: list[UploadFile]
    returns: np.ndarray shape (T, D)
    """

    # Lazy imports (correct)
    from pose_detector import PoseDetector
    from app.core.pose_signature import extract_signature

    detector = PoseDetector()
    signatures = []

    for file in frames:
        # 1. Read raw bytes from UploadFile
        img_bytes = file.file.read()

        # 2. Convert bytes → numpy buffer
        np_img = np.frombuffer(img_bytes, np.uint8)

        # 3. Decode → OpenCV image
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            continue  # skip invalid frames

        # 4. Pose detection
        detector.findPose(img, draw=False)
        lm = detector.findPosition(img, draw=False)

        # MediaPipe pose has 33 landmarks
        if len(lm) < 17:
            continue

        # 5. Extract pose signature
        signature = extract_signature(lm)
        signatures.append(signature)

    if not signatures:
        raise ValueError("No valid pose detected")

    return np.array(signatures)


def check_liveness(signatures):
    """
    signatures: shape (T, D)
    """

    if signatures.shape[0] < 2:
        return False

    # Overall movement (start vs end)
    total_motion = np.linalg.norm(
        signatures[-1] - signatures[0]
    )

    # Temporal variation across frames
    temporal_variance = np.mean(
        np.std(signatures, axis=0)
    )

    return (
        total_motion > 0.05
        and temporal_variance > 0.002
    )
