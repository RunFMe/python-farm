from sqlalchemy.ext.mutable import MutableList
from flask_sqlalchemy import SQLAlchemy
from common.constants import TILE_NUM
from common.plants import Plant

db = SQLAlchemy()


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm.db'
    db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    money = db.Column(db.Integer, default=True, nullable=False)
    field = db.Column(MutableList.as_mutable(db.PickleType))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'field' not in kwargs:
            self.field = [Plant().info] * (TILE_NUM ** 2)

    def get_plant(self, col, row):
        if row >= TILE_NUM or col >= TILE_NUM:
            raise AttributeError("Plant {} {} doesn't exist"
                                 .format(col, row))
        return Plant(self.field[row * TILE_NUM + col])

    def set_plant(self, col, row, plant: Plant):
        if row >= TILE_NUM or col >= TILE_NUM:
            raise AttributeError("Plant {} {} doesn't exist"
                                 .format(col, row))
        self.field[row * TILE_NUM + col] = plant.info

    def get_snapshot(self):
        return {'money': self.money,
                'field': self.field}

    def __repr__(self):
        return "<User {} with field {} and money {}>".format(self.username,
                                                             self.field,
                                                             self.money)
