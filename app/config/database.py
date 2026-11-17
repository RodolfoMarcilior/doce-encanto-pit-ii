import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / 'data'
DB_PATH = DATA_DIR / 'cupcakes.db'


def get_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS products (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          description TEXT NOT NULL,
          price REAL NOT NULL CHECK(price >= 0),
          category TEXT NOT NULL DEFAULT 'Tradicional',
          image TEXT,
          active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS orders (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          customer_name TEXT NOT NULL,
          customer_phone TEXT NOT NULL,
          delivery_address TEXT NOT NULL,
          notes TEXT,
          total REAL NOT NULL CHECK(total >= 0),
          status TEXT NOT NULL DEFAULT 'Recebido',
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS order_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
          product_id INTEGER NOT NULL REFERENCES products(id),
          quantity INTEGER NOT NULL CHECK(quantity > 0),
          unit_price REAL NOT NULL CHECK(unit_price >= 0)
        );
        ''')
        # Migração compatível com bancos criados em versões anteriores.
        order_columns = {row['name'] for row in db.execute('PRAGMA table_info(orders)').fetchall()}
        if 'payment_method' not in order_columns:
            db.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT NOT NULL DEFAULT 'Não informado'")

        count = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        if count == 0:
            products = [
                ('Chocolate Belga', 'Massa fofinha de chocolate com cobertura cremosa de chocolate belga.', 9.90, 'Chocolate', '🍫'),
                ('Red Velvet', 'Massa red velvet com cobertura suave de cream cheese.', 11.50, 'Especiais', '❤️'),
                ('Doce de Leite', 'Cupcake de baunilha recheado com doce de leite artesanal.', 10.00, 'Tradicional', '🍯'),
                ('Ninho com Morango', 'Creme de leite em pó, morangos e massa de baunilha.', 12.00, 'Especiais', '🍓'),
                ('Limão Siciliano', 'Massa leve com creme cítrico e toque de raspas.', 9.50, 'Frutados', '🍋'),
                ('Baunilha Clássico', 'Massa de baunilha com buttercream delicado.', 8.50, 'Tradicional', '🧁')
            ]
            db.executemany('INSERT INTO products (name, description, price, category, image) VALUES (?, ?, ?, ?, ?)', products)
