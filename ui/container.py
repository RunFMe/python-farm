from ui import Widget
from ui import MouseClickEvent
import logging
import pygame


class Container(Widget):
    def __init__(self, position, size, background=None, catch_click=True):
        super().__init__(position, size, background)
        self.catch_click = catch_click
        self.children = []

        self.add_callback(MouseClickEvent.signal, self._click_child)

    def _click_child(self, event: MouseClickEvent):
        for child in self.children:
            if child.rect.collidepoint(event.position):
                logging.debug('Pass click event {} to a child with {}'
                              .format(event.position, child.rect))

                child_click = MouseClickEvent(event.position - child.position)
                child.emit_event(child_click)

    def add_child(self, child: Widget):
        self.children.append(child)

    def draw(self, surface, parent_abs_pos):
        super().draw(surface, parent_abs_pos)
        container_abs_pos = parent_abs_pos + self.position

        for child in self.children:
            child.draw(surface, container_abs_pos)

    def has_widget_at(self, pos):
        if not self.rect.collidepoint(*pos):
            return False
        elif self.catch_click:
            return True
        else:
            for child in self.children:
                if child.has_widget_at(pos - self.position):
                    return True

        return False
