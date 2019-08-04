import os
from flask import Flask
from .db import db


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    import app.payments.controllers as pay_mod

    app.register_blueprint(pay_mod.module)

    return app
