"""
LordWolf AI Studio
Video Engine
"""

from dataclasses import dataclass
from typing import List


@dataclass
class VideoFrame:

    image_path: str

    duration: float = 1.0

    audio_path: str = ""

    animation: str = ""


class VideoEngine:
    """
    Рушій фінального відео-рендеру.
    """

    def __init__(self):

        self.frames: List[VideoFrame] = []

    def add_frame(self, image_path, duration=1.0, audio_path="", animation=""):

        frame = VideoFrame(

            image_path=image_path,

            duration=duration,

            audio_path=audio_path,

            animation=animation

        )

        self.frames.append(frame)

        return frame

    def clear(self):

        self.frames.clear()

    def total_duration(self):

        return sum(frame.duration for frame in self.frames)

    def get_frames(self):

        return self.frames

    def build_video_plan(self):

        """
        Поки що не рендерить MP4.
        Але створює повний план відео.
        """

        return {

            "total_frames": len(self.frames),

            "total_duration": self.total_duration(),

            "frames": [

                {

                    "image": f.image_path,

                    "audio": f.audio_path,

                    "animation": f.animation,

                    "duration": f.duration

                }

                for f in self.frames

            ]

        }