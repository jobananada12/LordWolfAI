"""
LordWolf AI Studio
Voice AI
"""

from dataclasses import dataclass


@dataclass
class Voice:

    name: str

    gender: str

    language: str

    emotion: str = "Normal"

    speed: float = 1.0

    pitch: float = 1.0


class VoiceAI:
    """
    AI керування голосами.
    """

    def __init__(self):

        self.voices = {}

        self.load_default_voices()

    def load_default_voices(self):

        defaults = [

            Voice(
                "Narrator",
                "Unknown",
                "uk"
            ),

            Voice(
                "Male",
                "Male",
                "uk"
            ),

            Voice(
                "Female",
                "Female",
                "uk"
            ),

            Voice(
                "Old Man",
                "Male",
                "uk"
            ),

            Voice(
                "Young Girl",
                "Female",
                "uk"
            )

        ]

        for voice in defaults:

            self.voices[voice.name] = voice

    def get_voice(self, name):

        return self.voices.get(name)

    def get_all(self):

        return list(self.voices.values())

    def add_voice(self, voice):

        self.voices[voice.name] = voice

    def remove_voice(self, name):

        if name in self.voices:

            del self.voices[name]

    def clear(self):

        self.voices.clear()

        self.load_default_voices()