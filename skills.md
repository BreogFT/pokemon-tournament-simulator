Skills del Proyecto
El agente debe seguir estas reglas:
- Mantener arquitectura modular.
- No mezclar lógica de dominio con lógica de servicios.
- No acceder directamente a archivos desde models/.
- Toda persistencia debe pasar por services/persistencia.py.
- La UI nunca debe contener lógica de simulación.
- Los modelos deben ser simples, claros y sin efectos secundarios.
- La simulación debe ser determinista salvo reglas especiales.

### Motor de combate
El simulador incluye un motor de combate que calcula daño, ventajas y resistencias según el tipo de cada Pokémon. El sistema utiliza ruletas de variación para introducir aleatoriedad controlada y determina el ganador de cada enfrentamiento.

### Progresión y evoluciones
Los Pokémon ganan experiencia tras cada combate. Al alcanzar ciertos umbrales suben de nivel y pueden evolucionar, lo que actualiza sus estadísticas y forma parte del ciclo de temporada.

### Ascensos y descensos
Al finalizar cada temporada, los equipos mejor clasificados ascienden a ligas superiores y los peor clasificados descienden. Este proceso está centralizado en `services/ascensos_descensos.py`.

### Orquestador de temporada
Coordina el ciclo completo de una temporada: generación de equipos, simulación de combates, progresión, actualización de clasificaciones y aplicación de ascensos/descensos.

### Generador de equipos
Crea equipos equilibrados a partir de la Pokédex, seleccionando Pokémon adecuados para cada liga y ajustando su nivel inicial.

