from ui import Label


class StatusBar(Label):
    def __init__(self, position):
        from client.game import game
        super().__init__('', position)
        self.money = None

        self.set_money(game.farm.get_money())

    def set_money(self, new_amount):
        self.money = new_amount
        self.set_text("Money: {}".format(self.money))

    def draw(self, surface, parent_abs_pos):
        from client.game import game
        if self.money != game.farm.get_money():
            self.set_money(game.farm.get_money())

        super().draw(surface, parent_abs_pos)
