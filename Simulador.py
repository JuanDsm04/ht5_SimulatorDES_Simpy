# Description: Simulador de un sistema operativo con un procesador y memoria RAM
# Autor: Juan Solís
# Version: 1.0

# Clase Proceso
class Proceso:
    def __init__(self, id, ram_requerida, cantidad_instrucciones):
        self.id = id
        self.ram_requerida = ram_requerida
        self.cantidad_instrucciones = cantidad_instrucciones
        self.estado = None