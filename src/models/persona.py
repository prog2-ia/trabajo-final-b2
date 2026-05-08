class Persona:

    def __init__(self, id_persona, nombre, edad):
        self.id = id_persona
        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Edad: {self.edad}"