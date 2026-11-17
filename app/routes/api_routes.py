from flask import Blueprint, jsonify
from app.controllers.product_controller import index, show
from app.controllers.order_controller import create_order

api = Blueprint('api', __name__)

@api.get('/health')
def health():
    return jsonify({'status': 'ok', 'app': 'Cupcake Gourmet'})

@api.get('/products')
def products():
    return index()

@api.get('/products/<int:product_id>')
def product_detail(product_id):
    return show(product_id)

@api.post('/orders')
def orders():
    return create_order()
