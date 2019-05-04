import pygame
import logging

from common.constants import WINDOW_H, WINDOW_W
from client.login_window import LoginWindow
from client.farm import Farm
from common.plants import PlantManager
from client.sio import run_sockets


class Game:
    def __init__(self):
        logging.basicConfig(level='DEBUG')
        pygame.init()
        pygame.display.set_caption("PyFarmGame " + "v. ")
        PlantManager.load_config('common/plants_config.json', True)
        logging.info("Loaded configs for game")

        self.farm = Farm()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H),
                                              pygame.DOUBLEBUF)
        self.timer = pygame.time.Clock()
        self.active_window = LoginWindow((WINDOW_W, WINDOW_H))
        logging.info("Created Game instance")

        run_sockets()
        logging.info("Set socket listener")

    def run(self):
        while self.active_window.running:
            events = pygame.event.get()
            self.active_window.accept_events(events)
            self.active_window.draw(self.screen)

            pygame.display.flip()

    def shutdown(self):
        self.active_window.running = False

    def set_active_screen(self, new_window):
        self.active_window = new_window


game = Game()
