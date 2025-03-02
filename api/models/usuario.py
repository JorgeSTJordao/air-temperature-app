from api import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False, unique=True)
    consultas = db.relationship("Consulta", backref="usuario", lazy=True)

    @staticmethod
    def create(email, senha, telefone):
        usuario = Usuario(email=email, senha=senha, telefone=telefone)
        db.session.add(usuario)
        db.session.commit()

        return usuario
    
    @staticmethod
    def read_all():
        return Usuario.query.all()
    
    @staticmethod
    def read_user(email):
        return Usuario.query.filter_by(email=email).first()
