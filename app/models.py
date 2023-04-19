from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

#  Example on creating a join-table as it's own class
# class Follow(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     followed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     following_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def saveFollow(self):
#         db.session.add(self)
#         db.session.commit()


follows = db.Table(
    'follows',
    db.Column('followed_by_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)

likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    following = db.relationship('User',
        #this is multi-join!
        # c is short for column
        primaryjoin = (follows.c.followed_by_id==id),
        secondaryjoin = (follows.c.following_id==id),
        secondary = follows,
        backref = db.backref('follows', lazy='dynamic'),
        lazy = 'dynamic'
    )

    def follow(self, user):
        self.following.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.following.remove(user)
        db.session.commit()
    

#as an example for backref
#with the post below
# p1 = Post()
# p1.author

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) 
        #self.password = password   ---OLD  not hashed

    def saveUser(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String)
    body = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
                                #  notice          ^^^^^ --> lowercase?  yep.  User.id
    liked = db.relationship('User',
        secondary = 'likes',
        backref = 'liked',
        lazy = 'dynamic'
    )

    def __init__(self, title, img_url, body, user_id):
        self.title = title
        self.img_url = img_url
        self.body = body
        self.user_id = user_id

    def savePost(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

    def deletePost(self):
        db.session.delete(self)
        db.session.commit()
    
    def likePost(self, user):
        self.liked.append(user)
        db.session.commit()

    def to_dict(self):
        return {
            'title' : self.title,
            'id' : self.id,
            'img_url' : self.img_url,
            'body' : self.body,
            'date_created' : self.date_created,
            'user_id' : self.user_id,
            'author' : self.author.username

        }
    


class Driver(db.Model):
    d_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    nation = db.Column(db.String)

    def __init__(self, id, first_name, last_name, nation):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nation = nation

    def saveDriver(self):
        db.session.add(self)
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    miles = db.Column(db.Integer)
    desc = db.Column(db.String)
    name = db.Column(db.String)
    img_url = db.Column(db.String)
    price = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, make, model, year, miles, desc, name, img_url, price=0):
        self.make = make
        self.model = model
        self.year = year
        self.miles = miles
        self.desc = desc
        self.name = name
        self.img_url = img_url
        self.price = price

    def to_dict(self):
        return {
            'id' : self.id,
            'make' : self.make,
            'model' : self.model,
            'year' : self.year,
            'miles' : self.miles,
            'desc' : self.desc,
            'name' : self.name,
            'img_url' : self.img_url,
            'price' : self.price,
            'date_created' : self.date_created,
        }
    
    def saveProduct(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

    def deleteProduct(self):
        db.session.delete(self)
        db.session.commit()