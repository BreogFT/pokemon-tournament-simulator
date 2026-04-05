"""
progresion.py
=============
Módulo encargado de gestionar la línea evolutiva y progresión de los Pokémon de
los entrenadores en el simulador de torneos.
"""

import random


def puede_evolucionar(pokemon_id: str, entrenador: dict, pokedex: dict, temporada: int) -> list[str]:
    """
    Comprueba si el Pokémon tiene evoluciones disponibles y válidas, excluyendo megas.

    Parameters
    ----------
    pokemon_id : str
        ID interno del Pokémon a evaluar.
    entrenador : dict
        Datos del entrenador (por si hubiera restricciones en un futuro).
    pokedex : dict
        Pokédex indexada por ID interno.
    temporada : int
        Temporada actual.

    Returns
    -------
    list[str]
        Lista de IDs internos de las evoluciones válidas.
    """
    entry = pokedex.get(pokemon_id)
    if not entry:
        return []

    evos = entry.get("evoluciones", [])
    evos_validas = []

    for evo_id in evos:
        evo_entry = pokedex.get(evo_id)
        if not evo_entry:
            continue
        
        # Filtrar megas (formas que contienen "mega") u otras formas no estándar si es necesario
        forma = evo_entry.get("forma", "").lower()
        if "mega" in forma or "gigamax" in forma:
            continue
            
        evos_validas.append(evo_id)

    return evos_validas


def evolucion_aleatoria(entrenador: dict, pokedex: dict, temporada: int) -> bool:
    """
    Selecciona aleatoriamente un Pokémon del equipo que pueda evolucionar, y lo evoluciona.

    Parameters
    ----------
    entrenador : dict
        Entrenador a cuyo equipo se aplicará la evolución in-place.
    pokedex : dict
        Pokédex indexada.
    temporada : int
        Temporada actual.

    Returns
    -------
    bool
        True si se produjo alguna evolución, False si ningún Pokémon podía evolucionar.
    """
    equipo = (
        entrenador["equipo_completo"]
        if entrenador.get("equipo_completo")
        else list(entrenador.get("pokemon_fijos", []))
    )

    if not equipo:
        return False

    # Buscar candidatos viables
    candidatos_evolucion = []
    for pid in equipo:
        evos_validas = puede_evolucionar(pid, entrenador, pokedex, temporada)
        if evos_validas:
            candidatos_evolucion.append((pid, evos_validas))

    if not candidatos_evolucion:
        return False

    # Seleccionar un Pokémon al azar de los que pueden evolucionar
    elegido_id, evos_posibles = random.choice(candidatos_evolucion)
    
    # Seleccionar la evolución al azar (útil para casos como Eevee)
    nueva_evo_id = random.choice(evos_posibles)

    # Aplicar evolución
    # TODO: conservar mejoras/objetos cuando estén implementados
    idx = equipo.index(elegido_id)
    equipo[idx] = nueva_evo_id

    # Asegurar que el entrenador tiene la lista inicializada si usó pokemon_fijos
    entrenador["equipo_completo"] = equipo

    return True


def evolucion_selectiva(entrenador: dict, pokedex: dict, temporada: int, pokemon_id: str) -> bool:
    """
    Aplica la evolución a un Pokémon concreto elegido por el usuario.

    Parameters
    ----------
    entrenador : dict
        Entrenador del equipo.
    pokedex : dict
        Pokédex indexada.
    temporada : int
        Temporada actual.
    pokemon_id : str
        ID del Pokémon a evolucionar.

    Returns
    -------
    bool
        True si evolucionó exitosamente, False de lo contrario.
    """
    equipo = (
        entrenador["equipo_completo"]
        if entrenador.get("equipo_completo")
        else list(entrenador.get("pokemon_fijos", []))
    )

    if pokemon_id not in equipo:
        return False

    evos_validas = puede_evolucionar(pokemon_id, entrenador, pokedex, temporada)
    if not evos_validas:
        return False

    nueva_evo_id = random.choice(evos_validas)
    
    idx = equipo.index(pokemon_id)
    equipo[idx] = nueva_evo_id
    entrenador["equipo_completo"] = equipo

    return True


def aplicar_evoluciones_generales(entrenadores: dict, pokedex: dict, temporada: int) -> None:
    """
    Aplica una evolución aleatoria a todos los entrenadores del simulador.

    Parameters
    ----------
    entrenadores : dict
        Diccionario principal de entrenadores, o lista con los perfiles.
        Asumimos iteración sobre los valores del diccionario por ID rápido
        revisando que contengan los datos.
    pokedex : dict
        Pokédex indexada por ID interno.
    temporada : int
        Temporada actual.
    """
    # Si recibimos el dict principal que contiene la lista 'entrenadores', usamos eso
    lista_entrenadores = entrenadores.get("entrenadores", [])
    if isinstance(entrenadores, list):
        lista_entrenadores = entrenadores

    for entrenador in lista_entrenadores:
        evolucion_aleatoria(entrenador, pokedex, temporada)
