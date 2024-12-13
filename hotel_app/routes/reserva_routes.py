# routes/reserva_routes.py
from flask import Blueprint, jsonify, request
from models import db

reserva_bp = Blueprint('reservas', __name__)

# Obtener todas las reservas
@reserva_bp.route('/', methods=['GET'])
def get_reservas():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM reservas")
    rows = cursor.fetchall()
    reservas = []
    for row in rows:
        reserva = {
            'id': row[0],
            'cliente_id': row[1],
            'habitacion_id': row[2],
            'fecha_reserva': row[3].strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_entrada': row[4].strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_salida': row[5].strftime('%Y-%m-%d %H:%M:%S')
        }
        reservas.append(reserva)
    return jsonify(reservas)

# Obtener una reserva por ID
@reserva_bp.route('/<int:id>', methods=['GET'])
def get_reserva(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM reservas WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        reserva = {
            'id': row[0],
            'cliente_id': row[1],
            'habitacion_id': row[2],
            'fecha_reserva': row[3].strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_entrada': row[4].strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_salida': row[5].strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(reserva)
    return jsonify({'message': 'Reserva no encontrada'}), 404

# Crear una nueva reserva
@reserva_bp.route('/', methods=['POST'])
def create_reserva():
    data = request.get_json()
    cliente_id = data['cliente_id']
    habitacion_id = data['habitacion_id']
    fecha_reserva = data['fecha_reserva']
    fecha_entrada = data['fecha_entrada']
    fecha_salida = data['fecha_salida']

    cursor = db.connection.cursor()
    cursor.execute("""
        INSERT INTO reservas (cliente_id, habitacion_id, fecha_reserva, fecha_entrada, fecha_salida)
        VALUES (%s, %s, %s, %s, %s)
    """, (cliente_id, habitacion_id, fecha_reserva, fecha_entrada, fecha_salida))
    db.connection.commit()

    return jsonify({'message': 'Reserva creada exitosamente'}), 201

# Actualizar una reserva existente
@reserva_bp.route('/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    cliente_id = data.get('cliente_id')
    habitacion_id = data.get('habitacion_id')
    fecha_entrada = data.get('fecha_entrada')
    fecha_salida = data.get('fecha_salida')

    cursor = db.connection.cursor()
    cursor.execute("""
        UPDATE reservas
        SET cliente_id = %s, habitacion_id = %s, fecha_entrada = %s, fecha_salida = %s
        WHERE id = %s
    """, (cliente_id, habitacion_id, fecha_entrada, fecha_salida, id))
    db.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Reserva no encontrada'}), 404

    return jsonify({'message': 'Reserva actualizada exitosamente'})

# Eliminar una reserva
@reserva_bp.route('/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = %s", (id,))
    db.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Reserva no encontrada'}), 404

    return jsonify({'message': 'Reserva eliminada exitosamente'})
