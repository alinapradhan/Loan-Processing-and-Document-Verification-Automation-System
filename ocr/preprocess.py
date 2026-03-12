import cv2
import numpy as np


def preprocess_image(file_bytes: bytes):
    np_data = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    _, thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresholded
