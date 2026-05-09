import sqlite3
from detalle_venta import DetalleVenta

class DetalleVentaRepository:
    def __init__(self):
        with sqlite3.connect("kiosco.db") as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS detalles_venta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_id INTEGER,
                    producto_id INTEGER,
                    producto_nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL
                )
            """)

    def agregar(self, detalle):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute(
                """INSERT INTO detalles_venta 
                   (venta_id, producto_id, producto_nombre, cantidad, precio_unitario) 
                   VALUES (?, ?, ?, ?, ?)""",
                (detalle.venta_id, detalle.producto_id, detalle.producto_nombre, 
                 detalle.cantidad, detalle.precio_unitario)
            )
            detalle.id = cursor.lastrowid

    def obtener_por_venta(self, venta_id):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute(
                "SELECT id, venta_id, producto_id, producto_nombre, cantidad, precio_unitario FROM detalles_venta WHERE venta_id = ?", 
                (venta_id,)
            )
            detalles = []
            for fila in cursor:
                det = DetalleVenta(
                    id=fila[0], venta_id=fila[1], producto_id=fila[2],
                    producto_nombre=fila[3], cantidad=fila[4], precio_unitario=fila[5]
                )
                detalles.append(det)
            return detalles