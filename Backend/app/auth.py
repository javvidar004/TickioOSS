"""
Utilidades de autenticación y seguridad
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """Hashear una contraseña"""
    return generate_password_hash(password)


def verify_password(stored_hash, password):
    """Verificar contraseña"""
    return check_password_hash(stored_hash, password)


def token_required(fn):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            return fn(user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
    return decorated
