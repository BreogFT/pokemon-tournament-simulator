class Division:
    def __init__(self, nombre, equipos):
        self.nombre = nombre
        self.equipos = equipos

    def __repr__(self):
        return f"<Division {self.nombre}>"
