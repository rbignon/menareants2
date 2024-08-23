import re

from ursina import Entity

from .units import Unit


__all__ = ['Tile', 'Map']


class Tile(Entity):
    textures = {}

    _types = {}

    def __init__(self, x: int, y: int, texture_id: str):
        super().__init__(
                    model='plane',
                    scale=(1, 1, 1),
                    x=x,
                    z=-y,
                    y=0,
                    collider='box',
                    texture=self.textures[texture_id]
        )

    @classmethod
    def register(cls, type_id: str):
        def register_func(type_cls):
            cls._types[type_id] = type_cls
            return type_cls

        return register_func

    @classmethod
    def build(cls, x, y, type_id: str, texture_id: str):
        k = cls._types[type_id]
        return k(x, y, texture_id)


@Tile.register('m')
class Sea(Tile):
    textures =  {
        'm': 'mer.png',
        'a': 'bordsud.png',
        'b': 'bordnord.png',
        'c': 'bordest.png',
        'd': 'bordouest.png',
        'e': 'bordse.png',
        'f': 'bordso.png',
        'g': 'bordno.png',
        'h': 'bordne.png',
        'i': 'coinne.png',
        'j': 'coinno.png',
        'k': 'coinse.png',
        'l': 'coinso.png',
    }


@Tile.register('t')
class Ground(Tile):
    textures = {
        't': 'terre.png',
    }


@Tile.register('p')
class Bridge(Tile):
    textures = {
        'n': 'ponthorizontal.png',
        'o': 'pontvertical.png',
        'p': 'pontgauche.png',
        'q': 'pontdroite.png',
        'r': 'ponthaut.png',
        's': 'pontbas.png',
    }


@Tile.register('M')
class Montain(Tile):
    textures = {
        'M': 'montagne.png'
    }



class Map(Entity):
    def __init__(self):
        self.map = []
        self.units = []

    def load(self, fp):
        is_map = False

        for line in fp.readlines():
            line = line.strip()

            if line == '' or line.startswith('#'):
                continue

            if line == 'MAP':
                is_map = True
            elif line == 'EOM':
                is_map = False
            elif is_map:
                x = []
                for i in range(len(line)//5):
                    x.append(Tile.build(len(x), len(self.map), line[i*5], line[i*5+4]))
                self.map.append(x)
            elif line.startswith('UNIT'):
                t, o, x, y, n = re.match(r'UNIT (\d+) ([\w\*]) (\d+),(\d+) (\d+)', line).groups()
                self.units.append(Unit.build(self, int(x), int(y), int(t), o, n))

    @property
    def width(self):
        return len(self.map[0])

    @property
    def height(self):
        return len(self.map)
