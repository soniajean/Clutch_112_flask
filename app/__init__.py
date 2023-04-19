from flask import Flask

from config import Config

from .auth.routes import auth
from .ig.routes import ig
from .api.routes import api
from .driver.routes import driver
from .shop.routes import shop
from .payments.routes import payments

from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

login = LoginManager()
moment = Moment(app)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)
# set up a re-route for unauthorized access
login.login_view = 'auth.loginPage'


app.register_blueprint(auth)
app.register_blueprint(ig)
app.register_blueprint(api)
app.register_blueprint(driver)
app.register_blueprint(shop)
app.register_blueprint(payments)

from . import routes