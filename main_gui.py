import tkinter as tk
from tkinter import messagebox, simpledialog
from producto import Producto
from venta import Venta
from detalle_venta import DetalleVenta
from producto_repository import ProductoRepository
from venta_repository import VentaRepository
from detalle_venta_repository import DetalleVentaRepository
import datetime

class KioscoGUI:
    def __init__(self, root):
        self.repo_producto = ProductoRepository()
        self.repo_venta = VentaRepository()
        self.repo_detalle = DetalleVentaRepository()

        root.title("Demo 1.0 - Por Ignacio Ruíz")
        root.geometry("300x350")
        root.configure(padx=20, pady=20)

        tk.Label(root, text="=== Gestión de Ventas ===", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Listar Productos", command=self.listar, width=25, height=2).pack(pady=5)
        tk.Button(root, text="Agregar Producto", command=self.agregar, width=25, height=2).pack(pady=5)
        tk.Button(root, text="Registrar Venta Rápida", command=self.venta_rapida, width=25, height=2).pack(pady=5)
        tk.Button(root, text="Reporte del Día", command=self.reporte, width=25, height=2).pack(pady=5)

    def listar(self):
        productos = self.repo_producto.obtener_todos()
        if not productos:
            messagebox.showinfo("Catálogo", "No hay productos cargados en la base.")
            return
        texto = ""
        for p in productos:
            texto += f"ID: {p.id} | {p.nombre} | ${p.precio:.2f} | Stock: {p.stock}\n"
        messagebox.showinfo("Productos", texto)

    def agregar(self):
        nombre = simpledialog.askstring("Nuevo Producto", "Nombre del producto:")
        if not nombre: return
        precio = simpledialog.askfloat("Nuevo Producto", "Precio:")
        if not precio or precio <= 0: return
        stock = simpledialog.askinteger("Nuevo Producto", "Stock inicial:")
        if stock is None or stock < 0: return

        nuevo = Producto(nombre, precio, stock)
        self.repo_producto.agregar(nuevo)
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.")

    def venta_rapida(self):
        id_prod = simpledialog.askinteger("Venta", "Ingrese el ID del producto a vender:")
        if not id_prod: return
        producto = self.repo_producto.obtener_por_id(id_prod)
        if not producto:
            messagebox.showerror("Error", "El producto no existe en la base de datos.")
            return
            
        cantidad = simpledialog.askinteger("Venta", f"Cantidad a vender de '{producto.nombre}':")
        if not cantidad or cantidad <= 0 or cantidad > producto.stock:
            messagebox.showerror("Error", "Cantidad inválida o stock insuficiente.")
            return
        
        nueva_venta = Venta()
        self.repo_venta.agregar(nueva_venta)
        
        detalle = DetalleVenta(nueva_venta.id, producto.id, producto.nombre, cantidad, producto.precio)
        self.repo_detalle.agregar(detalle)
        
        self.repo_producto.actualizar_stock(producto.id, producto.stock - cantidad)
        nueva_venta.total = detalle.subtotal()
        self.repo_venta.actualizar_total(nueva_venta)
        
        messagebox.showinfo("Éxito", f"Venta registrada.\nTotal a cobrar: ${nueva_venta.total:.2f}")

    def reporte(self):
        hoy = datetime.datetime.now().strftime("%Y-%m-%d")
        total = self.repo_venta.total_recaudado_hoy()
        messagebox.showinfo("Reporte", f"Total recaudado hoy ({hoy}):\n\n${total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KioscoGUI(root)
    root.mainloop()