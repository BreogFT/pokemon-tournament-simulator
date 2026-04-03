import random

class Simulacion:
    def simular_partido(self, equipo_a, equipo_b):
        # Simulación simple basada en azar
        ganador = random.choice([equipo_a, equipo_b])
        return ganador
