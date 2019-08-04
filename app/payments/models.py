from app.db import db
from datetime import datetime
import hashlib


class Payment:
    @classmethod
    def generate_sign(cls, data, keys):
        secret = "SecretKey01"
        sha_str = ""
        # Поле для уникальности shop_order_id, для тестового приложения
        test_key_to_return = ""
        for index, key in enumerate(keys):
            if key == "shop_order_id":
                key_for_test_app = data[key] + str(db.session.query(Log.shop_order_id).count())
                # Запоминаю значения поля shop_order_id, для тестового приложения
                test_key_to_return = key_for_test_app
            else:
                key_for_test_app = data[key]
            if index == len(keys) - 1:
                sha_str = sha_str + key_for_test_app
            else:
                sha_str = sha_str + key_for_test_app + ":"

        sha_str = sha_str + secret

        sha_signature = hashlib.sha256(sha_str.encode()).hexdigest()
        return [sha_signature, test_key_to_return]


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Integer, nullable=False, default=None)
    amount = db.Column(db.REAL, nullable=False, default=None)
    description = db.Column(db.VARCHAR(255), nullable=True, default="")
    shop_order_id = db.Column(db.Integer, nullable=False, unique=True)
    transfer_time = db.Column(db.TIMESTAMP, nullable=False, default=None)

    def __init__(self, currency, amount, description, shop_order_id):
        self.currency = currency
        self.amount = amount
        self.description = description,
        self.shop_order_id = shop_order_id
        self.transfer_time = datetime.now()

    def log(self):
        print("log")

