from flask import Blueprint, jsonify, request
from models import db
from pymysql.err import IntegrityError

cliente_bp = Blueprint('clientes', __name__)

@cliente_bp.route('/', methods=['GET'])
def get_clientes():
    # Obtener todos los clientes 
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    clientes = [
        {
            'id': row[0],
            'nombre': row[1],
            'direccion': row[2],
            'telefono': row[3],
            'email': row[4],
            'fecha_registro': row[5].strftime('%Y-%m-%d %H:%M:%S')
        } for row in rows
    ]
    return jsonify(clientes)

@cliente_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    # Obtener un cliente por ID
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    row = cursor.fetchone()

    if row:
        cliente = {
            'id': row[0],
            'nombre': row[1],
            'direccion': row[2],
            'telefono': row[3],
            'email': row[4],
            'fecha_registro': row[5].strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(cliente)
    return jsonify({'message': 'Cliente no encontrado'}), 404

@cliente_bp.route('/', methods=['POST'])
def create_cliente():
    # Crear un nuevo cliente 
    data = request.get_json()
    nombre = data['nombre']
    direccion = data.get('direccion', '')
    telefono = data.get('telefono', '')
    email = data['email']

    cursor = db.connection.cursor()
    try:
        cursor.execute("""INSERT INTO clientes (nombre, direccion, telefono, email)
            VALUES (%s, %s, %s, %s)""", (nombre, direccion, telefono, email))
        db.connection.commit()
    except IntegrityError:
        return jsonify({'message': 'El email ya está registrado'}), 400

    return jsonify({'message': 'Cliente creado exitosamente'}), 201

@cliente_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    # Actualizar un cliente existente
    data = request.get_json()
    nombre = data['nombre']
    direccion = data.get('direccion')
    telefono = data.get('telefono')
    email = data['email']

    cursor = db.connection.cursor()
    cursor.execute("""UPDATE clientes
        SET nombre = %s, direccion = %s, telefono = %s, email = %s
        WHERE id = %s
    """, (nombre, direccion, telefono, email, id))
    db.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    return jsonify({'message': 'Cliente actualizado exitosamente'}), 200

@cliente_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    # Eliminar un cliente
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    db.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
