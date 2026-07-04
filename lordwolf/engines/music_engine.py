"""
LordWolf AI Studio
Music Engine
"""

from dataclasses import dataclass


@dataclass
class MusicTrack:

    name: str

    mood: str

    duration: float = 0.0

    file_path: str = ""


class MusicEngine:
    """
    Рушій музики та емоційних треків.
    """

    def __init__(self):

        self.tracks = []

    def add_track(self, name, mood="neutral", duration=0.0):

        track = MusicTrack(

            name=name,

            mood=mood,

            duration=duration

        )

        self.tracks.append(track)

        return track

    def get_tracks(self):

        return self.tracks

    def clear(self):

        self.tracks.clear()

    def total_duration(self):

        return sum(track.duration for track in self.tracks)

    def find_by_mood(self, mood):

        return [

            track

            for track in self.tracks

            if track.mood == mood

        ]