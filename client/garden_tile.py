import logging

from client.plant_dialogue import PlantDialogue
from ui import Widget, MouseClickEvent


class GardenTile(Widget):
    def __init__(self, pos, size, plant_col, plant_row):
        super().__init__(pos, size)
        self.plant_pos = (plant_col, plant_row)

        self.add_callback(MouseClickEvent.signal, self._tile_click)

        logging.debug("Created farm tile {}".format(self.rect))

    def draw(self, surface, parent_abs_pos):
        from client.game import game
        super().draw(surface, parent_abs_pos)

        plant_img = game.farm.get_plant(*self.plant_pos).image
        surface.blit(plant_img, parent_abs_pos + self.position)

    def _tile_click(self, event):
        from client.game import game

        plant = game.farm.get_plant(*self.plant_pos)

        if plant.type == 'empty':
            main_screen = game.active_window
            dialogue = PlantDialogue(self.position, *self.plant_pos)

            main_screen.show_dialogue(dialogue)
        elif plant.ready_to_harvest:
            logging.debug("Harvested plant at {} {}".format(*self.plant_pos))

            game.farm.harvest_plant(*self.plant_pos)
