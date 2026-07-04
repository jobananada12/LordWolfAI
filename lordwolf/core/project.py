"""
Project Manager
"""


class Project:

    def __init__(self):

        self.name = "Untitled"

        self.author = ""

        self.script = ""

        self.characters = []

        self.backgrounds = []

        self.scenes = []

    def new(self):

        self.name = "New Project"

        self.script = ""

        self.characters.clear()

        self.backgrounds.clear()

        self.scenes.clear()