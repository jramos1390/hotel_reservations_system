class Reserva:
    def __init__(self, id, cliente_id, habitacion_id, fecha_reserva, fecha_entrada, fecha_salida, estado):
        """
        Clase que representa una reserva en el sistema.

        :param id: ID de la reserva (int)
        :param cliente_id: ID del cliente asociado a la reserva (int)
        :param habitacion_id: ID de la habitación reservada (int)
        :param fecha_reserva: Fecha de creación de la reserva (datetime o str)
        :param fecha_entrada: Fecha de inicio de la reserva (datetime o str)
        :param fecha_salida: Fecha de fin de la reserva (datetime o str)
        :param estado: Estado de la reserva (str)
        """
        self.id = id
        self.cliente_id = cliente_id
        self.habitacion_id = habitacion_id
        self.fecha_reserva = fecha_reserva
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado = estado

    def to_dict(self):
        """
        Convierte los atributos de la instancia en un diccionario.

        :return: Diccionario con los datos de la reserva.
        """
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "habitacion_id": self.habitacion_id,
            "fecha_reserva": self.fecha_reserva,
            "fecha_entrada": self.fecha_entrada,
            "fecha_salida": self.fecha_salida,
            "estado": self.estado
        }
