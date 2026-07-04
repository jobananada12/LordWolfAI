"""
LordWolf AI Studio
Voice Engine
"""

from dataclasses import dataclass


@dataclass
class VoiceTrack:

    text: str

    voice: str

    speed: float = 1.0

    pitch: float = 1.0

    file_path: str = ""


class VoiceEngine:
    """
    Рушій озвучення персонажів.
    """

    def __init__(self):

        self.tracks = []

    def add_voice(self, text, voice="Narrator", speed=1.0, pitch=1.0):

        track = VoiceTrack(

            text=text,

            voice=voice,

            speed=speed,

            pitch=pitch

        )

        self.tracks.append(track)

        return track

    def clear(self):

        self.tracks.clear()

    def get_tracks(self):

        return self.tracks

    def total_lines(self):

        return len(self.tracks)