from hashlib import sha1

from ursina import Entity, Vec3, color
from ursina.shaders import basic_lighting_shader


class Unit(Entity):
    _types = {}

    def __init__(self, parent, x, y, owner, num):
        super().__init__(
                parent=parent,
                x=x,
                z=-y,
                y=0.25,
                collider='box',
                shader=basic_lighting_shader,
        )
        self.owner = owner
        self.num = num

    def on_mouse_enter(self):
        self.prev_color = self.color
        self.color = color.rgb(1, 0, 0)

    def on_mouse_exit(self):
        self.color = self.prev_color

    @classmethod
    def register(cls, type_id):
        def register_func(type_cls):
            cls._types[type_id] = type_cls
            return type_cls

        return register_func

    @classmethod
    def build(cls, parent, x, y, type_id, owner, num):
        k = cls._types[type_id]
        return k(parent, x, y, owner, num)


class DumbUnit(Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = 'cube'
        self.scale = Vec3(0.8, 0.5, 0.8)
        self.color = '#%06x' % (int(sha1(self.__class__.__name__.encode('utf-8')).hexdigest(), 16) % (256**3))


@Unit.register(1)
class Army(Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = 'FinalBaseMesh'
        self.scale /= 10
        self.texture = 'brick'



@Unit.register(2)
class Caserne(DumbUnit):
    pass


@Unit.register(3)
class CharFactory(DumbUnit):
    pass


@Unit.register(4)
class Char(DumbUnit):
    pass


@Unit.register(5)
class MissLauncher(DumbUnit):
    pass


@Unit.register(6)
class City(DumbUnit):
    pass


@Unit.register(7)
class Capitale(DumbUnit):
    pass


@Unit.register(8)
class ShipYard(DumbUnit):
    pass


@Unit.register(9)
class Boat(DumbUnit):
    pass


@Unit.register(10)
class NuclearSearch(DumbUnit):
    pass


@Unit.register(11)
class NuclearSilo(DumbUnit):
    pass


@Unit.register(12)
class Engineer(DumbUnit):
    pass


@Unit.register(13)
class DefenseTower(DumbUnit):
    pass


@Unit.register(14)
class Tourist(DumbUnit):
    pass


@Unit.register(15)
class Mine(DumbUnit):
    pass


@Unit.register(16)
class Obelisk(DumbUnit):
    pass


@Unit.register(17)
class McDo(DumbUnit):
    pass


@Unit.register(18)
class Tree(DumbUnit):
    pass


@Unit.register(19)
class Megalopole(DumbUnit):
    pass


@Unit.register(22)
class Plane(DumbUnit):
    pass


@Unit.register(23)
class Jouano(DumbUnit):
    pass


@Unit.register(24)
class BarbedWire(DumbUnit):
    pass


@Unit.register(25)
class Airport(DumbUnit):
    pass


@Unit.register(26)
class Radar(DumbUnit):
    pass


@Unit.register(27)
class EiffelTower(DumbUnit):
    pass


@Unit.register(28)
class Boeing(DumbUnit):
    pass


@Unit.register(29)
class Cavern(DumbUnit):
    pass


@Unit.register(30)
class Gulag(DumbUnit):
    pass



