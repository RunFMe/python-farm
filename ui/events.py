from common import Vector


class Event:
    signal = 'empty_event'

    def __init__(self):
        pass


class MouseClickEvent(Event):
    signal = 'on_mouse_click'

    def __init__(self, pos):
        super().__init__()
        self.position = Vector(*pos)

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, new_x):
        self.position = Vector(new_x, self.y)

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, new_y):
        self.position = Vector(self.x, new_y)
