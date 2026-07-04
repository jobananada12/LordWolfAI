"""
LordWolf AI Studio
Animation Engine
"""

from dataclasses import dataclass
from typing import List


@dataclass
class AnimationClip:

    name: str

    duration: float

    loop: bool = False


class AnimationEngine:
    """
    Рушій анімації.
    """

    def __init__(self):

        self.timeline: List[AnimationClip] = []

    def add_clip(self, name, duration, loop=False):

        clip = AnimationClip(

            name=name,

            duration=duration,

            loop=loop

        )

        self.timeline.append(clip)

        return clip

    def remove_clip(self, index):

        if 0 <= index < len(self.timeline):

            del self.timeline[index]

    def clear(self):

        self.timeline.clear()

    def total_duration(self):

        return sum(

            clip.duration

            for clip in self.timeline

        )

    def get_timeline(self):

        return self.timeline