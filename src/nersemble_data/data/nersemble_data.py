from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

import numpy as np
from dreifus.camera import CameraCoordinateConvention, PoseType
from dreifus.matrix import Pose, Intrinsics
from elias.config import Config
from elias.util import load_json

from nersemble_data.constants import ASSETS
from nersemble_data.util.video import VideoFrameLoader


@dataclass
class CameraParams(Config):
    world_2_cam: Dict[str, Pose]
    intrinsics: Intrinsics


class NeRSembleParticipantDataManager:
    def __init__(self, nersemble_folder: str, participant_id: int):
        self._location = nersemble_folder
        self._participant_id = participant_id

    # ----------------------------------------------------------
    # Assets
    # ----------------------------------------------------------

    def load_camera_calibration(self) -> CameraParams:
        camera_params = load_json(self.get_camera_calibration_path())
        world_2_cam = camera_params['world_2_cam']
        world_2_cam = {serial: Pose(pose, camera_coordinate_convention=CameraCoordinateConvention.OPEN_CV, pose_type=PoseType.WORLD_2_CAM)
                       for serial, pose in world_2_cam.items()}
        intrinsics = Intrinsics(camera_params['intrinsics'])
        camera_params = CameraParams(world_2_cam, intrinsics)
        return camera_params

    def list_timesteps(self, sequence_name: str) -> List[int]:
        return list(range(self.get_n_timesteps(sequence_name)))

    def list_cameras(self, sequence_name: str) -> List[str]:
        # TODO: Untested
        images_folder = Path(self.get_images_path(sequence_name, "serial")).parent
        serials = [camera_file.name.split('_')[1] for camera_file in images_folder.iterdir()]
        return serials

    def get_n_timesteps(self, sequence_name: str) -> int:
        serials = self.list_cameras(sequence_name)
        serial = serials[0]
        video_capture = VideoFrameLoader(self.get_images_path(sequence_name, serial))
        n_frames = video_capture.get_n_frames()
        return n_frames

    def load_image(self, sequence_name: str, serial: str, timestep: int, as_uint8: bool = False) -> np.ndarray:
        # TODO: Add apply color calibration
        video_capture = VideoFrameLoader(self.get_images_path(sequence_name, serial))
        image = video_capture.load_frame(timestep)

        if not as_uint8:
            image = image / 255.

        return image

    # ----------------------------------------------------------
    # Paths
    # ----------------------------------------------------------

    def get_camera_calibration_path(self) -> str:
        relative_path = ASSETS['nvs']['global']['calibration'].format(p_id=self._participant_id)
        return f"{self._location}/{relative_path}"

    def get_images_path(self, sequence_name: str, serial: str) -> str:
        relative_path = ASSETS['nvs']['per_cam']['images'].format(p_id=self._participant_id, seq_name=sequence_name, serial=serial)
        return f"{self._location}/{relative_path}"
