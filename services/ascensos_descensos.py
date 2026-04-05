"""
ascensos_descensos.py
=====================
Módulo para gestionar el intercambio de entrenadores entre divisiones
al finalizar una temporada.
"""

def aplicar_ascensos_descensos(zona: dict) -> None:
    """
    Aplica el sistema de ascensos y descensos dentro de una zona específica.
    La zona contiene dos divisiones, A y B.
    
    Regla:
    - Los 2 peores de la División A (últimos de la lista) bajan a B.
    - Los 2 mejores de la División B (primeros de la lista) suben a A.
    
    Se asume que 'division_a' y 'division_b' son listas de entrenadores u objetos
    similares, ordenados por su clasificación final en la liga respectiva (índice 0 
    es el campeón, índice -1 es el último lugar).

    Parameters
    ----------
    zona : dict
        Diccionario que representa una zona (Norte, Sur, Este u Oeste), con 
        al menos las claves "division_a" y "division_b", ambas apuntando a listas.
    """
    if "division_a" not in zona or "division_b" not in zona:
        return

    div_a = zona["division_a"]
    div_b = zona["division_b"]

    # Asegurarnos de que tienen suficientes equipos
    if len(div_a) < 2 or len(div_b) < 2:
        return

    # Extraer los que bajan y los que suben
    descensos = div_a[-2:]
    ascensos = div_b[:2]

    # Quedan
    se_quedan_en_a = div_a[:-2]
    se_quedan_en_b = div_b[2:]

    # Actualizar listas de la zona en su nueva división
    # Consideramos que los recién ascendidos pueden ir al final de A,
    # y los recién descendidos al principio de B, pero el orden inicial
    # para la siguiente temporada a veces da igual hasta que se juega.
    zona["division_a"] = se_quedan_en_a + ascensos
    zona["division_b"] = descensos + se_quedan_en_b
