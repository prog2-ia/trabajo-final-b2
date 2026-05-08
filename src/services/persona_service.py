from models.persona import Persona
from exceptions.persona_no_encontrada import PersonaNoEncontradaException
from exceptions.datos_invalidos import DatosInvalidosException
from exceptions.lista_vacia import ListaVaciaException


class PersonaService:

    def __init__(self):
        self.personas = []
        self.contador_id = 1

    def agregar_persona(self, nombre, edad):

        if not nombre.strip():
            raise DatosInvalidosException("El nombre no puede estar vacío")

        if edad < 0 or edad > 120:
            raise DatosInvalidosException("Edad inválida")

        persona = Persona(self.contador_id, nombre, edad)
        self.personas.append(persona)

        self.contador_id += 1

    def listar_personas(self):

        if len(self.personas) == 0:
            raise ListaVaciaException("No hay personas registradas")

        return self.personas

    def buscar_por_id(self, id_persona):

        for persona in self.personas:
            if persona.id == id_persona:
                return persona

        raise PersonaNoEncontradaException(
            f"No existe una persona con ID {id_persona}"
        )

    def eliminar_persona(self, id_persona):

        persona = self.buscar_por_id(id_persona)
        self.personas.remove(persona)
