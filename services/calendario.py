class Calendario:
    def generar_partidos(self, equipos):
        # Genera un calendario round-robin simple
        partidos = []
        for i in range(len(equipos)):
            for j in range(i + 1, len(equipos)):
                partidos.append((equipos[i], equipos[j]))
        return partidos
