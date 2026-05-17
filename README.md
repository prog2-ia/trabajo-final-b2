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
trabajo-final-b2/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── src/
    ├── __init__.py
    │
    ├── menu/
    │   ├── __init__.py
    │   └── menu_principal.py
    │
    ├── models/
    │   ├── __init__.py
    │   ├── cliente.py
    │   └── factura.py
    │
    ├── services/
    │   ├── __init__.py
    │   └── gestor_facturacion.py
    │
    ├── exceptions/
    │   ├── __init__.py
    │   └── excepciones.py
    │
    └── data/
        └── backups/
```

## Ejecución

Desde la carpeta principal del proyecto:

```bash
python main.py
```

No requiere librerías externas.

El proyecto se ha desarrollado en local, por lo que no queda reflejado todo el progreso en el repositorio. Aunque inicialmente estaba previsto realizarlo en pareja, finalmente mi compañero no pudo participar, por lo que el trabajo fue desarrollado individualmente. Debido a ello, utilicé parcialmente inteligencia artificial como apoyo en la revisión, organización y mejora del proyecto.
