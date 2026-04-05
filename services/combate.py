"""
combate.py
==========
Módulo para gestionar las lógicas de combate entre Pokémon y entre entrenadores
(ligas y torneos) usando un sistema probabilístico de ruleta basado en tabla de tipos.
"""

import random

# Placeholder para la tabla de tipos.
# Puede sustituirse en el futuro cargando un JSON externo.
# Estructura: typeChart[tipo_atacante][tipo_defensor] -> multiplier
DEFAULT_TYPE_CHART = {
    # Aquí irá la tabla real más adelante.
}

def contar_matchups(types_att: list[str], types_def: list[str], type_chart: dict) -> tuple[int, int]:
    """
    Cuenta el número de ventajas y resistencias entre los tipos del atacante 
    y los tipos del defensor.

    Parameters
    ----------
    types_att : list[str]
        Tipos del Pokémon atacante.
    types_def : list[str]
        Tipos del Pokémon defensor.
    type_chart : dict
        Tabla de multiplicadores type_chart[att][def].

    Returns
    -------
    tuple[int, int]
        (ventajas, resistencias)
    """
    ventajas = 0
    resistencias = 0

    for t_att in types_att:
        # Prevenimos KeyError si la tabla aún no está completa.
        if t_att not in type_chart:
            continue
            
        for t_def in types_def:
            mult = type_chart[t_att].get(t_def, 1.0)
            if mult > 1.0:
                ventajas += 1
            elif mult < 1.0:  # 0.5 o 0.0
                resistencias += 1

    return ventajas, resistencias


def decidir_probabilidades(types_a: list[str], types_b: list[str], type_chart: dict) -> tuple[float, float]:
    """
    Decide la probabilidad de victoria en la ruleta basándose en las ventajas 
    y resistencias de tipos netas entre dos Pokémon.

    Parameters
    ----------
    types_a : list[str]
        Tipos del Pokémon A.
    types_b : list[str]
        Tipos del Pokémon B.
    type_chart : dict
        Tabla de multiplicadores.

    Returns
    -------
    tuple[float, float]
        (prob_A, prob_B) donde prob_A + prob_B == 1
    """
    ventajas_a, resistencias_a = contar_matchups(types_a, types_b, type_chart)
    ventajas_b, resistencias_b = contar_matchups(types_b, types_a, type_chart)

    net_ventaja = ventajas_a - ventajas_b
    
    # Tablas de probabilidad preestablecidas
    prob_ventaja_map = {1: 0.65, 2: 0.75, 3: 0.85}
    prob_resistencia_map = {1: 0.60, 2: 0.65, 3: 0.70}

    def get_prob_ventaja(v: int) -> float:
        if v >= 4: return 0.95
        return prob_ventaja_map.get(v, 0.5)

    def get_prob_resistencia(r: int) -> float:
        if r >= 4: return 0.75
        return prob_resistencia_map.get(r, 0.5)

    if net_ventaja > 0:
        pA = get_prob_ventaja(net_ventaja)
        return pA, 1.0 - pA
    elif net_ventaja < 0:
        pB = get_prob_ventaja(abs(net_ventaja))
        return 1.0 - pB, pB
    else:  # net_ventaja == 0
        if resistencias_a > resistencias_b:
            # A tiene más resistencias a favor (menos daño recibido) => más ventaja real
            diff_res = resistencias_a - resistencias_b
            pA = get_prob_resistencia(diff_res)
            return pA, 1.0 - pA
        elif resistencias_b > resistencias_a:
            diff_res = resistencias_b - resistencias_a
            pB = get_prob_resistencia(diff_res)
            return 1.0 - pB, pB
        else:
            return 0.5, 0.5


def tirar_ruleta(pA: float, pB: float) -> str:
    """
    Lanza una tirada probabilística para decidir el ganador del turno.

    Returns
    -------
    str
        'A' o 'B'
    """
    resultado = random.random()
    if resultado < pA:
        return 'A'
    return 'B'


def simular_duelo(pokemon_a: dict, pokemon_b: dict, type_chart: dict) -> str:
    """
    Simula un duelo 1vs1 calculando probabilidades y tirando la ruleta hasta
    que uno de los Pokémon se queda sin vidas.

    Parameters
    ----------
    pokemon_a : dict
        Dato temporal con "tipos" y "vidas" del Pokémon A.
    pokemon_b : dict
        Dato temporal con "tipos" y "vidas" del Pokémon B.
    type_chart : dict
        Tabla de tipos.

    Returns
    -------
    str
        El ganador ('A' o 'B').
    """
    tipos_a = pokemon_a.get("tipos", [])
    tipos_b = pokemon_b.get("tipos", [])
    
    vidas_a = pokemon_a.get("vidas", 1)
    vidas_b = pokemon_b.get("vidas", 1)

    pA, pB = decidir_probabilidades(tipos_a, tipos_b, type_chart)

    while vidas_a > 0 and vidas_b > 0:
        ganador_turno = tirar_ruleta(pA, pB)
        if ganador_turno == 'A':
            vidas_b -= 1
        else:
            vidas_a -= 1

    # Actualizamos las vidas en los objetos por si necesitan registrar el daño residual
    pokemon_a["vidas"] = vidas_a
    pokemon_b["vidas"] = vidas_b

    return 'A' if vidas_a > 0 else 'B'


def _simular_enfrentamiento_equipos(equipo_a: list[dict], equipo_b: list[dict], type_chart: dict) -> str:
    """
    Función auxiliar para procesar batallas de equipos uno a uno.
    Los parámetros deben venir ya barajados y recortados al tamaño necesario.

    Returns
    -------
    str
        'A' o 'B' dependiendo de quién gane la batalla de equipos completa.
    """
    # Índices del Pokémon activo
    idx_a = 0
    idx_b = 0
    
    while idx_a < len(equipo_a) and idx_b < len(equipo_b):
        pkm_a = equipo_a[idx_a]
        pkm_b = equipo_b[idx_b]
        
        ganador_duelo = simular_duelo(pkm_a, pkm_b, type_chart)
        
        if ganador_duelo == 'A':
            idx_b += 1  # El b ha perdido sus vidas
        else:
            idx_a += 1  # El a ha perdido sus vidas

    return 'A' if idx_a < len(equipo_a) else 'B'


def simular_combate_liga(entrenador_a: dict, entrenador_b: dict, type_chart: dict) -> str:
    """
    Simula un combate 3vs3 para la fase de ligas.

    Parameters
    ----------
    entrenador_a, entrenador_b : dict
        Deben incluir una lista "equipo_batalla" con los Pokémon procesados (tipos, vidas),
        típicamente se construyen a partir del ID del equipo_completo cruzado con la Pokédex.

    Returns
    -------
    str
        Ganador: 'A' o 'B'
    """
    # Tomamos como máximo 3 Pokémon del equipo (asumimos que en el nivel superior ya
    # se han mapeado a la estructura {"tipos": [...], "vidas": N}).
    # Para ser purista, random.sample baraja y selecciona de golpe.
    # Pero si recibimos menos de 3 lo toleramos.
    roster_a = entrenador_a.get("equipo_batalla", [])
    roster_b = entrenador_b.get("equipo_batalla", [])

    k_a = min(3, len(roster_a))
    k_b = min(3, len(roster_b))

    if k_a == 0: return 'B'
    if k_b == 0: return 'A'

    # Copiamos para no mutar irreversiblemente las vidas globales si aplica
    # aunque 'vidas' ya lo mutamos en simular_duelo, la lista es una nueva instanciación de punteros.
    # Para que las vidas funcionen bien, requerimos copias de los diccionarios, 
    # ya que simular_duelo decrementa las vidas in-place.
    equipo_a_copia = [{"tipos": list(p["tipos"]), "vidas": p["vidas"]} for p in random.sample(roster_a, k_a)]
    equipo_b_copia = [{"tipos": list(p["tipos"]), "vidas": p["vidas"]} for p in random.sample(roster_b, k_b)]

    return _simular_enfrentamiento_equipos(equipo_a_copia, equipo_b_copia, type_chart)


def simular_combate_torneo(entrenador_a: dict, entrenador_b: dict, type_chart: dict) -> str:
    """
    Simula un combate completo con todo el equipo disponible (hasta 6vs6) 
    para la fase de torneo mundial.

    Parameters
    ----------
    entrenador_a, entrenador_b : dict
        Mismo formato que liga, "equipo_batalla".

    Returns
    -------
    str
        Ganador: 'A' o 'B'
    """
    roster_a = entrenador_a.get("equipo_batalla", [])
    roster_b = entrenador_b.get("equipo_batalla", [])

    if not roster_a: return 'B'
    if not roster_b: return 'A'

    # Copiamos y barajamos todos. Note que random.sample(x, len(x)) es equivalente a barajar
    equipo_a_copia = [{"tipos": list(p["tipos"]), "vidas": p["vidas"]} for p in random.sample(roster_a, len(roster_a))]
    equipo_b_copia = [{"tipos": list(p["tipos"]), "vidas": p["vidas"]} for p in random.sample(roster_b, len(roster_b))]

    return _simular_enfrentamiento_equipos(equipo_a_copia, equipo_b_copia, type_chart)
