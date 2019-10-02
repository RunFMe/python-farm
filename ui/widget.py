import logging
from typing import Callable

import pygame

from common import Vector
from ui import Event


class Widget:
    def __init__(self, position, size, background=None):
        self.rect = pygame.Rect(position, size)
        self.modified = False
        self.background = None
        self.callbacks = {}

        # Load image if background is str before all checks on background
        if isinstance(background, str):
            background = pygame.image.load(background)

        # check different types of background
        if isinstance(background, pygame.Surface):
            self.background = pygame.transform.scale(background,
                                                     self.size).convert_alpha()
        elif isinstance(background, tuple):
            self.background = pygame.Surface(self.size)
            self.background.fill(background)
            self.background = self.background.convert_alpha()
        elif background is not None:
            raise AttributeError("Type of background {} is not available"
                                 .format(type(background)))

    def draw(self, surface, parent_abs_pos):
        if self.background is not None:
            surface.blit(self.background, parent_abs_pos + self.position)

    def mark_modified(self, modified=True):
        self.modified = modified

    def has_widget_at(self, pos):
        return self.rect.collidepoint(*pos)

    @property
    def position(self):
        return Vector(self.rect.x, self.rect.y)

    @position.setter
    def position(self, new_pos):
        self.rect = pygame.Rect(new_pos, (self.rect.width, self.rect.height))

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, new_x):
        self.rect = pygame.Rect((new_x, self.rect.y),
                                (self.rect.width, self.rect.height))

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, new_y):
        self.rect = pygame.Rect((self.rect.x, new_y),
                                (self.rect.width, self.rect.height))

    @property
    def size(self):
        return self.rect.width, self.rect.height

    @size.setter
    def size(self, new_size):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, *new_size)

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, new_width):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, new_width,
                                self.rect.height)

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, new_height):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,
                                new_height)

    def add_callback(self, signal, func: Callable, data=None):
        if signal not in self.callbacks:
            self.callbacks[signal] = []

        self.callbacks[signal].append((func, data))

    def emit_event(self, event: Event):
        logging.debug('Received signal {}'.format(event.signal))

        if event.signal in self.callbacks:
            for callback, data in self.callbacks[event.signal]:
                if data is None:
                    callback(event)
                else:
                    callback(event, data)
