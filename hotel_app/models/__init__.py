from flask_mysqldb import MySQL

# Inicializa la conexión a la base de datos
db = MySQL()

# Importa los modelos individuales
from .habitacion import Habitacion
from .reserva import Reserva
from .cliente import Cliente
from .usuario import Usuario
