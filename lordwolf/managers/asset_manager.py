"""
LordWolf AI Studio
Asset Manager
"""

from pathlib import Path


class AssetManager:
    """
    Керує всіма ресурсами проєкту.
    """

    def __init__(self):

        self.assets = {
            "characters": [],
            "backgrounds": [],
            "props": [],
            "music": [],
            "sounds": [],
            "fonts": [],
            "icons": []
        }

    def add_asset(self, category, asset):

        if category not in self.assets:
            self.assets[category] = []

        self.assets[category].append(asset)

    def remove_asset(self, category, asset):

        if category not in self.assets:
            return

        if asset in self.assets[category]:
            self.assets[category].remove(asset)

    def get_assets(self, category):

        return self.assets.get(category, [])

    def clear_category(self, category):

        if category in self.assets:
            self.assets[category].clear()

    def clear(self):

        for category in self.assets:
            self.assets[category].clear()

    def asset_exists(self, category, asset):

        return asset in self.assets.get(category, [])

    def import_asset(self, category, filepath):

        path = Path(filepath)

        if not path.exists():
            return False

        self.add_asset(category, str(path))

        return True

    def get_summary(self):

        return {
            category: len(items)
            for category, items in self.assets.items()
        }