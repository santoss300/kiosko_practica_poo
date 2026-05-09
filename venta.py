import datetime

class Venta:
    def __init__(self, total=0.0, fecha=None, id=None):
        self.id = id
        # Si no nos pasan una fecha (como al crear una venta nueva), usamos la actual
        if fecha is None:
            self.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.fecha = fecha
        self.total = total

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "total": self.total
        }