import sqlite3
import datetime
from venta import Venta

class VentaRepository:
    def __init__(self):
        with sqlite3.connect("kiosco.db") as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    total REAL NOT NULL
                )
            """)

    def agregar(self, venta):
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute(
                "INSERT INTO ventas (fecha, total) VALUES (?, ?)",
                (venta.fecha, venta.total)
            )
            venta.id = cursor.lastrowid

    def actualizar_total(self, venta):
        with sqlite3.connect("kiosco.db") as conn:
            conn.execute(
                "UPDATE ventas SET total = ? WHERE id = ?",
                (venta.total, venta.id)
            )

    def ventas_del_dia(self, dia=None):
        if dia is None:
            # Si no nos pasan día, tomamos el formato YYYY-MM-DD de hoy
            dia = datetime.datetime.now().strftime("%Y-%m-%d")
            
        with sqlite3.connect("kiosco.db") as conn:
            # Buscamos fechas que empiecen con el texto del día
            cursor = conn.execute("SELECT id, fecha, total FROM ventas WHERE fecha LIKE ?", (f"{dia}%",))
            ventas = []
            for fila in cursor:
                ventas.append(Venta(id=fila[0], fecha=fila[1], total=fila[2]))
            return ventas

    def total_recaudado_hoy(self):
        dia = datetime.datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect("kiosco.db") as conn:
            cursor = conn.execute("SELECT SUM(total) FROM ventas WHERE fecha LIKE ?", (f"{dia}%",))
            resultado = cursor.fetchone()[0]
            # Si no hay ventas, la suma da None, así que devolvemos 0.0
            if resultado is None:
                return 0.0
            return resultado