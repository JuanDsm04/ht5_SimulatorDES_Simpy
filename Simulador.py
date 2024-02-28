# Description: Simulador de un sistema operativo con un procesador y memoria RAM
# Autor: Juan Solís
# Version: 1.0

import simpy
import random

# Clase Proceso
class Proceso:
    def __init__(self, id, ram_requerida, cantidad_instrucciones):
        self.id = id
        self.ram_requerida = ram_requerida
        self.cantidad_instrucciones = cantidad_instrucciones
        self.estado = None

# Función que simula la llegada de un proceso al sistema
def llega_proceso_al_sistema(env, ram, cantidad_procesos):

    # New
    id_proceso = 1
    for _ in range(cantidad_procesos):
        yield env.timeout(random.expovariate(1.0 /intervalo_exponencial))
        ram_requerida = random.randint(1, 10)  
        cantidad_instrucciones = random.randint(1, 10)

        proceso = Proceso(id_proceso, ram_requerida, cantidad_instrucciones)
        id_proceso += 1

        with ram.get(ram_requerida) as recurso:
            # Ready
            yield recurso
            proceso.estado = 'ready'
            yield env.timeout(1)

# Parámetros de simulación
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
random.seed(100)
instrucciones_atendibles = 3
intervalo_exponencial = 10

cantidad_procesos_a_ejecutar = int(input("Cantidad de procesos a ejecutar: "))

env.process(llega_proceso_al_sistema(env, ram, cantidad_procesos_a_ejecutar))
env.run(until=simpy.core.Infinity)