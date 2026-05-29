"""
Script de utilidades para la base de datos
"""
from app import create_app
from database import db, reset_db


def create_tables():
    """Crear todas las tablas"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print('✓ Tablas creadas exitosamente')


def drop_tables():
    """Eliminar todas las tablas"""
    app = create_app()
    with app.app_context():
        db.drop_all()
        print('✓ Tablas eliminadas exitosamente')


def reset():
    """Reiniciar base de datos"""
    app = create_app()
    reset_db(app)
    print('✓ Base de datos reiniciada')


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'create':
            create_tables()
        elif command == 'drop':
            drop_tables()
        elif command == 'reset':
            reset()
        else:
            print('Comando no reconocido')
    else:
        print('Uso: python manage.py [create|drop|reset]')
