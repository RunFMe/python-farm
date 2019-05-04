import logging

from common.constants import *
from common.plants import Plant, PlantManager
from ui import Dialogue, WindowLayer, Container, ImageButton, MouseClickEvent


class PlantDialogue(Dialogue):
    def __init__(self, position, col, row):
        logging.debug("Creating Plant Dialogue")
        super().__init__((WINDOW_W, WINDOW_H))
        self.row = row
        self.col = col

        main_layer = WindowLayer(self)
        self.append_layer(main_layer)

        main_container = Container(position + (GARDEN_X, GARDEN_Y),
                                   (PLANT_DIALOGUE_W, PLANT_DIALOGUE_H),
                                   PLANT_DIALOGUE_COLOR)
        main_layer.add_child(main_container)

        cabbage_button = ImageButton(PlantManager.get_sprites('cabbage')[-1],
                                     main_container.position)
        cabbage_button.add_callback(MouseClickEvent.signal, self._click_plant,
                                    'cabbage')
        main_layer.add_child(cabbage_button)

    def _click_plant(self, event, data):
        from client.game import game
        game.farm.plant(self.col, self.row, data)
        self._active = False

        logging.debug("A new plant {} was planted at {} {}"
                      .format(data, self.row, self.col))
