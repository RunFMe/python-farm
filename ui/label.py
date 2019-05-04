import pygame
from ui import Widget
import logging


class Label(Widget):
    def __init__(self, label, position, background=None, font_size=12,
                 color=(255, 255, 0), margin_x=4, margin_y=0):
        self.label = label
        self.color = color
        self.font_size = font_size
        self.label_font = pygame.font.Font("client/dejavusansmono.ttf",
                                           self.font_size)
        self.margin_x = margin_x
        self.margin_y = margin_y
        self._text_img = None

        size = self._calculate_size(self._render_text())
        super().__init__(position, size, background)

        logging.debug(
            "Created Label at {} with text {}".format(self.rect, self.label))

    def _render_text(self):
        if self._text_img is None or self.modified:
            self._text_img = self.label_font.render(self.label, 0, self.color)
        return self._text_img.convert_alpha()

    def _calculate_size(self, image: pygame.Surface):
        rect = image.get_rect()
        return rect.width + 2 * self.margin_x, rect.height + 2 * self.margin_y

    def draw(self, surface, parent_abs_pos):
        super().draw(surface, parent_abs_pos)

        text = self._render_text()
        surface.blit(text, (parent_abs_pos[0] + self.x + self.margin_x,
                            parent_abs_pos[1] + self.y + self.margin_y))

    def set_text(self, text):
        self.mark_modified()
        self.label = text
        self.size = self._calculate_size(self._render_text())

        logging.debug(
            "Changed text and resized label. New text {}, new size {}".format(
                text, self.size))

    def get_text(self):
        return self.label
