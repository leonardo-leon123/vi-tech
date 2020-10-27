from flask import Blueprint, render_template,redirect,url_for,flash,request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,login_required
from database import User
from blue_print import db

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    correo = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(correo=correo).first()

    if not user or not check_password_hash(user.password,password):
        flash('Tu correo o contraseña son invalidos porfavor checa de nuevo')
        return redirect(url_for('auth.login'))
    
    login_user(user)

    return redirect(url_for('app.inicio'))

@auth.route('/Registro')
def registro():
    return render_template('registro.html') 


@auth.route('/Registro', methods=['POST'])
def signup_post():
    nombre = request.form.get('nombre')
    apellido = request.form.get('lastname')
    correo = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(correo=correo).first()

    if user:
        flash('Este correo ya existe :( intenta con otro o inicia sesión')
        return redirect(url_for('auth.registro'))

    new_user = User(nombre=nombre,apellido=apellido,correo=correo,password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    
    flash('Tu cuenta fue creada con exito! Porfavor ahora Inicia Sesión')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))