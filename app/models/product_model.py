from app.config.database import get_db


def all_active():
    with get_db() as db:
        rows = db.execute('SELECT * FROM products WHERE active = 1 ORDER BY id DESC').fetchall()
        return [dict(row) for row in rows]


def find_active(product_id):
    with get_db() as db:
        row = db.execute('SELECT * FROM products WHERE id = ? AND active = 1', (product_id,)).fetchone()
        return dict(row) if row else None
