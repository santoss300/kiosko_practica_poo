class DetalleVenta:
    def __init__(self, venta_id, producto_id, producto_nombre, cantidad, precio_unitario, id=None):
        self.id = id
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def to_dict(self):
        return {
            "id": self.id,
            "venta_id": self.venta_id,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal()
        }