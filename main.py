import datetime
from producto import Producto
from venta import Venta
from detalle_venta import DetalleVenta
from producto_repository import ProductoRepository
from venta_repository import VentaRepository
from detalle_venta_repository import DetalleVentaRepository

def mostrar_menu():
    print("\n=== CAJA KIOSCO ===")
    print("1. Listar productos")
    print("2. Agregar producto")
    print("3. Registrar venta")
    print("4. Reporte del día")
    print("5. Salir")

def listar_productos(repo_prod):
    productos = repo_prod.obtener_todos()
    print("\n--- Catálogo de Productos ---")
    if not productos:
        print("No hay productos cargados.")
        return
    for p in productos:
        print(f"ID: {p.id} | Nombre: {p.nombre} | Precio: ${p.precio:.2f} | Stock: {p.stock}")

def agregar_producto(repo_prod):
    nombre = input("Ingrese el nombre del producto: ")
    try:
        precio = float(input("Ingrese el precio: "))
        stock = int(input("Ingrese el stock inicial: "))
        
        # Validaciones solicitadas
        if precio <= 0:
            print("Error: El precio debe ser mayor a cero.")
            return
        if stock < 0:
            print("Error: El stock no puede ser negativo.")
            return
            
        nuevo_producto = Producto(nombre, precio, stock)
        repo_prod.agregar(nuevo_producto)
        print(f"Producto '{nombre}' agregado con éxito. ID asignado: {nuevo_producto.id}")
        
    except ValueError:
        print("Error: Debe ingresar valores numéricos válidos para precio y stock.")

def registrar_venta(repo_prod, repo_venta, repo_detalle):
    listar_productos(repo_prod)
    carrito = []
    
    while True:
        try:
            prod_id_str = input("\nIngrese el ID del producto (o 'fin' para terminar la carga): ")
            if prod_id_str.lower() == 'fin':
                break
                
            prod_id = int(prod_id_str)
            producto = repo_prod.obtener_por_id(prod_id)
            
            if not producto:
                print("Error: Producto no encontrado.")
                continue
                
            cantidad = int(input(f"Ingrese la cantidad para '{producto.nombre}': "))
            if cantidad <= 0:
                print("Error: La cantidad debe ser mayor a cero.")
                continue
                
            # Verificar stock actual menos lo que ya tenemos en el carrito para este producto
            stock_en_carrito = sum(item['cantidad'] for item in carrito if item['producto'].id == prod_id)
            if producto.stock < (cantidad + stock_en_carrito):
                print(f"Error: Stock insuficiente. Stock disponible: {producto.stock - stock_en_carrito}")
                continue
                
            carrito.append({"producto": producto, "cantidad": cantidad})
            print(f"Agregado al ticket: {producto.nombre} x{cantidad}")
            
        except ValueError:
            print("Error: Ingrese un ID numérico o 'fin'.")

    if not carrito:
        print("Venta cancelada. No se agregaron productos.")
        return

    # Proceso de cierre de venta
    nueva_venta = Venta()
    repo_venta.agregar(nueva_venta) # Aquí obtiene su ID
    
    total_venta = 0.0
    detalles_guardados = []
    
    for item in carrito:
        prod = item['producto']
        cant = item['cantidad']
        
        detalle = DetalleVenta(
            venta_id=nueva_venta.id,
            producto_id=prod.id,
            producto_nombre=prod.nombre,
            cantidad=cant,
            precio_unitario=prod.precio
        )
        repo_detalle.agregar(detalle)
        detalles_guardados.append(detalle)
        
        # Descontamos stock físico
        nuevo_stock = prod.stock - cant
        repo_prod.actualizar_stock(prod.id, nuevo_stock)
        
        total_venta += detalle.subtotal()
        
    # Actualizamos el total general de la venta
    nueva_venta.total = total_venta
    repo_venta.actualizar_total(nueva_venta)
    
    # Imprimir el comprobante formateado
    print("\n" + "="*40)
    print(f"VENTA #{nueva_venta.id} — {nueva_venta.fecha[:-3]}") # Cortamos los segundos para que quede YYYY-MM-DD HH:MM
    print("="*40)
    for det in detalles_guardados:
        print(f"{det.producto_nombre} x{det.cantidad} ${det.subtotal():.2f}")
    print("-" * 40)
    print(f"TOTAL: ${total_venta:.2f}")
    print("=" * 40)

def reporte_del_dia(repo_venta, repo_detalle):
    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    ventas_hoy = repo_venta.ventas_del_dia(hoy)
    
    print("\n" + "="*40)
    print(f"REPORTE DE CAJA — {hoy}")
    print("="*40)
    
    if not ventas_hoy:
        print("No se registraron ventas en el día de hoy.")
    else:
        for v in ventas_hoy:
            hora = v.fecha.split(" ")[1][:-3] # Extraer HH:MM de YYYY-MM-DD HH:MM:SS
            print(f"Venta #{v.id} — {hora}")
            detalles = repo_detalle.obtener_por_venta(v.id)
            for det in detalles:
                # El formato >8.2f alinea los precios a la derecha
                print(f"{det.producto_nombre} x{det.cantidad} ${det.subtotal():>8.2f}")
            print(f"Subtotal: ${v.total:.2f}")
            print("")
            
    total_recaudado = repo_venta.total_recaudado_hoy()
    print("-" * 40)
    print(f"Total de ventas: {len(ventas_hoy)}")
    print(f"TOTAL RECAUDADO: ${total_recaudado:.2f}")
    print("=" * 40)

def main():
    # Instanciamos los repositorios. Esto también crea las tablas si no existen.
    repo_producto = ProductoRepository()
    repo_venta = VentaRepository()
    repo_detalle = DetalleVentaRepository()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            listar_productos(repo_producto)
        elif opcion == '2':
            agregar_producto(repo_producto)
        elif opcion == '3':
            registrar_venta(repo_producto, repo_venta, repo_detalle)
        elif opcion == '4':
            reporte_del_dia(repo_venta, repo_detalle)
        elif opcion == '5':
            print("Saliendo del sistema de caja...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()