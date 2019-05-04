def cls_init(cls):
    cls.cls_init()

    return cls


class Vector(tuple):
    def __new__(cls, x, y):
        return super().__new__(cls, (x, y))

    def __init__(self, x, y):
        super().__init__()

    def __add__(self, other):
        return Vector(self[0] + other[0],
                      self[1] + other[1])

    def __sub__(self, other):
        return Vector(self[0] - other[0],
                      self[1] - other[1])

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


def load_sprites(files):
    import pygame
    return [pygame.image.load(file) for file in files]
