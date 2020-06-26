from app import db


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(64), nullable=False, index=True)
    product_name = db.Column(db.String(64), nullable=False, index=True)
    account_number = db.Column(db.Integer(64), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(64), nullable=False, index=True)
    customer_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    balance = db.Column(db.Integer, nullable=False, index=True)
    month_end = db.Column(db.DateTime, index=True)
    flag = db.Column(db.String(64), nullable=False, index=True)

    def __repr__(self):
        return '<Accounts %r>' % self.account_number
