"""
LordWolf AI Studio
Project Manager
"""

from pathlib import Path
import json


class ProjectManager:
    """
    Керує проєктами LordWolf AI Studio.
    """

    def __init__(self):

        self.current_project = None

        self.project_data = {}

    def new_project(self, name):

        self.current_project = name

        self.project_data = {

            "name": name,

            "script": "",

            "characters": [],

            "backgrounds": [],

            "scenes": [],

            "music": [],

            "sounds": []
        }

        return self.project_data

    def save_project(self, filename):

        if self.project_data is None:
            return False

        path = Path(filename)

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                self.project_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        return True

    def load_project(self, filename):

        path = Path(filename)

        with open(path, "r", encoding="utf-8") as file:

            self.project_data = json.load(file)

        self.current_project = self.project_data.get("name")

        return self.project_data

    def get_project(self):

        return self.project_data

    def set_script(self, script):

        self.project_data["script"] = script

    def get_script(self):

        return self.project_data.get("script", "")

    def clear(self):

        self.current_project = None

        self.project_data = {}