from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_login import LoginManager
import pymysql
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.cliente_routes import cliente_bp
from routes.habitacion_routes import habitacion_bp
from routes.reserva_routes import reserva_bp
from models.usuario import Usuario
from datetime import datetime

# Crear la aplicación Flask
app = Flask(
    __name__,
    static_folder='hotel_reservations_system/presentation_layer/assets',
    template_folder='hotel_reservations_system/presentation_layer'
)

# Configurar la base de datos
app.config.from_object(Config)
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Habilitar CORS
#app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registrar los blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
app.register_blueprint(habitacion_bp, url_prefix='/api/habitaciones')
app.register_blueprint(reserva_bp, url_prefix='/api/reservas')

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

#ruta login
@app.route('/login')
def login():
    return render_template('login.html')

#ruta registro
@app.route('/register')
def register():
    return render_template('register.html')

#ruta administracion
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/clientes')
def admin_clientes():
    return render_template('admin/clientes.html')

@app.route('/admin/habitaciones')
def admin_habitaciones():
    return render_template('admin/habitaciones.html')

@app.route('/admin/reservas')
def admin_reservas():
    return render_template('admin/reservas.html')

#

@app.route('/api/reservas', methods=['GET'])
def get_reservas():
    """
    Endpoint para obtener todas las reservas de la base de datos.
    """
    connection = db.connection  # Obtiene la conexión a la base de datos desde Flask-MySQLdb
    try:
        with connection.cursor() as cursor:
            # Consulta SQL para obtener las reservas y sus relaciones
            query = """
                SELECT 
                    r.id, 
                    c.nombre AS cliente_id, 
                    h.id AS habitacion_id, 
                    r.fecha_reserva, 
                    r.fecha_inicio, 
                    r.fecha_fin, 
                    r.estado
                FROM reservas r
                JOIN clientes c ON r.cliente_id = c.id
                JOIN habitaciones h ON r.habitacion_id = h.id
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Convertir las filas en una lista de diccionarios
            reservas = [
                {
                    "id": row[0],
                    "cliente_id": row[1],
                    "habitacion_id": row[2],
                    "fecha_reserva": row[3].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[3], datetime) else row[3],
                    "fecha_inicio": row[4].strftime('%Y-%m-%d') if isinstance(row[4], datetime) else row[4],
                    "fecha_fin": row[5].strftime('%Y-%m-%d') if isinstance(row[5], datetime) else row[5],
                    "estado": row[6]
                }
                for row in rows
            ]

            if not reservas:
                return jsonify({"message": "No hay reservas disponibles"}), 404

            return jsonify(reservas)
    except pymysql.MySQLError as e:
        print(f"Error en la consulta: {str(e)}")  # Log del error
        return jsonify({"error": f"Error en la consulta: {str(e)}"}), 500


# Conexión a la base de datos
def get_connection():
    connection = pymysql.connect(
        host='0.0.0.0',
       #host='10.0.2.15',
        user='hotel_user',
        password='Pude1',
        db='hotel_reservations',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# Cargar usuario para la autenticación
@login_manager.user_loader
def load_user(user_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    if row:
        return Usuario(id=row[0], email=row[1], password=row[2], nombre=row[3], rol=row[4])
    return None

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
