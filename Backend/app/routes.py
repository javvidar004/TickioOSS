from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database import db
from models import User, Ticket
from auth import hash_password, verify_password, token_required

# Crear blueprint para la API
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ==================== AUTENTICACIÓN ====================

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
        
        # Validaciones
        if len(data['password']) < 6:
            return jsonify({'success': False, 'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': 'El nombre de usuario ya existe'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'El email ya está registrado'}), 409
        
        # Crear usuario
        user = User(
            username=data['username'],
            email=data['email'],
            password=hash_password(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Generar token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Autenticar usuario y obtener JWT"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'success': False, 'error': 'Usuario y contraseña requeridos'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not verify_password(user.password, data['password']):
            return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'}), 401
        
        if not user.is_active:
            return jsonify({'success': False, 'error': 'Usuario inactivo'}), 403
        
        # Generar token JWT
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'Autenticación exitosa',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== TICKETS ====================

@api_bp.route('/tickets', methods=['POST'])
@token_required
def create_ticket(user_id):
    """Crear un nuevo ticket"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['title', 'description']):
            return jsonify({'success': False, 'error': 'Título y descripción requeridos'}), 400
        
        if len(data['title']) < 3:
            return jsonify({'success': False, 'error': 'El título debe tener al menos 3 caracteres'}), 400
        
        if len(data['description']) < 10:
            return jsonify({'success': False, 'error': 'La descripción debe tener al menos 10 caracteres'}), 400
        
        ticket = Ticket(
            title=data['title'],
            description=data['description'],
            user_id=user_id,
            status=Ticket.STATUS_OPEN
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ticket creado exitosamente',
            'data': ticket.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
@token_required
def get_ticket(user_id, ticket_id):
    """Obtener detalles de un ticket"""
    try:
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'success': False, 'error': 'Ticket no encontrado'}), 404
        
        # Solo el creador puede ver sus tickets
        if ticket.user_id != user_id:
            return jsonify({'success': False, 'error': 'No tienes permiso para ver este ticket'}), 403
        
        return jsonify({
            'success': True,
            'data': ticket.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/tickets/user/list', methods=['GET'])
@token_required
def list_user_tickets(user_id):
    """Listar todos los tickets del usuario autenticado"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        paginated_tickets = Ticket.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page
        )
        
        return jsonify({
            'success': True,
            'data': [ticket.to_dict() for ticket in paginated_tickets.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated_tickets.total,
                'pages': paginated_tickets.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/tickets/<int:ticket_id>/status', methods=['PUT'])
@token_required
def update_ticket_status(user_id, ticket_id):
    """Actualizar el estado de un ticket"""
    try:
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'success': False, 'error': 'Ticket no encontrado'}), 404
        
        # Solo el creador puede actualizar su ticket
        if ticket.user_id != user_id:
            return jsonify({'success': False, 'error': 'No tienes permiso para actualizar este ticket'}), 403
        
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'success': False, 'error': 'Status requerido'}), 400
        
        if data['status'] not in Ticket.VALID_STATUSES:
            return jsonify({
                'success': False,
                'error': f'Estado inválido. Estados válidos: {", ".join(Ticket.VALID_STATUSES)}'
            }), 400
        
        ticket.status = data['status']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Estado del ticket actualizado',
            'data': ticket.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== HEALTH CHECK ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar que la API está funcionando"""
    return jsonify({
        'success': True,
        'message': 'API de Ticketing funcionando correctamente'
    }), 200
