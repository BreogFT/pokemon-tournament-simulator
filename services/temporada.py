"""
temporada.py
============
Módulo orquestador del ciclo completo de una temporada en el simulador.
Se encarga de ejecutar el flujo paso a paso desde las ligas divisionales
hasta los torneos, progresiones (evolución y captura) y los ascensos/descensos.
"""

from services.progresion import aplicar_evoluciones_generales, evolucion_selectiva
from services.generador_equipos import aplicar_capturas
from services.ascensos_descensos import aplicar_ascensos_descensos


def ejecutar_temporada(estado: dict, pokedex: dict, temporada_num: int) -> int:
    """
    Ejecuta el bucle principal de una temporada concreta según las reglas del simulador.

    Parameters
    ----------
    estado : dict
        Objeto global de la partida, debería contener al menos la lista plana 
        "entrenadores" y una estructura "zonas" que divide a dichos entrenadores 
        en las 4 áreas (Norte, Sur, Este, Oeste), cada una con "division_a" y "division_b".
    pokedex : dict
        La base de datos de los Pokémon parseada e indexada por ID interno.
    temporada_num : int
        El número de la temporada actual a simular.

    Returns
    -------
    int
        El número de la siguiente temporada (temporada_num + 1).
    """

    # Número base de candidatos de captura
    bonificaciones_captura = {e["id"]: 3 for e in estado.get("entrenadores", [])}

    # 1. Simular ligas de división A y B.
    # TODO: Invocar módulo de simulación de liga a nivel zonal y divisional aquí.
    # ej: for zona in estado["zonas"].values():
    #         simular_liga(zona["division_a"])
    #         simular_liga(zona["division_b"])

    # 2. Registrar bonificaciones de aparición para ganadores de A y B.
    # TODO: Obtener a los campeones reales una vez implementada la simulación de liga.
    # Hipotético:
    # for zona in estado["zonas"].values():
    #     campeon_a = zona["division_a"][0]["id"]
    #     campeon_b = zona["division_b"][0]["id"]
    #     bonificaciones_captura[campeon_a] += 1
    #     bonificaciones_captura[campeon_b] += 1

    # 3. Clasificar los 2 mejores de cada división A al torneo mundial.
    # TODO: Juntar a los TOP 2 de las Divisiones A (8 participantes en total).
    
    # 4. Simular el torneo mundial.
    # TODO: Ejecutar el bracket de simulación del Mundial con los 8 clasificados.

    # 5. Aplicar bonificaciones del campeón mundial.
    # TODO: Identificar al campeón del paso 4. Supondremos un 'campeon_mundial_id' dummy.
    campeon_mundial_id = None # Placeholder

    if campeon_mundial_id and campeon_mundial_id in bonificaciones_captura:
        # +1 candidato de aparición adicional (se puede acumular si también ganó su liga)
        bonificaciones_captura[campeon_mundial_id] += 1
        
        # 5.1 Evolución selectiva
        # TODO: Implementar UI en el futuro para recibir el ID del Pokémon.
        # pokemon_id_seleccionado = UI.mostrar_equipo_y_elegir(campeon_mundial)
        # evolucion_selectiva(campeon_mundial, pokedex, temporada_num, pokemon_id_seleccionado)
        pass

    # 6. Aplicar evolución aleatoria general a todos los entrenadores.
    aplicar_evoluciones_generales(estado.get("entrenadores", []), pokedex, temporada_num)

    # 7 y 8. Generar candidatos de captura y aplicar capturas según reglas.
    for entrenador in estado.get("entrenadores", []):
        num_cand = bonificaciones_captura.get(entrenador["id"], 3)
        aplicar_capturas(entrenador, pokedex, temporada_num, num_candidatos=num_cand)

    # 9. Aplicar ascensos y descensos entre divisiones.
    for nombre_zona, zona_data in estado.get("zonas", {}).items():
        aplicar_ascensos_descensos(zona_data)

    # 10. Preparar datos para la siguiente temporada.
    # TODO: Podría implicar reseteo de clasificaciones y guardado (persistencia).
    
    return temporada_num + 1
