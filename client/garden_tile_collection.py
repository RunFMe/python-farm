from ui import Container
from client.garden_tile import GardenTile
from common.constants import TILE_PADDING, TILE_SIZE, TILE_NUM
import logging


class GardenTileCollection(Container):
    def __init__(self, pos):
        from client.game import game
        super().__init__(pos, self._get_size())
        self.tiles = [[self._get_child_farm_tile(i, j)
                       for i in range(game.farm.field_size)]
                      for j in range(game.farm.field_size)]

        logging.debug("Created Farm Tile Collection {}".format(self.rect))

    def get_tile(self, col, row):
        return self.tiles[col][row]

    def _get_child_farm_tile(self, col, row):
        garden_tile = GardenTile(GardenTileCollection._get_tile_pos(col, row),
                                (TILE_SIZE, TILE_SIZE),
                                col, row)
        self.add_child(garden_tile)

        return garden_tile

    @staticmethod
    def _get_tile_pos(col, row):
        return ((TILE_SIZE + TILE_PADDING) * col,
                (TILE_SIZE + TILE_PADDING) * row)

    @staticmethod
    def _get_size():
        size = (TILE_SIZE + TILE_PADDING) * TILE_NUM - TILE_PADDING
        return size, size
