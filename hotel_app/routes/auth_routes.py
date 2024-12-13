from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.usuario import Usuario
from models.cliente import Cliente

auth_bp = Blueprint('auth', __name__)

# Ruta para registrar un nuevo usuario
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Manejar el registro de usuarios
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nombre = request.form['nombre']
        rol = request.form['rol']

        # Hashear la contraseña
        hashed_password = generate_password_hash(password)

        # Guardar en la base de datos
        cursor = db.connection.cursor()
        cursor.execute(
            "INSERT INTO usuarios (email, password, nombre, rol) VALUES (%s, %s, %s, %s)",
            (email, hashed_password, nombre, rol)
        )
        db.connection.commit()

        flash('Usuario registrado exitosamente')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

# Ruta para el login de usuario
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Consultar la base de datos para encontrar al usuario
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        row = cursor.fetchone()

        # Verificar si el usuario existe y si la contraseña es correcta
        if row and check_password_hash(row[2], password):  # row[2] es la contraseña hasheada
            user = Usuario(id=row[0], email=row[1], password=row[2], nombre=row[3], rol=row[4])
            login_user(user)
            return redirect(url_for('home'))  # Redirigir a la página principal o la que elijas
        else:
            flash('Credenciales inválidas')
    
    return render_template('login.html')

# Ruta para cerrar sesión
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
