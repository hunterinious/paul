from app.db import db
from app.payments.models import PaymentHistory
import hashlib


def generate_sign(data, keys):
    secret = "SecretKey01"
    sha_str = ""
    # Поле для уникальности shop_order_id, для тестового приложения
    test_key_to_return = ""
    for index, key in enumerate(keys):
        if key == "shop_order_id":
            orders_count = db.session.query(PaymentHistory.shop_order_id).count()
            key_for_test_app = f'{data[key]}{orders_count}'
            # Запоминаю значения поля shop_order_id, для тестового приложения
            test_key_to_return = key_for_test_app
        else:
            key_for_test_app = data[key]
        if index == len(keys) - 1:
            sha_str += key_for_test_app
        else:
            sha_str += key_for_test_app + ":"

    sha_str = sha_str + secret

    sha_signature = hashlib.sha256(sha_str.encode()).hexdigest()
    return sha_signature, test_key_to_return