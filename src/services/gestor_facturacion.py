import json
import pickle
from datetime import datetime
from pathlib import Path

from src.exceptions import (
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    DatosInvalidosError,
    FacturaError,
)
from src.models import Cliente, Factura


class GestorFacturacion:
    """Servicio principal para gestionar clientes, facturas y persistencia."""

    def __init__(self):
        self.clientes = []
        self.facturas = []

        self.base_dir = Path(__file__).resolve().parents[1]
        self.data_dir = self.base_dir / "data"
        self.backups_dir = self.data_dir / "backups"

        self.clientes_path = self.data_dir / "clientes.json"
        self.facturas_path = self.data_dir / "facturas.json"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)

        self.cargar_datos()

    def _validar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto recibido no es un cliente válido")

        if not cliente.codigo:
            raise DatosInvalidosError("El código del cliente no puede estar vacío")

        if not cliente.nombre:
            raise DatosInvalidosError("El nombre del cliente no puede estar vacío")

        if not cliente.email or "@" not in cliente.email:
            raise DatosInvalidosError("El email del cliente no es válido")

        if cliente.saldo < 0:
            raise DatosInvalidosError("El saldo inicial no puede ser negativo")

    def registrar_cliente(self, cliente):
        self._validar_cliente(cliente)

        if any(c.codigo == cliente.codigo for c in self.clientes):
            raise ClienteDuplicadoError(f"Ya existe un cliente con código {cliente.codigo}")

        self.clientes.append(cliente)
        self.guardar_datos()

    def buscar_cliente(self, codigo):
        codigo = str(codigo).strip()

        for cliente in self.clientes:
            if cliente.codigo == codigo:
                return cliente

        raise ClienteNoEncontradoError(f"No existe un cliente con código {codigo}")

    def eliminar_cliente(self, codigo):
        cliente = self.buscar_cliente(codigo)

        tiene_facturas = any(
            factura.cliente.codigo == cliente.codigo
            for factura in self.facturas
        )

        if tiene_facturas:
            raise FacturaError("No se puede eliminar un cliente con facturas asociadas")

        self.clientes.remove(cliente)
        self.guardar_datos()

    def emitir_factura(self, numero_factura, cliente):
        if any(factura.numero == int(numero_factura) for factura in self.facturas):
            raise FacturaError(f"Ya existe una factura con número {numero_factura}")

        factura = Factura(numero_factura, cliente)
        self.facturas.append(factura)
        self.guardar_datos()

        return factura

    def guardar_datos(self):
        with self.clientes_path.open("w", encoding="utf-8") as fichero:
            json.dump(
                [cliente.to_dict() for cliente in self.clientes],
                fichero,
                indent=4,
                ensure_ascii=False,
            )

        with self.facturas_path.open("w", encoding="utf-8") as fichero:
            json.dump(
                [factura.to_dict() for factura in self.facturas],
                fichero,
                indent=4,
                ensure_ascii=False,
            )

    def cargar_datos(self):
        self.clientes = []
        self.facturas = []

        if self.clientes_path.exists():
            try:
                with self.clientes_path.open("r", encoding="utf-8") as fichero:
                    datos_clientes = json.load(fichero)

                self.clientes = [
                    Cliente.from_dict(data)
                    for data in datos_clientes
                ]

            except (json.JSONDecodeError, TypeError):
                self.clientes = []

        if self.facturas_path.exists():
            try:
                with self.facturas_path.open("r", encoding="utf-8") as fichero:
                    datos_facturas = json.load(fichero)

                for data in datos_facturas:
                    codigo_cliente = data.get("codigo_cliente", "")

                    try:
                        cliente = self.buscar_cliente(codigo_cliente)
                        self.facturas.append(Factura.from_dict(data, cliente))
                    except ClienteNoEncontradoError:
                        continue

            except (json.JSONDecodeError, TypeError):
                self.facturas = []

    def calcular_total_facturado(self):
        return sum(factura.calcular_total() for factura in self.facturas)

    def mostrar_reporte(self):
        print("\n========== REPORTE GENERAL ==========")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Facturas registradas: {len(self.facturas)}")
        print(f"Total facturado: {self.calcular_total_facturado():.2f} €")
        print("=====================================")

    def exportar_reporte_txt(self):
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = self.data_dir / f"reporte_facturacion_{fecha}.txt"

        with ruta.open("w", encoding="utf-8") as fichero:
            fichero.write("REPORTE GENERAL DE FACTURACIÓN\n")
            fichero.write("================================\n")
            fichero.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            fichero.write(f"Clientes registrados: {len(self.clientes)}\n")
            fichero.write(f"Facturas registradas: {len(self.facturas)}\n")
            fichero.write(f"Total facturado: {self.calcular_total_facturado():.2f} €\n\n")

            fichero.write("CLIENTES\n")
            fichero.write("--------\n")

            for cliente in self.clientes:
                fichero.write(str(cliente) + "\n")

            fichero.write("\nFACTURAS\n")
            fichero.write("--------\n")

            for factura in self.facturas:
                fichero.write(str(factura) + "\n")

                for item in factura:
                    fichero.write(
                        f"  - {item['descripcion']}: {item['precio']:.2f} €\n"
                    )

        return ruta

    def crear_backup_pickle(self):
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = self.backups_dir / f"backup_facturacion_{fecha}.pickle"

        datos = {
            "clientes": [cliente.to_dict() for cliente in self.clientes],
            "facturas": [factura.to_dict() for factura in self.facturas],
            "fecha": datetime.now().isoformat(timespec="seconds"),
        }

        with ruta.open("wb") as fichero:
            pickle.dump(datos, fichero)

        return ruta

    def listar_backups(self):
        backups = []

        for ruta in sorted(self.backups_dir.glob("*.pickle"), reverse=True):
            backups.append(
                {
                    "nombre": ruta.name,
                    "ruta": ruta,
                    "tamano": ruta.stat().st_size,
                    "modificado": ruta.stat().st_mtime,
                }
            )

        return backups

    def restaurar_backup_pickle(self, ruta_backup):
        ruta_backup = Path(ruta_backup)

        if not ruta_backup.exists():
            raise FileNotFoundError(f"No existe el backup: {ruta_backup}")

        with ruta_backup.open("rb") as fichero:
            datos = pickle.load(fichero)

        self.clientes = [
            Cliente.from_dict(data)
            for data in datos.get("clientes", [])
        ]

        self.facturas = []

        for data in datos.get("facturas", []):
            try:
                cliente = self.buscar_cliente(data.get("codigo_cliente", ""))
                self.facturas.append(Factura.from_dict(data, cliente))
            except ClienteNoEncontradoError:
                continue

        self.guardar_datos()