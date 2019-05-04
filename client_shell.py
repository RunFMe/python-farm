import eventlet

from client.game import game
from common.plants import PlantManager

if __name__ == '__main__':
    game.run()

# from ui import Container, Button
# from ui import MouseClickEvent
# pygame.init()
# screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
# pygame.display.set_caption("PyFarmGame " + "v. " )
#
# container = Container((0, 0), (100, 100), (0, 100, 100))
#
# b = Button('lol', (0, 0))
# b.add_callback(MouseClickEvent.signal, print)
# container.add_child(b)
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             e = MouseClickEvent(pygame.mouse.get_pos())
#
#             container._call_callback(e)
#
#     container.draw(screen)
#     pygame.display.flip()
