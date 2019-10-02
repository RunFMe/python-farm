from ui import Window


class Dialogue(Window):
    def __init__(self, size):
        super().__init__(size)
        self._active = True

    def is_active(self):
        return self._active

    def catches_click_at(self, position):
        for layer in self.layers:
            if layer.has_widget_at(position):
                return True

        return False
