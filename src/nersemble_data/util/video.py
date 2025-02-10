import cv2
import numpy as np


class VideoFrameLoader:

    def __init__(self, video_path: str):
        self._video_capture = cv2.VideoCapture(video_path)

    def get_n_frames(self) -> int:
        n_frames = int(self._video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        return n_frames

    def load_frame(self, frame_id: int) -> np.ndarray:
        # set frame position
        self._video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        success, image = self._video_capture.read()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image
