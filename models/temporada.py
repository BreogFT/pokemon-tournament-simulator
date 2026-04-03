class Temporada:
    def __init__(self, numero, liga):
        self.numero = numero
        self.liga = liga

    def __repr__(self):
        return f"<Temporada {self.numero}>"
