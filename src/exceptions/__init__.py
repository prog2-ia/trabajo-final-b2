class ClienteDuplicadoError(Exception):
    """Se lanza cuando se intenta registrar un cliente ya existente."""


class ClienteNoEncontradoError(Exception):
    """Se lanza cuando no se encuentra un cliente."""


class FacturaError(Exception):
    """Se lanza cuando existe un error relacionado con una factura."""


class DatosInvalidosError(Exception):
    """Se lanza cuando los datos introducidos no son válidos."""
