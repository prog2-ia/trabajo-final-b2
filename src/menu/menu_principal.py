from src.modelos import Cliente
from src.services import GestorFacturacion
from src.exceptions import (
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    FacturaError,
    DatosInvalidosError
)


class MenuFacturacion:

    def __init__(self):
        self.gestor = GestorFacturacion()

    # =========================
    # MENÚ PRINCIPAL
    # =========================
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
                    print("\nSaliendo del sistema...")
                    break

                else:
                    print("\nOpción inválida")

            except ValueError:
                print("\nDebe introducir un número")

            except Exception as e:
                print(f"\nError inesperado: {e}")

    # =========================
    # MOSTRAR MENÚ
    # =========================
    def mostrar_menu(self):

        print("\n========== SISTEMA FACTURACIÓN ==========")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Emitir factura")
        print("4. Mostrar facturas")
        print("5. Eliminar cliente")
        print("6. Buscar cliente")
        print("7. Mostrar reporte")
        print("8. Salir")
        print("=========================================")

    # =========================
    # REGISTRAR CLIENTE
    # =========================
    def registrar_cliente(self):

        try:
            codigo = input("Código cliente: ").strip()
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            saldo = float(input("Saldo inicial: "))

            if saldo < 0:
                raise DatosInvalidosError(
                    "El saldo no puede ser negativo"
                )

            cliente = Cliente(codigo, nombre, email)
            cliente.saldo = saldo

            self.gestor.registrar_cliente(cliente)

            print("\nCliente registrado correctamente")

        except ValueError:
            print("\nEl saldo debe ser numérico")

        except ClienteDuplicadoError as e:
            print(f"\n{e}")

        except DatosInvalidosError as e:
            print(f"\n{e}")

    # =========================
    # LISTAR CLIENTES
    # =========================
    def listar_clientes(self):

        clientes = self.gestor.clientes

        if len(clientes) == 0:
            print("\nNo hay clientes registrados")
            return

        print("\n========== CLIENTES ==========")

        for cliente in clientes:

            print(
                f"Código: {cliente.codigo} | "
                f"Nombre: {cliente.nombre} | "
                f"Email: {cliente.email} | "
                f"Saldo: {cliente.saldo}"
            )

    # =========================
    # BUSCAR CLIENTE
    # =========================
    def buscar_cliente(self):

        try:
            codigo = input("Código del cliente: ")

            cliente = self.gestor.buscar_cliente(codigo)

            print("\n========== CLIENTE ==========")
            print(f"Código: {cliente.codigo}")
            print(f"Nombre: {cliente.nombre}")
            print(f"Email: {cliente.email}")
            print(f"Saldo: {cliente.saldo}")

        except ClienteNoEncontradoError as e:
            print(f"\n{e}")

    # =========================
    # ELIMINAR CLIENTE
    # =========================
    def eliminar_cliente(self):

        try:
            codigo = input("Código del cliente a eliminar: ")

            self.gestor.eliminar_cliente(codigo)

            print("\nCliente eliminado correctamente")

        except ClienteNoEncontradoError as e:
            print(f"\n{e}")

    # =========================
    # EMITIR FACTURA
    # =========================
    def emitir_factura(self):

        try:
            codigo_cliente = input("Código cliente: ")

            cliente = self.gestor.buscar_cliente(codigo_cliente)

            numero_factura = int(input("Número factura: "))

            factura = self.gestor.emitir_factura(
                numero_factura,
                cliente
            )

            while True:

                descripcion = input(
                    "\nDescripción del item "
                    "(o 'fin' para terminar): "
                )

                if descripcion.lower() == "fin":
                    break

                precio = float(input("Precio: "))

                if precio <= 0:
                    raise DatosInvalidosError(
                        "El precio debe ser mayor a 0"
                    )

                factura.agregar_item(descripcion, precio)

            print("\nFactura creada correctamente")

        except ValueError:
            print("\nDatos numéricos inválidos")

        except ClienteNoEncontradoError as e:
            print(f"\n{e}")

        except FacturaError as e:
            print(f"\n{e}")

        except DatosInvalidosError as e:
            print(f"\n{e}")

    # =========================
    # MOSTRAR FACTURAS
    # =========================
    def mostrar_facturas(self):

        facturas = self.gestor.facturas

        if len(facturas) == 0:
            print("\nNo hay facturas registradas")
            return

        print("\n========== FACTURAS ==========")

        for factura in facturas:

            print(f"\nFactura Nº: {factura.numero}")
            print(f"Cliente: {factura.cliente.nombre}")

            for item in factura.items:
                print(
                    f" - {item['descripcion']} "
                    f"=> ${item['precio']}"
                )

            print(f"TOTAL: ${factura.calcular_total()}")


# =========================
# MAIN
# =========================

def main():

    menu = MenuFacturacion()
    menu.iniciar()


if __name__ == "__main__":
    main()