"""
generador_equipos.py
====================
Módulo encargado de la lógica de generación y evolución de equipos de entrenadores
a lo largo de las temporadas del simulador de torneos Pokémon.

Estructura de IDs de Pokémon (pokedex.json):
    "<numero>-<forma_idx>"  →  ej. "4-00" (Charmander normal), "6-01" (Charizard mega-x)

Campos relevantes de cada entrada en pokedex.json:
    - id         : str  → identificador interno único
    - numero     : int  → número de la especie (mismo para todas sus formas)
    - forma      : str  → "normal", "mega", "mega x", "mega y", "alola", "hisui", …
    - categorias : list → puede incluir "legendario", "primera_evolucion", etc.
    - evoluciones: list → lista de IDs a los que puede evolucionar
"""

import json
import random


# ---------------------------------------------------------------------------
# 1. Carga de datos
# ---------------------------------------------------------------------------

def cargar_datos() -> tuple[dict, dict]:
    """
    Lee y devuelve los datos de la Pokédex y de los entrenadores.

    Returns
    -------
    pokedex : dict
        Diccionario indexado por ID interno ("4-00", "6-01", …) con todos
        los datos de cada entrada de la Pokédex.
    entrenadores : dict
        Diccionario con la clave "entrenadores" tal y como está en el JSON,
        más un índice auxiliar indexado por "id" de entrenador para acceso rápido.

    Raises
    ------
    FileNotFoundError
        Si alguno de los archivos JSON no se encuentra en la ruta esperada.
    """
    with open("data/pokedex.json", encoding="utf-8") as f:
        raw_pokedex: list[dict] = json.load(f)

    # Indexamos la Pokédex por ID interno para acceso O(1)
    pokedex: dict[str, dict] = {entry["id"]: entry for entry in raw_pokedex}

    with open("data/entrenadores.json", encoding="utf-8") as f:
        raw_entrenadores: dict = json.load(f)

    # Índice rápido por id de entrenador
    entrenadores_idx: dict[str, dict] = {
        e["id"]: e for e in raw_entrenadores["entrenadores"]
    }
    entrenadores = {
        **raw_entrenadores,
        "_idx": entrenadores_idx,
    }

    return pokedex, entrenadores


# ---------------------------------------------------------------------------
# 2. Equipo inicial
# ---------------------------------------------------------------------------

def generar_equipo_inicial(entrenador: dict) -> list[str]:
    """
    Devuelve el equipo inicial de un entrenador, compuesto únicamente por
    sus Pokémon fijos.

    No añade Pokémon adicionales, no genera evoluciones ni aplica mejoras.

    Parameters
    ----------
    entrenador : dict
        Entrada de un entrenador tal y como aparece en entrenadores.json.

    Returns
    -------
    list[str]
        Lista de IDs internos de los Pokémon fijos del entrenador.
        Ejemplo: ["4-00", "131-00"]
    """
    return list(entrenador["pokemon_fijos"])


# ---------------------------------------------------------------------------
# 3. Candidatos para captura
# ---------------------------------------------------------------------------

def generar_candidatos_captura(entrenador: dict, pokedex: dict[str, dict], num_candidatos: int = 3) -> list[str]:
    """
    Genera una lista de N Pokémon candidatos aleatorios que el entrenador
    podría capturar, respetando las siguientes restricciones:

    - No se incluyen megas (forma que contiene la cadena "mega").

    Parameters
    ----------
    entrenador : dict
        Entrada del entrenador. Se consultan "equipo_completo" y "pokemon_fijos".
    pokedex : dict[str, dict]
        Pokédex indexada por ID interno.

    Returns
    -------
    list[str]
        Lista de exactamente `num_candidatos` IDs internos candidatos.
        Si no hay suficientes candidatos válidos devuelve los que haya
        (puede ser una lista con menos de tres elementos).
    """
    def _es_candidato_valido(entry: dict) -> bool:
        """Aplica todos los filtros de elegibilidad."""
        # Filtro 1: no incluir megas
        if "mega" in entry.get("forma", "").lower():
            return False
        return True

    candidatos_validos: list[str] = [
        entry["id"]
        for entry in pokedex.values()
        if _es_candidato_valido(entry)
    ]

    # Devolvemos los candidatos aleatorios sin repetición
    cantidad = min(num_candidatos, len(candidatos_validos))
    return random.sample(candidatos_validos, cantidad)


# ---------------------------------------------------------------------------
# 4. Evaluación de captura
# ---------------------------------------------------------------------------

def evaluar_captura(entrenador: dict, candidato: str, pokedex: dict[str, dict], temporada: int) -> bool:
    """
    Determina si el entrenador captura el Pokémon candidato en una temporada dada,
    según las reglas de fases evolutivas y la restricción especial para legendarios.

    Parameters
    ----------
    entrenador : dict
        Entrada del entrenador.
    candidato : str
        ID interno del Pokémon candidato a capturar.
    pokedex : dict[str, dict]
        Pokédex indexada por ID interno para consultar categorías.
    temporada : int
        Número de temporada actual (ligas + torneos mundiales transcurridos).

    Returns
    -------
    bool
        True si cumple los requisitos para ser capturado, False en caso contrario.
    """
    entry = pokedex.get(candidato)
    if not entry:
        return False
        
    categorias_candidato = entry.get("categorias", [])
    
    # 1. Reglas generales por temporada
    es_capturable_por_temporada = False
    
    if "primera_evolucion" in categorias_candidato or "fase_unica" in categorias_candidato:
        es_capturable_por_temporada = True
    elif "segunda_evolucion" in categorias_candidato:
        if temporada >= 3:
            es_capturable_por_temporada = True
    elif "tercera_evolucion" in categorias_candidato:
        if temporada >= 5:
            es_capturable_por_temporada = True
            
    if not es_capturable_por_temporada:
        return False
        
    # 2. Determinar categorías especiales del candidato
    es_legendario = "legendario" in categorias_candidato
    es_paradoja = "paradoja" in categorias_candidato
    es_ultraente = "ultraente" in categorias_candidato
    es_fase_unica_o_final = "fase_unica" in categorias_candidato or "fase_final" in categorias_candidato

    # 3. Condición especial para capturar legendarios (fase_unica o fase_final)
    #    Si es legendario + paradoja/ultraente, se aplica SOLO la condición de legendario.
    if es_legendario and es_fase_unica_o_final:
        equipo_actual = (
            entrenador["equipo_completo"]
            if entrenador.get("equipo_completo")
            else entrenador["pokemon_fijos"]
        )
        
        count_fase_final = 0
        count_fase_unica = 0
        has_primera_evolucion = False
        
        for pid in equipo_actual:
            if pid not in pokedex:
                continue
            cats = pokedex[pid].get("categorias", [])
            if "fase_final" in cats:
                count_fase_final += 1
            if "fase_unica" in cats:
                count_fase_unica += 1
            if "primera_evolucion" in cats:
                has_primera_evolucion = True
                
        condicion_X = count_fase_final >= 2
        condicion_Y = count_fase_final >= 1 and count_fase_unica >= 1
        condicion_Z = not has_primera_evolucion
        
        if not ((condicion_X or condicion_Y) and condicion_Z):
            return False

    # 4. Condición para paradojas y ultraentes NO legendarios
    #    Se evalúa una sola vez aunque tenga ambas etiquetas.
    elif (es_paradoja or es_ultraente) and not es_legendario:
        equipo_actual = (
            entrenador["equipo_completo"]
            if entrenador.get("equipo_completo")
            else entrenador["pokemon_fijos"]
        )
        
        count_fase_final = sum(
            1 for pid in equipo_actual
            if pid in pokedex and "fase_final" in pokedex[pid].get("categorias", [])
        )
        
        if count_fase_final < 1:
            return False

    # 5. Si no es legendario, ni paradoja, ni ultraente:
    #    Solo se aplican las reglas de temporada (ya evaluadas arriba).

    return True


# ---------------------------------------------------------------------------
# 5. Aplicar capturas
# ---------------------------------------------------------------------------

def aplicar_capturas(entrenador: dict, pokedex: dict[str, dict], temporada: int, num_candidatos: int = 3) -> None:
    """
    Orquesta el proceso de captura para un entrenador en una temporada:

    1. Genera N candidatos aleatorios válidos.
    2. Filtra cuáles son capturables según las reglas de evaluar_captura().
    3. Si hay opciones válidas, elige una al azar y se añade al equipo.

    No genera evoluciones ni aplica otras mejoras por ahora.
    No modifica el archivo entrenadores.json; opera en memoria.

    Parameters
    ----------
    entrenador : dict
        Entrada del entrenador (modificada en-lugar si hay captura).
    pokedex : dict[str, dict]
        Pokédex indexada por ID interno.
    temporada : int
        Número de temporada actual.
    num_candidatos : int, opcional
        Número de candidatos que se generan para elegir (por defecto 3).
    """
    candidatos = generar_candidatos_captura(entrenador, pokedex, num_candidatos)
    
    # Filtrar candidatos según las reglas
    candidatos_validos = [
        c for c in candidatos 
        if evaluar_captura(entrenador, c, pokedex, temporada)
    ]
    
    # Elegir uno al azar si hay válidos
    if candidatos_validos:
        candidato_elegido = random.choice(candidatos_validos)
        
        # Nos aseguramos de no perder los Pokémon fijos al inicializar equipo_completo
        if not entrenador.get("equipo_completo"):
            entrenador["equipo_completo"] = list(entrenador.get("pokemon_fijos", []))
            
        entrenador["equipo_completo"].append(candidato_elegido)

    # TODO: añadir llamadas a evoluciones y otras mejoras cuando estén implementadas
