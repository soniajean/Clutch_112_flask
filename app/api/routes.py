from flask import Blueprint, request
from ..models import Product

api = Blueprint('api', __name__, url_prefix='/api')



@api.get('/product')
def getProduct():
    product = Product.query.all()
    productlist = [p.to_dict() for p in product]
    return {
        'status': 'ok',
        'data': productlist
    }

@api.get('/product/<int:product_id>')
def getSingleProduct(product_id):
    p = Product.query.get(product_id)
    if p:
        product = p.to_dict()
        return {
            'status': 'ok',
            'data' : product
        }
    return {
        'status' : 'NOT ok',
        'message' : 'That product is not available!!'
    }

@api.post('/createproduct')
def createProductAPI():
    data = request.json # This coming from the POST request body

    title = data['title']
    price = data['price']
    description = data['description']
    category = data['category']
    img_url = data['img_url']
   

    new = Product(title, price, description, category, img_url)
    new.saveProduct()
    return {
        'status' : 'ok',
        'message' : 'new product has been created!'
    }

@api.get('/product/item/<int:user_id>')
def getPostsByUser(user_id):
    product = Product.query.filter(Product.user_id == user_id).all()
    # Just so we can see the other example of the same query above:
    # posts = Post.query.filter_by(user_id == user_id).all()

    if product:
        return {
            'status' : 'ok',
            'product' : [p.to_dict() for p in product]
        }
    return {
        'status' : ' NOT ok',
        'message' : 'No product available to return from that ID'
    }