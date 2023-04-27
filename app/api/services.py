import requests
import time

def get_products(products):
    url= f'https://fakestoreapi.com/products/{products}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        product = {
        'product_id' : data["id"],
        'product_name' : data["title"],
        'price' : data["price"],
        'description' : data["description"],
        'category': data["category"],
        'product_image' : data["image"]
        }
        return product
    else:
        return None

# print(get_products(1))