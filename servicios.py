from src.modelos import Cliente, Factura

class GestorFacturacion:
    def __init__(self):
        self.__clientes = [] # Atributo privado [4]
        self.__facturas = []

    def registrar_cliente(self, cliente: Cliente):
        self.__clientes.append(cliente)

    def emitir_factura(self, numero: int, cliente: Cliente) -> Factura:
        nueva_factura = Factura(numero, cliente)
        self.__facturas.append(nueva_factura)
        return nueva_factura

    def mostrar_reporte(self):
        print("\n--- REPORTE DE GESTIÓN ---")
        for cliente in self.__clientes:
            # Polimorfismo: se llama al método común de la interfaz [9, 14]
            print(cliente.generar_documento())
        
        total = sum(f.calcular_total() for f in self.__facturas)
        print(f"Total Ingresos: ${total:.2f}")

    @property
    def clientes(self): # Paréntesis corregidos en la version de antes me daba errores
        return self.__clientes
