from datetime import datetime

from src.models import Cliente
from src.services import GestorFacturacion
from src.exceptions import (
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    DatosInvalidosError,
    FacturaError,
)


class MenuPrincipal:
    def __init__(self):
        self.gestor = GestorFacturacion()

    def iniciar(self):
        while True:
            self.mostrar_menu()
            try:
                opcion = int(input("Seleccione una opción: "))

                if opcion == 1:
                    self.registrar_cliente()
                elif opcion == 2:
                    self.listar_clientes()
                elif opcion == 3:
                    self.emitir_factura()
                elif opcion == 4:
                    self.mostrar_facturas()
                elif opcion == 5:
                    self.eliminar_cliente()
                elif opcion == 6:
                    self.buscar_cliente()
                elif opcion == 7:
                    self.gestor.mostrar_reporte()
                elif opcion == 8:
                    self.exportar_reporte_txt()
                elif opcion == 9:
                    self.crear_backup()
                elif opcion == 10:
                    self.listar_backups()
                elif opcion == 11:
                    self.restaurar_backup()
                elif opcion == 12:
                    self.demostrar_operadores()
                elif opcion == 13:
                    print("\nGuardando datos y saliendo del sistema...")
                    self.gestor.guardar_datos()
                    break
                else:
                    print("\nOpción inválida")

            except ValueError:
                print("\nDebe introducir un número válido")
            except Exception as e:
                print(f"\nError inesperado: {e}")

    def mostrar_menu(self):
        print("\n========== SISTEMA FACTURACIÓN ==========")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Emitir factura")
        print("4. Mostrar facturas")
        print("5. Eliminar cliente")
        print("6. Buscar cliente")
        print("7. Mostrar reporte por pantalla")
        print("8. Exportar reporte a fichero TXT")
        print("9. Crear backup binario con pickle")
        print("10. Listar backups")
        print("11. Restaurar backup")
        print("12. Demostración de operadores especiales")
        print("13. Salir")
        print("=========================================")

    def registrar_cliente(self):
        try:
            codigo = input("Código cliente: ").strip()
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            saldo = float(input("Saldo inicial: "))

            cliente = Cliente(codigo, nombre, email, saldo)
            self.gestor.registrar_cliente(cliente)
            print("\nCliente registrado correctamente")

        except ValueError:
            print("\nEl saldo debe ser numérico")
        except (ClienteDuplicadoError, DatosInvalidosError) as e:
            print(f"\n{e}")

    def listar_clientes(self):
        if not self.gestor.clientes:
            print("\nNo hay clientes registrados")
            return

        print("\n========== CLIENTES ==========")
        for cliente in self.gestor.clientes:
            print(cliente)

    def buscar_cliente(self):
        try:
            codigo = input("Código del cliente: ")
            cliente = self.gestor.buscar_cliente(codigo)
            print("\n========== CLIENTE ==========")
            print(cliente)
        except ClienteNoEncontradoError as e:
            print(f"\n{e}")

    def eliminar_cliente(self):
        try:
            codigo = input("Código del cliente a eliminar: ")
            self.gestor.eliminar_cliente(codigo)
            print("\nCliente eliminado correctamente")
        except (ClienteNoEncontradoError, FacturaError) as e:
            print(f"\n{e}")

    def emitir_factura(self):
        try:
            codigo_cliente = input("Código cliente: ")
            cliente = self.gestor.buscar_cliente(codigo_cliente)
            numero_factura = int(input("Número factura: "))
            factura = self.gestor.emitir_factura(numero_factura, cliente)

            while True:
                descripcion = input("\nDescripción del item (o 'fin' para terminar): ")
                if descripcion.lower().strip() == "fin":
                    break

                precio = float(input("Precio: "))
                # Uso de __iadd__: modifica la propia factura.
                factura += (descripcion, precio)
                self.gestor.guardar_datos()

            print("\nFactura creada correctamente")

        except ValueError:
            print("\nDatos numéricos inválidos")
        except (ClienteNoEncontradoError, FacturaError, DatosInvalidosError) as e:
            print(f"\n{e}")

    def mostrar_facturas(self):
        if not self.gestor.facturas:
            print("\nNo hay facturas registradas")
            return

        print("\n========== FACTURAS ==========")
        for factura in self.gestor.facturas:
            print(f"\n{factura}")
            for indice, item in enumerate(factura):
                print(f"  [{indice}] {item['descripcion']} => {item['precio']:.2f} €")

    def exportar_reporte_txt(self):
        ruta = self.gestor.exportar_reporte_txt()
        print(f"\nReporte exportado correctamente: {ruta}")

    def crear_backup(self):
        ruta = self.gestor.crear_backup_pickle()
        print(f"\nBackup creado correctamente: {ruta}")

    def listar_backups(self):
        backups = self.gestor.listar_backups()
        if not backups:
            print("\nNo existen backups")
            return

        print("\n========== BACKUPS ==========")
        for i, backup in enumerate(backups, start=1):
            fecha = datetime.fromtimestamp(backup["modificado"]).strftime("%d/%m/%Y %H:%M:%S")
            print(f"{i}. {backup['nombre']} | {backup['tamano']} bytes | {fecha}")

    def restaurar_backup(self):
        backups = self.gestor.listar_backups()
        if not backups:
            print("\nNo existen backups para restaurar")
            return

        self.listar_backups()
        try:
            indice = int(input("Seleccione el número de backup a restaurar: ")) - 1
            if indice < 0 or indice >= len(backups):
                print("\nSelección inválida")
                return
            self.gestor.restaurar_backup_pickle(backups[indice]["ruta"])
            print("\nBackup restaurado correctamente")
        except ValueError:
            print("\nDebe introducir un número válido")

    def demostrar_operadores(self):
        """Demuestra T08 sin alterar permanentemente los datos del usuario."""
        if not self.gestor.facturas:
            print("\nDebe existir al menos una factura para ejecutar la demostración")
            return

        factura = self.gestor.facturas[0]
        print("\n========== DEMOSTRACIÓN T08 ==========")
        print(f"Factura original: {factura}")

        factura_nueva = factura + ("Item añadido con __add__", 10)
        print("\n1) factura + item devuelve una nueva factura")
        print(f"Original: {len(factura)} items")
        print(f"Nueva: {len(factura_nueva)} items")

        factura_temporal = ("Item inicial con __radd__", 5) + factura
        print("\n2) item + factura usa __radd__ y añade al inicio")
        print(f"Primer item de la nueva factura: {factura_temporal[0]}")

        if len(factura_nueva) > 0:
            print("\n3) factura[0] usa __getitem__")
            print(factura_nueva[0])

        if len(factura_nueva) > 0:
            factura_nueva[0] = ("Item modificado con __setitem__", 99)
            print("\n4) factura[0] = item usa __setitem__")
            print(factura_nueva[0])

        print("\n5) Comparación de facturas por total")
        print(f"Factura original < factura nueva: {factura < factura_nueva}")
