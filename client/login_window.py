from ui import Button, MouseClickEvent, Window, WindowLayer
from client.main_window import MainWindow
from client.sio import sio


class LoginWindow(Window):
    def __init__(self, size):
        super().__init__(size)

        main_layer = WindowLayer(self)
        start_button = Button('Start Game', main_layer.rect.center)
        start_button.add_callback(MouseClickEvent.signal, self._start_game)
        main_layer.add_child(start_button)

        self.append_layer(main_layer)

    def _start_game(self, event):
        from client.game import game
        sio.emit('login', 'kke')
        main_window = MainWindow(self.size)
        game.set_active_screen(main_window)
