class Liga:
    def __init__(self, nombre, divisiones):
        self.nombre = nombre
        self.divisiones = divisiones

    def __repr__(self):
        return f"<Liga {self.nombre}>"
