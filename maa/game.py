from ursina import DirectionalLight, Vec3, camera, Sky

from .camera import Camera
from .map import Map

class Game:
    def __init__(self):
        self.map = Map()

    def load(self, map_filename):
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
