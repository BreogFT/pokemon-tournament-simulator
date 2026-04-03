class Equipo:
    def __init__(self, nombre, entrenador):
        self.nombre = nombre
        self.entrenador = entrenador

    def __repr__(self):
        return f"<Equipo {self.nombre}>"
