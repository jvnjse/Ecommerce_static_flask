from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(200), nullable=False)
    image_file1 = db.Column(db.String(200), nullable=False)
    image_file2 = db.Column(db.String(200), nullable=False)
    image_file3 = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f"<CartItem {self.id}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address_line1 = db.Column(db.String(200), nullable=False)
    address_line2 = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    pin = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    products_string = db.Column(db.String(500), nullable=False)
    time_ordered = db.Column(db.DateTime, index=True, default=datetime.utcnow)


    def __repr__(self):
        return f"<Order {self.id}>"

