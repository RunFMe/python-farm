from ui import WindowLayer, Window
from client.garden_tile_collection import GardenTileCollection
from common.constants import GARDEN_X, GARDEN_Y
from client.statusbar import StatusBar
import pygame


class MainWindow(Window):
    def __init__(self, size):
        super().__init__(size)

        # Create base layer
        farm_bg = pygame.image.load('client/images/background.png')
        farm_layer = WindowLayer(self, farm_bg)
        self.append_layer(farm_layer)

        # Create Landing Spot
        garden = GardenTileCollection((GARDEN_X, GARDEN_Y))
        farm_layer.add_child(garden)

        # Create GUI
        gui_layer = WindowLayer(self)
        self.append_layer(gui_layer)

        status_bar = StatusBar((0, 0))
        gui_layer.add_child(status_bar)
