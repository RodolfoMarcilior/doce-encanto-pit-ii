from flask import jsonify
from app.models import product_model


def index():
    return jsonify(product_model.all_active())


def show(product_id):
    product = product_model.find_active(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado.'}), 404
    return jsonify(product)
