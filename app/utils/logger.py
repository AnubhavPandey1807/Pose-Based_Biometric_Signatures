import csv
import os
from datetime import datetime

LOG_FILE = "pose_angles.csv"

def log_angle_to_csv(angles):
    """
    angles: iterable of numeric pose angles
    """
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            header = ["timestamp"] + [f"angle_{i}" for i in range(len(angles))]
            writer.writerow(header)

        writer.writerow([datetime.utcnow().isoformat()] + list(angles))
