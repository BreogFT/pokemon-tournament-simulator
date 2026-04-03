class Entrenador:
    def __init__(self, nombre, equipo):
        self.nombre = nombre
        self.equipo = equipo  # lista de Pokémon

    def __repr__(self):
        return f"<Entrenador {self.nombre}>"
