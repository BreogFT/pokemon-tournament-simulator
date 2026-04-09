"""
ligas.py
========
Módulo encargado de la simulación de ligas Pokémon. 
Gestiona la creación de calendarios round-robin, la simulación de jornadas 
y el mantenimiento de la tabla de clasificación.
"""

import random

class Liga:
    """
    Representa una liga divisional dentro del simulador.
    """
    def __init__(self, nombre: str, equipos: list, motor_combate, type_chart: dict):
        """
        Inicia la liga.

        Parameters
        ----------
        nombre : str
            Nombre de la liga (ej. "Norte División A").
        equipos : list
            Lista de entrenadores (objetos/diccionarios) que participan.
        motor_combate : module
            Módulo o clase que contiene la lógica de simulación de combates.
        type_chart : dict
            Tabla de tipos para los combates.
        """
        self.nombre = nombre
        self.equipos = equipos
        self.motor_combate = motor_combate
        self.type_chart = type_chart
        self.jornadas = []
        
        # Inicializar clasificación
        self.clasificacion = {
            e["id"]: {
                "nombre": e["nombre"],
                "puntos": 0,
                "goles_favor": 0,
                "goles_contra": 0,
                "partidos_jugados": 0,
                "victorias": 0,
                "empates": 0, # Aunque el sistema de ruleta suele ser binario, lo dejamos por estructura
                "derrotas": 0
            } for e in self.equipos
        }

    def generar_calendario(self):
        """
        Construye un calendario round-robin (todos contra todos) usando el método del círculo.
        """
        n = len(self.equipos)
        if n < 2:
            return

        equipos_temp = list(self.equipos)
        
        # Si es impar, añadir un "BYE" ficticio
        if n % 2 != 0:
            equipos_temp.append(None)
            n += 1

        rondas = n - 1
        partidos_por_ronda = n // 2
        
        self.jornadas = []

        for r in range(rondas):
            jornada = []
            for i in range(partidos_por_ronda):
                e1 = equipos_temp[i]
                e2 = equipos_temp[n - 1 - i]
                
                if e1 is not None and e2 is not None:
                    jornada.append((e1, e2))
            
            self.jornadas.append(jornada)
            
            # Rotar equipos (manteniendo el primero fijo)
            equipos_temp = [equipos_temp[0]] + [equipos_temp[-1]] + equipos_temp[1:-1]

    def simular_partido(self, equipo1: dict, equipo2: dict):
        """
        Simula un combate entre dos entrenadores y actualiza la clasificación.
        
        El sistema de combate actual (combate.py) devuelve 'A' o 'B'.
        Usamos simular_combate_liga que es el estándar 3vs3 para ligas.
        """
        # El motor_combate debe tener el método simular_combate_liga (o simular_combate si así lo pide la interfaz)
        # Adaptamos para que llame a simular_combate_liga segun combate.py
        try:
            resultado = self.motor_combate.simular_combate_liga(equipo1, equipo2, self.type_chart)
        except AttributeError:
            # Fallback por si se inyecta un motor con nombre genérico
            resultado = self.motor_combate.simular_combate(equipo1, equipo2, self.type_chart)

        stats1 = self.clasificacion[equipo1["id"]]
        stats2 = self.clasificacion[equipo2["id"]]
        
        stats1["partidos_jugados"] += 1
        stats2["partidos_jugados"] += 1

        if resultado == 'A':
            stats1["puntos"] += 3
            stats1["victorias"] += 1
            stats2["derrotas"] += 1
            # "Goles" en este contexto pueden ser vidas restantes o simplemente un marcador simbólico
            # Usaremos un marcador fijo 1-0 para la clasificación si no hay marcador de vidas
            stats1["goles_favor"] += 1
            stats2["goles_contra"] += 1
        else:
            stats2["puntos"] += 3
            stats2["victorias"] += 1
            stats1["derrotas"] += 1
            stats2["goles_favor"] += 1
            stats1["goles_contra"] += 1

    def simular_jornada(self, numero_jornada: int):
        """
        Simula todos los partidos de una jornada específica.
        """
        if numero_jornada < 0 or numero_jornada >= len(self.jornadas):
            return
        
        jornada = self.jornadas[numero_jornada]
        resultados_jornada = []

        for e1, e2 in jornada:
            ganador = self.simular_partido(e1, e2)
            resultados_jornada.append({
                "local": e1["nombre"],
                "visitante": e2["nombre"]
            })
            
        return resultados_jornada

    def simular_liga(self):
        """
        Orquesta la simulación completa de la liga.
        """
        self.generar_calendario()
        
        resultados_totales = []
        for i in range(len(self.jornadas)):
            res = self.simular_jornada(i)
            resultados_totales.append({
                "jornada": i + 1,
                "partidos": res
            })
            
        # Ordenar clasificación
        # 1. Puntos
        # 2. Diferencia de goles (favor - contra)
        # 3. Goles a favor
        tabla_ordenada = sorted(
            self.clasificacion.values(),
            key=lambda x: (x["puntos"], (x["goles_favor"] - x["goles_contra"]), x["goles_favor"]),
            reverse=True
        )
        
        return {
            "liga": self.nombre,
            "resultados": resultados_totales,
            "clasificacion_final": tabla_ordenada
        }
