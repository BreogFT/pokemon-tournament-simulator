import json

class Persistencia:
    def cargar_json(self, ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar_json(self, ruta, datos):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
