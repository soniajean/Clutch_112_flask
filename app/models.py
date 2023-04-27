from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

cart = db.Table(
    'my_cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False )
    
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def saveUser(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False, )
    title = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String)
    category = db.Column(db.String)
    img_url = db.Column(db.String)
    carted = db.relationship('User',
    secondary='my_cart',
    backref='carted',
    lazy='dynamic'
    )

    def __init__(self, id, product_id, title, description, category, img_url, price=0):
        self.id = id
        self.product_id = product_id
        self.title = title
        self.price = price
        self.description = description
        self.category = category
        self.img_url = img_url

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'img_url': self.img_url

        }

    def saveProduct(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

    def deleteProduct(self):
        db.session.delete(self)
        db.session.commit()
