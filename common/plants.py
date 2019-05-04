from common.utils import cls_init, load_sprites
import time
import logging
import json


class PlantManager:
    _plants = {}
    empty_info = ('empty', 0.0)

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("Plant Manager is static class")

    @classmethod
    def register(cls, plant_type, stage_duration, cost, sprites=None):
        if plant_type in cls._plants:
            raise AttributeError("Plant {} is registered"
                                 .format(plant_type))

        if sprites is None:
            sprites = []
        cls._plants[plant_type] = {'duration': stage_duration,
                                   'sprites': sprites,
                                   'cost': cost}

    @classmethod
    def get_description(cls, plant_type):
        cls._check_type_or_throw(plant_type)
        return cls._plants[plant_type]

    @classmethod
    def get_sprites(cls, plant_type):
        cls._check_type_or_throw(plant_type)
        return cls._plants[plant_type]['sprites']

    @classmethod
    def get_cost(cls, plant_type):
        cls._check_type_or_throw(plant_type)
        return cls._plants[plant_type]['cost']

    @classmethod
    def get_duration(cls, plant_type):
        cls._check_type_or_throw(plant_type)
        return cls._plants[plant_type]['duration']

    @classmethod
    def get_num_stages(cls, plant_type):
        return len(cls.get_sprites(plant_type))

    @classmethod
    def _check_type_or_throw(cls, plant_type):
        if not cls.has_type(plant_type):
            raise AttributeError("Plant {} is not registered"
                                 .format(plant_type))

    @classmethod
    def has_type(cls, plant_type):
        return plant_type in cls._plants

    @classmethod
    def check_info(cls, info):
        return (isinstance(info, tuple) and len(info) == 2 and
                info[0] in PlantManager._plants and
                (isinstance(info[1], float) or isinstance(info[1], int)))

    @classmethod
    def load_config(cls, filename, with_sprites=False):
        with open(filename) as f:
            data = json.load(f)

        for plant_data in data:
            if with_sprites:
                sprites = load_sprites(plant_data['sprites'])
            else:
                sprites = None

            cls.register(plant_data['type'], plant_data['duration'],
                         plant_data['cost'], sprites)

        # check that empty plant was in config to avoid further bugs
        if not cls.has_type('empty'):
            raise RuntimeError("Empty plant was not registered")


class Plant:
    def __init__(self, info=None):
        if info is None:
            info = PlantManager.empty_info

        if not PlantManager.check_info(info):
            raise AttributeError(
                "Plant info must be tuple(existing_plant_type, plant_time)"
                "and it is {}".format(info))
        self.info = info

    @property
    def type(self):
        return self.info[0]

    @property
    def plant_time(self):
        return self.info[1]

    @property
    def cost(self):
        return PlantManager.get_cost(self.type)

    @property
    def num_stages(self):
        return PlantManager.get_num_stages(self.type)

    @property
    def duration(self):
        return PlantManager.get_duration(self.type)

    @property
    def stage(self):
        delta_time = time.time() - self.plant_time
        return min(int(delta_time // self.duration), self.num_stages - 1)

    @property
    def image(self):
        return PlantManager.get_sprites(self.type)[self.stage]

    @property
    def ready_to_harvest(self):
        ready = (self.stage == self.num_stages - 1)
        logging.debug(
            "Ready to harvest" if ready else "Plant is not ready to harvest")
        return ready

    def __repr__(self):
        return ('<Plant {} with plant_time {}>'
                .format(self.type, self.plant_time))
