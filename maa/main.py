import sys
from pathlib import Path

from ursina import Ursina, Sky, Vec3, DirectionalLight, camera, application, texture_importer

from .camera import Camera
from .map import Map


# Mokey patching to be able to find assets in several kind of directories
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
        self.map = Map()

    @classmethod
    def run(cls):
        return cls().main()

    def main(self):
        if len(sys.argv) < 2:
            print(f'Syntax: {sys.argv[0]} MAP_FILENAME', file=sys.stderr)
            return 1

        map_filename = sys.argv[1]

        self.app = Ursina(title='Men are Ants')
        self.camera = Camera(rotation_smoothing=0, enabled=1, rotation=(30,30,0))

        sun = DirectionalLight()
        sun.look_at(Vec3(-1,-1,-1))

        self.sky = Sky()

        DirectionalLight(y=2, z=3, rotation=(45, -45, 45))

        with open(map_filename, 'r') as fp:
            self.map.load(fp)

        self.camera.position = (self.map.width/2, 0, -self.map.height/2)
        #self.camera.target_fov = 10
        #self.camera.set_orthographic(True)
        #camera.z = -200
        #camera.fov = 10
        #self.camera.target_fov = 10
        camera.z = -50
        self.camera.target_z = -50
        self.camera.rotate_around_mouse_hit = False

        print('coucou')

        self.app.run()
