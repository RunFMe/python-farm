import pygame
import time
from threading import Lock
import logging
from client.sio import sio

from common.plants import Plant
from common.constants import FIELD_SIZE


class Farm:
    def __init__(self, field_size=FIELD_SIZE):
        logging.info("Created Farm instance")
        self.field_size = field_size
        self.field = [[Plant() for _ in range(field_size)] for _ in
                      range(field_size)]
        self.money = 0
        self.lock = Lock()

    def init_state(self, info):
        self._set_money(info['money'])
        for i, plant_info in enumerate(info['field']):
            col, row = i % self.field_size, i // self.field_size
            plant_info = tuple(plant_info)
            self.set_plant(col, row, plant_info)

    def _set_money(self, money):
        logging.info("New money value is {}".format(money))
        with self.lock:
            self.money = money

    def set_plant(self, col, row, plant_info):
        logging.info("New plant at {} {} is {}".format(col, row, plant_info))
        with self.lock:
            self.field[row][col] = Plant(plant_info)

    def get_plant(self, col, row):
        return self.field[row][col]

    def harvest_plant(self, col, row):
        plant = self.get_plant(col, row)
        self._set_money(self.money + plant.cost)
        self._set_fake_plant(col, row, Plant())

        sio.emit('harvest', (col, row))

    def get_money(self):
        return self.money

    def _set_fake_plant(self, col, row, plant):
        with self.lock:
            self.field[row][col] = plant

    def plant(self, col, row, plant_type):
        fake_plant = Plant((plant_type, time.time()))
        self._set_fake_plant(col, row, fake_plant)

        sio.emit('plant', (col, row, plant_type))
