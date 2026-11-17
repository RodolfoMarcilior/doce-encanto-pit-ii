from app.config.database import get_db


def create(order):
    with get_db() as db:
        cursor = db.execute('''INSERT INTO orders
            (customer_name, customer_phone, delivery_address, notes, total, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (order['customer_name'], order['customer_phone'], order['delivery_address'], order['notes'], order['total'], order['payment_method']))
        order_id = cursor.lastrowid
        db.executemany('''INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)''', [
                (order_id, item['product_id'], item['quantity'], item['unit_price'])
                for item in order['items']
            ])
        return order_id
