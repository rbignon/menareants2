import sys
import re
from hashlib import sha1

from ursina import Ursina, Sky, Entity, EditorCamera, Mesh, Vec2, Vec3, color, DirectionalLight
from ursina.shaders import basic_lighting_shader

from .camera import Camera
from .map import Map


class Main:
    def __init__(self):
        self.app = Ursina()
        sun = DirectionalLight()
        sun.look_at(Vec3(-1,-1,-1))

        self.sky = Sky()

        DirectionalLight(y=2, z=3, rotation=(45, -45, 45))
        #sun = DirectionalLight(y=-50, rotation_x=120)
        #sun = DirectionalLight(y=-50, rotation_x=90)
        #sun._light.get_lens().set_near_far(0,30)
        #sun._light.show_frustum()

        self.camera = Camera(rotation_smoothing=0, enabled=1, rotation=(30,30,0))
        self.map = Map()

    @classmethod
    def run(cls):
        return cls().main()

    def main(self):
        filename = sys.argv[1]

        with open(filename, 'r') as fp:
            self.map.load(fp)

        #hit_plane = Entity(model='plane', collider='box', scale=100, alpha=.2, visible=False)
        #centering_offset = Vec2(-.5, -.5)

        #self.camera.position = (len(self.map[0]), -len(self.map), -20)
        #camera.z = -60
        self.camera.position = (self.map.width/2, 0, -self.map.height/2)
        #self.camera.target_fov = 10
        from ursina import camera
        #self.camera.set_orthographic(True)
        #camera.z = -200
        #camera.fov = 10
        #self.camera.target_fov = 10
        camera.z = -50
        self.camera.target_z = -50
        self.camera.rotate_around_mouse_hit = False

        #terrain = Entity(model=Mesh(vertices=[], triangles=[], uvs=[], colors=[]), scale=(w,1,h), y=-.01, collider='box')
        #terrain.scale *= 5

        #i = 0
        #for z in range(h):
        #    for x in range(w):
        #        terrain.model.vertices.append(Vec3((x/min_dim)+(centering_offset.x), 0, (z/min_dim)+centering_offset.y))
        #        terrain.model.uvs.append((x/w, z/h))

        #        if x > 0 and z > 0:
        #            terrain.model.triangles.append((i, i-1, i-w-1, i-w-0))

        #        i += 1

        #terrain.model.generate()
        print('coucou')

        self.app.run()
