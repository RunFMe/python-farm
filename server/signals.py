from flask_socketio import send, emit
from server.models import User
import logging
from flask_socketio import SocketIO, join_room
from server.models import db
from flask import g, request, session
from common.plants import Plant
import time

socketio = SocketIO()


def init_app(app):
    app.config['SECRET_KEY'] = 'secret!'
    socketio.init_app(app)


@socketio.on('connect')
def connection_handler():
    logging.info('User connected to server')


@socketio.on('disconnect')
def disconnection_handler():
    logging.info('User disconnected')


@socketio.on('login')
def auth(username):
    u = User.query.filter_by(username=username).one()

    if u is None:
        emit('auth_failed')
    else:
        session['user'] = u
        join_room(username)

        emit('auth_success', u.get_snapshot())


@socketio.on('harvest')
def harvest_handler(col, row):
    user = session['user']
    cur_plant = user.get_plant(col, row)
    user.money = user.money + cur_plant.cost

    new_plant = Plant()
    user.set_plant(col, row, new_plant)

    db.session.add(user)
    db.session.commit()

    emit('set_plant',
         {'position': (col, row),
          'new_plant': new_plant.info},
         room=user.username)


@socketio.on('plant')
def plant_handler(col, row, plant_type):
    user = session['user']
    if user.get_plant(col, row).type != 'empty':
        pass

    new_plant = Plant((plant_type, time.time()))
    user.set_plant(col, row, new_plant)

    db.session.add(user)
    db.session.commit()

    emit('set_plant',
         {'position': (col, row),
          'new_plant': new_plant.info},
         room=user.username)
