from flask import jsonify, request, Blueprint, render_template, redirect, g
from app.payments.models import PaymentHistory
from app.payments.generate_sign import generate_sign
from app.db import db
from loguru import logger
from sqlalchemy import exc
import requests

module = Blueprint('payments', __name__, url_prefix='/payments')
logger.add("app/logs/log.log")

@module.before_request
def before_request_func():
    if request.endpoint != 'payments.index':
        req_data = None
        keys_required = []

        if request.endpoint == 'payments.pay_eur':
            req_data = request.get_json()
            keys_required = ["shop_order_id", "amount", "currency", "shop_id"]
        elif request.endpoint == 'payments.pay_usd':
            req_data = request.form
            keys_required = ["shop_amount", "shop_currency", "shop_id", "shop_order_id", "payer_currency"]
        elif request.endpoint == 'payments.pay_rub':
            req_data = request.form
            keys_required = ["payway", "amount", "currency", "shop_order_id", "shop_id"]

        keys_sorted = sorted(keys_required)
        signature, order_id = generate_sign(req_data, keys_sorted)
        g.sha_signature = signature
        g.shop_order_id = order_id


@module.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@module.route('/pay_eur', methods=['POST', 'GET'])
def pay_eur():
    req_data = request.get_json()
    try:
        amount = req_data["amount"]
        currency = req_data["currency"]
        description = req_data["description"]
        shop_order_id = req_data["shop_order_id"]
    except KeyError as e:
        logger.error(str(e))
        return jsonify(error=str(e), description="Key was not specified"), 400


    # Использую g.shop_order_id, чтоб shop_order_id был уникальным,
    # в реальном приложении надо использовать параметр с формы
    try:
        history = PaymentHistory(currency=currency, amount=amount,
                                 description=description, shop_order_id=g.shop_order_id)
        db.session.add(history)
        db.session.commit()
    except exc.IntegrityError as e:
        logger.exception('got exception on create payment_history', exc_info=True)
        return jsonify(error=str(e), description="Payment history was not created, duplicate or null column"), 400
    except exc.DataError as e:
        logger.exception('got exception on create payment_history', exc_info=True)
        return jsonify(error=str(e), description="Payment history was not created, wrong argument types"), 400
    return jsonify({'sign': g.sha_signature, 'shop_order_id': g.shop_order_id})


@module.route('/pay_usd', methods=['POST', 'GET'])
def pay_usd():
    req_data = request.form
    try:
        amount = req_data["shop_amount"]
        currency = req_data["shop_currency"]
        description = req_data["description"]
        shop_order_id = req_data["shop_order_id"]
    except KeyError as e:
        logger.error(str(e))
        return jsonify(error=str(e), description="Key was not specified"), 400

    headers = {'Content-Type': 'application/json'}
    # Использую g.shop_order_id, чтоб shop_order_id был уникальным,
    # в реальном приложении надо использовать параметр с формы
    response = requests.post("https://core.piastrix.com/bill/create",
                             json={"payer_currency": req_data["payer_currency"],
                                              "shop_amount": amount,
                                              "shop_currency": currency,
                                              "shop_id": req_data["shop_id"],
                                              "shop_order_id": g.shop_order_id,
                                              "description": description,
                                              "sign": g.sha_signature},
                             headers=headers)

    response_data = response.json()

    if not response_data["error_code"]:
        try:
            history = PaymentHistory(currency=currency, amount=amount,
                                     description=description, shop_order_id=g.shop_order_id)
            db.session.add(history)
            db.session.commit()
        except exc.IntegrityError as e:
            logger.exception('got exception on create payment_history', exc_info=True)
            return jsonify(error=str(e), description="Payment history was not created, duplicate or null column"), 400
        except exc.DataError as e:
            logger.exception('got exception on create payment_history', exc_info=True)
            return jsonify(error=str(e), description="Payment history was not created, wrong argument types"), 400
    else:
        logger.error(response_data)
        return jsonify(description="Invalid payment options")

    data = response_data["data"]
    return redirect(data["url"])


@module.route('/pay_rub', methods=['POST', 'GET'])
def pay_rub():
    req_data = request.form
    try:
        amount = req_data["amount"]
        currency = req_data["currency"]
        shop_order_id = req_data["shop_order_id"]
        description = req_data["description"]
    except KeyError as e:
        logger.error(str(e))
        return jsonify(error=str(e), description="Key was not specified"), 400

    headers = {'Content-Type': 'application/json'}
    # Использую g.shop_order_id, чтоб shop_order_id был уникальным,
    # в реальном приложении надо использовать параметр с формы
    response = requests.post("https://core.piastrix.com/invoice/create",
                             json={"amount": req_data["amount"],
                                              "currency": req_data["currency"],
                                              "payway": req_data["payway"],
                                              "shop_id": req_data["shop_id"],
                                              "shop_order_id": g.shop_order_id,
                                              "description": description,
                                              "sign": g.sha_signature},
                             headers=headers)
    response_data = response.json()
    if not response_data["error_code"]:
        try:
            history = PaymentHistory(currency=currency, amount=amount,
                                     description=description, shop_order_id=g.shop_order_id)
            db.session.add(history)
            db.session.commit()
        except exc.IntegrityError as e:
            logger.exception('got exception on create payment_history', exc_info=True)
            return jsonify(error=str(e), description="Payment history was not created, duplicate or null column"), 400
        except exc.DataError as e:
            logger.exception('got exception on create payment_history', exc_info=True)
            return jsonify(error=str(e), description="Payment history was not created, wrong argument types"), 400

        return render_template("pay_rub.html", data=response_data)
    else:
        logger.error(response_data)
        return jsonify(description="Invalid payment options")
