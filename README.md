# Pokémon Tournament Simulator

Simulador modular de torneos Pokémon con divisiones, ligas, temporadas y un torneo superior.  
El proyecto está organizado en capas: `models`, `services`, `ui` y `data`.

## Estructura
- `models/`: Clases principales del dominio.
- `services/`: Lógica de simulación, calendario, reglas especiales y persistencia.
- `ui/`: Interfaz de línea de comandos.
- `data/`: Archivos JSON con datos base.

## Funcionalidades de Servicios (Módulos Recientes)

### services/combate.py
Este módulo gestiona las mecánicas de combate mediante un sistema de ruletas probabilísticas.
- **Ventajas y Resistencias**: Basado en multiplicadores de la tabla de tipos (x2, x0.5, etc.).
- **Ruletas de Probabilidad**: Calcula las probabilidades de victoria por turno basándose en la ventaja neta de tipos o resistencias.
- **Motor de Duelos 1vs1**: Simulación de enfrentamientos individuales hasta agotar vidas.
- **Motor de Combates de Liga**: Formato 3vs3 seleccionando Pokémon aleatorios del equipo del entrenador.
- **Motor de Combates de Torneo**: Formato de equipo completo (hasta 6vs6) con orden de salida aleatorio.

### services/progresion.py
Gestiona el crecimiento de los equipos a lo largo de las temporadas.
- **Evolución Aleatoria**: Los entrenadores evolucionan un Pokémon de su equipo al azar tras cada temporada.
- **Evolución Selectiva**: Permite al campeón del torneo mundial elegir específicamente qué Pokémon evolucionar.
- **Validación de Evoluciones**: Verifica la línea evolutiva en la Pokédex y filtra formas especiales (Megas/Gigamax) según la temporada.

### services/generador_equipos.py
Se encarga de la expansión de los equipos mediante capturas.
- **Candidatos de Captura**: Genera una lista de candidatos (base de 3, ampliable con bonificaciones por victorias).
- **Reglas Especiales**: Filtros específicos para Legendarios, Paradojas y Ultraentes basados en la composición del equipo.
- **Captura Aleatoria**: Selección final entre candidatos que cumplen los requisitos de temporada y fase evolutiva.

### services/ascensos_descensos.py
Controla la movilidad entre divisiones al cierre de cada temporada.
- **Ascensos**: Los 2 mejores entrenadores de la División B suben a la División A.
- **Descensos**: Los 2 peores entrenadores de la División A bajan a la División B.

### services/temporada.py
Orquestador maestro que ejecuta el ciclo de vida de la temporada en 10 pasos:
1. Simulación de Ligas A y B.
2. Registro de bonificaciones para ganadores de liga.
3. Clasificación al Torneo Mundial.
4. Simulación del Torneo Mundial.
5. Aplicación de bonificaciones al Campeón Mundial.
6. Aplicación de progresiones (evoluciones generales).
7. Generación de candidatos de captura.
8. Aplicación de capturas.
9. Ejecución de ascensos y descensos.
10. Preparación de datos para la siguiente temporada.

## Estado actual del proyecto
- **Completo**: Pokédex unificada, Base de datos de entrenadores, Motor de combate probabilístico (Ruleta), Sistema de progresión/evoluciones, Lógica de capturas y candidatos, Orquestación del ciclo de temporada.
- **En desarrollo**: Simulación real de enfrentamientos de liga y torneo (integración final del motor de combate), Mejora de la interfaz de usuario, Sistema de registro de historial de temporadas.

## Ejecución
```bash
python main.py
```

