Skills del Proyecto
El agente debe seguir estas reglas:
- Mantener arquitectura modular.
- No mezclar lógica de dominio con lógica de servicios.
- No acceder directamente a archivos desde models/.
- Toda persistencia debe pasar por services/persistencia.py.
- La UI nunca debe contener lógica de simulación.
- Los modelos deben ser simples, claros y sin efectos secundarios.
- La simulación debe ser determinista salvo reglas especiales.
