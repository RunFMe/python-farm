import socketio
from threading import Thread
import logging

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connection established')


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


@sio.on('auth_failed')
def auth_failed():
    from client.game import game
    logging.critical('AUTHENTICATION FAILED')
    game.shutdown()


@sio.on('auth_success')
def auth_success(farm_data):
    logging.info("Authentication was successful")
    from client.game import game
    farm = game.farm

    farm.init_state(farm_data)


@sio.on('set_plant')
def set_plant_handler(data):
    logging.info("Server asked to set plant with data {}"
                 .format(data))

    from client.game import game
    farm = game.farm

    farm.set_plant(*data['position'], tuple(data['new_plant']))


def run_sockets():
    sio.connect('http://localhost:5000')
    logging.info('Connected to server')

    listener = Thread(target=sio.wait)
    listener.start()
    logging.info('Started socket thread')
