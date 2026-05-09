class Producto:
    def __init__(self, nombre, precio, stock, id=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }