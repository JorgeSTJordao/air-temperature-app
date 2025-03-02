from api import db

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)