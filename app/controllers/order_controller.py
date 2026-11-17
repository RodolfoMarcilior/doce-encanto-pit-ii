from flask import request, jsonify
from app.config.database import get_db
from app.models.order_model import create


def create_order():
    data = request.get_json(silent=True) or {}
    customer_name = str(data.get('customer_name') or '').strip()
    customer_phone = str(data.get('customer_phone') or '').strip()
    delivery_address = str(data.get('delivery_address') or '').strip()
    notes = str(data.get('notes') or '')[:500]
    payment_method = str(data.get('payment_method') or '').strip()
    allowed_payment_methods = {'Pix', 'Dinheiro', 'Cartão'}
    items = data.get('items')

    if not customer_name or not customer_phone or not delivery_address:
        return jsonify({'error': 'Preencha nome, telefone e endereço.'}), 400
    if payment_method not in allowed_payment_methods:
        return jsonify({'error': 'Selecione uma forma de pagamento válida.'}), 400
    if not isinstance(items, list) or not items:
        return jsonify({'error': 'Adicione pelo menos um produto ao carrinho.'}), 400

    normalized = []
    with get_db() as db:
        for item in items:
            try:
                product_id = int(item.get('product_id'))
                quantity = int(item.get('quantity'))
            except (TypeError, ValueError, AttributeError):
                return jsonify({'error': 'Um dos itens do pedido é inválido.'}), 400
            product = db.execute('SELECT id, price FROM products WHERE id = ? AND active = 1', (product_id,)).fetchone()
            if not product or quantity < 1 or quantity > 50:
                return jsonify({'error': 'Um dos itens do pedido é inválido.'}), 400
            normalized.append({'product_id': product['id'], 'quantity': quantity, 'unit_price': product['price']})

    total = round(sum(item['unit_price'] * item['quantity'] for item in normalized), 2)
    order_id = create({'customer_name': customer_name, 'customer_phone': customer_phone,
        'delivery_address': delivery_address, 'notes': notes, 'payment_method': payment_method, 'total': total, 'items': normalized})
    return jsonify({'message': 'Pedido registrado com sucesso!', 'order_id': order_id, 'total': total,
        'payment_method': payment_method, 'status': 'Recebido'}), 201
