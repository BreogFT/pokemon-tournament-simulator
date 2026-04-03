class Pokemon:
    def __init__(self, nombre, tipo, nivel):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel

    def __repr__(self):
        return f"<Pokemon {self.nombre} (Nv {self.nivel})>"
