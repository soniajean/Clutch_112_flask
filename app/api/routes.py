from flask import Blueprint, request
from ..models import Post, Product

api = Blueprint('api', __name__, url_prefix='/api')

@api.get('/posts')
def getPosts():
    posts = Post.query.all()
    postlist = [p.to_dict() for p in posts]
    return {
        'status': 'ok',
        'data': postlist
    }
@api.route('/products')
def getProds():
    prods = Product.query.all()
    prodlist = [p.to_dict() for p in prods]
    return {
        'status': 'ok',
        'data' : prodlist,
        'item_count' : len(prodlist)
    }

@api.get('/post/<int:post_id>')
def getSinglePost(post_id):
    p = Post.query.get(post_id)
    if p:
        post = p.to_dict()
        return {
            'status': 'ok',
            'data' : post
        }
    return {
        'status' : 'NOT ok',
        'message' : 'There is no post for the id you have submitted!'
    }
@api.route('/product/<int:prod_id>')
def getIndProd(prod_id):
    p = Product.query.get(prod_id)
    if p:
        prod = p.to_dict()
        return {
            'status': 'ok',
            'data': prod,
        }
    return {
        'status': 'Error',
        'message': 'No product with that ID exists',
    }

@api.post('/createpost')
def createPostAPI():
    data = request.json # This coming from the POST request body

    title = data['title']
    img_url = data['img_url']
    body = data['body']
    user_id = data['user_id']

    new = Post(title, img_url, body, user_id)
    new.savePost()
    return {
        'status' : 'ok',
        'message' : 'new post has been created!'
    }

@api.get('/post/author/<int:user_id>')
def getPostsByUser(user_id):
    posts = Post.query.filter(Post.user_id == user_id).all()
    # Just so we can see the other example of the same query above:
    # posts = Post.query.filter_by(user_id == user_id).all()

    if posts:
        return {
            'status' : 'ok',
            'posts' : [p.to_dict() for p in posts]
        }
    return {
        'status' : ' NOT ok',
        'message' : 'No posts available to return from that ID'
    }