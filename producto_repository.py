import sqlite3
from producto import Producto

class ProductoRepository:
    def __init__(self):
        with sqlite3.connect("kiosco.db") as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            """)

    def agregar(self, producto):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (producto.nombre, producto.precio, producto.stock)
            )
            producto.id = cursor.lastrowid

    def obtener_todos(self):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY nombre")
            productos = []
            for fila in cursor:
                # Fila es una tupla: (id, nombre, precio, stock)
                prod = Producto(nombre=fila[1], precio=fila[2], stock=fila[3], id=fila[0])
                productos.append(prod)
            return productos

    def obtener_por_id(self, id):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute("SELECT id, nombre, precio, stock FROM productos WHERE id = ?", (id,))
            fila = cursor.fetchone()
            if fila:
                return Producto(nombre=fila[1], precio=fila[2], stock=fila[3], id=fila[0])
            return None

    def actualizar_stock(self, id, nuevo_stock):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id))
            # rowcount nos dice cuántas filas fueron afectadas. Si es mayor a 0, se actualizó.
            return cursor.rowcount > 0

    def eliminar(self, id):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute("DELETE FROM productos WHERE id = ?", (id,))
            return cursor.rowcount > 0