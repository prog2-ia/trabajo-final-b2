class Cliente:
    """Modelo de cliente del sistema de facturación."""

    def __init__(self, codigo, nombre, email, saldo=0.0):
        self.codigo = str(codigo).strip()
        self.nombre = str(nombre).strip()
        self.email = str(email).strip()
        self.saldo = float(saldo)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "email": self.email,
            "saldo": self.saldo,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("codigo", ""),
            data.get("nombre", ""),
            data.get("email", ""),
            data.get("saldo", 0.0),
        )

    def __str__(self):
        return (
            f"Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Email: {self.email} | Saldo: {self.saldo:.2f} €"
        )

    def __repr__(self):
        return f"Cliente(codigo={self.codigo!r}, nombre={self.nombre!r})"
