import pygame

from common import Vector
from ui import Container, MouseClickEvent
import logging


class WindowLayer(Container):
    def __init__(self, parent_window, background=None):
        super().__init__((0, 0), parent_window.size, background, False)


class Window:
    def __init__(self, size):
        self.layers = []
        self.size = size
        self.running = True
        self._dialogue = None

    def draw(self, surface):
        for layer in self.layers:
            layer.draw(surface, Vector(0, 0))

        if self.has_dialogue():
            self._dialogue.draw(surface)

    def accept_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT or (
                self._dialogue is not None and not self._dialogue.running):
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = MouseClickEvent(pygame.mouse.get_pos())

            if self.has_dialogue():
                if self._dialogue.catches_click_at(mouse_click.position):
                    self._dialogue.accept_event(event)
                else:
                    self._dialogue = None
            else:
                for layer in self.layers:
                    if layer.has_widget_at(mouse_click.position):
                        layer.emit_event(mouse_click)
                        break

    def has_dialogue(self):
        self._check_dialogue_active()
        return self._dialogue is not None

    def _check_dialogue_active(self):
        if self._dialogue is not None and not self._dialogue.is_active():
            logging.debug("Exiting Dialogue")
            self._dialogue = None

    def accept_events(self, events):
        for event in events:
            self.accept_event(event)

    def append_layer(self, new_layer):
        self.layers.append(new_layer)

    def show_dialogue(self, dialogue_window):
        logging.debug("Adding dialogue to a screen")
        self._dialogue = dialogue_window
