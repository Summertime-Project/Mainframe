from unittest import TestCase
from camera import Camera
import cv2


class TestCamera(TestCase):
    def test_close(self):
        cap = cv2.VideoCapture(0)
        camera = Camera(cap)

        frame = camera.get_frame()
        camera.release()

        ret, frame = cap.read()
        self.assertFalse(ret)

        self.assertFalse(camera.is_opened())

        frame = camera.get_frame()
        self.assertIsNone(frame)
