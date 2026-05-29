"""
Script para inicializar la base de datos con datos de ejemplo
"""
from app import create_app
from database import db, reset_db
from models import User, Ticket
from auth import hash_password


def seed_database():
    """Poblar la base de datos con datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        # Limpiar y recrear tablas
        reset_db(app)
        
        # Crear usuarios de ejemplo
        users = [
            User(
                username='juan',
                email='juan@example.com',
                password=hash_password('password123'),
                first_name='Juan',
                last_name='Pérez'
            ),
            User(
                username='maria',
                email='maria@example.com',
                password=hash_password('password123'),
                first_name='María',
                last_name='González'
            ),
            User(
                username='carlos',
                email='carlos@example.com',
                password=hash_password('password123'),
                first_name='Carlos',
                last_name='López'
            )
        ]
        
        db.session.add_all(users)
        db.session.commit()
        
        # Crear tickets de ejemplo
        tickets = [
            Ticket(
                title='Error en login',
                description='No puedo iniciar sesión en la aplicación, me aparece un error genérico',
                user_id=1,
                status=Ticket.STATUS_OPEN
            ),
            Ticket(
                title='Solicitud de nueva funcionalidad',
                description='Necesitamos agregar un sistema de notificaciones por email cuando se actualiza un ticket',
                user_id=2,
                status=Ticket.STATUS_IN_PROGRESS
            ),
            Ticket(
                title='Base de datos lenta',
                description='Las consultas están tardando más de lo normal, especialmente en horas pico',
                user_id=3,
                status=Ticket.STATUS_OPEN
            ),
        ]
        
        db.session.add_all(tickets)
        db.session.commit()
        
        print('✓ Base de datos inicializada con éxito')
        print(f'✓ {len(users)} usuarios creados')
        print(f'✓ {len(tickets)} tickets creados')
        print('\nCredenciales de ejemplo:')
        print('  - username: juan | password: password123')
        print('  - username: maria | password: password123')
        print('  - username: carlos | password: password123')


if __name__ == '__main__':
    seed_database()
