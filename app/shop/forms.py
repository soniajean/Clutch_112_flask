from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class CreateProdForm(FlaskForm):
    make = StringField("Make", validators = [DataRequired()])
    model = StringField("Model")
    year = IntegerField('Year')
    miles = IntegerField('Miles')
    desc = StringField("Description")
    name = StringField('Special name for this?')
    img_url = StringField("Img_url")
    price = IntegerField('Price')
    submit = SubmitField()


class UpdateProdForm(FlaskForm):
    make = StringField("Make")
    model = StringField("Model")
    year = IntegerField('Year')
    miles = IntegerField('Miles')
    desc = StringField("Description")
    name = StringField('Special name for this?')
    img_url = StringField("Img_url")
    price = IntegerField('Price')
    submit = SubmitField()