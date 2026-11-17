import os
from pathlib import Path
from flask import Flask, send_from_directory
from app.config.database import init_db
from app.routes.api_routes import api

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR / 'public'), static_url_path='')
app.register_blueprint(api, url_prefix='/api')
init_db()

@app.get('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(_error):
    return {'error': 'Rota não encontrada.'}, 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f'Doce Encanto disponível na porta {port}')
    app.run(host='0.0.0.0', port=port, debug=False)
