from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors

if not app.debug:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handlers = RotatingFileHandler('logs/errors.logs', maxBytes=10240,
                                        backupCount=10)
    file_handlers.setFormatter(logging.Formatter(
        '%(asctime)s, %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handlers.setLevel(logging.INFO)
    app.logger.addHandler(file_handlers)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Server logs')
    