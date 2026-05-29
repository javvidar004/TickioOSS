from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """Inicializar la base de datos"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()


def reset_db(app):
    """Reiniciar la base de datos (solo para desarrollo)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
