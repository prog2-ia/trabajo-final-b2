from abc import ABC, abstractmethod
# Este codigo establece la aquitectura base oara cualquier objeto que represente un negocio. Al usar ABC, definimos un molde que no se puede
# usar de por si, sirve para que otras clases mas especificas como cliente o proveedor hereden su estructura

# Lo mas importante es el @abstractmethod , que funciona como un contrato en obligatorio, cualquier clase hija tienen que implementar su 
# propia version gernerar_documento o el codigo dara error
class EntidadNegocio(ABC):
    """Clase Base Abstracta (ABC) para entidades del sistema [3]."""
    
    def __init__(self, id_entidad: str, nombre: str):
        self._id_entidad = id_entidad  # Atributo protegido [4]
        self.nombre = nombre

    @abstractmethod
    def generar_documento(self) -> str:
        """Método abstracto para obligar al polimorfismo [5, 6]."""
        pass

    @property
    def identificador(self) -> str:
        """Propiedad para acceder al ID protegido [7]."""
        return self._id_entidad
