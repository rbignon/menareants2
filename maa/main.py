import sys
from pathlib import Path

from ursina import Ursina, camera, application, texture_importer

from .menu import MainMenu


__all__ = ['Main']


# Monkey patching to be able to find assets in several kind of directories
potential_assets_folders = [
    Path(__file__).parent.parent / 'assets',
    Path(sys.prefix) / 'share' / 'menareants' / 'assets',
    Path(sys.prefix) / 'local' / 'share' / 'menareants' / 'assets',
]

for asset_folder in potential_assets_folders:
    if asset_folder.exists():
        application.asset_folder = asset_folder

        application.scenes_folder = asset_folder / 'scenes/'
        application.scripts_folder = asset_folder / 'scripts/'
        application.fonts_folder = asset_folder / 'fonts/'

        application.compressed_textures_folder = asset_folder / 'textures_compressed/'
        application.compressed_models_folder = asset_folder / 'models_compressed/'
        application._model_path.append_path(str(application.asset_folder.resolve()))
        texture_importer.folders.append(asset_folder)
        break
else:
    print('Unable to find assets', file=sys.stderr)
    sys.exit(1)


class Main:
    def __init__(self):
        pass

    @classmethod
    def run(cls):
        return cls().main()

    def main(self):
        self.app = Ursina(title='Men are Ants')
        self.menu = MainMenu()
        self.menu.open()

        self.app.run()
