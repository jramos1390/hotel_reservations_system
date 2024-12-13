from flask import Blueprint, jsonify, request
from models import db

habitacion_bp = Blueprint('habitaciones', __name__)

# Obtener todas las habitaciones
@habitacion_bp.route('/', methods=['GET'])
def get_habitaciones():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM habitaciones")
    rows = cursor.fetchall()
    habitaciones = [
        {
            'id': row[0],
            'numero_habitacion': row[1],
            'tipo': row[2],
            'descripcion': row[3],
            'precio': float(row[4]),
            'estado': row[5],
            'imagen': row[6]
        } for row in rows
    ]
    return jsonify(habitaciones)

# Obtener una habitación por ID
@habitacion_bp.route('/<int:id>', methods=['GET'])
def get_habitacion(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM habitaciones WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        habitacion = {
            'id': row[0],
            'numero_habitacion': row[1],
            'tipo': row[2],
            'descripcion': row[3],
            'precio': float(row[4]),
            'estado': row[5],
            'imagen': row[6]
        }
        return jsonify(habitacion)
    return jsonify({'message': 'Habitación no encontrada'}), 404

# Crear una nueva habitación
@habitacion_bp.route('/', methods=['POST'])
def create_habitacion():
    data = request.get_json()
    numero_habitacion = data['numero_habitacion']
    tipo = data['tipo']
    descripcion = data.get('descripcion', '')
    precio = data['precio']
    estado = data.get('estado', 'Disponible')
    imagen = data.get('imagen', '')

    cursor = db.connection.cursor()
    cursor.execute("""
        INSERT INTO habitaciones (numero_habitacion, tipo, descripcion, precio, estado, imagen)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (numero_habitacion, tipo, descripcion, precio, estado, imagen))
    db.connection.commit()
    return jsonify({'message': 'Habitación creada exitosamente'}), 201

# Actualizar una habitación existente
@habitacion_bp.route('/<int:id>', methods=['PUT'])
def update_habitacion(id):
    data = request.get_json()
    numero_habitacion = data.get('numero_habitacion')
    tipo = data.get('tipo')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    estado = data.get('estado')
    imagen = data.get('imagen')

    cursor = db.connection.cursor()
    cursor.execute("""
        UPDATE habitaciones
        SET numero_habitacion = %s, tipo = %s, descripcion = %s, precio = %s, estado = %s, imagen = %s
        WHERE id = %s
    """, (numero_habitacion, tipo, descripcion, precio, estado, imagen, id))
    db.connection.commit()
    if cursor.rowcount == 0:
        return jsonify({'message': 'Habitación no encontrada'}), 404

    return jsonify({'message': 'Habitación actualizada exitosamente'})

# Eliminar una habitación
@habitacion_bp.route('/<int:id>', methods=['DELETE'])
def delete_habitacion(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM habitaciones WHERE id = %s", (id,))
    db.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Habitación no encontrada'}), 404

    return jsonify({'message': 'Habitación eliminada exitosamente'})

# Obtener habitaciones disponibles
@habitacion_bp.route('/disponibles', methods=['GET'])
def habitaciones_disponibles():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM habitaciones WHERE estado = 'Disponible'")
    rows = cursor.fetchall()
    habitaciones = [
        {
            'id': row[0],
            'numero_habitacion': row[1],
            'tipo': row[2],
            'descripcion': row[3],
            'precio': float(row[4]),
            'estado': row[5],
            'imagen': row[6]
        } for row in rows
    ]
    if not habitaciones:
        return jsonify({'message': 'No hay habitaciones disponibles'}), 404
    return jsonify(habitaciones)
