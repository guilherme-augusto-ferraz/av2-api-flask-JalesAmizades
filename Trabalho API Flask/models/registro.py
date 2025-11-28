from database import db
from datetime import datetime
# Modelo para os registros
class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120))
    obs = db.Column(db.String(300), default='')
    data = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)