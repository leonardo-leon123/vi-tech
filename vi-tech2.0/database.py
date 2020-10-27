from flask_login import UserMixin
from blue_print import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(1000))
    apellido = db.Column(db.String(1000))
    correo = db.Column(db.String(1000))
    password = db.Column(db.String(1000))