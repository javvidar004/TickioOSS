import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import config
from database import db
from routes import api_bp


def create_app(config_name=None):
    """Factory function para crear la aplicación Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    
    # Inicializar base de datos
    with app.app_context():
        db.create_all()
    
    # Rutas raíz
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Bienvenido a la API de Ticketing',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/v1/health',
                'auth': {
                    'register': 'POST /api/v1/auth/register',
                    'login': 'POST /api/v1/auth/login'
                },
                'tickets': {
                    'create': 'POST /api/v1/tickets',
                    'get': 'GET /api/v1/tickets/<id>',
                    'list': 'GET /api/v1/tickets/user/list',
                    'update_status': 'PUT /api/v1/tickets/<id>/status'
                }
            }
        }), 200
    
    # Manejo de errores JWT
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'success': False, 'error': 'No autorizado. Token inválido o expirado'}), 401
    
    # Manejo de errores generales
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 'Recurso no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
