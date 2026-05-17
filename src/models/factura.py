from functools import total_ordering
from src.exceptions import DatosInvalidosError


@total_ordering
class Factura:
    """
    Modelo de factura.

    Implementa contenidos del tema de sobrecarga de operadores:
    - factura + item: devuelve una nueva factura con el item añadido.
    - factura += item: modifica la factura actual.
    - item + factura: devuelve una nueva factura con el item al principio.
    - factura[i]: permite leer items por índice o slice.
    - factura[i] = item: permite modificar items por índice.
    - comparaciones entre facturas por importe total.
    """

    def __init__(self, numero, cliente, items=None):
        self.numero = int(numero)
        self.cliente = cliente
        self.items = []
        for item in items or []:
            self.items.append(self._normalizar_item(item))

    @staticmethod
    def _normalizar_item(item):
        """
        Convierte un item a un diccionario homogéneo.
        Acepta:
        - dict: {"descripcion": "...", "precio": 10.0}
        - tuple/list: ("descripcion", 10.0)
        """
        if isinstance(item, dict):
            descripcion = item.get("descripcion", "")
            precio = item.get("precio", 0)
        elif isinstance(item, (tuple, list)) and len(item) == 2:
            descripcion, precio = item
        else:
            raise DatosInvalidosError(
                "El item debe ser un diccionario o una tupla/lista (descripcion, precio)"
            )

        descripcion = str(descripcion).strip()
        if not descripcion:
            raise DatosInvalidosError("La descripción del item no puede estar vacía")

        try:
            precio = float(precio)
        except (TypeError, ValueError) as exc:
            raise DatosInvalidosError("El precio debe ser numérico") from exc

        if precio <= 0:
            raise DatosInvalidosError("El precio debe ser mayor a 0")

        return {"descripcion": descripcion, "precio": precio}

    def agregar_item(self, descripcion, precio):
        self.items.append(self._normalizar_item((descripcion, precio)))

    def calcular_total(self):
        return sum(item["precio"] for item in self.items)

    def copia(self):
        return Factura(self.numero, self.cliente, [item.copy() for item in self.items])

    # ---------- Sobrecarga de operadores matemáticos ----------
    def __add__(self, other):
        nueva_factura = self.copia()
        nueva_factura.items.append(self._normalizar_item(other))
        return nueva_factura

    def __iadd__(self, other):
        self.items.append(self._normalizar_item(other))
        return self

    def __radd__(self, other):
        nueva_factura = self.copia()
        nueva_factura.items.insert(0, self._normalizar_item(other))
        return nueva_factura

    # ---------- Indexación y división con [] ----------
    def __getitem__(self, indice):
        return self.items[indice]

    def __setitem__(self, indice, valor):
        if isinstance(indice, slice):
            self.items[indice] = [self._normalizar_item(item) for item in valor]
        else:
            self.items[indice] = self._normalizar_item(valor)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    # ---------- Comparadores por total ----------
    def __eq__(self, other):
        if not isinstance(other, Factura):
            return NotImplemented
        return self.calcular_total() == other.calcular_total()

    def __lt__(self, other):
        if not isinstance(other, Factura):
            return NotImplemented
        return self.calcular_total() < other.calcular_total()

    def to_dict(self):
        return {
            "numero": self.numero,
            "codigo_cliente": self.cliente.codigo,
            "items": [item.copy() for item in self.items],
            "total": self.calcular_total(),
        }

    @classmethod
    def from_dict(cls, data, cliente):
        return cls(data.get("numero", 0), cliente, data.get("items", []))

    def __str__(self):
        return (
            f"Factura Nº {self.numero} | Cliente: {self.cliente.nombre} | "
            f"Items: {len(self.items)} | Total: {self.calcular_total():.2f} €"
        )

    def __repr__(self):
        return f"Factura(numero={self.numero!r}, cliente={self.cliente.codigo!r})"
