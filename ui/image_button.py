import logging

import pygame

from ui import Widget


class ImageButton(Widget):
    def __init__(self, image, position, size=None, margin_x=4, margin_y=0):
        if isinstance(image, str):
            image = pygame.image.load(image)
        if size is not None:
            image = pygame.transform.scale(image, size)

        self.image = image
        self.margin_x = margin_x
        self.margin_y = margin_y

        size = self._calculate_size()
        super().__init__(position, size)

        logging.debug(
            "Created Image Button at {}".format(self.rect))

    def _calculate_size(self):
        rect = self.image.get_rect()
        return rect.width + 2 * self.margin_x, rect.height + 2 * self.margin_y

    def draw(self, surface, parent_abs_pos):
        super().draw(surface, parent_abs_pos)

        surface.blit(self.image, (parent_abs_pos[0] + self.x + self.margin_x,
                                  parent_abs_pos[1] + self.y + self.margin_y))
