from main import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    accounts = db.relationship('Account', backref='customer', lazy=True)

    def __repr__(self):
        return '<Customer %r>' % self.customer_name


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    product_type = db.Column(db.String(64), unique=True, nullable=False, index=True)
    accounts = db.relationship('Account', backref='product', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.product_name


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    balance = db.Column(db.Integer, nullable=False, index=True)
    flag = db.Column(db.String(64), nullable=False, index=True)
    month_end = db.Column(db.DateTime, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __repr__(self):
        return '<Account %r>' % self.product_name
