from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class CreateProdForm(FlaskForm):
    id = StringField('id') 
    product_id = StringField('prod_id') 
    title = StringField("Title", validators = [DataRequired()])
    price = IntegerField('Price')
    desc = StringField("Description")
    category = StringField("Category")
    img_url = StringField("Img_url")
    rating = IntegerField('Rating')
    date_created = StringField('Date Created')
    submit = SubmitField()


class UpdateProdForm(FlaskForm):
    id = StringField('id') 
    product_id = StringField('prod_id') 
    title = StringField('Name of Product')
    price = IntegerField('Price')
    desc = StringField("Description")
    category = StringField("Category")
    img_url = StringField("Img_url")
    rating = IntegerField('Rating')
    date_created = StringField('Date Created')
    submit = SubmitField()

