from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database import db

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'chave'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token expira em 1 hora

    # Inicializando as extensoes
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importação os models
    from models.user import User
    from models.registro import Registro

    # Registrando rotas
    from routes.users import users_bp
    from routes.registros import registros_bp

    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(registros_bp, url_prefix='/api/registros')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)