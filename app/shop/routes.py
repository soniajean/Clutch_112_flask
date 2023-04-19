from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CreateProdForm, UpdateProdForm
from app.models import Product

shop = Blueprint('shop', __name__, template_folder='shop_templates')

@shop.route('/shop', methods=['GET'])
def shop_home():
    prods = Product.query.order_by(Product.date_created.desc()).all()
    return render_template('shop_home.html', prods = prods)

@shop.route('/shop/create', methods=['GET', 'POST'])
def createProd():
    form = CreateProdForm()
    if request.method == 'POST':
        if form.validate():
            make = form.make.data
            model = form.model.data
            year = form.year.data
            miles = form.miles.data
            desc = form.desc.data
            name = form.name.data
            img_url = form.img_url.data
            price = form.price.data
            new = Product(make, model, year, miles, desc, name, img_url, price)
            new.saveProduct()
            flash('Product created!', category='success')
            return redirect(url_for('shop.shop_home'))
    return render_template('create_prod.html', form=form)

@shop.route('/shop/product/<int:prod_id>')
def indProd(prod_id):
    prod = Product.query.get(prod_id)
    return render_template('product.html', prod = prod)

@shop.route('/shop/update/<int:prod_id>', methods=['GET', 'POST'])
def updateProd(prod_id):
    form = UpdateProdForm()
    prod = Product.query.get(prod_id)
    if request.method == 'POST':
        make = form.make.data
        model = form.model.data
        year = form.year.data
        miles = form.miles.data
        desc = form.desc.data
        name = form.name.data
        img_url = form.img_url.data
        price = form.price.data

        prod.make = make
        prod.model = model
        prod.year = year
        prod.miles = miles
        prod.desc = desc
        prod.name = name
        prod.img_url = img_url
        prod.price = price
        prod.saveChanges()
        flash('Product updated!', category='success')
        return redirect(url_for('shop.indProd', prod_id=prod_id))
    return render_template('update_prod.html', prod=prod, form=form)

@shop.get('/shop/delete/<int:prod_id>')
def delProd(prod_id):
    prod = Product.query.get(prod_id)
    prod.deleteProduct()
    flash('Product has been deleted- Byebye!', category='danger')
    return redirect(url_for('shop.shop_home'))