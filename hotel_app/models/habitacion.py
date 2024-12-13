class Habitacion:
    def __init__(self, id, numero_habitacion, tipo, descripcion, precio, estado, imagen):
        """
        Clase que representa una habitación en el sistema.

        :param id: ID de la habitación (int)
        :param numero_habitacion: Número de la habitación (str)
        :param tipo: Tipo de la habitación (str)
        :param descripcion: Descripción de la habitación (str)
        :param precio: Precio de la habitación (float)
        :param estado: Estado de la habitación (str)
        :param imagen: Ruta de la imagen de la habitación (str)
        """
        self.id = id
        self.numero_habitacion = numero_habitacion
        self.tipo = tipo
        self.descripcion = descripcion
        self.precio = precio
        self.estado = estado
        self.imagen = imagen

    def to_dict(self):
        """
        Convierte los atributos de la instancia en un diccionario.

        :return: Diccionario con los datos de la habitación.
        """
        return {
            "id": self.id,
            "numero_habitacion": self.numero_habitacion,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "estado": self.estado,
            "imagen": self.imagen
        }
