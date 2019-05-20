from flask import Flask
from server.signals import socketio, init_app as init_app_socketio
from server.models import db, init_app as init_app_db
from common.plants import PlantManager
import logging

logging.basicConfig(level=logging.INFO)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Init flask
app = Flask(__name__)
init_app_db(app)
init_app_socketio(app)


if __name__ == '__main__':
    # Load configs
    PlantManager.load_config('common/plants_config.json')

    # Initialize database
    with app.app_context():
        db.create_all()

    socketio.run(app, '127.0.0.1', 5000)

