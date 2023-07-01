from typing import Optional

import cv2
import numpy as np


class Camera:
    def __init__(self, connection: cv2.VideoCapture):
        self.connection = connection

    def get_frame(self) -> Optional[np.ndarray]:
        ret, frame = self.connection.read()
        return frame if ret else None

    def release(self) -> None:
        self.connection.release()

    def is_opened(self) -> bool:
        return self.connection.isOpened()
