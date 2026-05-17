# Proyecto de Programación II - Gestor de facturación y clientes

## Descripción

Aplicación de consola en Python para gestionar clientes, emitir facturas, añadir conceptos, consultar reportes y crear copias de seguridad.

## Funcionalidades principales

1. Registrar clientes.
2. Listar clientes.
3. Buscar clientes.
4. Eliminar clientes sin facturas asociadas.
5. Emitir facturas.
6. Añadir conceptos a facturas.
7. Mostrar facturas.
8. Mostrar reporte general.
9. Guardar y cargar datos en ficheros JSON.
10. Exportar reporte a fichero TXT.
11. Crear y restaurar backups binarios con pickle.
12. Listar backups guardados en el directorio de datos.
13. Demostrar operadores especiales aplicados a la clase `Factura`.

## Estructura del proyecto

```text
trabajo-final-b2-main/
├── main.py
├── README.md
├── requirements.txt
└── src/
    ├── data/
    │   ├── clientes.json
    │   ├── facturas.json
    │   └── backups/
    ├── exceptions/
    ├── menu/
    ├── models/
    └── services/
```

## Ejecución

Desde la carpeta principal del proyecto:

```bash
python main.py
```

No requiere librerías externas.

## Ejemplo de uso de operadores especiales

```python
from src.models import Cliente, Factura

cliente = Cliente("C001", "Cliente de prueba", "cliente@email.com")
factura = Factura(1, cliente)

factura += ("Concepto 1", 100)       # __iadd__
factura2 = factura + ("Concepto 2", 50)  # __add__
factura3 = ("Concepto 0", 25) + factura  # __radd__

print(factura[0])                    # __getitem__
factura[0] = ("Concepto modificado", 120)  # __setitem__
print(len(factura))                  # __len__
print(factura < factura2)            # __lt__
```
