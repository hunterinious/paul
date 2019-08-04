from app.db import db
from datetime import datetime


class PaymentHistory(db.Model):
    __tablename__ = 'paymenthistory'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Integer, nullable=False, default=None)
    amount = db.Column(db.REAL, nullable=False, default=None)
    description = db.Column(db.String, nullable=True, default="")
    shop_order_id = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    transfer_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())

    # def __init__(self, **kwargs):
    #     super(PaymentHistory, self).__init__(**kwargs)


