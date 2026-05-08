from src.base import EntidadNegocio

class Cliente(EntidadNegocio):
    def __init__(self, id_entidad: str, nombre: str, email: str):
        super().__init__(id_entidad, nombre) # Uso de super() [8]
        self.__email = email  # Encapsulamiento privado [4]
        self.__saldo_pendiente = 0.0

    @property
    def saldo(self) -> float:
        return self.__saldo_pendiente

    @saldo.setter
    def saldo(self, valor: float):
        """Validación de datos en el setter [5, 7]."""
        if valor >= 0:
            self.__saldo_pendiente = valor
        else:
            print("Error: El saldo no puede ser negativo.")

    def generar_documento(self) -> str:
        """Implementación polimórfica [5, 9]."""
        # Se corrigió el acceso al identificador
        return f"Cliente: {self.nombre} (ID: {self.identificador}) - Email: {self.__email}"

    def __str__(self) -> str:
        """Representación informal para el usuario [10, 11]."""
        return f"Cliente: {self.nombre} | Saldo: ${self.__saldo_pendiente:.2f}"

class Factura:
    def __init__(self, numero: int, cliente: Cliente):
        self.numero = numero
        self.cliente = cliente
        self.__items = []

    def agregar_item(self, item: str, precio: float):
        self.__items.append({"item": item, "precio": precio})

    def __len__(self) -> int:
        """Sobrecarga de len() para contar productos [12, 13]."""
        return len(self.__items)

    def calcular_total(self) -> float:
        return sum(item["precio"] for item in self.__items)